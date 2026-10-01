# WDX Delivery Planner

Operational route-planning project for Netherlands and Belgium warehouse delivery operations.

## Read this first

Any coding or analysis agent working in this repository **must read**:

1. `AGENTS.md`
2. `business/REQUIREMENTS.md`
3. `business/WORK_STATUS.md`
4. `docs/ACCEPTANCE.md`
5. `review/REVIEW_REQUEST.md`

The project goal is not to produce a mathematically impressive optimizer. The goal is to produce routes that resemble decisions made by an experienced dispatcher while still satisfying all hard constraints.

## Core principle

**Geography first, feasibility always, optimization second.**

Do not treat Route numbers as geographic order. Do not force a strict “maximum two Routes per vehicle” rule. First determine real geographic continuity, then assign vehicles, then order stops.

## Collaboration model

- `business/REQUIREMENTS.md` is the canonical business baseline.
- `business/WORK_STATUS.md` is the current execution state and must be updated after meaningful work.
- `business/DECISIONS.md` is an append-only record of important decisions and assumptions.
- `docs/ACCEPTANCE.md` defines what counts as a valid result.
- `review/REVIEW_REQUEST.md` is the handoff from the implementation agent to the reviewer.
- `prompts/IMPLEMENTATION_AGENT.md` contains the standard prompt for an autonomous implementation agent.

Do not claim the project is optimized merely because tests pass. Hard-constraint correctness and operational route quality are separate acceptance layers.
