# Workflow Patterns

Patterns for structuring multi-step processes in skills.

## Sequential Workflows

For complex tasks, break operations into clear, sequential steps. Give Claude an overview early in SKILL.md:

```markdown
Filling a PDF form involves these steps:

1. Analyze the form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Validate mapping (run validate_fields.py)
4. Fill the form (run fill_form.py)
5. Verify output (run verify_output.py)
```

### When to Use
- Operations must happen in order
- Each step depends on previous output
- Validation between steps is needed

## Conditional Workflows

For tasks with branching logic, guide Claude through decision points:

```markdown
1. Determine the modification type:
   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow:
   a. [step]
   b. [step]

3. Editing workflow:
   a. [step]
   b. [step]
```

### When to Use
- Task varies based on input type
- Different approaches for different scenarios
- Need to avoid running unnecessary steps

## Hybrid: Sequential with Branches

Combine both patterns for complex processes:

```markdown
## Deployment Process

### Phase 1: Pre-flight (always)
1. Run tests
2. Check environment

### Phase 2: Build (conditional)
- **Frontend only?** → `npm run build:frontend`
- **Full stack?** → `npm run build:all`

### Phase 3: Deploy (sequential)
1. Upload artifacts
2. Run migrations
3. Health check
```

## Workflow Visualization Tips

Use ASCII diagrams for complex flows:

```
Start → Check Type → [Type A] → Process A → End
                  ↘ [Type B] → Process B ↗
```

Keep diagrams simple - if it's too complex, split into sub-workflows.
