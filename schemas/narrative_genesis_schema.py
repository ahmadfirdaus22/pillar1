"""
Pydantic Schema Models for Narrative Genesis Input
Validates the complete input structure with strict type checking and business logic validation.
"""

from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime


class ToneGuardrails(BaseModel):
    """Tone guidelines for brand voice"""
    allowed: List[str] = Field(..., min_length=1, description="Allowed tone characteristics")
    forbidden: List[str] = Field(..., min_length=1, description="Forbidden tone characteristics")
    
    @model_validator(mode='after')
    def check_no_overlap(self):
        """Ensure allowed and forbidden lists don't overlap"""
        allowed_set = set(tone.lower() for tone in self.allowed)
        forbidden_set = set(tone.lower() for tone in self.forbidden)
        overlap = allowed_set & forbidden_set
        if overlap:
            raise ValueError(f"Tone guardrails overlap detected: {overlap}. A tone cannot be both allowed and forbidden.")
        return self


class BrandIdentityCore(BaseModel):
    """Core brand identity and philosophy"""
    product_name: str = Field(..., min_length=1, description="Product name")
    archetype: str = Field(..., min_length=1, description="Brand archetype")
    core_philosophy: str = Field(..., min_length=1, description="Core brand philosophy")
    tone_guardrails: ToneGuardrails


class TheWorld(BaseModel):
    """Status quo description - current state of reality"""
    description: str = Field(..., min_length=1)
    consensus_reality: str = Field(..., min_length=1)


class TheEnemy(BaseModel):
    """The antagonist or problem to fight against"""
    name: str = Field(..., min_length=1)
    manifestation: str = Field(..., min_length=1, description="How the enemy shows up")
    why_fight_it: str = Field(..., min_length=1, description="Why this enemy must be defeated")


class TheChangeVehicle(BaseModel):
    """The mechanism of transformation"""
    what_is_new: str = Field(..., min_length=1, description="What new insight or tool enables change")
    mechanism: str = Field(..., min_length=1, description="How the change vehicle works")


class ThePromisedLand(BaseModel):
    """The desired future state"""
    vision: str = Field(..., min_length=1, description="Vision of the future")
    emotional_payoff: str = Field(..., min_length=1, description="Emotional benefit")


class TransformationThesis(BaseModel):
    """Emotional transformation from pain to desired state"""
    from_state: str = Field(..., min_length=1, description="Emotional starting point or pain state")
    to_state: str = Field(..., min_length=1, description="Desired emotional outcome state")


class StrategicNarrativeFramework(BaseModel):
    """Matt Orlić framework - Storytelling that Sells structure"""
    comment: Optional[str] = None
    the_world_status_quo: TheWorld
    the_enemy: TheEnemy
    the_change_vehicle: TheChangeVehicle
    the_promised_land: ThePromisedLand
    transformation_thesis: TransformationThesis
    proof_points: List[str] = Field(..., min_length=1, description="Evidence and validation points")


class BasePersona(BaseModel):
    """Character demographics and role"""
    name: str = Field(..., min_length=1)
    role: str = Field(..., min_length=1)
    demographics: str = Field(..., min_length=1)
    product_relation: Literal[
        "The Unaware/Novice",
        "The Skeptic",
        "The Stumbler",
        "The Convert",
    ] = Field(..., description="How the character currently relates to the product or solution")
    social_setting: Optional[str] = Field(
        default=None,
        description="Primary social setting or environment of the character",
    )


class LoreSeed(BaseModel):
    """Character's core beliefs and internal world"""
    central_belief: str = Field(..., min_length=1)
    internal_monologue_style: str = Field(..., min_length=1)
    obsession_topics: List[str] = Field(..., min_length=1)
    affliction: str = Field(..., min_length=1, description="Internal wound or recurring emotional pain")
    aspiration: str = Field(..., min_length=1, description="Specific goal or desire the character wants to achieve")


class EvolutionParameters(BaseModel):
    """Parameters controlling character autonomy and evolution"""
    autonomy_level: Literal["Low", "Medium", "High"] = Field(..., description="Character autonomy level")
    memory_retention: str = Field(..., min_length=1, description="How character remembers past events")
    hallucination_permission: str = Field(..., min_length=1, description="Permission to imagine scenarios")
    
    @field_validator('hallucination_permission')
    @classmethod
    def validate_hallucination(cls, v: str) -> str:
        """Validate hallucination permission format"""
        valid_values = ["Allowed", "Not Allowed", "Limited"]
        if not any(valid in v for valid in valid_values):
            raise ValueError(f"hallucination_permission must contain one of: {valid_values}")
        return v


class AutonomousCharacterSeed(BaseModel):
    """Truth Terminal concept - Character with autonomy and evolution"""
    comment: Optional[str] = None
    base_persona: BasePersona
    lore_seed: LoreSeed
    evolution_parameters: EvolutionParameters


class LanguageModel(BaseModel):
    """Language patterns for target audience"""
    slang_whitelist: List[str] = Field(..., min_length=1)
    cultural_references: List[str] = Field(..., min_length=1)
    
    @field_validator('slang_whitelist')
    @classmethod
    def validate_slang(cls, v: List[str]) -> List[str]:
        """Ensure slang entries are reasonable strings"""
        for slang in v:
            if not slang or len(slang.strip()) == 0:
                raise ValueError("Slang whitelist cannot contain empty strings")
            if len(slang) > 50:
                raise ValueError(f"Slang entry too long: {slang[:30]}...")
        return v


class TargetAudienceContext(BaseModel):
    """Target audience definition and language"""
    persona_code: str = Field(..., min_length=1)
    pain_points: List[str] = Field(..., min_length=1)
    language_model: LanguageModel


class Meta(BaseModel):
    """Metadata about the input"""
    project_name: str
    version: str
    input_by: str
    timestamp: str
    
    @field_validator('timestamp')
    @classmethod
    def validate_timestamp(cls, v: str) -> str:
        """Validate ISO format timestamp"""
        try:
            datetime.fromisoformat(v.replace('Z', '+00:00'))
        except ValueError:
            raise ValueError(f"Timestamp must be in ISO format: {v}")
        return v


class NarrativeGenesisInput(BaseModel):
    """Root model for complete Narrative Genesis Input"""
    meta: Meta
    brand_identity_core: BrandIdentityCore
    strategic_narrative_framework: StrategicNarrativeFramework
    autonomous_character_seed: AutonomousCharacterSeed
    target_audience_context: TargetAudienceContext
    
    @model_validator(mode='after')
    def validate_consistency(self):
        """Cross-field validation for business logic consistency"""
        # Check if character demographics align with target audience
        character_demo = self.autonomous_character_seed.base_persona.demographics.lower()
        target_code = self.target_audience_context.persona_code.lower()
        
        # Example: If target is GENZ, character should mention Gen Z related terms
        if 'genz' in target_code or 'gen_z' in target_code:
            if not any(term in character_demo for term in ['24', '23', '25', '26', 'gen z', 'genz']):
                # Warning but not blocking
                pass
        
        return self
    
    class Config:
        """Pydantic configuration"""
        str_strip_whitespace = True
        validate_assignment = True
