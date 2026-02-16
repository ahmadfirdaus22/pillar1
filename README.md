# Pillar 1: Narrative Genesis Input Processor

**Version 2.0** - Matt Orlić Framework + Truth Terminal Concept

A Python-based system that validates and transforms narrative input into AI agent-ready configurations. This is the foundation layer that feeds structured storytelling frameworks into downstream content generation systems.

## Philosophy

Pillar 1 embodies three core concepts:

1. **Matt Orlić's Storytelling Framework** - Strategic narrative structure (The World, The Enemy, The Change Vehicle, The Promised Land)
2. **Truth Terminal Concept** - Autonomous character evolution with obsessions and recursive memory
3. **Strict Validation** - Pydantic-based type checking to ensure data integrity

## Architecture

```
Pillar1/
├── input_master.json                    # Master input (or use UI)
├── ui_app.py                            # Streamlit web interface
├── ui_helpers.py                        # UI utility functions
├── ui_styles.py                         # Custom CSS styling
├── run_ui.sh                            # UI launch script
├── schemas/
│   └── narrative_genesis_schema.py      # Pydantic validation models
├── processors/
│   ├── validator.py                     # Input validation + error reporting
│   ├── distributor.py                   # Config distribution logic
│   └── transformers.py                  # Data transformation utilities
├── output/
│   └── agent_configs/
│       └── scriptwriter_config.json     # Generated AI agent config
├── process_narrative.py                 # CLI entry point
├── .streamlit/
│   └── config.toml                      # Streamlit configuration
└── requirements.txt                     # Python dependencies (includes streamlit)
```

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or with virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Quick Start

You can use Pillar 1 in two ways:

### Option A: Web UI (Recommended for beginners)

Launch the interactive Streamlit interface:

```bash
# Run the UI
./run_ui.sh

# Or manually
source venv/bin/activate
streamlit run ui_app.py
```

The UI will open at `http://localhost:8501` with:
- Interactive forms for all input fields
- Real-time validation feedback
- Visual progress indicators
- JSON import/export
- Direct config generation

See [UI_GUIDE.md](UI_GUIDE.md) for detailed usage instructions.

### Option B: Command Line (For advanced users)

#### 1. Edit Your Input

Open `input_master.json` and fill in your brand narrative:

```json
{
  "meta": {
    "project_name": "Your Project Name",
    "version": "1.0",
    "input_by": "Your Name",
    "timestamp": "2026-02-12T10:00:00Z"
  },
  "brand_identity_core": {
    "product_name": "YourProduct",
    "archetype": "The Rebel",
    "core_philosophy": "Your core belief...",
    "tone_guardrails": {
      "allowed": ["Sarcastic", "Data-driven"],
      "forbidden": ["Corporate Speak", "Preachy"]
    }
  },
  ...
}
```

#### 2. Run the Processor

```bash
# Basic usage
python process_narrative.py

# Validate only (no config generation)
python process_narrative.py --validate-only

# Custom input file
python process_narrative.py --input my_input.json

# Custom output directory
python process_narrative.py --output ./my_configs
```

#### 3. Check Generated Configs

After successful processing:

```
output/
└── agent_configs/
    ├── scriptwriter_config.json      # Ready for Scriptwriter Agent
    └── distribution_report.json      # Summary report
```

## Input Structure Explained

### Brand Identity Core

Defines your product's voice and personality:

- **product_name**: Your product name
- **archetype**: Brand archetype (e.g., "The Rebel", "The Sage")
- **core_philosophy**: One-line belief statement
- **tone_guardrails**: What voice is allowed vs forbidden

**Example:**
```json
"brand_identity_core": {
  "product_name": "FrugalFin",
  "archetype": "The Enlightened Rebel",
  "core_philosophy": "Uang adalah alat kebebasan, bukan alat pamer.",
  "tone_guardrails": {
    "allowed": ["Sarcastic", "Raw/Unfiltered", "Data-driven"],
    "forbidden": ["Corporate Speak", "Preachy/Motivator Style"]
  }
}
```

### Strategic Narrative Framework (Matt Orlić)

The core storytelling structure:

1. **the_world_status_quo**: Current broken reality
2. **the_enemy**: What we're fighting against
3. **the_change_vehicle**: Your product/solution mechanism
4. **the_promised_land**: Desired future state
5. **proof_points**: Evidence and validation

**Example:**
```json
"strategic_narrative_framework": {
  "the_enemy": {
    "name": "The Algorithmic Consumerism",
    "manifestation": "Notifikasi diskon, FOMO instagram, Paylater trap.",
    "why_fight_it": "Karena sistem ini didesain untuk membuatmu tetap miskin selamanya."
  },
  "the_promised_land": {
    "vision": "Kebebasan dari rasa takut cek saldo ATM.",
    "emotional_payoff": "Ketenangan (Peace of Mind) & Kontrol Penuh."
  }
}
```

### Autonomous Character Seed (Truth Terminal)

Character that can evolve and develop obsessions:

- **base_persona**: Demographics and role
- **lore_seed**: Core beliefs and internal monologue style
- **evolution_parameters**: Autonomy, memory, and imagination settings

**Example:**
```json
"autonomous_character_seed": {
  "base_persona": {
    "name": "Sarah",
    "role": "The Glitch in the Matrix",
    "demographics": "24th, Jakarta, Gaji UMR++, Debt-ridden."
  },
  "lore_seed": {
    "central_belief": "Sistem keuangan dunia dirancang untuk memiskinkan Gen Z.",
    "obsession_topics": ["Latte Factor", "Compound Interest vs Inflation"]
  },
  "evolution_parameters": {
    "autonomy_level": "High",
    "memory_retention": "Cumulative",
    "hallucination_permission": "Allowed"
  }
}
```

### Target Audience Context

Who you're speaking to:

- **persona_code**: Audience identifier
- **pain_points**: Their struggles
- **language_model**: Slang and cultural references they use

**Example:**
```json
"target_audience_context": {
  "persona_code": "GENZ_STRUGGLE_01",
  "pain_points": [
    "Gaji numpang lewat",
    "Takut ketinggalan tren (FOMO)"
  ],
  "language_model": {
    "slang_whitelist": ["Jujurly", "Boncos", "Rungkad"],
    "cultural_references": ["Sandwich Generation", "K-Pop Merch"]
  }
}
```

## Validation Rules

The system enforces strict validation:

### Required Fields
- All fields marked in schema are required
- Empty strings are not allowed
- Arrays must have at least 1 item (where specified)

### Business Logic Checks
- ✓ Tone guardrails: `allowed` and `forbidden` cannot overlap
- ✓ Autonomy level must be: "Low", "Medium", or "High"
- ✓ Slang entries must be reasonable length (< 50 chars)
- ✓ Timestamps must be ISO format
- ✓ At least 1 proof point required

### Cross-Field Validation
- Character demographics should align with target audience
- Archetype should match tone characteristics
- Proof points should be substantial (> 20 chars)

## Output Format: Scriptwriter Config

The generated `scriptwriter_config.json` contains:

```json
{
  "agent_type": "scriptwriter",
  "system_prompt_base": {
    "full_prompt": "You are Sarah, The Glitch in the Matrix...",
    "brand_voice": { ... },
    "narrative_framework": { ... },
    "character_seed": { ... }
  },
  "guardrails": {
    "forbidden_words": [...],
    "required_themes": [...]
  },
  "context": {
    "enemy": { ... },
    "promised_land": { ... },
    "target_audience": { ... }
  },
  "content_generation_params": {
    "remember_past_scripts": true,
    "allow_character_evolution": true,
    ...
  }
}
```

### How Scriptwriter Uses This Config

1. **Load config** at session start
2. **Use `full_prompt`** as AI system prompt
3. **Check guardrails** before generating
4. **Reference context** during generation
5. **Validate output** against forbidden words

## Advanced Usage

### Validation Only Mode

Test your input without generating configs:

```bash
python process_narrative.py --validate-only
```

Output:
```
✓ Validation PASSED

Input Statistics:
  Product: FrugalFin
  Character: Sarah
  Target: GENZ_STRUGGLE_01
  Autonomy: High
  Proof Points: 3
  Slang Terms: 5
```

### Programmatic Usage

Use as a Python module:

```python
from pathlib import Path
from processors.validator import NarrativeValidator
from processors.distributor import distribute_configs

# Validate input
validator = NarrativeValidator()
report = validator.validate_from_file(Path("input_master.json"))

if report.is_valid:
    # Distribute configs
    output_dir = Path("output/agent_configs")
    dist_report = distribute_configs(report.data, output_dir)
    print(dist_report)
```

### Testing Individual Validators

```bash
# Test validator only
python processors/validator.py input_master.json

# Output will show validation results and stats
```

## Troubleshooting

### Common Errors

**Error: "Tone guardrails overlap detected"**
- **Cause**: Same tone appears in both `allowed` and `forbidden` lists
- **Fix**: Remove the duplicate from one list

**Error: "validation_error: autonomy_level"**
- **Cause**: `autonomy_level` is not "Low", "Medium", or "High"
- **Fix**: Use exact capitalization: `"High"` not `"high"` or `"HIGH"`

**Error: "Field required"**
- **Cause**: Missing required field in JSON
- **Fix**: Check the error location and add the missing field

**Error: "Timestamp must be in ISO format"**
- **Cause**: Invalid timestamp format
- **Fix**: Use format: `"2026-02-12T10:00:00Z"`

### Validation Warnings (Non-blocking)

Warnings don't stop processing but suggest improvements:

- Archetype/tone mismatch (e.g., "Rebel" without rebellious tones)
- Short proof points (< 20 chars)
- Character demographics don't mention audience pain points

## System Prompt Example

Given the FrugalFin input, the system generates:

```
You are Sarah, The Glitch in the Matrix. You are 24 years old, living in Jakarta, 
earning UMR++, and struggling with debt.

Your Core Belief: Sistem keuangan dunia dirancang untuk memiskinkan Gen Z.

Your Mission: Fight against The Algorithmic Consumerism - the endless notifications, 
FOMO instagram posts, and Paylater traps that keep people poor forever.

Your Voice: Sarcastic, Raw/Unfiltered, Data-driven, Cult-like (in a fun way).
NEVER use: Corporate Speak, Preachy/Motivator Style, or Judge Poverty.

Your Obsessions: Latte Factor, Compound Interest vs Inflation, Minimalism as Rebellion.

When creating content, always reference:
- The Enemy: Algorithmic systems designed to extract money
- The Promised Land: Kebebasan dari rasa takut cek saldo ATM
- Proof: Users save 30% in month 1 using behavioral psychology

Speak to: GENZ_STRUGGLE_01 - those with "Gaji numpang lewat", FOMO fears, 
and frustration that their assets never grow.

Use their language: Jujurly, Boncos, Rungkad, Healing, Budak Korporat.
```

## Web UI Features

The Streamlit interface provides:

### Interactive Forms
- Section-by-section navigation with progress tracking
- Dynamic lists for proof points, obsessions, slang, etc.
- Real-time tone overlap detection
- Field validation with immediate feedback

### Visual Feedback
- Completion checkmarks for each section
- Progress bar showing overall completion
- Color-coded validation messages
- Status badges (complete/incomplete)

### Import/Export
- Load FrugalFin example with one click
- Upload existing JSON files
- Export input as JSON with timestamp
- Download generated configs directly

### Validation & Generation
- Validate button with detailed error reporting
- Generate configs with visual confirmation
- Preview system prompt before generation
- Statistics dashboard showing input metrics

### User Experience
- Responsive design for all screen sizes
- Custom styling with brand colors
- Collapsible sections for easier navigation
- Help text and tooltips throughout

See [UI_GUIDE.md](UI_GUIDE.md) for complete UI documentation.

## Future Extensions (Roadmap)

- [x] Web UI for input editing ✅ COMPLETE
- [ ] QA Validator agent config generation
- [ ] Character Evolution Engine config
- [ ] Version history tracking
- [ ] Multi-language support (ID/EN toggle)
- [ ] Agent feedback loop (which configs performed best)
- [ ] A/B testing different frameworks

## Technical Details

### Dependencies

- **pydantic** (>=2.5.0): Data validation and settings management
- **pydantic-settings** (>=2.1.0): Enhanced settings features
- **python-dotenv** (>=1.0.0): Environment variable management
- **streamlit** (>=1.30.0): Web UI framework for interactive interface

### Python Version

- Requires Python 3.9+
- Tested on Python 3.9, 3.10, 3.11

### File Encodings

All files use UTF-8 encoding to support Indonesian language characters.

## Contributing

When extending this system:

1. **Add new agent types** in `processors/distributor.py`
2. **Add validation rules** in `schemas/narrative_genesis_schema.py`
3. **Add transformers** in `processors/transformers.py`
4. **Update tests** when modifying schemas

## License

Internal project for FrugalFin Launch Alpha.

## Contact

For questions or issues:
- Input by: Brand Strategy Lead
- Project: FrugalFin Launch Alpha v2.0

---

**Remember**: This is the foundation. The quality of your input determines the quality of everything downstream. Take time to craft your narrative thoughtfully.
