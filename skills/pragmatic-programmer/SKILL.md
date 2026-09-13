---
name: pragmatic-programmer
description: "Use for a targeted engineering decision: an unexplained green result, duplicate knowledge, a boundary contract, a reversible next step, a spike versus real path, or shared state and finite resources. Skip routine edits with no such decision."
license: Apache-2.0
---

# Pragmatic Programmer

Use this as an optional decision aid at a named engineering uncertainty, not as a mandatory checklist for every edit. It does not grant authority or replace a repository's safety, testing, or permission rules.

Conceptual reference: [*The Pragmatic Programmer: Your Journey to Mastery*, 20th Anniversary Edition](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/) by David Thomas and Andrew Hunt. The guidance below is paraphrased.

## Why is this green?

When a fix or test passes but the mechanism is unclear, state three things: what failed before, what the change altered, and what input, ordering, or environment could make it fail again. If any answer is missing, treat the result as evidence of behavior, not proof of cause. Investigate the smallest relevant path until the next decision is supported. Do not turn this into a mandatory postmortem for an already-explained change.

## DRY is about knowledge

Before adding or merging similar code, ask whether the same real-world fact would need to change in both places for the same reason. If yes, establish one authority and derive or reuse the other representation. If no, similar syntax may be coincidental; avoid coupling two concerns that will diverge. Search the relevant scope before creating a second definition.

## Contracts and real input validation

For a new or changed boundary, state the preconditions, promised result, and invariants that must survive the operation. Keep assumptions inside the boundary explicit. Validate untrusted or external input at the real boundary and provide normal error handling there; an assertion or an internal precondition is not input validation.

## Reversible small steps

Choose the smallest change that reaches a useful feedback point. Prefer a change with an easy undo path when the decision is uncertain. For a hard-to-reverse decision, identify the affected consumer or data, recovery path, and the missing evidence before proceeding. Do not require formal alternatives for an ordinary reversible edit.

## Spike or real path?

Use a spike to answer one named uncertainty with a stop condition. Keep it isolated and discard it or deliberately rebuild it before it becomes production behavior. Use a thin real path when the question is whether the actual layers connect end to end; that path must meet the normal quality bar and remains part of the product.

## Shared state and finite resources

If another actor can change a value between a read, decision, and write, design the check-and-update as one owned operation or use an appropriate synchronization boundary. For a finite resource such as a lock, connection, process, port, or temporary artifact, name its owner, release point, and recovery if setup fails. Keep acquisition and release balanced, and check for leftovers at the relevant close point.

## Impossible versus operational errors

Use an assertion only for a state made unreachable by an enforced internal invariant, and keep assertion conditions free of side effects. Invalid input, unavailable services, exhausted capacity, and missing resources are operational failures: handle or report them explicitly. Never use an assertion instead of boundary validation or error handling.

## Finish the scoped work

When safe local work and disposable fixtures are available, carry the requested artifact through the checks affected by the change before handing it back. Repeat a check only when a change or new evidence makes another run informative. Production side effects remain outside this skill's authority.
