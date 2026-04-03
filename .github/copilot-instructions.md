# Project Guidelines

## Purpose
This repository is an **Agent Prompt Instruction Project** — it contains only agent configurations, instructions, and prompts. No application source code lives here.

## Repository Structure
```
.github/
  agents/
    product-analyst/      # Product Analysis agent config & instructions
    technical-leader/     # Technical Leader agent config & instructions
  instructions/
    product-analyst/      # File-scoped instructions for product analysis tasks
    technical-leader/     # File-scoped instructions for technical leadership tasks
  prompts/
    product-analyst/      # Reusable prompts for product analysis workflows
    technical-leader/     # Reusable prompts for technical leadership workflows
```

## Conventions
- Each agent role lives in its own subfolder under `agents/`, `instructions/`, and `prompts/`.
- Agent files use `.agent.md`, instruction files use `.instructions.md`, prompt files use `.prompt.md`.
- Keep agent instructions focused on the role's scope — avoid cross-role concerns in a single file.
- Document each agent's trigger phrases clearly in the `description` frontmatter field.

## Build and Test
- No build step required — this is a documentation/configuration-only repo.
