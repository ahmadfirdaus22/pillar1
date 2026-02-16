"""
Configuration Distributor
Generates agent-specific configuration files from validated input.
"""

import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

from schemas.narrative_genesis_schema import NarrativeGenesisInput
from processors.transformers import (
    build_full_system_prompt,
    extract_all_contexts,
    ContextMerger,
    NarrativeFormatter,
    CharacterExtractor,
    VoiceEngineBuilder,
    NarrativeStateMachine,
    OrlicFrameworkImplementation,
    TruthTerminalLoreEngine
)


class AgentConfigGenerator:
    """Generates configuration files for AI agents"""
    
    def __init__(self, output_dir: Path):
        """
        Initialize generator
        
        Args:
            output_dir: Directory to write config files
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_scriptwriter_config(self, validated_input: NarrativeGenesisInput) -> Dict[str, Any]:
        """
        Generate configuration for Scriptwriter Agent (Pillar 3)
        
        Args:
            validated_input: Validated narrative genesis input
            
        Returns:
            Scriptwriter configuration dictionary
        """
        brand = validated_input.brand_identity_core
        framework = validated_input.strategic_narrative_framework
        character = validated_input.autonomous_character_seed
        audience = validated_input.target_audience_context
        
        # Build comprehensive system prompt
        system_prompt = build_full_system_prompt(validated_input)
        
        # Extract narrative journey
        narrative_journey = NarrativeFormatter.format_narrative_journey(framework)
        
        # Extract character traits
        character_traits = CharacterExtractor.extract_character_traits(character)
        
        # Format proof points
        proof_points = NarrativeFormatter.format_proof_points(framework.proof_points)
        
        config = {
            "agent_type": "scriptwriter",
            "version": "1.0",
            "generated_at": datetime.now().isoformat(),
            "source_project": validated_input.meta.project_name,
            
            "system_prompt_base": {
                "full_prompt": system_prompt,
                "brand_voice": {
                    "product_name": brand.product_name,
                    "archetype": brand.archetype,
                    "philosophy": brand.core_philosophy,
                    "tone_allowed": brand.tone_guardrails.allowed,
                    "tone_forbidden": brand.tone_guardrails.forbidden
                },
                "narrative_framework": {
                    "framework_type": "Matt Orlić - Storytelling that Sells",
                    "world_status_quo": narrative_journey["current_world"],
                    "consensus_reality": narrative_journey["consensus_reality"],
                    "enemy": {
                        "name": narrative_journey["enemy_name"],
                        "manifestation": narrative_journey["enemy_manifestation"],
                        "why_fight": narrative_journey["why_fight"]
                    },
                    "change_vehicle": {
                        "mechanism": narrative_journey["change_mechanism"],
                        "new_insight": narrative_journey["new_insight"]
                    },
                    "promised_land": {
                        "vision": narrative_journey["promised_land"],
                        "emotional_payoff": narrative_journey["emotional_payoff"]
                    }
                },
                "character_seed": {
                    "name": character_traits["identity"]["name"],
                    "role": character_traits["identity"]["role"],
                    "demographics": character_traits["identity"]["demographics"],
                    "core_belief": character_traits["psychology"]["central_belief"],
                    "internal_style": character_traits["psychology"]["internal_style"],
                    "obsessions": character_traits["psychology"]["obsessions"],
                    "autonomy_level": character_traits["behavior"]["autonomy_level"],
                    "memory_retention": character_traits["behavior"]["memory_type"],
                    "hallucination_permission": character_traits["behavior"]["imagination_allowed"]
                }
            },
            
            "guardrails": {
                "forbidden_words": brand.tone_guardrails.forbidden,
                "forbidden_styles": [
                    "Corporate Speak",
                    "Generic Motivational",
                    "Condescending",
                    "Overly Polished"
                ],
                "required_themes": [
                    framework.the_enemy.name,
                    "Financial Consciousness",
                    "System Awareness"
                ],
                "character_consistency_rules": [
                    f"Always speak as {character.base_persona.name}",
                    f"Maintain {character.lore_seed.internal_monologue_style} style",
                    f"Reference obsessions: {', '.join(character.lore_seed.obsession_topics)}"
                ]
            },
            
            "context": {
                "enemy": {
                    "name": framework.the_enemy.name,
                    "how_it_shows_up": framework.the_enemy.manifestation,
                    "why_we_fight": framework.the_enemy.why_fight_it
                },
                "promised_land": {
                    "vision": framework.the_promised_land.vision,
                    "emotional_benefit": framework.the_promised_land.emotional_payoff
                },
                "target_audience": {
                    "persona_code": audience.persona_code,
                    "pain_points": audience.pain_points,
                    "slang_to_use": audience.language_model.slang_whitelist,
                    "cultural_references": audience.language_model.cultural_references
                },
                "proof_and_credibility": {
                    "proof_points": proof_points["full_list"],
                    "proof_points_formatted": proof_points["bullet_points"]
                }
            },
            
            "content_generation_params": {
                "remember_past_scripts": True,
                "allow_character_evolution": character.evolution_parameters.autonomy_level == "High",
                "use_cumulative_memory": "cumulative" in character.evolution_parameters.memory_retention.lower(),
                "can_imagine_scenarios": "allowed" in character.evolution_parameters.hallucination_permission.lower(),
                "must_cite_proof": True,
                "always_reference_enemy": True,
                "always_point_to_promised_land": True
            },
            
            "usage_instructions": {
                "how_to_use": [
                    "1. Load this config at the start of scriptwriting session",
                    "2. Use system_prompt_base.full_prompt as the AI system prompt",
                    "3. Before generating script, check guardrails.forbidden_words",
                    "4. After generating, validate against guardrails and context",
                    "5. Ensure character consistency using character_seed parameters"
                ],
                "script_structure_requirements": [
                    "Must address 'The Enemy' explicitly",
                    "Must paint 'The Promised Land' vision",
                    "Must use target audience slang naturally",
                    "Must cite at least one proof point",
                    "Must maintain character voice throughout"
                ]
            }
        }
        
        return config
    
    def save_scriptwriter_config(self, validated_input: NarrativeGenesisInput) -> Path:
        """
        Generate and save scriptwriter config to file (LEGACY FORMAT)
        
        Args:
            validated_input: Validated narrative genesis input
            
        Returns:
            Path to saved config file
        """
        config = self.generate_scriptwriter_config(validated_input)
        
        output_file = self.output_dir / "scriptwriter_config.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        return output_file
    
    def generate_pillar3_config(self, validated_input: NarrativeGenesisInput) -> Dict[str, Any]:
        """
        Generate Pillar 3 Logic Context configuration (NEW FORMAT)
        
        Args:
            validated_input: Validated narrative genesis input
            
        Returns:
            Pillar 3 configuration dictionary
        """
        brand = validated_input.brand_identity_core
        framework = validated_input.strategic_narrative_framework
        character = validated_input.autonomous_character_seed
        audience = validated_input.target_audience_context
        
        # Build role definition
        persona = character.base_persona
        role_def = f"Kamu adalah {persona.name}, {persona.role}. {persona.demographics}"
        
        config = {
            "meta": {
                "generated_for": "Pillar 3 (AI Scriptwriter Agent)",
                "source_input": "NarrativeGenesisInput_v2.0",
                "generation_timestamp": datetime.now().isoformat()
            },
            "agent_system_prompt_config": {
                "role_definition": role_def,
                "voice_engine": VoiceEngineBuilder.build_voice_engine(brand, character, audience)
            },
            "narrative_state_machine": NarrativeStateMachine.build_state_machine(framework, character),
            "orlic_framework_implementation": OrlicFrameworkImplementation.build_framework_implementation(framework),
            "truth_terminal_lore_engine": TruthTerminalLoreEngine.build_lore_engine(character)
        }
        
        return config
    
    def save_pillar3_config(self, validated_input: NarrativeGenesisInput) -> Path:
        """
        Generate and save Pillar 3 Logic Context config to file
        
        Args:
            validated_input: Validated narrative genesis input
            
        Returns:
            Path to saved config file
        """
        config = self.generate_pillar3_config(validated_input)
        
        output_file = self.output_dir / "output_pillar3_logic_context.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        return output_file
    
    def generate_all_configs(self, validated_input: NarrativeGenesisInput) -> Dict[str, Path]:
        """
        Generate all agent configs (Pillar 3, legacy scriptwriter, etc.)
        
        Args:
            validated_input: Validated narrative genesis input
            
        Returns:
            Dictionary mapping agent type to config file path
        """
        configs = {}
        
        # Pillar 3 Logic Context (NEW PRIMARY FORMAT)
        pillar3_path = self.save_pillar3_config(validated_input)
        configs["pillar3_logic"] = pillar3_path
        
        # Scriptwriter config (LEGACY - for backward compatibility)
        scriptwriter_path = self.save_scriptwriter_config(validated_input)
        configs["scriptwriter_legacy"] = scriptwriter_path
        
        # Future: Add more agent types here
        # configs["qa_validator"] = self.save_qa_config(validated_input)
        # configs["character_engine"] = self.save_character_config(validated_input)
        
        return configs
    
    def generate_summary_report(self, validated_input: NarrativeGenesisInput) -> Dict[str, Any]:
        """
        Generate summary report of what was distributed
        
        Args:
            validated_input: Validated narrative genesis input
            
        Returns:
            Summary report dictionary
        """
        quick_ref = ContextMerger.create_quick_reference(validated_input)
        
        return {
            "distribution_summary": {
                "timestamp": datetime.now().isoformat(),
                "source_project": validated_input.meta.project_name,
                "input_version": validated_input.meta.version,
                "generated_configs": ["pillar3_logic", "scriptwriter_legacy"],
                "quick_reference": quick_ref
            },
            "agent_assignments": {
                "pillar3_logic": {
                    "purpose": "AI Scriptwriter Agent with enhanced voice engine and state machine",
                    "config_file": "output_pillar3_logic_context.json",
                    "format": "Enhanced with voice_engine, narrative_state_machine, orlic_framework, lore_engine",
                    "key_features": [
                        "Granular syntax constraints",
                        "Vocabulary whitelist/blacklist",
                        "Tone modifiers (sarcasm, optimism, paranoia)",
                        "Narrative phase awareness",
                        "Script structure templates",
                        "Memory buffer for character evolution"
                    ]
                },
                "scriptwriter_legacy": {
                    "purpose": "Generate content scripts using character voice (LEGACY FORMAT)",
                    "config_file": "scriptwriter_config.json",
                    "key_inputs": [
                        "System prompt with character personality",
                        "Narrative framework (Orlić structure)",
                        "Guardrails and forbidden words",
                        "Target audience context"
                    ]
                }
            }
        }


class DistributionReport:
    """Report on config distribution results"""
    
    def __init__(self, configs: Dict[str, Path], summary: Dict[str, Any]):
        self.configs = configs
        self.summary = summary
    
    def __str__(self) -> str:
        lines = [
            "✓ Configuration Distribution Complete",
            f"\nGenerated {len(self.configs)} config file(s):",
            ""
        ]
        
        for agent_type, path in self.configs.items():
            lines.append(f"  [{agent_type}] → {path}")
        
        lines.append("\n📋 Quick Reference:")
        quick_ref = self.summary["distribution_summary"]["quick_reference"]
        for key, value in quick_ref.items():
            lines.append(f"  {key}: {value}")
        
        return "\n".join(lines)
    
    def save_report(self, output_dir: Path) -> Path:
        """Save distribution report to file"""
        report_file = output_dir / "distribution_report.json"
        
        report_data = {
            "configs": {k: str(v) for k, v in self.configs.items()},
            "summary": self.summary
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        return report_file


def distribute_configs(validated_input: NarrativeGenesisInput, output_dir: Path) -> DistributionReport:
    """
    Main function to distribute all configs
    
    Args:
        validated_input: Validated narrative genesis input
        output_dir: Directory to write configs
        
    Returns:
        DistributionReport with results
    """
    generator = AgentConfigGenerator(output_dir)
    
    # Generate all configs
    configs = generator.generate_all_configs(validated_input)
    
    # Generate summary
    summary = generator.generate_summary_report(validated_input)
    
    # Create report
    report = DistributionReport(configs, summary)
    
    # Save report
    report.save_report(output_dir)
    
    return report


if __name__ == "__main__":
    print("Distributor module loaded. Import and use distribution functions.")
