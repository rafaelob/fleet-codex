# Changelog

## 0.5.0 — 2026-09-22

- Replace the retired `gpt-5.6-sol` and `gpt-5.6-luna` model ids with
  `gpt-6-sol` and `gpt-6-luna` in all three arrangements: lead `config.toml`,
  every role card, and the README model tables.
- Allocation, reasoning effort and thread caps are unchanged; every Luna role
  remains at `max` and Astra roles are untouched.
- Configuration change only; the dated runtime evidence still refers to the
  retired ids and has not been re-run against the new models.

## 0.4.0 — 2026-09-20

- Lower Advanced Delivery's total-thread cap from five to four, matching
  Balanced Delivery's four (three active children each); Lean is unchanged at
  three total, two active.
- Rewrite the shared `codex-orchestration` skill and every arrangement's AGENTS
  snippets around bounded, single-mission delegation: an accepted delivery
  closes the child's mission, a follow-up only corrects or clarifies that same
  delivery, a finished child is never reused for new work, and a child is never
  woken to ask for status or an acknowledgement.
- Configuration and instruction change only; not exercised in a new native
  concurrency or saturation run.

## 0.3.0 — 2026-09-13

- Set native child waits to a one-minute minimum and five-minute default in all
  three arrangements, preserving budgets, goals, models, caps and hooks.
- Extend the existing optional orchestration skill with task-appropriate waits,
  meaningful progress signals and a separate point for investigating a stall.
  Keep the installable rules concise.
- Explain context flow, automatic goal continuation, timing tradeoffs, upgrade
  and rollback; distinguish configuration evidence from unmeasured quota savings.
- Validate optional wait fields, including types, bounds and effective ordering.

## 0.2.1 — 2026-09-13

- Keep insertable delegation rules concise: remove roster counts, concurrency
  figures, model-allocation summaries, and runtime-evidence links from snippets.
- Invoke the optional orchestration skill with a native-reading fallback; keep
  optional Pragmatic Programmer guidance in a separate engineering section.

## 0.2.0 — 2026-09-13

- Add Balanced Delivery for everyday product work: two Astra roles, two Sol roles,
  and eight Luna roles, with explicit implementation and read-only boundaries.
- Rebalance Advanced to four Astra, four Sol and seven Luna roles, without Terra.
- Reserve Lean's single Astra role for advice; integration remains Sol high and
  its six other roles use Luna max, including implementation and independent review.
- Simplify active teams to at most four, three and two children respectively,
  with progressively smaller catalogs of fifteen, twelve and eight roles. Removed
  responsibilities have explicit owners; all handoffs go through the parent.
- Keep prior native runtime evidence explicitly historical; do not claim that
  allocation changes or smaller caps have received complete runtime validation.

## 0.1.0

- Introduce Advanced Delivery for complex product work and Lean Delivery for
  cost-conscious work with a lighter specialist allocation.
- Provide 19 independent agent TOMLs per arrangement, minimal configuration
  fragments, and suggested AGENTS.md sections for user or project installation.
- Add optional Apache-2.0 routing and pragmatic engineering skills with inline
  invocation triggers, plus an MIT spawn-contract hook.
- Keep reusable skills outside arrangements and open an independent plugin
  contribution area for standard packages containing skills, MCP and hooks.
- Add optional ASCII-safe, role-themed nickname pools and structured, concise
  instruction sections with explicit fresh-context child briefs.
- Account for the measured V2 namespaced hook identity and configure the explicit
  V2 total-thread cap rather than the legacy child-cap field.
- Explain fresh-context delegation, role/model ownership, follow-ups, concurrency
  and runtime limitations, with official documentation and pinned source links.
- Provide English installation/contribution guides, a complementary PT-BR guide,
  issue forms, a PR template and credential-free cross-platform CI.
- Document temporary-directory isolation for Windows runtime tests, based on
  a real sandbox startup failure and a successful control-preserving correction.

See [validation](validation.md) for measured results and compatibility limits.
