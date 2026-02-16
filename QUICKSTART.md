# Quick Start Guide

## Installation (5 minutes)

### Option 1: Automated Setup (Recommended)

```bash
# Run the setup script
./setup.sh
```

### Option 2: Manual Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Step 1: Activate Environment

```bash
source venv/bin/activate
```

### Step 2: Edit Your Input

Open `input_master.json` and customize it with your brand data:

- Change `product_name` to your product
- Update `base_persona` with your character details
- Modify `the_enemy` to what you're fighting against
- Set `the_promised_land` to your vision
- Add your `proof_points`
- Update `slang_whitelist` with your audience's language

### Step 3: Run the Processor

```bash
# Test validation first
python process_narrative.py --validate-only

# If validation passes, generate configs
python process_narrative.py
```

### Step 4: Check Output

Your generated config is in:
```
output/agent_configs/scriptwriter_config.json
```

## What You Get

The system generates a **scriptwriter_config.json** with:

1. **Full System Prompt** - Ready to paste into AI
2. **Brand Voice Guidelines** - What tones to use/avoid
3. **Narrative Framework** - The Enemy, Promised Land, etc.
4. **Character Seed** - Personality and obsessions
5. **Guardrails** - Forbidden words and required themes
6. **Target Audience Context** - Who to speak to and how

## Next Steps

Use the generated `scriptwriter_config.json` with:
- Claude / GPT as a system prompt
- Your custom AI scriptwriting pipeline
- Pillar 3 (Scriptwriter Agent)

## Troubleshooting

**"python: command not found"**
- Use `python3` instead: `python3 process_narrative.py`

**"ModuleNotFoundError: No module named 'pydantic'"**
- Activate venv: `source venv/bin/activate`
- Install deps: `pip install -r requirements.txt`

**"Validation FAILED"**
- Read the error messages carefully
- Check the README.md "Troubleshooting" section
- Common issues: overlapping tone guardrails, wrong autonomy_level value

## Example Output

After successful run:

```
✓ Validation PASSED

Input Statistics:
  Product: FrugalFin
  Character: Sarah
  Target: GENZ_STRUGGLE_01
  Autonomy: High
  Proof Points: 3
  Slang Terms: 5

✓ Configuration Distribution Complete

Generated 1 config file(s):
  [scriptwriter] → output/agent_configs/scriptwriter_config.json

Process completed successfully!
```

## Need Help?

Read the full [README.md](README.md) for detailed explanations of:
- Input structure
- Validation rules
- Advanced usage
- Programmatic API
