"""
Input Validator Module
Validates JSON input against Pydantic schemas and provides detailed error reporting.
"""

import json
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
from pydantic import ValidationError

from schemas.narrative_genesis_schema import NarrativeGenesisInput


class ValidationReport:
    """Structured validation report"""
    
    def __init__(self, is_valid: bool, errors: Optional[list] = None, data: Optional[NarrativeGenesisInput] = None):
        self.is_valid = is_valid
        self.errors = errors or []
        self.data = data
    
    def __str__(self) -> str:
        if self.is_valid:
            return "✓ Validation PASSED - Input is valid"
        
        report = ["✗ Validation FAILED\n"]
        report.append(f"Found {len(self.errors)} error(s):\n")
        
        for i, error in enumerate(self.errors, 1):
            report.append(f"{i}. {error['type']}")
            report.append(f"   Location: {' -> '.join(str(loc) for loc in error['loc'])}")
            report.append(f"   Message: {error['msg']}")
            if 'input' in error:
                report.append(f"   Input value: {error['input']}")
            report.append("")
        
        return "\n".join(report)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get machine-readable summary"""
        return {
            "is_valid": self.is_valid,
            "error_count": len(self.errors),
            "errors": self.errors
        }


class NarrativeValidator:
    """Validates Narrative Genesis Input"""
    
    def __init__(self):
        self.last_report: Optional[ValidationReport] = None
    
    def load_json(self, file_path: Path) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
        """
        Load JSON file with error handling
        
        Returns:
            (success, data, error_message)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return True, data, None
        except FileNotFoundError:
            return False, None, f"File not found: {file_path}"
        except json.JSONDecodeError as e:
            return False, None, f"Invalid JSON syntax: {e.msg} at line {e.lineno}, column {e.colno}"
        except Exception as e:
            return False, None, f"Error loading file: {str(e)}"
    
    def validate_from_file(self, file_path: Path) -> ValidationReport:
        """
        Validate input from JSON file
        
        Args:
            file_path: Path to input JSON file
            
        Returns:
            ValidationReport with validation results
        """
        # Load JSON
        success, data, error = self.load_json(file_path)
        if not success:
            self.last_report = ValidationReport(is_valid=False, errors=[{
                "type": "file_loading_error",
                "loc": ["file"],
                "msg": error,
                "input": str(file_path)
            }])
            return self.last_report
        
        # Validate against schema
        return self.validate_from_dict(data)
    
    def validate_from_dict(self, data: Dict[str, Any]) -> ValidationReport:
        """
        Validate input from dictionary
        
        Args:
            data: Dictionary containing input data
            
        Returns:
            ValidationReport with validation results
        """
        try:
            # Parse and validate
            validated_input = NarrativeGenesisInput(**data)
            
            # Additional business logic checks
            warnings = self._perform_business_logic_checks(validated_input)
            
            self.last_report = ValidationReport(is_valid=True, data=validated_input)
            
            # If there are warnings, add them as info
            if warnings:
                print("\n⚠ Warnings (non-blocking):")
                for warning in warnings:
                    print(f"  - {warning}")
            
            return self.last_report
            
        except ValidationError as e:
            errors = []
            for error in e.errors():
                errors.append({
                    "type": error["type"],
                    "loc": error["loc"],
                    "msg": error["msg"],
                    "input": error.get("input", "N/A")
                })
            
            self.last_report = ValidationReport(is_valid=False, errors=errors)
            return self.last_report
        
        except Exception as e:
            self.last_report = ValidationReport(is_valid=False, errors=[{
                "type": "unexpected_error",
                "loc": ["root"],
                "msg": str(e),
                "input": "N/A"
            }])
            return self.last_report
    
    def _perform_business_logic_checks(self, validated_input: NarrativeGenesisInput) -> list:
        """
        Perform additional business logic validation beyond schema
        
        Returns:
            List of warning messages (non-blocking)
        """
        warnings = []
        
        # Check archetype and tone consistency
        archetype = validated_input.brand_identity_core.archetype.lower()
        allowed_tones = [t.lower() for t in validated_input.brand_identity_core.tone_guardrails.allowed]
        
        if 'rebel' in archetype:
            if not any(tone in ['sarcastic', 'raw', 'unfiltered'] for tone in allowed_tones):
                warnings.append("Archetype is 'Rebel' but tone doesn't include rebellious characteristics")
        
        # Check if proof points are substantial
        proof_points = validated_input.strategic_narrative_framework.proof_points
        if any(len(point) < 20 for point in proof_points):
            warnings.append("Some proof points seem too short - consider adding more detail")
        
        # Check character age vs target audience
        demo = validated_input.autonomous_character_seed.base_persona.demographics
        pain_points = validated_input.target_audience_context.pain_points
        
        if any('gaji' in p.lower() or 'salary' in p.lower() for p in pain_points):
            if not any(term in demo.lower() for term in ['gaji', 'salary', 'umr', 'debt']):
                warnings.append("Target audience has salary pain points but character demographics don't mention income/debt")
        
        return warnings
    
    def get_validation_stats(self) -> Dict[str, Any]:
        """Get statistics about the validated input"""
        if not self.last_report or not self.last_report.is_valid:
            return {"status": "no_valid_data"}
        
        data = self.last_report.data
        return {
            "status": "valid",
            "product_name": data.brand_identity_core.product_name,
            "character_name": data.autonomous_character_seed.base_persona.name,
            "target_persona": data.target_audience_context.persona_code,
            "proof_points_count": len(data.strategic_narrative_framework.proof_points),
            "allowed_tones": len(data.brand_identity_core.tone_guardrails.allowed),
            "forbidden_tones": len(data.brand_identity_core.tone_guardrails.forbidden),
            "slang_count": len(data.target_audience_context.language_model.slang_whitelist),
            "autonomy_level": data.autonomous_character_seed.evolution_parameters.autonomy_level
        }


def validate_input_file(file_path: str) -> ValidationReport:
    """
    Convenience function to validate a file
    
    Args:
        file_path: Path to input JSON file
        
    Returns:
        ValidationReport
    """
    validator = NarrativeValidator()
    return validator.validate_from_file(Path(file_path))


if __name__ == "__main__":
    # CLI usage for testing
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python validator.py <input_file.json>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    report = validate_input_file(file_path)
    
    print(report)
    
    if report.is_valid:
        validator = NarrativeValidator()
        validator.last_report = report
        stats = validator.get_validation_stats()
        print("\n📊 Input Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        sys.exit(0)
    else:
        sys.exit(1)
