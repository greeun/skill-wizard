---
name: skill-wizard
description: Complete guide for creating Claude Code skills through interactive wizard. Use when users want to create a new skill, update an existing skill, need help writing skill descriptions, want skill templates by type, or ask about skill creation workflow. Covers skill concepts, core principles, and step-by-step creation process.
license: Apache-2.0
---

# Skill Creation Wizard

A complete, interactive guide for creating effective Claude Code skills.

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. They transform Claude from a general-purpose agent into a specialized agent equipped with procedural knowledge.

**What Skills Provide:**
1. **Specialized workflows** - Multi-step procedures for specific domains
2. **Tool integrations** - Instructions for working with specific file formats or APIs
3. **Domain expertise** - Company-specific knowledge, schemas, business logic
4. **Bundled resources** - Scripts, references, and assets for complex tasks

## Core Principles

### Concise is Key

The context window is a public good. Skills share it with system prompt, conversation history, other skills' metadata, and user requests.

**Default assumption: Claude is already very smart.** Only add context Claude doesn't have. Challenge each piece: "Does Claude really need this?" and "Does this justify its token cost?"

Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

| Level | When to Use | Example |
|-------|-------------|---------|
| **High** (guidelines) | Multiple approaches valid | "Consider these factors when reviewing..." |
| **Medium** (patterns) | Preferred method with flexibility | "Follow this pattern, adjust as needed..." |
| **Low** (scripts) | Exact sequence required | "Run these commands in order..." |

Think of Claude as exploring a path: narrow bridge needs guardrails (low freedom), open field allows many routes (high freedom).

### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/      - Executable code (Python/Bash)
    ├── references/   - Documentation loaded as needed
    └── assets/       - Files used in output (templates, icons)
```

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

### Progressive Disclosure Design

Skills use a three-level loading system:

1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by Claude (Unlimited)

**Key guideline:** Keep SKILL.md body under 500 lines. Split content into reference files when approaching this limit.

**Pattern 1: High-level guide with references**
```markdown
## Quick start
[code example]

## Advanced features
- **Forms**: See [references/forms.md](references/forms.md)
- **API**: See [references/api.md](references/api.md)
```

**Pattern 2: Domain-specific organization**
```
skill/
├── SKILL.md (overview + navigation)
└── references/
    ├── finance.md
    ├── sales.md
    └── product.md
```

When user asks about sales, Claude only reads sales.md.

For workflow patterns, see [references/workflows.md](references/workflows.md).
For output patterns, see [references/output-patterns.md](references/output-patterns.md)

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

### What NOT to Include

A skill should only contain essential files. Do NOT create:
- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md

The skill is for an AI agent to do the job. It should not contain auxiliary context about the creation process, setup procedures, or user-facing documentation. Additional docs just add clutter.

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

**Step 1: Initialize**
```bash
python ~/.claude/skills/skill-creator/scripts/init_skill.py <skill-name> --path <location>
```

The script creates:
- Skill directory at specified path
- SKILL.md template with frontmatter and TODO placeholders
- Example `scripts/`, `references/`, `assets/` directories

**Step 2: Edit**
- Update SKILL.md frontmatter (name, description)
- Write instructions in SKILL.md body
- Implement scripts (test them!)
- Add reference documentation
- Delete unused example files

**Step 3: Test**
- Run test scenarios (happy path, edge case, out of scope)
- Verify skill triggers correctly
- Check output quality

**Step 4: Package**
```bash
python ~/.claude/skills/skill-creator/scripts/package_skill.py <skill-path>
```

The script:
1. **Validates**: frontmatter, naming, structure, description quality
2. **Packages**: creates `.skill` file (zip with .skill extension)

If validation fails, fix errors and run again.

**Step 5: Iterate**
After real usage, note struggles and improve SKILL.md or resources.

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

### References
- **Description writing**: [references/description-guide.md](references/description-guide.md)
- **Type templates**: [references/type-templates.md](references/type-templates.md)
- **Test scenarios**: [references/test-scenarios.md](references/test-scenarios.md)
- **Workflow patterns**: [references/workflows.md](references/workflows.md)
- **Output patterns**: [references/output-patterns.md](references/output-patterns.md)

### Scripts
- **Wizard CLI**: [scripts/wizard.py](scripts/wizard.py)
- **Test generator**: [scripts/generate_tests.py](scripts/generate_tests.py)
- **Initialize skill**: `~/.claude/skills/skill-creator/scripts/init_skill.py`
- **Package skill**: `~/.claude/skills/skill-creator/scripts/package_skill.py`
