#    ADR-0000 : ADR IMPLEMENTATION

## STATUS

Proposed / Accepted / Deprecated / Superseded / Rejected

![adr's life cycle](https://blog.stephane-robert.info/_astro/lifecycle-adr.hrD8d9bw_WCpH.svg)

## CONTEXT/PROBLEM

Our project is complex, and we currently lack clear architectural decisions. As a team of four developers, it is essential to document these choices.

Without proper documentation, the reasoning behind architectural decisions tends to be lost over time. Documenting them would not only preserve this knowledge but also improve team presentations and discussions, helping each member deepen their understanding.

Additionally, it would make the project easier to maintain in the long term.

## DECISION

**We decide to adopt Architecture Decision Records (ADR)** as the primary method for documenting architectural decisions.

This choice is motivated by the need for a structured, traceable, and version-controlled approach that remains close to the codebase. ADRs ensure that each decision is documented consistently and that the reasoning behind it is preserved over time.

#### Advantages :
- Structured and consistent: Each decision follows the same format
- Captures the “why”: Focuses on reasoning, not just the outcome
- Version-controlled: Stored in the code repository (Git history)
- Traceable over time: Easy to track how decisions evolved
- Close to the codebase: Developers can access it directly

#### Disadvantages :
- More formal and time-consuming: Requires discipline to write and maintain
- Can feel heavy for small teams/projects
- Less visual and less intuitive than a wiki
- Harder for non-technical stakeholders to read

## Alternatives


### Option A : Notion

#### Advantages :
- Easy to use and quick to write
- Flexible format: No strict structure required
- Good for collaboration and sharing knowledge
- More accessible for non-technical team members
- Supports rich content (diagrams, images, links, etc.)

#### Disadvantages :
- Lack of structure: Decisions may be inconsistent or incomplete
- Poor traceability: Harder to follow the evolution of decisions
- Knowledge can become outdated quickly
- Disconnected from the codebase
- Search and organization can become messy over time

### Option B : 


## CONSEQUENCES

### ✅ Positive

- Improved knowledge sharing: All team members can understand past decisions and their rationale
- Better onboarding: New contributors can quickly get up to speed
- Stronger maintainability: Easier to revisit and update decisions when the project evolves
- Clear decision history: Enables tracking of changes and evolution over time
- Alignment within the team: Encourages discussion and validation of architectural choices

### ❌ Negative

- Additional overhead: Writing ADRs requires time and discipline
- Adoption effort: Team members need to get used to the format and process
- Risk of inconsistency: If not enforced, ADRs may not be written systematically

## IMMPLEMENTATION

- use `make adr` to create a new adr
- Review ADRs during code reviews or team discussions
- Update ADR status when decisions evolve (Accepted, Deprecated, etc.)

## NOTES

> ADRs are reserved for important architectural decisions requiring traceability


