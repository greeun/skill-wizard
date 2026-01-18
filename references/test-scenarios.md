# Test Scenario Guide

Every skill should be tested with three types of scenarios before deployment.

## Why Test Scenarios Matter

```
Untested Skill
    ↓
Triggers incorrectly (or not at all)
    ↓
User frustration / skill abandoned
```

Testing prevents:
- **False negatives**: Skill doesn't trigger when it should
- **False positives**: Skill triggers when it shouldn't
- **Partial matches**: Skill triggers but handles task poorly

## The Three Test Types

### 1. Happy Path (Should Trigger ✓)

A typical request that clearly matches the skill's purpose.

**Characteristics:**
- Uses keywords from the description
- Matches the primary use case
- Unambiguous intent

**Example for `pdf-table-extractor`:**
```
User: "Extract the table from page 3 of this PDF"
Expected: Skill triggers, extracts table successfully
```

### 2. Edge Case (Should Trigger ✓, but tricky)

An unusual but valid request that the skill should handle.

**Characteristics:**
- Uses synonyms instead of exact keywords
- Indirect phrasing
- Boundary conditions

**Example for `pdf-table-extractor`:**
```
User: "Get the data from this document into a spreadsheet"
Expected: Skill triggers (document → PDF, data → table, spreadsheet → CSV)
```

### 3. Out of Scope (Should NOT Trigger ✗)

A request that seems related but shouldn't activate the skill.

**Characteristics:**
- Similar domain but different task
- Would be handled by a different skill
- Outside the skill's capabilities

**Example for `pdf-table-extractor`:**
```
User: "Edit the text in this PDF"
Expected: Skill does NOT trigger (editing ≠ extraction)
```

---

## Generating Test Scenarios

### Method 1: Keyword Expansion

Take your description's trigger keywords and create variations:

**Description keywords:** `PDF, table, extract, data, document`

| Type | Scenario |
|------|----------|
| Happy Path | "Extract tables from this PDF" |
| Edge Case | "Pull the data from this document" |
| Out of Scope | "Create a table in this PDF" |

### Method 2: User Persona Simulation

Imagine different users asking for the same thing:

| Persona | Request Style |
|---------|--------------|
| Technical | "Run pdfplumber extraction on report.pdf" |
| Non-technical | "I need to get the numbers from this PDF file" |
| Rushed | "table from pdf please" |
| Detailed | "Could you please extract the financial data table from page 5 of the quarterly report PDF?" |

### Method 3: Inversion Testing

For each "should trigger" case, create a "should NOT trigger" inverse:

| Triggers | Does NOT Trigger |
|----------|-----------------|
| "Extract table from PDF" | "Extract table from Excel" |
| "Convert PDF to CSV" | "Convert CSV to PDF" |
| "Read PDF data" | "Write PDF data" |

---

## Test Scenario Template

Use this template to document your test scenarios:

```markdown
## Test Scenarios for [skill-name]

### Happy Path Tests

**Test 1: [Name]**
- Request: "[User's exact words]"
- Expected: Skill triggers and [expected behavior]
- Keywords matched: [list]

**Test 2: [Name]**
- Request: "[User's exact words]"
- Expected: Skill triggers and [expected behavior]
- Keywords matched: [list]

### Edge Case Tests

**Test 1: [Name]**
- Request: "[User's exact words]"
- Expected: Skill triggers and [expected behavior]
- Challenge: [Why this is tricky]

**Test 2: [Name]**
- Request: "[User's exact words]"
- Expected: Skill triggers and [expected behavior]
- Challenge: [Why this is tricky]

### Out of Scope Tests

**Test 1: [Name]**
- Request: "[User's exact words]"
- Expected: Skill does NOT trigger
- Reason: [Why this shouldn't trigger]
- Better skill: [Which skill should handle this]

**Test 2: [Name]**
- Request: "[User's exact words]"
- Expected: Skill does NOT trigger
- Reason: [Why this shouldn't trigger]
```

---

## Example: Complete Test Suite

### For `sales-analytics` skill

**Description:**
```
Sales data analysis with revenue metrics, pipeline tracking, and
forecast generation. Use when analyzing sales data, generating sales
reports, tracking pipeline, or when user mentions revenue, deals,
forecast, CRM, or sales metrics.
```

### Happy Path Tests

**Test 1: Direct Request**
- Request: "Generate a sales report for Q4"
- Expected: Skill triggers, produces quarterly sales report
- Keywords matched: sales, report

**Test 2: Metric Query**
- Request: "What's our current pipeline value?"
- Expected: Skill triggers, queries pipeline data
- Keywords matched: pipeline

**Test 3: Forecast Request**
- Request: "Create a revenue forecast for next month"
- Expected: Skill triggers, generates forecast
- Keywords matched: revenue, forecast

### Edge Case Tests

**Test 1: Indirect Phrasing**
- Request: "How are we doing on our numbers this quarter?"
- Expected: Skill triggers, shows key metrics
- Challenge: No explicit keywords, relies on context ("numbers", "quarter")

**Test 2: Synonym Usage**
- Request: "Show me the deal flow"
- Expected: Skill triggers, shows pipeline
- Challenge: "deal flow" = pipeline (synonym)

**Test 3: Partial Context**
- Request: "Compare this month to last month"
- Expected: Skill triggers if in sales context
- Challenge: Needs conversation context to determine domain

### Out of Scope Tests

**Test 1: Different Data Domain**
- Request: "Analyze our website traffic"
- Expected: Skill does NOT trigger
- Reason: Website analytics ≠ sales analytics
- Better skill: `web-analytics`

**Test 2: Different Action**
- Request: "Enter this new deal into the CRM"
- Expected: Skill does NOT trigger
- Reason: Data entry ≠ data analysis
- Better skill: `crm-data-entry`

**Test 3: Similar Keywords, Different Intent**
- Request: "Help me write a sales email"
- Expected: Skill does NOT trigger
- Reason: Sales communication ≠ sales data analysis
- Better skill: `email-writer`

---

## Running Tests

### Manual Testing

1. Start a new Claude conversation
2. Enter each test request
3. Observe if skill triggers
4. Verify output quality

### Test Checklist

For each test:
- [ ] Skill triggered correctly (or didn't, as expected)
- [ ] Output format matches expectations
- [ ] No errors or exceptions
- [ ] Completes in reasonable time

### Post-Test Actions

| Result | Action |
|--------|--------|
| Happy path fails to trigger | Add missing keywords to description |
| Edge case fails to trigger | Add synonyms to description |
| Out of scope incorrectly triggers | Narrow description scope |
| Output quality poor | Improve SKILL.md instructions |

---

## Common Test Failures

### 1. Description Too Narrow

**Symptom:** Happy path triggers, edge cases don't

**Fix:** Add more trigger keywords and synonyms
```yaml
# Before
description: Extract tables from PDF files.

# After
description: Extract tables from PDF files. Use when extracting
data, parsing documents, converting PDF to spreadsheet, or when
user mentions PDF, table, data extraction, or document parsing.
```

### 2. Description Too Broad

**Symptom:** Out of scope requests trigger the skill

**Fix:** Add specificity or exclusions
```yaml
# Before
description: Work with documents and data.

# After
description: Extract data from PDF documents (not editing).
Use when extracting tables or text from PDFs, not for
modifying PDF content.
```

### 3. Missing Context Handling

**Symptom:** Skill fails when request lacks explicit keywords

**Fix:** Add conversational triggers
```yaml
# Before
description: Generate sales reports with revenue metrics.

# After
description: Generate sales reports with revenue metrics.
Use when analyzing sales data, generating reports, or when
user asks about revenue, deals, pipeline, or Q1/Q2/Q3/Q4 performance.
```

---

## Test Scenario Generation Script

Use the wizard's test generator for automated suggestions:

```bash
python ~/.claude/skills/skill-wizard/scripts/generate_tests.py \
  --description "Your skill description here" \
  --type document-processor
```

This outputs suggested test scenarios based on:
- Keywords extracted from description
- Common patterns for the skill type
- Known edge cases and out-of-scope examples
