#!/usr/bin/env python3
"""
Pillar 1: Narrative Genesis Input Processor - Streamlit UI
Interactive web interface for creating and managing narrative input.
"""

import streamlit as st
import json
from datetime import datetime
from pathlib import Path

from ui_helpers import (
    initialize_session_state,
    create_dynamic_list,
    build_input_dict_from_session,
    load_session_from_dict,
    validate_input_data,
    show_validation_result,
    check_tone_overlap,
    load_example_data,
    get_section_completion
)
from ui_styles import (
    load_custom_styles,
    create_section_header,
    create_subsection_header,
    show_progress_bar,
    show_info_box
)
from processors.transformers import build_full_system_prompt
from process_narrative import generate_pillars_from_data


# Page configuration
st.set_page_config(
    page_title="Pillar 1: Narrative Genesis",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom styles
load_custom_styles()

# Initialize session state
initialize_session_state()

# App title
st.title("📝 Pillar 1: Narrative Genesis Input Processor")
st.markdown("*Interactive UI for creating AI agent configurations*")
st.markdown("---")

# Sidebar navigation
with st.sidebar:
    st.header("🧭 Navigation")
    
    sections = [
        "Project Info",
        "Brand Identity",
        "Strategic Narrative",
        "Character Seed",
        "Target Audience",
        "Generate & Export"
    ]
    
    # Show completion status
    completion = get_section_completion()
    
    for section in sections:
        is_complete = completion.get(section, False)
        icon = "✓" if is_complete else "○"
        if st.button(f"{icon} {section}", key=f"nav_{section}", use_container_width=True):
            st.session_state.current_section = section
    
    st.markdown("---")
    
    # Progress indicator
    complete_count = sum(1 for v in completion.values() if v)
    progress_pct = (complete_count / len(completion)) * 100
    st.markdown("**Overall Progress**")
    show_progress_bar(progress_pct, f"{complete_count}/{len(completion)}")
    
    st.markdown("---")
    
    # Quick actions
    st.header("⚡ Quick Actions")
    
    if st.button("📁 Load Example (FrugalFin)", use_container_width=True):
        if load_example_data():
            st.success("✓ Example loaded!")
            st.rerun()
        else:
            st.error("✗ Example file not found")
    
    uploaded_file = st.file_uploader("📤 Upload JSON", type=['json'])
    if uploaded_file is not None:
        try:
            data = json.load(uploaded_file)
            load_session_from_dict(data)
            st.success("✓ JSON loaded successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"✗ Error loading JSON: {str(e)}")
    
    if st.button("🔄 Reset All Fields", use_container_width=True):
        for key in list(st.session_state.keys()):
            if not key.startswith('_'):
                del st.session_state[key]
        st.rerun()


# Main content area
current_section = st.session_state.current_section

# ============================================================================
# SECTION 1: PROJECT INFO
# ============================================================================
if current_section == "Project Info":
    create_section_header("Project Information", "ℹ️")
    
    st.session_state.meta_project_name = st.text_input(
        "Project Name *",
        value=st.session_state.meta_project_name,
        help="Name of your project or campaign",
        placeholder="e.g., FrugalFin Launch Alpha"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.meta_version = st.text_input(
            "Version",
            value=st.session_state.meta_version,
            help="Version number or identifier"
        )
    with col2:
        st.session_state.meta_input_by = st.text_input(
            "Created By *",
            value=st.session_state.meta_input_by,
            help="Your name or role",
            placeholder="e.g., Brand Strategy Lead"
        )
    
    # Timestamp (auto-generated but editable)
    st.caption("Timestamp (ISO format)")
    st.session_state.meta_timestamp = st.text_input(
        "Timestamp",
        value=st.session_state.meta_timestamp,
        help="ISO format timestamp",
        label_visibility="collapsed"
    )
    
    if st.button("🕐 Update to Current Time"):
        st.session_state.meta_timestamp = datetime.now().isoformat()
        st.rerun()
    
    st.markdown("---")
    if st.button("Next: Brand Identity →", type="primary"):
        st.session_state.current_section = "Brand Identity"
        st.rerun()


# ============================================================================
# SECTION 2: BRAND IDENTITY
# ============================================================================
elif current_section == "Brand Identity":
    create_section_header("Brand Identity Core", "🎯")
    
    st.session_state.brand_product_name = st.text_input(
        "Product Name *",
        value=st.session_state.brand_product_name,
        help="The name of your product or service",
        placeholder="e.g., FrugalFin"
    )
    
    st.session_state.brand_archetype = st.text_input(
        "Brand Archetype *",
        value=st.session_state.brand_archetype,
        help="The archetypal identity of your brand",
        placeholder="e.g., The Enlightened Rebel"
    )
    
    st.session_state.brand_philosophy = st.text_area(
        "Core Philosophy *",
        value=st.session_state.brand_philosophy,
        help="Your brand's core belief or mission statement",
        placeholder="e.g., Money is a tool for freedom, not for showing off",
        height=100
    )
    
    create_subsection_header("Tone Guardrails")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Allowed Tones** *")
        st.caption("Tones your brand SHOULD use")
        
        # Common tone options
        common_allowed = ["Sarcastic", "Raw/Unfiltered", "Data-driven", "Cult-like (in a fun way)", 
                          "Empowering", "Witty", "Casual", "Professional"]
        
        selected_allowed = st.multiselect(
            "Select allowed tones",
            options=common_allowed,
            default=[t for t in st.session_state.brand_allowed_tones if t in common_allowed],
            key="allowed_multiselect",
            label_visibility="collapsed"
        )
        
        # Custom allowed tones
        custom_allowed = st.text_input(
            "Add custom allowed tone",
            key="custom_allowed",
            placeholder="Type and press Enter"
        )
        if custom_allowed and st.button("➕ Add", key="add_allowed"):
            if custom_allowed not in selected_allowed:
                selected_allowed.append(custom_allowed)
        
        st.session_state.brand_allowed_tones = selected_allowed
    
    with col2:
        st.markdown("**Forbidden Tones** *")
        st.caption("Tones your brand should NEVER use")
        
        # Common forbidden options
        common_forbidden = ["Corporate Speak", "Preachy/Motivator Style", "Judging Poverty",
                           "Condescending", "Overly Technical", "Boring", "Generic"]
        
        selected_forbidden = st.multiselect(
            "Select forbidden tones",
            options=common_forbidden,
            default=[t for t in st.session_state.brand_forbidden_tones if t in common_forbidden],
            key="forbidden_multiselect",
            label_visibility="collapsed"
        )
        
        # Custom forbidden tones
        custom_forbidden = st.text_input(
            "Add custom forbidden tone",
            key="custom_forbidden",
            placeholder="Type and press Enter"
        )
        if custom_forbidden and st.button("➕ Add", key="add_forbidden"):
            if custom_forbidden not in selected_forbidden:
                selected_forbidden.append(custom_forbidden)
        
        st.session_state.brand_forbidden_tones = selected_forbidden
    
    # Check for tone overlap
    overlap_warning = check_tone_overlap()
    if overlap_warning:
        st.warning(overlap_warning)
    else:
        st.success("✓ No tone overlap detected")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back: Project Info"):
            st.session_state.current_section = "Project Info"
            st.rerun()
    with col2:
        if st.button("Next: Strategic Narrative →", type="primary"):
            st.session_state.current_section = "Strategic Narrative"
            st.rerun()


# ============================================================================
# SECTION 3: STRATEGIC NARRATIVE
# ============================================================================
elif current_section == "Strategic Narrative":
    create_section_header("Strategic Narrative Framework", "📖")
    st.caption("Matt Orlić Framework - Storytelling that Sells")
    
    # The World Status Quo
    create_subsection_header("The World (Status Quo)")
    
    st.session_state.world_description = st.text_area(
        "Description of Current Reality *",
        value=st.session_state.world_description,
        help="Describe the current broken state of the world",
        placeholder="e.g., A world where people are enslaved by social validation and shopping algorithms",
        height=100
    )
    
    st.session_state.world_consensus = st.text_area(
        "Consensus Reality *",
        value=st.session_state.world_consensus,
        help="What people currently believe (that's actually a trap)",
        placeholder="e.g., People believe 'Self Reward' is mandatory, when it's actually a marketing trap",
        height=100
    )
    
    # The Enemy
    create_subsection_header("The Enemy")
    
    st.session_state.enemy_name = st.text_input(
        "Enemy Name *",
        value=st.session_state.enemy_name,
        help="Name of the antagonist or problem",
        placeholder="e.g., The Algorithmic Consumerism"
    )
    
    st.session_state.enemy_manifestation = st.text_area(
        "How The Enemy Shows Up *",
        value=st.session_state.enemy_manifestation,
        help="Concrete examples of how the enemy manifests",
        placeholder="e.g., Discount notifications, FOMO instagram, Paylater traps",
        height=100
    )
    
    st.session_state.enemy_why_fight = st.text_area(
        "Why We Must Fight It *",
        value=st.session_state.enemy_why_fight,
        help="Why this enemy must be defeated",
        placeholder="e.g., Because this system is designed to keep you poor forever",
        height=100
    )
    
    # The Change Vehicle
    create_subsection_header("The Change Vehicle")
    
    st.session_state.change_what_new = st.text_area(
        "What's New (The Insight) *",
        value=st.session_state.change_what_new,
        help="The new awareness or tool that enables change",
        placeholder="e.g., New awareness (Gnosis) that we can outsmart the system with data",
        height=100
    )
    
    st.session_state.change_mechanism = st.text_area(
        "How It Works (The Mechanism) *",
        value=st.session_state.change_mechanism,
        help="How your solution actually works",
        placeholder="e.g., FrugalFin AI that visualizes your 'broke future' if you buy that coffee",
        height=100
    )
    
    # The Promised Land
    create_subsection_header("The Promised Land")
    
    st.session_state.promised_vision = st.text_area(
        "The Vision *",
        value=st.session_state.promised_vision,
        help="The desired future state",
        placeholder="e.g., Freedom from fear of checking your ATM balance. Living 'Low Profile, High Profit'",
        height=100
    )
    
    st.session_state.promised_payoff = st.text_area(
        "Emotional Payoff *",
        value=st.session_state.promised_payoff,
        help="The emotional benefit of reaching the promised land",
        placeholder="e.g., Peace of Mind & Total Control",
        height=100
    )

    # Emotional Transformation Thesis
    create_subsection_header("Emotional Transformation (From → To)")
    st.caption("Capture the emotional journey your audience experiences across the narrative.")
    
    st.session_state.transformation_from_state = st.text_area(
        "From (Pain State) *",
        value=st.session_state.transformation_from_state,
        help="Describe the emotional starting point (pain, confusion, overwhelm, insecurity, chaos, etc.)",
        placeholder="e.g., Overwhelmed, insecure about money decisions, constantly anxious about spending.",
        height=80
    )
    
    st.session_state.transformation_to_state = st.text_area(
        "To (Desired State) *",
        value=st.session_state.transformation_to_state,
        help="Describe the desired emotional end state after transformation (clarity, control, confidence, etc.)",
        placeholder="e.g., Fully in control, confident about every purchase, clear long-term financial direction.",
        height=80
    )
    
    # Proof Points
    create_subsection_header("Proof Points")
    st.caption("Evidence and validation that your solution works")
    
    st.session_state.proof_points = create_dynamic_list(
        "proof_points",
        "Proof Point",
        st.session_state.proof_points,
        "Add concrete evidence (stats, testimonials, etc.)"
    )
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back: Brand Identity"):
            st.session_state.current_section = "Brand Identity"
            st.rerun()
    with col2:
        if st.button("Next: Character Seed →", type="primary"):
            st.session_state.current_section = "Character Seed"
            st.rerun()


# ============================================================================
# SECTION 4: CHARACTER SEED
# ============================================================================
elif current_section == "Character Seed":
    create_section_header("Autonomous Character Seed", "🎭")
    st.caption("Truth Terminal Concept - Character with evolution capability")
    
    # Base Persona
    create_subsection_header("Base Persona")
    
    st.session_state.character_name = st.text_input(
        "Character Name *",
        value=st.session_state.character_name,
        help="Name of your character/persona",
        placeholder="e.g., Sarah"
    )
    
    st.session_state.character_role = st.text_input(
        "Character Role *",
        value=st.session_state.character_role,
        help="Their role or identity",
        placeholder="e.g., The Glitch in the Matrix"
    )
    
    st.session_state.character_demographics = st.text_area(
        "Demographics *",
        value=st.session_state.character_demographics,
        help="Age, location, situation",
        placeholder="e.g., 24 years old, Jakarta, Salary UMR++, Debt-ridden",
        height=100
    )
    
    st.session_state.product_relation = st.selectbox(
        "Relationship to Product *",
        options=[
            "The Unaware/Novice",
            "The Skeptic",
            "The Stumbler",
            "The Convert",
        ],
        index=[
            "The Unaware/Novice",
            "The Skeptic",
            "The Stumbler",
            "The Convert",
        ].index(st.session_state.product_relation if st.session_state.product_relation in [
            "The Unaware/Novice",
            "The Skeptic",
            "The Stumbler",
            "The Convert",
        ] else "The Unaware/Novice"),
        help="How this character currently relates to your product or solution"
    )
    
    st.session_state.social_setting = st.text_area(
        "Social Setting / Environment",
        value=st.session_state.social_setting,
        help="Describe the primary environment where this character spends most of their time",
        placeholder="e.g., Fast-paced startup office in South Jakarta; cramped kost with 3 roommates; noisy open-plan office.",
        height=80
    )
    
    # Lore Seed
    create_subsection_header("Lore Seed (Character's Inner World)")
    
    st.session_state.lore_belief = st.text_area(
        "Central Belief *",
        value=st.session_state.lore_belief,
        help="The character's core worldview",
        placeholder="e.g., The world financial system is designed to impoverish Gen Z",
        height=100
    )
    
    st.session_state.lore_style = st.text_area(
        "Internal Monologue Style *",
        value=st.session_state.lore_style,
        help="How the character thinks and talks to themselves",
        placeholder="e.g., Paranoid but logical. Often talks to self about coffee price conspiracies",
        height=100
    )
    
    st.markdown("**Obsession Topics** *")
    st.caption("What the character is obsessed with")
    st.session_state.lore_obsessions = create_dynamic_list(
        "lore_obsessions",
        "Obsession",
        st.session_state.lore_obsessions,
        "Topics the character can't stop thinking about"
    )
    
    st.session_state.lore_affliction = st.text_area(
        "The Affliction (Internal Wound) *",
        value=st.session_state.lore_affliction,
        help="Describe the recurring internal pain, insecurity, or wound this character carries.",
        placeholder='e.g., Always feels left behind compared to college friends; terrified of making another \"stupid\" financial decision.',
        height=100
    )
    
    st.session_state.lore_aspiration = st.text_area(
        "The Aspiration (Specific Goal) *",
        value=st.session_state.lore_aspiration,
        help="Describe a concrete, time-bound goal the character wants to achieve in the next 3–6 months.",
        placeholder="e.g., Land the first paying client; save 20M emergency fund; lose 10kg before the wedding.",
        height=100
    )
    
    # Evolution Parameters
    create_subsection_header("Evolution Parameters")
    
    st.session_state.evolution_autonomy = st.selectbox(
        "Autonomy Level *",
        options=["Low", "Medium", "High"],
        index=["Low", "Medium", "High"].index(st.session_state.evolution_autonomy),
        help="How much freedom the character has to deviate from script"
    )
    
    st.session_state.evolution_memory = st.text_input(
        "Memory Retention *",
        value=st.session_state.evolution_memory,
        help="How the character remembers past events",
        placeholder="e.g., Cumulative (Remembers last week's failures as trauma)"
    )
    
    st.session_state.evolution_hallucination = st.text_input(
        "Hallucination Permission *",
        value=st.session_state.evolution_hallucination,
        help="Permission to imagine scenarios (must contain: Allowed, Not Allowed, or Limited)",
        placeholder="e.g., Allowed (Can imagine 'Dystopian Future' if spending)"
    )
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back: Strategic Narrative"):
            st.session_state.current_section = "Strategic Narrative"
            st.rerun()
    with col2:
        if st.button("Next: Target Audience →", type="primary"):
            st.session_state.current_section = "Target Audience"
            st.rerun()


# ============================================================================
# SECTION 5: TARGET AUDIENCE
# ============================================================================
elif current_section == "Target Audience":
    create_section_header("Target Audience Context", "👥")
    
    st.session_state.audience_code = st.text_input(
        "Persona Code *",
        value=st.session_state.audience_code,
        help="Identifier for your target audience segment",
        placeholder="e.g., GENZ_STRUGGLE_01"
    )
    
    st.markdown("**Pain Points** *")
    st.caption("What struggles or frustrations does your audience face?")
    st.session_state.audience_pain_points = create_dynamic_list(
        "audience_pain_points",
        "Pain Point",
        st.session_state.audience_pain_points,
        "Specific problems or frustrations"
    )
    
    create_subsection_header("Language Model")
    
    st.markdown("**Slang Whitelist** *")
    st.caption("Slang terms and expressions your audience uses")
    st.session_state.audience_slang = create_dynamic_list(
        "audience_slang",
        "Slang Term",
        st.session_state.audience_slang,
        "Words and phrases from their vocabulary"
    )
    
    st.markdown("**Cultural References** *")
    st.caption("Cultural touchpoints your audience relates to")
    st.session_state.audience_references = create_dynamic_list(
        "audience_references",
        "Cultural Reference",
        st.session_state.audience_references,
        "Pop culture, trends, phenomena they know"
    )
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back: Character Seed"):
            st.session_state.current_section = "Character Seed"
            st.rerun()
    with col2:
        if st.button("Next: Generate & Export →", type="primary"):
            st.session_state.current_section = "Generate & Export"
            st.rerun()


# ============================================================================
# SECTION 6: GENERATE & EXPORT
# ============================================================================
elif current_section == "Generate & Export":
    create_section_header("Generate & Export", "🚀")
    
    # Validate input
    st.subheader("1. Validate Input")
    st.caption("Check if your input is complete and valid")
    
    if st.button("🔍 Validate Input", type="primary", use_container_width=True):
        with st.spinner("Validating..."):
            input_dict = build_input_dict_from_session()
            report = validate_input_data(input_dict)
            st.session_state.validation_result = report
    
    if st.session_state.validation_result is not None:
        show_validation_result(st.session_state.validation_result)
    
    st.markdown("---")
    
    # Generate AI pillar outputs only (no legacy/non-AI configs)
    st.subheader("2. Generate AI Pillars 2/3/4")
    st.caption("Generate Pillar 2/3/4 JSON via a single LLM call (OpenRouter)")
    
    if st.button("⚙️ Generate AI Pillars", use_container_width=True):
        if st.session_state.validation_result is None or not st.session_state.validation_result.is_valid:
            st.error("❌ Please validate your input first and fix any errors")
        else:
            with st.spinner("Generating AI pillar outputs..."):
                pillars_output_root = Path("output")
                try:
                    pillar_paths = generate_pillars_from_data(
                        st.session_state.validation_result.data,
                        pillars_output_root,
                        source_input="ui_session"
                    )
                    st.session_state.pillar_paths = pillar_paths
                    st.success("✅ AI Pillar outputs (2/3/4) generated successfully!")
                except Exception as e:
                    st.error(f"❌ Error generating AI pillar outputs: {str(e)}")

    # Always show download/preview section when pillar paths are available
    pillar_paths = st.session_state.get("pillar_paths", {})
    if pillar_paths:
        st.write("**Download & Preview AI Pillar Outputs:**")

        # Pillar 2
        p2_file = pillar_paths.get("pillar2")
        if p2_file and Path(p2_file).exists():
            with open(p2_file, "r", encoding="utf-8") as f:
                p2_content = f.read()

            col1, col2 = st.columns([3, 1])
            with col1:
                st.download_button(
                    "📥 Download Pillar 2 Hook Intelligence (JSON)",
                    data=p2_content,
                    file_name="output_pillar2_psycho_tags_v2.1.json",
                    mime="application/json",
                    use_container_width=True,
                )
            with col2:
                if st.button("👁️ Preview", key="preview_p2", use_container_width=True):
                    st.session_state.show_p2_preview = True

            if st.session_state.get("show_p2_preview", False):
                with st.expander("📄 Pillar 2 Preview", expanded=True):
                    try:
                        st.json(json.loads(p2_content))
                    except Exception:
                        st.text(p2_content)
                    if st.button("✖️ Close Preview", key="close_p2"):
                        st.session_state.show_p2_preview = False
                        st.rerun()

        # Pillar 3
        p3_ai_file = pillar_paths.get("pillar3")
        if p3_ai_file and Path(p3_ai_file).exists():
            with open(p3_ai_file, "r", encoding="utf-8") as f:
                p3_ai_content = f.read()

            col1, col2 = st.columns([3, 1])
            with col1:
                st.download_button(
                    "📥 Download Pillar 3 Logic Context (AI JSON)",
                    data=p3_ai_content,
                    file_name="output_pillar3_logic_context_v2.1.json",
                    mime="application/json",
                    use_container_width=True,
                )
            with col2:
                if st.button("👁️ Preview", key="preview_p3", use_container_width=True):
                    st.session_state.show_p3_preview = True

            if st.session_state.get("show_p3_preview", False):
                with st.expander("📄 Pillar 3 Preview", expanded=True):
                    try:
                        st.json(json.loads(p3_ai_content))
                    except Exception:
                        st.text(p3_ai_content)
                    if st.button("✖️ Close Preview", key="close_p3"):
                        st.session_state.show_p3_preview = False
                        st.rerun()

        # Pillar 4
        p4_file = pillar_paths.get("pillar4")
        if p4_file and Path(p4_file).exists():
            with open(p4_file, "r", encoding="utf-8") as f:
                p4_content = f.read()

            col1, col2 = st.columns([3, 1])
            with col1:
                st.download_button(
                    "📥 Download Pillar 4 Visual Guide (JSON)",
                    data=p4_content,
                    file_name="output_pillar4_visual_guide_v2.1.json",
                    mime="application/json",
                    use_container_width=True,
                )
            with col2:
                if st.button("👁️ Preview", key="preview_p4", use_container_width=True):
                    st.session_state.show_p4_preview = True

            if st.session_state.get("show_p4_preview", False):
                with st.expander("📄 Pillar 4 Preview", expanded=True):
                    try:
                        st.json(json.loads(p4_content))
                    except Exception:
                        st.text(p4_content)
                    if st.button("✖️ Close Preview", key="close_p4"):
                        st.session_state.show_p4_preview = False
                        st.rerun()
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back: Target Audience"):
            st.session_state.current_section = "Target Audience"
            st.rerun()


# Footer
st.markdown("---")
st.caption("Pillar 1: Narrative Genesis Input Processor v2.0")
st.caption("Matt Orlić Framework + Truth Terminal Concept")
