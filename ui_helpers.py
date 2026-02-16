"""
UI Helper Functions for Streamlit Interface
Provides utilities for form management, validation, and data handling.
"""

import streamlit as st
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

from processors.validator import NarrativeValidator, ValidationReport
from schemas.narrative_genesis_schema import NarrativeGenesisInput


def initialize_session_state():
    """Initialize all session state variables with default values"""
    
    # Meta
    if 'meta_project_name' not in st.session_state:
        st.session_state.meta_project_name = "Launch Campaign Q1"
    if 'meta_version' not in st.session_state:
        st.session_state.meta_version = "1.0"
    if 'meta_input_by' not in st.session_state:
        st.session_state.meta_input_by = ""
    if 'meta_timestamp' not in st.session_state:
        st.session_state.meta_timestamp = datetime.now().isoformat()
    
    # Brand Identity
    if 'brand_product_name' not in st.session_state:
        st.session_state.brand_product_name = "FocusFlow"
    if 'brand_archetype' not in st.session_state:
        st.session_state.brand_archetype = ""
    if 'brand_philosophy' not in st.session_state:
        st.session_state.brand_philosophy = ""
    if 'brand_allowed_tones' not in st.session_state:
        st.session_state.brand_allowed_tones = []
    if 'brand_forbidden_tones' not in st.session_state:
        st.session_state.brand_forbidden_tones = []
    
    # Strategic Narrative - World
    if 'world_description' not in st.session_state:
        st.session_state.world_description = "Dunia di mana kesibukan dianggap sebagai produktivitas. Notifikasi tidak pernah berhenti."
    if 'world_consensus' not in st.session_state:
        st.session_state.world_consensus = "Jika kalender penuh dan selalu sibuk, berarti kamu produktif dan berharga."
    
    # Strategic Narrative - Enemy
    if 'enemy_name' not in st.session_state:
        st.session_state.enemy_name = "The Distraction Economy"
    if 'enemy_manifestation' not in st.session_state:
        st.session_state.enemy_manifestation = "Notifikasi chat, email masuk tanpa henti, meeting dadakan, dan social media yang terus menarik perhatian."
    if 'enemy_why_fight' not in st.session_state:
        st.session_state.enemy_why_fight = "Karena seluruh model bisnisnya dibangun dari fokus kita yang hancur dan energi kita yang habis."
    
    # Strategic Narrative - Change Vehicle
    if 'change_what_new' not in st.session_state:
        st.session_state.change_what_new = "AI-driven Deep Work protection."
    if 'change_mechanism' not in st.session_state:
        st.session_state.change_mechanism = "FocusFlow memblokir distraksi, mengatur blok Deep Work, dan menjaga energi dengan ritme kerja yang sehat."
    
    # Strategic Narrative - Promised Land
    if 'promised_vision' not in st.session_state:
        st.session_state.promised_vision = "Keseimbangan hidup di mana pekerjaan selesai tepat waktu tanpa lembur."
    if 'promised_payoff' not in st.session_state:
        st.session_state.promised_payoff = "Rasa tenang, jam kerja yang manusiawi, dan ruang untuk hidup di luar pekerjaan."

    # Strategic Narrative - Transformation Thesis
    if 'transformation_from_state' not in st.session_state:
        st.session_state.transformation_from_state = "Anxious, Reactive, & Overwhelmed. Cemas dan selalu bereaksi dadakan terhadap semua permintaan."
    if 'transformation_to_state' not in st.session_state:
        st.session_state.transformation_to_state = "Intentional, Calm, & In Control. Bekerja dengan sengaja, tenang, dan memegang kendali atas kalender dan energinya."
    
    # Proof Points
    if 'proof_points' not in st.session_state:
        st.session_state.proof_points = [""]
    
    # Character - Base Persona
    if 'character_name' not in st.session_state:
        st.session_state.character_name = "Sarah"
    if 'character_role' not in st.session_state:
        st.session_state.character_role = "Senior Marketing Associate"
    if 'character_demographics' not in st.session_state:
        st.session_state.character_demographics = "28 tahun, tinggal di Jakarta Selatan, bekerja di tech startup."
    if 'product_relation' not in st.session_state:
        st.session_state.product_relation = "The Stumbler"
    if 'social_setting' not in st.session_state:
        st.session_state.social_setting = "Open-plan office yang berisik, penuh meeting mendadak dan budaya 'ASAP'."
    
    # Character - Lore Seed
    if 'lore_belief' not in st.session_state:
        st.session_state.lore_belief = "Untuk bisa dianggap berharga, dia harus selalu sibuk dan tidak boleh terlihat santai."
    if 'lore_style' not in st.session_state:
        st.session_state.lore_style = "Overthinking, penuh self-criticism, tapi diam-diam sangat terstruktur di dalam kepala."
    if 'lore_obsessions' not in st.session_state:
        st.session_state.lore_obsessions = [
            "Promosi jabatan",
            "Perform di mata atasan",
            "Time management dan produktivitas"
        ]
    if 'lore_affliction' not in st.session_state:
        st.session_state.lore_affliction = (
            "Imposter Syndrome akut. Dia merasa harus bekerja 12 jam sehari hanya untuk membuktikan bahwa "
            "dia 'pantas' berada di posisinya. Dia takut jika dia istirahat, orang akan sadar dia tidak secerdas itu."
        )
    if 'lore_aspiration' not in st.session_state:
        st.session_state.lore_aspiration = (
            "Mendapatkan promosi menjadi 'Marketing Manager' dalam 3 bulan ke depan tanpa harus masuk rumah sakit "
            "karena tipes (burnout)."
        )
    
    # Character - Evolution
    if 'evolution_autonomy' not in st.session_state:
        st.session_state.evolution_autonomy = "Medium"
    if 'evolution_memory' not in st.session_state:
        st.session_state.evolution_memory = ""
    if 'evolution_hallucination' not in st.session_state:
        st.session_state.evolution_hallucination = ""
    
    # Target Audience
    if 'audience_code' not in st.session_state:
        st.session_state.audience_code = ""
    if 'audience_pain_points' not in st.session_state:
        st.session_state.audience_pain_points = [""]
    if 'audience_slang' not in st.session_state:
        st.session_state.audience_slang = [""]
    if 'audience_references' not in st.session_state:
        st.session_state.audience_references = [""]
    
    # UI State
    if 'current_section' not in st.session_state:
        st.session_state.current_section = "Project Info"
    if 'validation_result' not in st.session_state:
        st.session_state.validation_result = None
    if 'system_prompt_preview' not in st.session_state:
        st.session_state.system_prompt_preview = ""
    if 'pillar_paths' not in st.session_state:
        st.session_state.pillar_paths = {}
    if 'show_p2_preview' not in st.session_state:
        st.session_state.show_p2_preview = False
    if 'show_p3_preview' not in st.session_state:
        st.session_state.show_p3_preview = False
    if 'show_p4_preview' not in st.session_state:
        st.session_state.show_p4_preview = False


def create_dynamic_list(key: str, label: str, items: List[str], help_text: str = "") -> List[str]:
    """
    Create a dynamic list widget with add/remove buttons
    
    Args:
        key: Unique key for the widget
        label: Label to display
        items: Current list of items
        help_text: Optional help text
        
    Returns:
        Updated list of items
    """
    st.markdown(f"**{label}**")
    if help_text:
        st.caption(help_text)
    
    updated_items = []
    
    for i, item in enumerate(items):
        col1, col2 = st.columns([5, 1])
        with col1:
            value = st.text_input(
                f"{label} {i+1}",
                value=item,
                key=f"{key}_{i}",
                label_visibility="collapsed"
            )
            updated_items.append(value)
        with col2:
            if len(items) > 1:
                if st.button("🗑️", key=f"{key}_remove_{i}", help="Remove this item"):
                    updated_items.pop(i)
                    return updated_items
    
    if st.button(f"➕ Add {label}", key=f"{key}_add"):
        updated_items.append("")
    
    return updated_items


def build_input_dict_from_session() -> Dict[str, Any]:
    """
    Build complete input dictionary from session state
    
    Returns:
        Dictionary matching NarrativeGenesisInput structure
    """
    return {
        "meta": {
            "project_name": st.session_state.meta_project_name,
            "version": st.session_state.meta_version,
            "input_by": st.session_state.meta_input_by,
            "timestamp": st.session_state.meta_timestamp
        },
        "brand_identity_core": {
            "product_name": st.session_state.brand_product_name,
            "archetype": st.session_state.brand_archetype,
            "core_philosophy": st.session_state.brand_philosophy,
            "tone_guardrails": {
                "allowed": [t for t in st.session_state.brand_allowed_tones if t.strip()],
                "forbidden": [t for t in st.session_state.brand_forbidden_tones if t.strip()]
            }
        },
        "strategic_narrative_framework": {
            "comment": "User input from Streamlit UI",
            "the_world_status_quo": {
                "description": st.session_state.world_description,
                "consensus_reality": st.session_state.world_consensus
            },
            "the_enemy": {
                "name": st.session_state.enemy_name,
                "manifestation": st.session_state.enemy_manifestation,
                "why_fight_it": st.session_state.enemy_why_fight
            },
            "the_change_vehicle": {
                "what_is_new": st.session_state.change_what_new,
                "mechanism": st.session_state.change_mechanism
            },
            "the_promised_land": {
                "vision": st.session_state.promised_vision,
                "emotional_payoff": st.session_state.promised_payoff
            },
            "transformation_thesis": {
                "from_state": st.session_state.transformation_from_state,
                "to_state": st.session_state.transformation_to_state
            },
            "proof_points": [p for p in st.session_state.proof_points if p.strip()]
        },
        "autonomous_character_seed": {
            "comment": "Character with autonomous evolution capability",
            "base_persona": {
                "name": st.session_state.character_name,
                "role": st.session_state.character_role,
                "demographics": st.session_state.character_demographics,
                "product_relation": st.session_state.product_relation,
                "social_setting": st.session_state.social_setting or None
            },
            "lore_seed": {
                "central_belief": st.session_state.lore_belief,
                "internal_monologue_style": st.session_state.lore_style,
                "obsession_topics": [o for o in st.session_state.lore_obsessions if o.strip()],
                "affliction": st.session_state.lore_affliction,
                "aspiration": st.session_state.lore_aspiration
            },
            "evolution_parameters": {
                "autonomy_level": st.session_state.evolution_autonomy,
                "memory_retention": st.session_state.evolution_memory,
                "hallucination_permission": st.session_state.evolution_hallucination
            }
        },
        "target_audience_context": {
            "persona_code": st.session_state.audience_code,
            "pain_points": [p for p in st.session_state.audience_pain_points if p.strip()],
            "language_model": {
                "slang_whitelist": [s for s in st.session_state.audience_slang if s.strip()],
                "cultural_references": [r for r in st.session_state.audience_references if r.strip()]
            }
        }
    }


def load_session_from_dict(data: Dict[str, Any]):
    """
    Populate session state from input dictionary
    
    Args:
        data: Dictionary matching NarrativeGenesisInput structure
    """
    # Meta
    st.session_state.meta_project_name = data.get("meta", {}).get("project_name", "")
    st.session_state.meta_version = data.get("meta", {}).get("version", "1.0")
    st.session_state.meta_input_by = data.get("meta", {}).get("input_by", "")
    st.session_state.meta_timestamp = data.get("meta", {}).get("timestamp", datetime.now().isoformat())
    
    # Brand Identity
    brand = data.get("brand_identity_core", {})
    st.session_state.brand_product_name = brand.get("product_name", "")
    st.session_state.brand_archetype = brand.get("archetype", "")
    st.session_state.brand_philosophy = brand.get("core_philosophy", "")
    st.session_state.brand_allowed_tones = brand.get("tone_guardrails", {}).get("allowed", [])
    st.session_state.brand_forbidden_tones = brand.get("tone_guardrails", {}).get("forbidden", [])
    
    # Strategic Narrative
    framework = data.get("strategic_narrative_framework", {})
    world = framework.get("the_world_status_quo", {})
    st.session_state.world_description = world.get("description", "")
    st.session_state.world_consensus = world.get("consensus_reality", "")
    
    enemy = framework.get("the_enemy", {})
    st.session_state.enemy_name = enemy.get("name", "")
    st.session_state.enemy_manifestation = enemy.get("manifestation", "")
    st.session_state.enemy_why_fight = enemy.get("why_fight_it", "")
    
    change = framework.get("the_change_vehicle", {})
    st.session_state.change_what_new = change.get("what_is_new", "")
    st.session_state.change_mechanism = change.get("mechanism", "")
    
    promised = framework.get("the_promised_land", {})
    st.session_state.promised_vision = promised.get("vision", "")
    st.session_state.promised_payoff = promised.get("emotional_payoff", "")
    
    thesis = framework.get("transformation_thesis", {})
    st.session_state.transformation_from_state = thesis.get("from_state", "")
    st.session_state.transformation_to_state = thesis.get("to_state", "")
    
    st.session_state.proof_points = framework.get("proof_points", [""])
    if not st.session_state.proof_points:
        st.session_state.proof_points = [""]
    
    # Character
    character = data.get("autonomous_character_seed", {})
    persona = character.get("base_persona", {})
    st.session_state.character_name = persona.get("name", "")
    st.session_state.character_role = persona.get("role", "")
    st.session_state.character_demographics = persona.get("demographics", "")
    st.session_state.product_relation = persona.get("product_relation", "The Unaware/Novice")
    st.session_state.social_setting = persona.get("social_setting", "")
    
    lore = character.get("lore_seed", {})
    st.session_state.lore_belief = lore.get("central_belief", "")
    st.session_state.lore_style = lore.get("internal_monologue_style", "")
    st.session_state.lore_obsessions = lore.get("obsession_topics", [""])
    if not st.session_state.lore_obsessions:
        st.session_state.lore_obsessions = [""]
    st.session_state.lore_affliction = lore.get("affliction", "")
    st.session_state.lore_aspiration = lore.get("aspiration", "")
    
    evolution = character.get("evolution_parameters", {})
    st.session_state.evolution_autonomy = evolution.get("autonomy_level", "Medium")
    st.session_state.evolution_memory = evolution.get("memory_retention", "")
    st.session_state.evolution_hallucination = evolution.get("hallucination_permission", "")
    
    # Target Audience
    audience = data.get("target_audience_context", {})
    st.session_state.audience_code = audience.get("persona_code", "")
    st.session_state.audience_pain_points = audience.get("pain_points", [""])
    if not st.session_state.audience_pain_points:
        st.session_state.audience_pain_points = [""]
    
    language = audience.get("language_model", {})
    st.session_state.audience_slang = language.get("slang_whitelist", [""])
    if not st.session_state.audience_slang:
        st.session_state.audience_slang = [""]
    st.session_state.audience_references = language.get("cultural_references", [""])
    if not st.session_state.audience_references:
        st.session_state.audience_references = [""]


def validate_input_data(data_dict: Dict[str, Any]) -> ValidationReport:
    """
    Validate input data using existing validator
    
    Args:
        data_dict: Input dictionary to validate
        
    Returns:
        ValidationReport with results
    """
    validator = NarrativeValidator()
    return validator.validate_from_dict(data_dict)


def export_to_json(data: Dict[str, Any]) -> str:
    """
    Format data as JSON string for export
    
    Args:
        data: Dictionary to export
        
    Returns:
        Formatted JSON string
    """
    return json.dumps(data, indent=2, ensure_ascii=False)


def show_validation_result(report: ValidationReport):
    """
    Display validation results with color coding
    
    Args:
        report: ValidationReport to display
    """
    if report.is_valid:
        st.success("✓ Validation Passed! Your input is valid.")
        
        # Show statistics
        validator = NarrativeValidator()
        validator.last_report = report
        stats = validator.get_validation_stats()
        
        with st.expander("📊 Input Statistics"):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Product", stats.get('product_name', 'N/A'))
                st.metric("Character", stats.get('character_name', 'N/A'))
                st.metric("Target Persona", stats.get('target_persona', 'N/A'))
            with col2:
                st.metric("Autonomy Level", stats.get('autonomy_level', 'N/A'))
                st.metric("Proof Points", stats.get('proof_points_count', 0))
                st.metric("Slang Terms", stats.get('slang_count', 0))
    else:
        st.error("✗ Validation Failed")
        st.write(f"Found **{len(report.errors)}** error(s):")
        
        for i, error in enumerate(report.errors, 1):
            with st.expander(f"Error {i}: {error.get('type', 'Unknown')}"):
                st.write(f"**Location:** {' → '.join(str(loc) for loc in error.get('loc', []))}")
                st.write(f"**Message:** {error.get('msg', 'No message')}")
                if 'input' in error and error['input'] != 'N/A':
                    st.write(f"**Input value:** `{error['input']}`")


def check_tone_overlap() -> Optional[str]:
    """
    Check if there's overlap between allowed and forbidden tones
    
    Returns:
        Warning message if overlap detected, None otherwise
    """
    allowed_set = set(t.lower().strip() for t in st.session_state.brand_allowed_tones if t.strip())
    forbidden_set = set(t.lower().strip() for t in st.session_state.brand_forbidden_tones if t.strip())
    overlap = allowed_set & forbidden_set
    
    if overlap:
        return f"⚠️ Warning: Tones appear in both lists: {', '.join(overlap)}"
    return None


def load_example_data():
    """Load FrugalFin example data into session"""
    example_file = Path("input_master.json")
    if example_file.exists():
        with open(example_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            load_session_from_dict(data)
            return True
    return False


def get_section_completion() -> Dict[str, bool]:
    """
    Check which sections are complete
    
    Returns:
        Dictionary mapping section names to completion status
    """
    return {
        "Project Info": bool(
            st.session_state.meta_project_name and
            st.session_state.meta_input_by
        ),
        "Brand Identity": bool(
            st.session_state.brand_product_name and
            st.session_state.brand_archetype and
            st.session_state.brand_philosophy and
            st.session_state.brand_allowed_tones and
            st.session_state.brand_forbidden_tones
        ),
        "Strategic Narrative": bool(
            st.session_state.world_description and
            st.session_state.enemy_name and
            st.session_state.promised_vision and
            any(p.strip() for p in st.session_state.proof_points) and
            st.session_state.transformation_from_state and
            st.session_state.transformation_to_state
        ),
        "Character Seed": bool(
            st.session_state.character_name and
            st.session_state.character_role and
            st.session_state.lore_belief and
            any(o.strip() for o in st.session_state.lore_obsessions) and
            st.session_state.lore_affliction and
            st.session_state.lore_aspiration and
            st.session_state.product_relation
        ),
        "Target Audience": bool(
            st.session_state.audience_code and
            any(p.strip() for p in st.session_state.audience_pain_points) and
            any(s.strip() for s in st.session_state.audience_slang)
        )
    }
