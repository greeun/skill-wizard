---
name: skill-wizard
description: Interactive wizard for creating Claude Code skills through guided questions. Use when users want to create a new skill with step-by-step guidance, need help writing skill descriptions, want skill templates by type, or ask about skill creation workflow. Complements skill-creator with interactive approach.
---

# Skill Creation Wizard

An interactive, question-driven approach to creating effective Claude Code skills.

## When to Use This Wizard

- User wants to create a new skill but doesn't know where to start
- User needs help crafting an effective description
- User wants a template for a specific skill type
- User is unsure about skill structure decisions

## Wizard Workflow

Guide users through these 6 phases sequentially:

```
Phase 1: Purpose Discovery
    ↓
Phase 2: Type Selection
    ↓
Phase 3: Metadata Design (name + description)
    ↓
Phase 4: Content Architecture
    ↓
Phase 5: Resource Planning
    ↓
Phase 6: Validation & Generation
```

---

## Phase 1: Purpose Discovery

**Goal**: Understand the problem being solved.

Ask these questions (one at a time, not all at once):

1. "What repetitive task do you want to automate with this skill?"
2. "How many times have you done this task manually?"
   - If < 5 times: Warn that skills work best for proven, repeated workflows
3. "Can you give 2-3 concrete examples of how you'd use this skill?"
4. "What does a successful outcome look like?"

**Output**: Clear problem statement and success criteria.

---

## Phase 2: Type Selection

**Goal**: Match the skill to a proven pattern.

Present these 5 skill types:

| Type | Best For | Example |
|------|----------|---------|
| **Document Processor** | File format manipulation (PDF, DOCX, images) | "Extract tables from PDF" |
| **Code Automator** | Development workflows (test, review, refactor) | "Run tests and fix failures" |
| **Data Analyzer** | Queries, reports, data transformation | "Generate sales report from BigQuery" |
| **Workflow Orchestrator** | Multi-step processes with dependencies | "Deploy to staging with rollback" |
| **Domain Expert** | Specialized knowledge, guidelines, standards | "Apply brand guidelines to document" |

Ask: "Which type best matches your skill's purpose?"

For detailed templates by type, see [type-templates.md](references/type-templates.md).

---

## Phase 3: Metadata Design

**Goal**: Create optimal name and description.

### 3.1 Name

Rules:
- Lowercase letters, digits, hyphens only
- Max 64 characters
- Format: `verb-noun` or `domain-action` (e.g., `pdf-table-extractor`, `brand-style-applier`)

Ask: "What action + object describes your skill?" → Generate 3 name suggestions.

### 3.2 Description (CRITICAL)

The description is the **only signal** Claude uses to decide when to activate the skill.

**Formula**: `[What it does]. [When to use - trigger keywords]`

**Template**:
```
[Primary function] with support for [key capabilities].
Use when [trigger scenario 1], [trigger scenario 2], or [trigger keywords].
```

For comprehensive guidance, see [description-guide.md](references/description-guide.md).

**Generate 3 description options** based on user's answers from Phase 1, then ask user to pick or refine.

---

## Phase 4: Content Architecture

**Goal**: Design the SKILL.md body structure.

### Determine Freedom Level

Ask: "How strict should the skill's instructions be?"

| Level | When to Use | Example Instruction Style |
|-------|-------------|--------------------------|
| **High** (guidelines) | Multiple valid approaches | "Consider these factors when reviewing..." |
| **Medium** (patterns) | Preferred method with flexibility | "Follow this pattern, adjust as needed..." |
| **Low** (scripts) | Exact sequence required | "Run these commands in order..." |

### Select Structure Pattern

Based on skill type, recommend:

- **Document Processor**: Task-based (Quick Start → Task 1 → Task 2)
- **Code Automator**: Workflow-based (Decision Tree → Step 1 → Step 2)
- **Data Analyzer**: Reference-based (Overview → Schemas → Queries)
- **Workflow Orchestrator**: Sequential (Prerequisites → Phase 1 → Phase 2)
- **Domain Expert**: Guidelines-based (Principles → Standards → Examples)

---

## Phase 5: Resource Planning

**Goal**: Identify bundled resources needed.

### Scripts (`scripts/`)

Ask: "Are there operations that should run the same way every time?"

Examples:
- PDF rotation → `rotate_pdf.py`
- Data validation → `validate_schema.py`
- File conversion → `convert_format.py`

### References (`references/`)

Ask: "Is there detailed documentation Claude should reference while working?"

Examples:
- API specs → `api_reference.md`
- Database schemas → `schema.md`
- Company policies → `guidelines.md`

### Assets (`assets/`)

Ask: "Are there templates or files that should be copied/used in output?"

Examples:
- Boilerplate code → `templates/`
- Brand assets → `logo.png`
- Document templates → `template.docx`

---

## Phase 6: Validation & Generation

**Goal**: Verify and create the skill.

### Pre-Generation Checklist

Run through with user:

- [ ] Description includes both function AND triggers
- [ ] Name follows hyphen-case convention
- [ ] SKILL.md body planned under 500 lines
- [ ] Resources identified (scripts/references/assets)
- [ ] Freedom level matches task fragility

### Generate Test Scenarios

Create 3 test cases (see [test-scenarios.md](references/test-scenarios.md)):

1. **Happy path**: Typical request that should trigger the skill
2. **Edge case**: Unusual but valid request
3. **Out of scope**: Similar request that should NOT trigger

### Create the Skill

Option A: Use existing `skill-creator` scripts
```bash
# Initialize from skill-creator
python ~/.claude/skills/skill-creator/scripts/init_skill.py <skill-name> --path <location>
```

Option B: Use wizard script for guided generation
```bash
python ~/.claude/skills/skill-wizard/scripts/wizard.py
```

### Post-Generation

1. Edit generated SKILL.md with planned content
2. Implement identified scripts
3. Add reference documentation
4. Test with generated scenarios
5. Package when ready:
   ```bash
   python ~/.claude/skills/skill-creator/scripts/package_skill.py <skill-path>
   ```

---

## Quick Reference: Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Vague description | Skill doesn't trigger | Add specific trigger keywords |
| Too long SKILL.md | Context bloat | Split into references/ |
| No examples | Claude guesses format | Add concrete input/output pairs |
| Over-engineered | Unnecessary complexity | Start minimal, iterate |
| Untested | Unknown edge cases | Run 3 test scenarios |

---

## Resources

- **Description writing**: [references/description-guide.md](references/description-guide.md)
- **Type templates**: [references/type-templates.md](references/type-templates.md)
- **Test scenarios**: [references/test-scenarios.md](references/test-scenarios.md)
- **Wizard CLI**: [scripts/wizard.py](scripts/wizard.py)
