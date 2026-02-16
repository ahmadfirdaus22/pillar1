#!/usr/bin/env python3
"""
Pillar 1: Narrative Genesis Input Processor
Main entry point for validating and distributing narrative configuration
and orchestrating downstream pillar generation (Pillar 2/3/4) via a single
LLM call (OpenRouter).

Usage:
    python process_narrative.py
    python process_narrative.py --input custom_input.json
    python process_narrative.py --validate-only
"""

import sys
import os
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any

import requests
from dotenv import load_dotenv
import json_repair

from processors.validator import NarrativeValidator, ValidationReport
from processors.distributor import distribute_configs


# Load environment variables from .env at import time so that
# OPENROUTER_API_KEY and related config are available both for CLI
# usage and when this module is imported by the Streamlit UI.
load_dotenv()


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header():
    """Print application header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}  Pillar 1: Narrative Genesis Input Processor{Colors.END}")
    print(f"{Colors.CYAN}  Validates & Distributes AI Agent Configurations{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")


def print_success(message: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")


def print_error(message: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {message}{Colors.END}")


def print_info(message: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {message}{Colors.END}")


def print_warning(message: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")


def validate_input(input_file: Path, validator: NarrativeValidator) -> Optional[ValidationReport]:
    """
    Validate input file
    
    Args:
        input_file: Path to input JSON file
        validator: NarrativeValidator instance
        
    Returns:
        ValidationReport if successful, None if file doesn't exist
    """
    print_info(f"Loading input from: {input_file}")
    
    if not input_file.exists():
        print_error(f"Input file not found: {input_file}")
        return None
    
    print_info("Validating input against schema...")
    report = validator.validate_from_file(input_file)
    
    print()  # Blank line
    
    if report.is_valid:
        print_success("Validation PASSED")
        
        # Print statistics
        stats = validator.get_validation_stats()
        print(f"\n{Colors.BOLD}Input Statistics:{Colors.END}")
        print(f"  Product: {stats['product_name']}")
        print(f"  Character: {stats['character_name']}")
        print(f"  Target: {stats['target_persona']}")
        print(f"  Autonomy: {stats['autonomy_level']}")
        print(f"  Proof Points: {stats['proof_points_count']}")
        print(f"  Slang Terms: {stats['slang_count']}")
    else:
        print_error("Validation FAILED")
        print(f"\n{report}")
    
    return report


def distribute_configurations(report: ValidationReport, output_dir: Path):
    """
    Distribute configurations to agents
    
    Args:
        report: Validated input report
        output_dir: Output directory for configs
    """
    print(f"\n{Colors.BOLD}Distribution Phase{Colors.END}")
    print_info(f"Generating agent configurations...")
    
    try:
        # Distribute configs
        dist_report = distribute_configs(report.data, output_dir)
        
        print()  # Blank line
        print(dist_report)
        
        # Print file locations
        print(f"\n{Colors.BOLD}Generated Files:{Colors.END}")
        for agent_type, config_path in dist_report.configs.items():
            print(f"  {agent_type}: {Colors.CYAN}{config_path}{Colors.END}")
        
        report_path = output_dir / "distribution_report.json"
        print(f"  report: {Colors.CYAN}{report_path}{Colors.END}")
        
        print_success("\nDistribution complete!")
        
    except Exception as e:
        print_error(f"Distribution failed: {str(e)}")
        raise


def _build_pillars_prompt(input_data: Dict[str, Any], schema_version: str = "2.1.0") -> Dict[str, Any]:
    """
    Build the OpenRouter chat payload for generating Pillar 2, 3, and 4 in one call.

    The model is instructed to return a single JSON object:
    {
      "pillar2": { ... },
      "pillar3": { ... },
      "pillar4": { ... }
    }
    """
    # We only need a compact summary of the input; if input is huge, you can
    # add a manual summarisation step here later.
    user_input_snippet = json.dumps(input_data, ensure_ascii=False)[:8000]

    system_message = (
        "You are a Narrative Operating System generator. "
        "Given a Narrative Genesis Input JSON, you MUST output a single valid JSON object "
        "with three top-level keys: 'pillar2', 'pillar3', and 'pillar4'. "
        "Do not include any markdown, comments, or text outside the JSON."
    )

    # Skeletons keep the model aligned with our expected schemas without
    # requiring us to inline the full examples.
    user_instruction = {
        "instruction": {
            "schema_version": schema_version,
            "output_requirements": {
                "pillar2": {
                    "description": "Hook Intelligence / scraping config",
                    "required_top_level_keys": [
                        "meta",
                        "scraping_runtime_config",
                        "scraping_parameters",
                        "content_selection_rules",
                        "psychological_trigger_map",
                        "narrative_phase_constraints",
                        "implementation_notes"
                    ]
                },
                "pillar3": {
                    "description": "Logic & scripting context for AI Writer",
                    "required_top_level_keys": [
                        "meta",
                        "character_voice",
                        "dialogue_modes",
                        "script_templates",
                        "narrative_constraints"
                    ]
                },
                "pillar4": {
                    "description": "Visual production & QA guide",
                    "required_top_level_keys": [
                        "meta",
                        "art_direction_matrix",
                        "visual_presets",
                        "cross_pillar_links",
                        "visual_beats_sequence",
                        "editing_style_guide",
                        "quality_assurance_checklist",
                        "ai_generation_interface"
                    ]
                }
            },
            "meta_instructions": [
                "Always include a 'meta' block in each pillar with fields: generated_for, source_input, generation_timestamp, schema_version.",
                "Return strictly one JSON object, with no leading or trailing text."
            ]
        },
        "narrative_input": input_data,
        "narrative_input_snippet": user_input_snippet,
    }

    return {
        "model": os.getenv("OPENROUTER_MODEL", "openrouter/auto"),
        "messages": [
            {"role": "system", "content": system_message},
            {
                "role": "user",
                "content": (
                    "Use the following Narrative Genesis Input and instructions to generate "
                    "Pillar 2, Pillar 3, and Pillar 4 JSON objects in a single response.\n\n"
                    + json.dumps(user_instruction, ensure_ascii=False)
                ),
            },
        ],
        # Reasonable defaults; can be overridden via env if desired.
        "temperature": float(os.getenv("OPENROUTER_TEMPERATURE", "0.2")),
        "max_tokens": int(os.getenv("OPENROUTER_MAX_TOKENS", "4000")),
        # Ask OpenRouter / model to return a well-formed JSON object.
        # Many OpenRouter models support the OpenAI-compatible response_format.
        "response_format": {"type": "json_object"},
    }


def _normalize_input_data(input_data: Any) -> Dict[str, Any]:
    """
    Ensure we always pass a plain dict into the LLM layer.

    The validator and distributor use a Pydantic model (NarrativeGenesisInput),
    which is not JSON-serializable by default. This helper converts such models
    to plain dicts, while leaving normal dicts untouched.
    """
    # Pydantic v2 uses .model_dump(), v1 uses .dict()
    if hasattr(input_data, "model_dump"):
        return input_data.model_dump()
    if hasattr(input_data, "dict"):
        return input_data.dict()
    if isinstance(input_data, dict):
        return input_data
    raise TypeError(
        f"Unsupported input_data type for pillar generation: {type(input_data)!r}. "
        "Expected dict or Pydantic model with .model_dump()/.dict()."
    )


def _call_openrouter_for_pillars(input_data: Any) -> Dict[str, Any]:
    """
    Call OpenRouter once to generate Pillar 2, 3, and 4 JSON.

    Returns:
        Parsed JSON dict with keys 'pillar2', 'pillar3', 'pillar4'.
    """
    # Normalize NarrativeGenesisInput (Pydantic) → dict to avoid JSON
    # serialization issues when building the prompt payload.
    normalized_input = _normalize_input_data(input_data)

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not set in environment (check your .env).")

    url = os.getenv("OPENROUTER_API_URL", "https://openrouter.ai/api/v1/chat/completions")
    payload = _build_pillars_prompt(normalized_input)

    headers = {
        "Authorization": f"Bearer {api_key}",
        # Optional but recommended headers for OpenRouter
        "HTTP-Referer": os.getenv("OPENROUTER_HTTP_REFERER", "http://localhost"),
        "X-Title": os.getenv("OPENROUTER_X_TITLE", "NarrativeOS Pipeline"),
        "Content-Type": "application/json",
    }

    print_info("Calling OpenRouter to generate Pillar 2/3/4 in a single request...")
    response = requests.post(url, headers=headers, json=payload, timeout=120)
    if response.status_code != 200:
        raise RuntimeError(f"OpenRouter call failed: {response.status_code} {response.text}")

    data = response.json()

    # Depending on the OpenRouter model, the content may already be a JSON
    # object (when using response_format=json_object) or a JSON string.
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:
        raise RuntimeError(f"Unexpected OpenRouter response format: {data}") from exc

    # If the model already returned a dict, use it directly.
    if isinstance(content, dict):
        pillars = content
    else:
        # Parse JSON; if model adds markdown fences or stray text, try to recover.
        raw = str(content).strip()

        # Strip Markdown code fences if present (```json ... ```).
        if raw.startswith("```"):
            # Remove leading ``` or ```json line
            first_newline = raw.find("\n")
            if first_newline != -1:
                raw = raw[first_newline + 1 :]
            # Remove trailing ```
            if raw.endswith("```"):
                raw = raw[: -3].strip()

        # Aggressive sanitization & repair: fix common LLM JSON issues and use json_repair.
        import re
        # 1. Fix trailing commas before closing brackets/braces
        raw = re.sub(r',(\s*[}\]])', r'\1', raw)

        try:
            pillars = json.loads(raw)
        except json.JSONDecodeError as first_err:
            # Second attempt: json_repair can handle truncated strings, quotes, etc.
            try:
                pillars = json_repair.loads(raw)
            except Exception as repair_err:
                # As a last resort, try to extract the first JSON object and repair that.
                match = re.search(r"\{[\s\S]*\}", raw)
                if match:
                    try:
                        pillars = json_repair.loads(match.group(0))
                    except Exception:
                        raise RuntimeError(
                            f"Failed to parse/repair JSON from OpenRouter response. "
                            f"Original error: {first_err}; repair error: {repair_err}"
                        )
                else:
                    raise RuntimeError(
                        f"Failed to parse/repair JSON from OpenRouter response. "
                        f"Original error: {first_err}; repair error: {repair_err}"
                    )

    if not isinstance(pillars, dict):
        raise RuntimeError("Parsed pillars response is not a JSON object.")

    for key in ("pillar2", "pillar3", "pillar4"):
        if key not in pillars:
            raise RuntimeError(f"Missing '{key}' in pillars response.")

    return pillars


def run_narrative_pipeline(input_file: Path, output_root: Path) -> None:
    """
    High-level orchestration for generating Pillar 2, 3, and 4 via a single LLM call.

    Args:
        input_file: Path to the Narrative Genesis Input JSON.
        output_root: Base directory where pillar outputs will be stored.
    """
    print(f"\n{Colors.BOLD}Pillar Generation Phase (LLM){Colors.END}")
    print_info(f"Loading narrative input for pillars from: {input_file}")

    if not input_file.exists():
        print_warning(f"Input file not found for pillar generation: {input_file}")
        return

    try:
        with input_file.open("r", encoding="utf-8") as f:
            input_data = json.load(f)
    except Exception as exc:
        print_error(f"Failed to read input file for pillar generation: {exc}")
        return

    try:
        pillars = _call_openrouter_for_pillars(input_data)
    except Exception as exc:
        print_error(f"Pillar generation via OpenRouter failed: {exc}")
        return

    # Ensure output directory exists
    output_root.mkdir(parents=True, exist_ok=True)

    # Optionally stamp generation_timestamp if not set by model
    timestamp = datetime.now(timezone.utc).isoformat()

    def _stamp_meta(block: Dict[str, Any], generated_for: str) -> Dict[str, Any]:
        meta = block.get("meta") or {}
        meta.setdefault("generated_for", generated_for)
        meta.setdefault("source_input", str(input_file))
        meta.setdefault("generation_timestamp", timestamp)
        meta.setdefault("schema_version", meta.get("schema_version", "2.1.0"))
        block["meta"] = meta
        return block

    pillar2 = _stamp_meta(pillars["pillar2"], "Pillar 2 (Hook Intelligence System)")
    pillar3 = _stamp_meta(pillars["pillar3"], "Pillar 3 (Logic & Script Context)")
    pillar4 = _stamp_meta(pillars["pillar4"], "Pillar 4 (Visual Production & QA)")

    # Write individual pillar files
    p2_path = output_root / "output_pillar2_psycho_tags_v2.1.json"
    p3_path = output_root / "output_pillar3_logic_context_v2.1.json"
    p4_path = output_root / "output_pillar4_visual_guide_v2.1.json"
    raw_path = output_root / "raw_pillars_response.json"

    try:
        with p2_path.open("w", encoding="utf-8") as f:
            json.dump(pillar2, f, indent=2, ensure_ascii=False)
        with p3_path.open("w", encoding="utf-8") as f:
            json.dump(pillar3, f, indent=2, ensure_ascii=False)
        with p4_path.open("w", encoding="utf-8") as f:
            json.dump(pillar4, f, indent=2, ensure_ascii=False)

        # Save combined pillars for debugging/auditing
        with raw_path.open("w", encoding="utf-8") as f:
            json.dump(pillars, f, indent=2, ensure_ascii=False)

        print_success(f"Pillar 2 output written to: {p2_path}")
        print_success(f"Pillar 3 output written to: {p3_path}")
        print_success(f"Pillar 4 output written to: {p4_path}")
        print_info(f"Raw pillars response saved to: {raw_path}")
    except Exception as exc:
        print_error(f"Failed to write pillar outputs: {exc}")


def generate_pillars_from_data(
    input_data: Dict[str, Any],
    output_root: Path,
    source_input: str = "ui_session",
) -> Dict[str, Path]:
    """
    Public helper to generate Pillar 2/3/4 outputs from an in-memory
    Narrative Genesis Input dict. Intended to be used by the Streamlit UI.

    Returns:
        Dict mapping logical pillar names to written file paths.
    """
    print_info("Generating Pillar 2/3/4 via OpenRouter from in-memory data...")

    # Call LLM once
    pillars = _call_openrouter_for_pillars(input_data)

    # Ensure output directory exists
    output_root.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).isoformat()

    def _stamp_meta(block: Dict[str, Any], generated_for: str) -> Dict[str, Any]:
        meta = block.get("meta") or {}
        meta.setdefault("generated_for", generated_for)
        meta.setdefault("source_input", source_input)
        meta.setdefault("generation_timestamp", timestamp)
        meta.setdefault("schema_version", meta.get("schema_version", "2.1.0"))
        block["meta"] = meta
        return block

    pillar2 = _stamp_meta(pillars["pillar2"], "Pillar 2 (Hook Intelligence System)")
    pillar3 = _stamp_meta(pillars["pillar3"], "Pillar 3 (Logic & Script Context)")
    pillar4 = _stamp_meta(pillars["pillar4"], "Pillar 4 (Visual Production & QA)")

    p2_path = output_root / "output_pillar2_psycho_tags_v2.1.json"
    p3_path = output_root / "output_pillar3_logic_context_v2.1.json"
    p4_path = output_root / "output_pillar4_visual_guide_v2.1.json"
    raw_path = output_root / "raw_pillars_response.json"

    try:
        with p2_path.open("w", encoding="utf-8") as f:
            json.dump(pillar2, f, indent=2, ensure_ascii=False)
        with p3_path.open("w", encoding="utf-8") as f:
            json.dump(pillar3, f, indent=2, ensure_ascii=False)
        with p4_path.open("w", encoding="utf-8") as f:
            json.dump(pillar4, f, indent=2, ensure_ascii=False)

        with raw_path.open("w", encoding="utf-8") as f:
            json.dump(pillars, f, indent=2, ensure_ascii=False)

        print_success(f"Pillar 2 output written to: {p2_path}")
        print_success(f"Pillar 3 output written to: {p3_path}")
        print_success(f"Pillar 4 output written to: {p4_path}")
        print_info(f"Raw pillars response saved to: {raw_path}")
    except Exception as exc:
        print_error(f"Failed to write pillar outputs from UI session: {exc}")
        raise

    return {
        "pillar2": p2_path,
        "pillar3": p3_path,
        "pillar4": p4_path,
    }


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="Process Narrative Genesis Input and distribute to AI agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python process_narrative.py
  python process_narrative.py --input custom_input.json
  python process_narrative.py --validate-only
  python process_narrative.py --output ./configs
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        type=str,
        default='input_master.json',
        help='Input JSON file (default: input_master.json)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='output/agent_configs',
        help='Output directory for configs (default: output/agent_configs)'
    )
    
    parser.add_argument(
        '--validate-only', '-v',
        action='store_true',
        help='Only validate, do not distribute configs'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress header and extra output'
    )
    
    args = parser.parse_args()
    
    # Print header
    if not args.quiet:
        print_header()
    
    # Setup paths
    input_file = Path(args.input)
    output_dir = Path(args.output)
    pillars_output_root = Path("output")
    
    # Create validator
    validator = NarrativeValidator()
    
    # Validate input
    report = validate_input(input_file, validator)
    
    if report is None or not report.is_valid:
        return 1
    
    # If validate-only mode, stop here
    if args.validate_only:
        print_info("\nValidation-only mode: Skipping distribution")
        return 0
    
    # Distribute configurations
    try:
        distribute_configurations(report, output_dir)
    except Exception as e:
        print_error(f"\nFatal error during distribution: {str(e)}")
        if not args.quiet:
            import traceback
            print(f"\n{Colors.RED}Traceback:{Colors.END}")
            traceback.print_exc()
        return 1

    # Generate Pillar 2/3/4 via single LLM call
    try:
        run_narrative_pipeline(input_file, pillars_output_root)
    except Exception as e:
        print_error(f"\nFatal error during pillar generation: {str(e)}")
        if not args.quiet:
            import traceback
            print(f"\n{Colors.RED}Traceback (pillar generation):{Colors.END}")
            traceback.print_exc()
        # Do not hard-fail the entire process; return success for core distribution.
    
    # Success
    if not args.quiet:
        print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}  Process completed successfully!{Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
