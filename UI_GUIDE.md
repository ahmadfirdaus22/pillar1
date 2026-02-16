# Streamlit UI Guide

Complete guide for using the Pillar 1 web interface.

## Quick Start

### Launch the UI

```bash
# Option 1: Using the launch script (recommended)
./run_ui.sh

# Option 2: Manual launch
source venv/bin/activate
streamlit run ui_app.py
```

The UI will automatically open in your browser at `http://localhost:8501`

## Interface Overview

### Main Components

```
┌─────────────────────────────────────────────────────────┐
│  📝 Pillar 1: Narrative Genesis Input Processor         │
├──────────────┬──────────────────────────────────────────┤
│  Sidebar     │  Main Content Area                       │
│              │                                           │
│  Navigation  │  [Current Section Forms]                 │
│  - Progress  │                                           │
│  - Actions   │  [Input Fields]                          │
│              │                                           │
│              │  [Navigation Buttons]                    │
└──────────────┴──────────────────────────────────────────┘
```

### Sidebar Features

**Navigation Menu**
- Click any section to jump directly to it
- ✓ checkmark indicates completed sections
- ○ circle indicates incomplete sections

**Progress Bar**
- Shows overall completion percentage
- Updates automatically as you fill in fields

**Quick Actions**
- **Load Example**: Load FrugalFin example data
- **Upload JSON**: Import existing JSON file
- **Reset All**: Clear all fields (use with caution!)

## Section-by-Section Guide

### 1. Project Info

Basic metadata about your project.

**Required Fields:**
- **Project Name**: Name of your campaign or project
- **Created By**: Your name or role

**Optional Fields:**
- **Version**: Version identifier (defaults to "1.0")
- **Timestamp**: Auto-generated, but editable

**Tips:**
- Click "Update to Current Time" to refresh timestamp
- Project name helps organize multiple projects

### 2. Brand Identity

Define your brand's core identity and voice.

#### Product Information

**Product Name**: The name of your product/service
- Example: "FrugalFin"

**Archetype**: Your brand's archetypal identity
- Example: "The Enlightened Rebel"
- Common archetypes: The Hero, The Sage, The Explorer, The Rebel

**Core Philosophy**: One-line mission statement
- Example: "Money is a tool for freedom, not for showing off"

#### Tone Guardrails

**Allowed Tones** - Select or add tones your brand SHOULD use:
- Pre-set options: Sarcastic, Data-driven, Empowering, etc.
- Add custom tones using the text input

**Forbidden Tones** - Select or add tones your brand should NEVER use:
- Pre-set options: Corporate Speak, Preachy, Condescending, etc.
- Add custom tones using the text input

**Overlap Detection:**
- System automatically checks for tones in both lists
- Yellow warning appears if overlap detected
- Green checkmark when no overlap

### 3. Strategic Narrative

The Matt Orlić storytelling framework with five components.

#### The World (Status Quo)

**Description**: Current broken state of reality
- What's wrong with the world today?
- Example: "People are enslaved by social validation and shopping algorithms"

**Consensus Reality**: What people falsely believe
- The lie they've been sold
- Example: "'Self Reward' is mandatory (but it's actually a marketing trap)"

#### The Enemy

**Enemy Name**: Name the antagonist
- Example: "The Algorithmic Consumerism"

**How It Shows Up**: Concrete manifestations
- Specific examples people experience daily
- Example: "Discount notifications, FOMO instagram, Paylater traps"

**Why Fight It**: The stakes
- Why this must be defeated
- Example: "This system is designed to keep you poor forever"

#### The Change Vehicle

**What's New**: The insight or tool that enables change
- Example: "New awareness (Gnosis) that we can outsmart the system with data"

**How It Works**: Your solution's mechanism
- Example: "FrugalFin AI visualizes your 'broke future' if you buy that coffee"

#### The Promised Land

**The Vision**: Desired future state
- Where we're heading
- Example: "Freedom from fear of checking your ATM balance"

**Emotional Payoff**: How it feels
- The emotional benefit
- Example: "Peace of Mind & Total Control"

#### Proof Points

**Add Evidence**: Click "➕ Add Proof Point" to add more
- Statistics, testimonials, case studies
- Example: "Users save 30% in first month"
- Minimum 1 proof point required

**Tips:**
- Be specific with numbers and outcomes
- Each proof point should be substantial (>20 characters)

### 4. Character Seed

Create an autonomous character with evolution capability (Truth Terminal concept).

#### Base Persona

**Character Name**: Who they are
- Example: "Sarah"

**Role**: Their identity or archetype
- Example: "The Glitch in the Matrix"

**Demographics**: Age, location, situation
- Example: "24 years old, Jakarta, Salary UMR++, Debt-ridden"

#### Lore Seed (Inner World)

**Central Belief**: Character's core worldview
- Example: "The world financial system is designed to impoverish Gen Z"

**Internal Monologue Style**: How they think
- Example: "Paranoid but logical. Talks to self about coffee price conspiracies"

**Obsession Topics**: What they can't stop thinking about
- Dynamic list - add multiple obsessions
- Example: "Latte Factor", "Compound Interest vs Inflation"

#### Evolution Parameters

**Autonomy Level**: Select Low, Medium, or High
- **Low**: Stays strictly on script
- **Medium**: Can improvise within boundaries
- **High**: Free to deviate and evolve

**Memory Retention**: How they remember
- Example: "Cumulative (Remembers last week's failures as trauma)"

**Hallucination Permission**: Can they imagine scenarios?
- Must contain: "Allowed", "Not Allowed", or "Limited"
- Example: "Allowed (Can imagine 'Dystopian Future' if spending)"

### 5. Target Audience

Define who you're speaking to.

**Persona Code**: Audience identifier
- Example: "GENZ_STRUGGLE_01"
- Use for tracking and organization

**Pain Points**: Their struggles (dynamic list)
- Click ➕ to add more
- Example: "Salary barely covers basics", "FOMO spending"

#### Language Model

**Slang Whitelist**: Terms they use
- Example: "Jujurly", "Boncos", "Rungkad"
- Add all relevant slang and colloquialisms

**Cultural References**: What they relate to
- Pop culture, trends, phenomena
- Example: "Sandwich Generation", "K-Pop Merch"

### 6. Generate & Export

Final step - validate, generate, and export.

#### 1. Validate Input

Click **"🔍 Validate Input"** to check your data:
- Green success: All fields valid
- Red error: Shows specific issues and locations
- Fix errors and re-validate

**Validation Statistics:**
- Product name, character, target persona
- Autonomy level, proof points count, slang count

#### 2. Generate Configs

After validation passes:
1. Click **"⚙️ Generate Configs"**
2. System creates `scriptwriter_config.json`
3. Files saved to `output/agent_configs/`
4. Download button appears

**Generated Files:**
- `scriptwriter_config.json` - Full agent configuration
- `distribution_report.json` - Summary report

#### 3. Export JSON

Save your input for backup or sharing:
1. Click **"📄 Export JSON"**
2. Click **"📥 Download Input JSON"**
3. File saves with timestamp

**Use Cases:**
- Backup before major changes
- Share with team members
- Version control
- Reload later via "Upload JSON" in sidebar

#### 4. Preview System Prompt

See generated prompt before creating configs:
1. Click **"👁️ Preview System Prompt"**
2. View full prompt in text area
3. Check character voice, framework integration

## Dynamic Lists

Many sections use dynamic lists (proof points, obsessions, slang, etc.).

**Add Items:**
1. Type in the input field
2. Click "➕ Add [Item Name]"
3. New blank field appears below

**Remove Items:**
1. Click 🗑️ button next to unwanted item
2. Item removed immediately (if > 1 item remains)

**Tips:**
- At least one item always remains
- Empty items are filtered out during validation
- Add placeholders, then fill in

## Keyboard Shortcuts

- **Tab**: Move to next field
- **Shift+Tab**: Move to previous field
- **Enter**: Submit in text inputs (doesn't work in text areas)

## Common Workflows

### Starting Fresh

1. Launch UI: `./run_ui.sh`
2. Fill sections in order (or jump around via sidebar)
3. Check progress bar
4. Validate when complete
5. Generate configs

### Loading Example

1. Click "📁 Load Example (FrugalFin)" in sidebar
2. All fields populate with FrugalFin data
3. Modify as needed
4. Generate your own configs

### Importing Existing JSON

1. Click "📤 Upload JSON" in sidebar
2. Select your `.json` file
3. Fields populate automatically
4. Edit and regenerate

### Iterating on Input

1. Make changes in any section
2. Click "Validate Input" to check
3. Fix any errors shown
4. Re-generate configs
5. Download updated config

## Validation Messages

### Success Messages
- ✓ Green checkmark: Field/section complete
- ✅ "Validation Passed": All checks passed

### Warnings
- ⚠️ Yellow: Non-blocking issues (still generates)
- Example: "Proof points seem short"

### Errors
- ✗ Red X: Blocking issues (must fix)
- ❌ "Validation Failed": Shows error count and details

**Error Details:**
- **Location**: Which field has the issue
- **Message**: What's wrong
- **Input value**: What was provided

## Tips & Best Practices

### General

1. **Save Often**: Export JSON regularly as backup
2. **Use Examples**: Start with FrugalFin example, then modify
3. **Complete Sections**: Finish one section before moving to next
4. **Watch Progress**: Use progress bar to track completion

### Writing Content

1. **Be Specific**: Use concrete examples and numbers
2. **Show Don't Tell**: "Save 30%" not "Save money"
3. **Use Audience Language**: Check your slang whitelist
4. **Avoid Forbidden Tones**: Review your guardrails

### Character Development

1. **Make Them Real**: Give specific demographics
2. **Clear Beliefs**: One strong central belief
3. **Distinct Voice**: Unique internal monologue style
4. **Relevant Obsessions**: Tie to your product/mission

### Narrative Framework

1. **Name the Enemy**: Make it concrete and relatable
2. **Paint the Vision**: Make the promised land tangible
3. **Show Mechanism**: Explain HOW your solution works
4. **Prove It**: Add substantial proof points

## Troubleshooting

### UI Won't Load

**Problem**: Browser shows error or blank page

**Solutions:**
1. Check terminal for error messages
2. Ensure port 8501 isn't in use
3. Restart: Ctrl+C, then `./run_ui.sh` again
4. Check virtual environment is activated

### "Module not found" Error

**Problem**: Import errors in terminal

**Solutions:**
1. Activate venv: `source venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Re-launch: `./run_ui.sh`

### Validation Always Fails

**Problem**: Can't pass validation despite filling fields

**Solutions:**
1. Read error messages carefully - they show exact location
2. Check for overlapping tones (allowed vs forbidden)
3. Ensure autonomy level is exactly: "Low", "Medium", or "High"
4. Verify timestamp is ISO format
5. Check hallucination permission contains required words

### Can't Generate Configs

**Problem**: Generate button doesn't work

**Solutions:**
1. Validate first (button requires validation)
2. Check all required fields (marked with *)
3. Fix validation errors before generating
4. Check `output/agent_configs/` directory exists

### Changes Not Saving

**Problem**: Edits disappear when switching sections

**Solutions:**
- Fields auto-save to session state
- If losing data, try:
  1. Export JSON as backup
  2. Don't use browser back button
  3. Use navigation buttons/sidebar only

### Download Button Not Working

**Problem**: Download doesn't start

**Solutions:**
1. Check browser pop-up blocker
2. Allow downloads from localhost
3. Try different browser
4. Check browser console for errors

## Advanced Features

### Session State

- All data stored in browser session
- Persists between section changes
- Cleared on browser refresh
- Export JSON to save permanently

### Real-time Validation

Some validations happen live:
- Tone overlap detection (instant)
- Field completion (instant)
- Full validation (on button click)

### Custom Tones

Add unlimited custom tones:
1. Type in "Add custom..." field
2. Click ➕ Add button
3. Appears in list immediately

### Timestamp Management

Auto-generated but fully editable:
- Defaults to current time
- Editable for backdating
- Click "Update to Current Time" to refresh
- Must be ISO format (YYYY-MM-DDTHH:MM:SSZ)

## Keyboard Navigation

**Tab through fields:**
- Tab: Next field
- Shift+Tab: Previous field

**Within sections:**
- Use mouse for buttons and dropdowns
- Use keyboard for text inputs

## Browser Compatibility

**Recommended:**
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**Not supported:**
- Internet Explorer
- Very old mobile browsers

## Performance

**Large inputs:**
- System handles large text areas well
- Validation may take 1-2 seconds
- Progress indicators show during processing

**Many proof points/obsessions:**
- Dynamic lists handle 20+ items
- Scroll within sections as needed

## Data Privacy

**All processing happens locally:**
- No data sent to external servers
- Files saved to your computer only
- Session state in browser memory
- Export to own files under your control

## Next Steps

After generating configs:
1. Find output in `output/agent_configs/scriptwriter_config.json`
2. Use in Pillar 3 (Scriptwriter Agent)
3. Integrate with AI systems (Claude, GPT, etc.)
4. Iterate and regenerate as needed

---

**Need Help?**
- Check README.md for system overview
- Review examples in input_master.json
- Check validation error messages
- Consult PROJECT_SUMMARY.md for architecture
