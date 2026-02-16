"""
Data Transformation Utilities
Converts validated input into agent-ready formats and generates system prompts.
"""

from typing import Dict, Any, List
from schemas.narrative_genesis_schema import (
    NarrativeGenesisInput,
    AutonomousCharacterSeed,
    StrategicNarrativeFramework,
    TargetAudienceContext,
    BrandIdentityCore
)


class PromptBuilder:
    """Builds natural language prompts from structured data"""
    
    @staticmethod
    def build_system_prompt(
        character: AutonomousCharacterSeed,
        framework: StrategicNarrativeFramework,
        brand: BrandIdentityCore,
        audience: TargetAudienceContext
    ) -> str:
        """
        Generate comprehensive system prompt for AI agent
        
        Args:
            character: Character seed with persona and lore
            framework: Strategic narrative framework
            brand: Brand identity
            audience: Target audience context
            
        Returns:
            Natural language system prompt
        """
        persona = character.base_persona
        lore = character.lore_seed
        evolution = character.evolution_parameters
        
        prompt_parts = []
        
        # Character introduction
        prompt_parts.append(
            f"You are {persona.name}, {persona.role}. {persona.demographics}"
        )
        
        # Core belief
        prompt_parts.append(f"\nYour Core Belief: {lore.central_belief}")
        
        # Mission (The Enemy)
        enemy = framework.the_enemy
        prompt_parts.append(
            f"\nYour Mission: Fight against {enemy.name} - {enemy.manifestation} "
            f"{enemy.why_fight_it}"
        )
        
        # Voice and tone
        allowed = ", ".join(brand.tone_guardrails.allowed)
        forbidden = ", ".join(brand.tone_guardrails.forbidden)
        prompt_parts.append(
            f"\nYour Voice: {allowed}.\n"
            f"NEVER use: {forbidden}."
        )
        
        # Internal style
        prompt_parts.append(
            f"\nYour Internal Monologue: {lore.internal_monologue_style}"
        )
        
        # Obsessions
        obsessions = ", ".join(lore.obsession_topics)
        prompt_parts.append(f"\nYour Obsessions: {obsessions}.")
        
        # Framework references
        prompt_parts.append("\nWhen creating content, always reference:")
        prompt_parts.append(f"- The Enemy: {enemy.name}")
        prompt_parts.append(
            f"- The Promised Land: {framework.the_promised_land.vision}"
        )
        prompt_parts.append(
            f"- Proof: {' | '.join(framework.proof_points[:3])}"  # First 3 proof points
        )
        
        # Target audience
        pain_points_str = ", ".join([f'"{p}"' for p in audience.pain_points[:3]])
        prompt_parts.append(
            f"\nSpeak to: {audience.persona_code} - those with {pain_points_str}."
        )
        
        # Language
        slang = ", ".join(audience.language_model.slang_whitelist)
        prompt_parts.append(f"\nUse their language: {slang}.")
        
        # Evolution parameters
        prompt_parts.append(
            f"\n[System]: Autonomy Level = {evolution.autonomy_level} | "
            f"Memory = {evolution.memory_retention} | "
            f"Imagination = {evolution.hallucination_permission}"
        )
        
        return "\n".join(prompt_parts)
    
    @staticmethod
    def build_concise_prompt(character: AutonomousCharacterSeed, brand: BrandIdentityCore) -> str:
        """Build shorter version for character voice only"""
        persona = character.base_persona
        lore = character.lore_seed
        allowed = ", ".join(brand.tone_guardrails.allowed)
        
        return (
            f"You are {persona.name} ({persona.role}). "
            f"Core belief: {lore.central_belief}. "
            f"Voice: {allowed}."
        )


class CharacterExtractor:
    """Extracts character traits and attributes"""
    
    @staticmethod
    def extract_character_traits(character: AutonomousCharacterSeed) -> Dict[str, Any]:
        """
        Extract structured character traits
        
        Returns:
            Dictionary with categorized traits
        """
        persona = character.base_persona
        lore = character.lore_seed
        evolution = character.evolution_parameters
        
        return {
            "identity": {
                "name": persona.name,
                "role": persona.role,
                "demographics": persona.demographics
            },
            "psychology": {
                "central_belief": lore.central_belief,
                "internal_style": lore.internal_monologue_style,
                "obsessions": lore.obsession_topics
            },
            "behavior": {
                "autonomy_level": evolution.autonomy_level,
                "memory_type": evolution.memory_retention,
                "imagination_allowed": evolution.hallucination_permission
            }
        }
    
    @staticmethod
    def get_character_summary(character: AutonomousCharacterSeed) -> str:
        """One-line character summary"""
        persona = character.base_persona
        return f"{persona.name} - {persona.role}"


class NarrativeFormatter:
    """Formats narrative framework components"""
    
    @staticmethod
    def format_proof_points(proof_points: List[str]) -> Dict[str, Any]:
        """
        Structure proof points for different uses
        
        Returns:
            Formatted proof points
        """
        return {
            "full_list": proof_points,
            "bullet_points": [f"• {point}" for point in proof_points],
            "numbered": [f"{i+1}. {point}" for i, point in enumerate(proof_points)],
            "count": len(proof_points),
            "summary": " | ".join(proof_points[:2]) + ("..." if len(proof_points) > 2 else "")
        }
    
    @staticmethod
    def format_narrative_journey(framework: StrategicNarrativeFramework) -> Dict[str, str]:
        """
        Format the complete narrative journey (Orlić framework)
        
        Returns:
            Structured journey with all stages
        """
        return {
            "current_world": framework.the_world_status_quo.description,
            "consensus_reality": framework.the_world_status_quo.consensus_reality,
            "enemy_name": framework.the_enemy.name,
            "enemy_manifestation": framework.the_enemy.manifestation,
            "why_fight": framework.the_enemy.why_fight_it,
            "change_mechanism": framework.the_change_vehicle.mechanism,
            "new_insight": framework.the_change_vehicle.what_is_new,
            "promised_land": framework.the_promised_land.vision,
            "emotional_payoff": framework.the_promised_land.emotional_payoff
        }


class ContextMerger:
    """Merges multiple context sources"""
    
    @staticmethod
    def merge_contexts(
        brand: BrandIdentityCore,
        framework: StrategicNarrativeFramework,
        character: AutonomousCharacterSeed,
        audience: TargetAudienceContext
    ) -> Dict[str, Any]:
        """
        Merge all contexts into unified structure
        
        Returns:
            Merged context dictionary
        """
        return {
            "brand": {
                "name": brand.product_name,
                "archetype": brand.archetype,
                "philosophy": brand.core_philosophy,
                "voice": {
                    "allowed": brand.tone_guardrails.allowed,
                    "forbidden": brand.tone_guardrails.forbidden
                }
            },
            "narrative": NarrativeFormatter.format_narrative_journey(framework),
            "character": CharacterExtractor.extract_character_traits(character),
            "audience": {
                "code": audience.persona_code,
                "pain_points": audience.pain_points,
                "language": {
                    "slang": audience.language_model.slang_whitelist,
                    "references": audience.language_model.cultural_references
                }
            }
        }
    
    @staticmethod
    def create_quick_reference(validated_input: NarrativeGenesisInput) -> Dict[str, str]:
        """
        Create quick reference card with key info
        
        Returns:
            Condensed key information
        """
        brand = validated_input.brand_identity_core
        character = validated_input.autonomous_character_seed
        framework = validated_input.strategic_narrative_framework
        
        return {
            "product": brand.product_name,
            "character": f"{character.base_persona.name} ({character.base_persona.role})",
            "mission": f"Fight {framework.the_enemy.name}",
            "goal": framework.the_promised_land.vision,
            "voice": ", ".join(brand.tone_guardrails.allowed[:3]),
            "avoid": ", ".join(brand.tone_guardrails.forbidden[:3])
        }


class VoiceEngineBuilder:
    """Builds detailed voice engine configuration for Pillar 3"""
    
    @staticmethod
    def build_voice_engine(
        brand: BrandIdentityCore,
        character: AutonomousCharacterSeed,
        audience: TargetAudienceContext
    ) -> Dict[str, Any]:
        """
        Generate voice_engine with syntax, vocabulary, and tone modifiers
        
        Args:
            brand: Brand identity with tone guardrails
            character: Character with internal style
            audience: Target audience with language model
            
        Returns:
            Voice engine configuration dictionary
        """
        # Build vocabulary blacklist (merge forbidden tones with common violations)
        blacklist_base = [
            "Semangat Pagi",
            "Financial Freedom (terlalu jauh)",
            "Mindset Sukses",
            "Ayo Kawan",
            "Solusi Terbaik"
        ]
        vocabulary_blacklist = blacklist_base + brand.tone_guardrails.forbidden
        
        return {
            "syntax_constraints": [
                "Gunakan kalimat pendek-pendek (maksimal 12 kata per napas).",
                "Gunakan tanda kurung (...) untuk 'internal thought' atau pikiran intrusif.",
                "JANGAN gunakan tanda seru (!) untuk semangat. Gunakan hanya untuk kemarahan/kaget."
            ],
            "vocabulary_whitelist": audience.language_model.slang_whitelist,
            "vocabulary_blacklist": vocabulary_blacklist,
            "tone_modifiers": {
                "sarcasm_level": "High (8/10)",
                "optimism_level": "Low (2/10) - Masih skeptis",
                "paranoia_level": "Medium (5/10) - Curiga pada diskon"
            }
        }


class NarrativeStateMachine:
    """Builds narrative state machine for phase-aware content generation"""
    
    @staticmethod
    def build_state_machine(
        framework: StrategicNarrativeFramework,
        character: AutonomousCharacterSeed
    ) -> Dict[str, Any]:
        """
        Generate narrative state machine with phases and rules
        
        Args:
            framework: Strategic narrative framework
            character: Character seed for context
            
        Returns:
            State machine configuration dictionary
        """
        return {
            "current_phase": "PHASE_1_THE_WAKE_UP_CALL",
            "allowed_narrative_goals": [
                "Mengeluh tentang gaji yang cepat habis.",
                "Menyadari pola belanja impulsif.",
                f"Marah pada {framework.the_enemy.name}."
            ],
            "forbidden_narrative_goals": [
                "Memberikan solusi finansial ahli.",
                "Mengajarkan cara investasi saham.",
                "Menjadi sukses tiba-tiba."
            ],
            "brand_integration_rule": "LEVEL_0_AMBIENT (Produk hanya boleh disebut sebagai 'alat bantu', bukan pahlawan penyelamat hidup. Jangan hard selling.)"
        }


class OrlicFrameworkImplementation:
    """Structures Orlic framework as actionable script templates"""
    
    @staticmethod
    def build_framework_implementation(framework: StrategicNarrativeFramework) -> Dict[str, Any]:
        """
        Generate Orlic framework as script structure template
        
        Args:
            framework: Strategic narrative framework
            
        Returns:
            Orlic framework implementation dictionary
        """
        return {
            "identified_enemy": framework.the_enemy.name,
            "world_view": framework.the_world_status_quo.description,
            "script_structure_template": [
                {
                    "sequence": 1,
                    "type": "THE_WORLD (Hook)",
                    "instruction": f"Mulai dengan observasi sinis tentang: {framework.the_world_status_quo.consensus_reality}"
                },
                {
                    "sequence": 2,
                    "type": "THE_ENEMY (Conflict)",
                    "instruction": f"Tunjukkan bagaimana {framework.the_enemy.manifestation}"
                },
                {
                    "sequence": 3,
                    "type": "THE_CHANGE (Realization)",
                    "instruction": f"Momen 'Glitch': {framework.the_change_vehicle.what_is_new}"
                }
            ]
        }


class TruthTerminalLoreEngine:
    """Builds autonomous lore management system with memory and obsessions"""
    
    @staticmethod
    def build_lore_engine(character: AutonomousCharacterSeed) -> Dict[str, Any]:
        """
        Generate Truth Terminal lore engine with obsessions and memory
        
        Args:
            character: Character seed with lore and evolution parameters
            
        Returns:
            Lore engine configuration dictionary
        """
        return {
            "active_obsessions": character.lore_seed.obsession_topics,
            "memory_buffer": [
                "Trauma: Minggu lalu gagal bayar tagihan tepat waktu.",
                "Insight: Teman kantor yang gayanya hedon ternyata hutangnya banyak."
            ],
            "hallucination_guidance": character.evolution_parameters.hallucination_permission
        }


# Convenience functions for direct use
def build_full_system_prompt(validated_input: NarrativeGenesisInput) -> str:
    """Build complete system prompt from validated input"""
    return PromptBuilder.build_system_prompt(
        validated_input.autonomous_character_seed,
        validated_input.strategic_narrative_framework,
        validated_input.brand_identity_core,
        validated_input.target_audience_context
    )


def extract_all_contexts(validated_input: NarrativeGenesisInput) -> Dict[str, Any]:
    """Extract all contexts from validated input"""
    return ContextMerger.merge_contexts(
        validated_input.brand_identity_core,
        validated_input.strategic_narrative_framework,
        validated_input.autonomous_character_seed,
        validated_input.target_audience_context
    )


if __name__ == "__main__":
    print("Transformers module loaded. Import and use transformation functions.")
