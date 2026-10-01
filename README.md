# WDX Delivery Planner

Operational route-planning project for Netherlands and Belgium warehouse delivery operations.

## Read this first

Any coding or analysis agent working in this repository **must read**:

1. `AGENTS.md`
2. `business/REQUIREMENTS.md`
3. `business/WORK_STATUS.md`
4. `docs/ACCEPTANCE.md`
5. `docs/DATA_PRIVACY.md`
6. `review/REVIEW_FEEDBACK.md`
7. `review/REVIEW_REQUEST.md`

The project goal is not to produce a mathematically impressive optimizer. The goal is to produce routes that resemble decisions made by an experienced dispatcher while still satisfying all hard constraints.

## Core principle

**Geography first, feasibility always, optimization second.**

Do not treat Route numbers as geographic order. Do not force a strict “maximum two Routes per vehicle” rule. First determine real geographic continuity, then assign vehicles, then order stops.

## Collaboration model

- `business/REQUIREMENTS.md` is the canonical business baseline.
- `business/WORK_STATUS.md` is the current execution state and must be updated after meaningful work.
- `business/DECISIONS.md` is an append-only record of important decisions and assumptions.
- `docs/ACCEPTANCE.md` defines what counts as a valid result.
- `docs/DATA_PRIVACY.md` protects customer/operational data in this public repository.
- `review/REVIEW_REQUEST.md` is the implementation agent's evidence handoff to the reviewer.
- `review/REVIEW_FEEDBACK.md` is the independent reviewer's persistent feedback channel for the next correction cycle.
- `prompts/IMPLEMENTATION_AGENT.md` contains the standard prompt for an autonomous implementation agent.

Normal loop:

**implementation agent → commit + REVIEW_REQUEST → independent review → REVIEW_FEEDBACK → implementation agent fixes → new commit**

Real customer/order data should stay outside this public repository unless irreversibly sanitized.

## Reproducible baseline diagnostics

The initial runner validates a supplied ordered plan and reports six-station
geography and workload evidence. It does not assign vehicles automatically.
See [input contract and commands](docs/BASELINE_INPUT.md). The committed
examples/evidence use wholly invented data; real operational validation and the
343-task historical regression are pending.

Do not claim the project is optimized merely because tests pass. Hard-constraint correctness and operational route quality are separate acceptance layers.
