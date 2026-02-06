---
id: 007
title: Generate MCP Server & Todo Tooling Implementation Plan
stage: plan
date: 2026-01-24
surface: agent
model: gemini-1.5-pro
feature: 005-mcp-todo-tooling
branch: 005-mcp-todo-tooling
user: CLI_User
command: |
  ---
  description: Execute the implementation planning workflow using the plan template to generate design artifacts.
  handoffs: 
    - label: Create Tasks
      agent: sp.tasks
      prompt: Break the plan into tasks
      send: true
    - label: Create Checklist
      agent: sp.checklist
      prompt: Create a checklist for the following domain...
  ---

  ## User Input

  ```text
  $ARGUMENTS
  ```

  You **MUST** consider the user input before proceeding (if not empty).

  ## Outline

  1. **Setup**: Run `.specify/scripts/powershell/setup-plan.ps1 -Json` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

  2. **Load context**: Read FEATURE_SPEC and `.specify/memory/constitution.md`. Load IMPL_PLAN template (already copied).

  3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
     - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
     - Fill Constitution Check section from constitution
     - Evaluate gates (ERROR if violations unjustified)
     - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
     - Phase 1: Generate data-model.md, contracts/, quickstart.md
     - Phase 1: Update agent context by running the agent script
     - Re-evaluate Constitution Check post-design

  4. **Stop and report**: Command ends after Phase 2 planning. Report branch, IMPL_PLAN path, and generated artifacts.

  ## Phases

  ### Phase 0: Outline & Research

  1. **Extract unknowns from Technical Context** above:
     - For each NEEDS CLARIFICATION → research task
     - For each dependency → best practices task
     - For each integration → patterns task

  2. **Generate and dispatch research agents**:

     ```text
     For each unknown in Technical Context:
       Task: "Research {unknown} for {feature context}"
     For each technology choice:
       Task: "Find best practices for {tech} in {domain}"
     ```

  3. **Consolidate findings** in `research.md` using format:
     - Decision: [what was chosen]
     - Rationale: [why chosen]
     - Alternatives considered: [what else evaluated]

  **Output**: research.md with all NEEDS CLARIFICATION resolved

  ### Phase 1: Design & Contracts

  **Prerequisites:** `research.md` complete

  1. **Extract entities from feature spec** → `data-model.md`:
     - Entity name, fields, relationships
     - Validation rules from requirements
     - State transitions if applicable

  2. **Generate API contracts** from functional requirements:
     - For each user action → endpoint
     - Use standard REST/GraphQL patterns
     - Output OpenAPI/GraphQL schema to `/contracts/`

  3. **Agent context update**:
     - Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType gemini`
     - These scripts detect which AI agent is in use
     - Update the appropriate agent-specific context file
     - Add only new technology from current plan
     - Preserve manual additions between markers

  **Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

  ## Key rules

  - Use absolute paths
  - ERROR on gate failures or unresolved clarifications

  ---

  As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

  1) Determine Stage
     - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

  2) Generate Title and Determine Routing:
     - Generate Title: 3–7 words (slug for filename)
     - Route is automatically determined by stage:
       - `constitution` → `history/prompts/constitution/`
       - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
       - `general` → `history/prompts/general/`

  3) Create and Fill PHR (Shell first; fallback agent‑native)
     - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
     - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
     - If the script fails:
       - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
       - Allocate an ID; compute the output path based on stage from step 2; write the file
       - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

  4) Validate + report
     - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
     - On failure: warn, don't block. Skip only for `/sp.phr`.


  /sp.plan before planning make sure that you have context7 mcp server for getting official docs to make better plan Now plan: - Initialize MCP server using Official MCP SDK
  - Define MCP tool interfaces and schemas
  - Implement tool handlers backed by SQLModel
  - Enforce JWT-based user validation per tool
  - Ensure all tools are stateless and database-driven
  - Validate tool behavior with example inputs/outputs
labels: ["plan", "feature", "mcp-todo-tooling"]
links:
  spec: specs/005-mcp-todo-tooling/spec.md
  ticket: null
  adr: null
  pr: null
files: 
 - specs/005-mcp-todo-tooling/plan.md
 - specs/005-mcp-todo-tooling/research.md
 - specs/005-mcp-todo-tooling/data-model.md
 - specs/005-mcp-todo-tooling/contracts/openapi.yaml
 - specs/005-mcp-todo-tooling/quickstart.md
 - GEMINI.md
tests:

## Response snapshot

Implementation plan for 'MCP Server & Todo Tooling' feature generated successfully. Research, Data Model, API Contract, and Quickstart documents created. Ready for task breakdown.

## Outcome

- ✅ Impact: Implementation plan for MCP Server & Todo Tooling feature created and validated.
- 🧪 Tests: N/A
- 📁 Files: Plan, research, data model, API contract, and quickstart documents created/updated. Agent context updated.
- 🔁 Next prompts: Ready for `/sp.tasks`.
- 🧠 Reflection: Successfully executed the /sp.plan workflow for the MCP Server & Todo Tooling feature, including research, data model, API contracts, quickstart generation, and agent context update.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): Constitution checks passed.
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
