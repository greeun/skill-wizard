# Skill Type Templates

Ready-to-use SKILL.md templates for each skill type. Copy, customize, and adapt.

---

## Type 1: Document Processor

Best for: File format manipulation (PDF, DOCX, Excel, images)

### Template

```yaml
---
name: [format]-[action]
description: [Format] [primary action] with support for [feature 1], [feature 2], and [feature 3]. Use when working with [format] files, [action 1], [action 2], or when user mentions [format], [keyword 1], or [keyword 2].
---

# [Format] [Action]

## Quick Start

[Most common operation with code example]

```python
# Example code
```

## Supported Operations

### [Operation 1]

[Brief description + code example]

### [Operation 2]

[Brief description + code example]

### [Operation 3]

[Brief description + code example]

## Requirements

```bash
pip install [required-packages]
```

## Advanced Features

For complex operations, see:
- [FEATURE_1.md](references/FEATURE_1.md)
- [FEATURE_2.md](references/FEATURE_2.md)
```

### Example: PDF Table Extractor

```yaml
---
name: pdf-table-extractor
description: Extract tables from PDF documents into CSV or JSON format with support for multi-page tables, merged cells, and complex layouts. Use when extracting tables from PDFs, converting PDF data to spreadsheet, or when user mentions PDF tables, data extraction, or document parsing.
---

# PDF Table Extractor

## Quick Start

Extract tables from a PDF:

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    page = pdf.pages[0]
    tables = page.extract_tables()
    for table in tables:
        print(table)
```

## Supported Operations

### Single Page Extraction

```python
with pdfplumber.open("doc.pdf") as pdf:
    table = pdf.pages[0].extract_table()
```

### Multi-Page Tables

```python
all_tables = []
with pdfplumber.open("doc.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        all_tables.extend(tables)
```

### Export to CSV

```python
import csv

with open("output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(table)
```

## Requirements

```bash
pip install pdfplumber pandas
```

## Advanced Features

- Complex layouts: See [references/complex-layouts.md](references/complex-layouts.md)
- OCR for scanned PDFs: See [references/ocr-extraction.md](references/ocr-extraction.md)
```

### Typical Directory Structure

```
pdf-table-extractor/
├── SKILL.md
├── references/
│   ├── complex-layouts.md
│   └── ocr-extraction.md
└── scripts/
    ├── extract_tables.py
    └── convert_to_csv.py
```

---

## Type 2: Code Automator

Best for: Development workflows (test, review, refactor, lint)

### Template

```yaml
---
name: [action]-[target]
description: Automated [action] for [target] with [capability 1] and [capability 2]. Use when [scenario 1], [scenario 2], or when user mentions [tool], [action], or [problem].
---

# [Action] [Target]

## Workflow

```
[Step 1] → [Step 2] → [Step 3] → [Output]
```

## Decision Tree

1. Determine the task type:
   - **[Type A]?** → Follow [Section A] below
   - **[Type B]?** → Follow [Section B] below

## [Section A]: [Type A Workflow]

### Step 1: [Action]

```bash
[command]
```

### Step 2: [Action]

[Instructions]

### Step 3: [Action]

[Instructions]

## [Section B]: [Type B Workflow]

[Similar structure]

## Common Issues

| Issue | Solution |
|-------|----------|
| [Problem 1] | [Fix 1] |
| [Problem 2] | [Fix 2] |
```

### Example: Test Runner & Fixer

```yaml
---
name: test-runner-fixer
description: Automated test execution with failure analysis and suggested fixes. Use when running tests, debugging test failures, fixing broken tests, or when user mentions pytest, jest, test suite, CI failures, or test errors.
---

# Test Runner & Fixer

## Workflow

```
Run Tests → Analyze Failures → Suggest Fixes → Verify
```

## Decision Tree

1. Determine the test framework:
   - **Python (pytest)?** → Follow Python workflow below
   - **JavaScript (jest)?** → Follow JavaScript workflow below

## Python Workflow (pytest)

### Step 1: Run Tests

```bash
pytest --tb=short -v 2>&1 | head -100
```

### Step 2: Analyze Failures

For each failure:
1. Read the failing test file
2. Read the tested function
3. Compare expected vs actual

### Step 3: Fix Issues

Common fixes:
- Assertion error → Check expected values
- Import error → Verify module paths
- Attribute error → Check object structure

### Step 4: Verify

```bash
pytest [specific_test_file] -v
```

## JavaScript Workflow (jest)

### Step 1: Run Tests

```bash
npm test -- --verbose 2>&1 | head -100
```

[Continue similarly...]

## Common Issues

| Issue | Solution |
|-------|----------|
| ModuleNotFoundError | Check PYTHONPATH, verify imports |
| Timeout | Increase timeout, check async handling |
| Fixture not found | Verify conftest.py, check scope |
```

### Typical Directory Structure

```
test-runner-fixer/
├── SKILL.md
├── references/
│   ├── pytest-patterns.md
│   └── jest-patterns.md
└── scripts/
    ├── run_tests.py
    └── analyze_failure.py
```

---

## Type 3: Data Analyzer

Best for: Queries, reports, data transformation

### Template

```yaml
---
name: [domain]-[analyzer/reporter]
description: [Domain] data analysis with [capability 1], [capability 2], and [capability 3]. Use when querying [source], analyzing [metrics], generating [reports], or when user mentions [domain], [tool], or [data type].
---

# [Domain] Analyzer

## Overview

[What this skill analyzes and produces]

## Data Sources

### [Source 1]

**Connection:**
```python
# connection example
```

**Available tables/schemas:**
- `table_1`: [description]
- `table_2`: [description]

For full schema, see [references/schema.md](references/schema.md)

## Common Queries

### [Query Type 1]

```sql
SELECT ...
```

### [Query Type 2]

```sql
SELECT ...
```

## Report Templates

### [Report 1]

[Format and sections]

### [Report 2]

[Format and sections]
```

### Example: Sales Analytics

```yaml
---
name: sales-analytics
description: Sales data analysis with revenue metrics, pipeline tracking, and forecast generation. Use when analyzing sales data, generating sales reports, tracking pipeline, or when user mentions revenue, deals, forecast, CRM, or sales metrics.
---

# Sales Analytics

## Overview

Analyze sales data to generate insights on revenue, pipeline health, and forecasts.

## Data Sources

### Salesforce (via BigQuery)

**Connection:**
```python
from google.cloud import bigquery
client = bigquery.Client(project="your-project")
```

**Key tables:**
- `opportunities`: Deal records with stage, amount, close date
- `accounts`: Company information
- `users`: Sales rep data

For full schema, see [references/schema.md](references/schema.md)

## Common Queries

### Revenue by Quarter

```sql
SELECT
  FORMAT_DATE('%Y-Q%Q', close_date) as quarter,
  SUM(amount) as revenue
FROM opportunities
WHERE stage = 'Closed Won'
GROUP BY quarter
ORDER BY quarter
```

### Pipeline by Stage

```sql
SELECT
  stage,
  COUNT(*) as deals,
  SUM(amount) as value
FROM opportunities
WHERE stage NOT IN ('Closed Won', 'Closed Lost')
GROUP BY stage
```

## Report Templates

### Weekly Pipeline Report

```markdown
# Pipeline Report - [Date]

## Summary
- Total pipeline: $X
- New this week: $Y
- Moved to closed: $Z

## By Stage
[Table]

## At Risk Deals
[List]
```
```

### Typical Directory Structure

```
sales-analytics/
├── SKILL.md
├── references/
│   ├── schema.md
│   ├── metrics-definitions.md
│   └── report-templates.md
└── scripts/
    └── generate_report.py
```

---

## Type 4: Workflow Orchestrator

Best for: Multi-step processes with dependencies

### Template

```yaml
---
name: [process]-orchestrator
description: Multi-stage [process] with [capability 1], [capability 2], and [capability 3]. Use when [action 1], [action 2], or when user mentions [stage], [action], or [tool].
---

# [Process] Orchestrator

## Prerequisites

- [ ] [Requirement 1]
- [ ] [Requirement 2]
- [ ] [Requirement 3]

## Process Overview

```
Phase 1: [Name]
    ↓
Phase 2: [Name]
    ↓
Phase 3: [Name]
    ↓
Complete
```

## Phase 1: [Name]

**Goal:** [What this phase accomplishes]

### Steps

1. [Step 1]
   ```bash
   [command]
   ```

2. [Step 2]
   ```bash
   [command]
   ```

### Validation

```bash
[validation command]
```

**Expected output:** [description]

## Phase 2: [Name]

[Similar structure]

## Phase 3: [Name]

[Similar structure]

## Rollback Procedures

### If Phase 1 fails:
[Instructions]

### If Phase 2 fails:
[Instructions]

## Progress Tracking

Copy this checklist:
```
[ ] Phase 1: [Name]
[ ] Phase 2: [Name]
[ ] Phase 3: [Name]
```
```

### Example: Deployment Orchestrator

```yaml
---
name: deployment-orchestrator
description: Multi-stage deployment pipeline with pre-flight checks, staged rollout, and automatic rollback. Use when deploying to staging or production, managing releases, or when user mentions deploy, release, rollback, or CI/CD.
---

# Deployment Orchestrator

## Prerequisites

- [ ] All tests passing
- [ ] Version bumped
- [ ] Changelog updated
- [ ] Required approvals obtained

## Process Overview

```
Phase 1: Pre-flight Checks
    ↓
Phase 2: Build & Stage
    ↓
Phase 3: Deploy & Verify
    ↓
Phase 4: Monitor & Confirm
```

## Phase 1: Pre-flight Checks

**Goal:** Ensure deployment readiness

### Steps

1. Verify tests pass
   ```bash
   npm test
   ```

2. Check for uncommitted changes
   ```bash
   git status --porcelain
   ```

3. Validate environment config
   ```bash
   ./scripts/validate-env.sh production
   ```

### Validation

All commands must exit with code 0.

## Phase 2: Build & Stage

**Goal:** Create deployable artifacts

### Steps

1. Build production bundle
   ```bash
   npm run build:production
   ```

2. Upload to staging
   ```bash
   ./scripts/deploy.sh staging
   ```

3. Run smoke tests
   ```bash
   ./scripts/smoke-test.sh staging
   ```

## Phase 3: Deploy & Verify

**Goal:** Production deployment

### Steps

1. Create deployment tag
   ```bash
   git tag -a v$(cat VERSION) -m "Release $(cat VERSION)"
   ```

2. Deploy to production
   ```bash
   ./scripts/deploy.sh production
   ```

3. Verify health
   ```bash
   curl -f https://api.example.com/health
   ```

## Phase 4: Monitor & Confirm

**Goal:** Ensure stability

- Monitor error rates for 15 minutes
- Check key metrics dashboards
- Confirm with stakeholders

## Rollback Procedures

### If Phase 2 fails:
```bash
./scripts/rollback.sh staging
```

### If Phase 3 fails:
```bash
./scripts/rollback.sh production
git tag -d v$(cat VERSION)
```
```

### Typical Directory Structure

```
deployment-orchestrator/
├── SKILL.md
├── references/
│   ├── environment-configs.md
│   └── rollback-procedures.md
└── scripts/
    ├── validate-env.sh
    ├── deploy.sh
    ├── rollback.sh
    └── smoke-test.sh
```

---

## Type 5: Domain Expert

Best for: Specialized knowledge, guidelines, standards

### Template

```yaml
---
name: [domain]-[expert/guidelines]
description: [Domain] expertise with [area 1], [area 2], and [area 3] guidelines. Use when [scenario 1], [scenario 2], or when user mentions [domain], [standard], or [compliance].
---

# [Domain] Guidelines

## Core Principles

1. **[Principle 1]**: [Description]
2. **[Principle 2]**: [Description]
3. **[Principle 3]**: [Description]

## Standards

### [Standard Category 1]

| Element | Specification |
|---------|--------------|
| [Item 1] | [Spec] |
| [Item 2] | [Spec] |

### [Standard Category 2]

[Similar structure]

## Application Guidelines

### When [Scenario 1]

[Instructions and examples]

### When [Scenario 2]

[Instructions and examples]

## Review Checklist

- [ ] [Check 1]
- [ ] [Check 2]
- [ ] [Check 3]

## Examples

### Good Example

[Show correct application]

### Bad Example

[Show what to avoid]
```

### Example: Brand Style Guide

```yaml
---
name: brand-style-enforcer
description: Brand consistency enforcement for documents and presentations with color, typography, logo, and voice guidelines. Use when reviewing brand compliance, styling documents, creating presentations, or when user mentions branding, style guide, corporate identity, or brand consistency.
---

# Brand Style Guidelines

## Core Principles

1. **Consistency**: Same look and feel across all materials
2. **Clarity**: Clean, professional, easy to read
3. **Recognition**: Instantly identifiable as our brand

## Visual Standards

### Colors

| Use | Color | Hex | RGB |
|-----|-------|-----|-----|
| Primary | Blue | #0066CC | 0, 102, 204 |
| Secondary | Gray | #666666 | 102, 102, 102 |
| Accent | Orange | #FF6600 | 255, 102, 0 |
| Background | White | #FFFFFF | 255, 255, 255 |

### Typography

| Element | Font | Size | Weight |
|---------|------|------|--------|
| Headings | Inter | 24-48px | Bold |
| Body | Inter | 14-16px | Regular |
| Captions | Inter | 12px | Light |

### Logo Usage

- Minimum size: 32px height
- Clear space: 1x logo height on all sides
- Never stretch, rotate, or recolor

For logo files, see [assets/logos/](assets/logos/)

## Application Guidelines

### Documents

1. Use company template (see [assets/templates/](assets/templates/))
2. Headers: Primary blue, Inter Bold
3. Body: Dark gray, Inter Regular
4. One accent color per document maximum

### Presentations

1. Use slide master template
2. Maximum 6 bullet points per slide
3. Images should be high-quality (min 150 DPI)

## Review Checklist

- [ ] Correct logo version used
- [ ] Colors match brand palette
- [ ] Typography follows guidelines
- [ ] Adequate whitespace
- [ ] No stretched/distorted images

## Examples

### Good Example

[Screenshot or description of correct application]

### Bad Example

Common mistakes:
- Using navy blue (#000080) instead of brand blue (#0066CC)
- Logo too small or crowded
- Mixed fonts within same document
```

### Typical Directory Structure

```
brand-style-enforcer/
├── SKILL.md
├── references/
│   ├── color-specifications.md
│   ├── typography-guide.md
│   └── voice-and-tone.md
└── assets/
    ├── logos/
    │   ├── logo-primary.png
    │   └── logo-white.png
    └── templates/
        ├── document-template.docx
        └── presentation-template.pptx
```

---

## Template Selection Guide

| If your skill... | Use Type |
|-----------------|----------|
| Manipulates file formats | Document Processor |
| Automates dev tasks | Code Automator |
| Queries data / generates reports | Data Analyzer |
| Coordinates multi-step processes | Workflow Orchestrator |
| Provides specialized knowledge | Domain Expert |

When in doubt, start with **Document Processor** (most common) or **Domain Expert** (most flexible).
