# Review Checklist — the 12 dimensions (+ concurrency & performance)

Walk these in roughly this order. Each item is an **actionable question** to ask of the diff. Source: Google eng-practices, "What to look for in a code review", extended with concurrency/perf deep-dives.

> Design and Functionality are the highest-value lenses — spend most of your attention there. Naming/Comments/Style are cheap to fix and rarely blocking.

## 1. Design (most important)
- Is the overall approach sound for the problem, or is there a materially simpler one?
- Do the new pieces interact cleanly with existing code? Right layer / right module?
- Does this belong here, or in a shared library / different service?
- Is *now* the right time, or is it speculative ("we might need…")?

## 2. Functionality
- Does it actually do what the PR description claims?
- Is the behavior good for **end-users** AND **future developers** reading it?
- **Edge cases:** empty / null / huge inputs, off-by-one, timezone/locale, unicode, pagination boundaries.
- **Error paths:** are failures handled, surfaced, and recoverable — not swallowed?
- For UI changes: can you validate behavior, or should you request a demo/screenshot?

## 3. Complexity
- Can a reader understand each line/function/class *quickly*? If not, it's too complex.
- **Over-engineering check:** generic abstractions, config knobs, or "future-proofing" nobody asked for? Solve the *known* problem.
- Could this be split into smaller, independently-reviewable changes?

## 4. Tests
- Are new/changed behaviors covered (unit / integration / e2e as appropriate)?
- Tests in the **same PR** as the code (barring a real emergency)?
- Would the tests **actually fail** if the code broke? (No tautological asserts, no false positives.)
- Are tests readable and not over-complex? Test code is maintained code too.

## 5. Naming
- Does each name communicate what it is / does — long enough to be clear, short enough to read?
- No misleading names (a `get` that mutates, a `count` that returns a list)?

## 6. Comments
- Do comments explain **why**, not restate **what**? (If you need a comment to explain *what*, prefer simplifying the code.)
- Justified exceptions: regex, non-obvious algorithms, hard-won workarounds (link the issue).
- Any stale comments / dead TODOs to remove?

## 7. Style
- Conforms to the language's style guide / repo linter? The **linter is the authority** — don't hand-review what a formatter owns.
- Extra polish beyond the guide → prefix `Nit:` and make it optional.
- No giant reformat mixed into a functional change (should be a separate PR).

## 8. Consistency
- Matches surrounding code's existing patterns? If existing code conflicts with the style guide, the guide wins for *required* rules; otherwise bias to local consistency.
- New inconsistency introduced → ask for a TODO + tracking issue rather than blocking, when the change is otherwise net-positive.

## 9. Documentation
- If this changes how users **build / test / call / deploy** the code, are README / docs / generated references updated?
- Code deleted or deprecated → corresponding docs removed/updated?

## 10. Every Line
- Review **every human-written line** you're assigned. Don't rubber-stamp blocks you don't understand — ask.
- May *scan* (not line-review): generated code, large data files, vendored deps, lockfiles.
- Out of your depth on part of it (security, concurrency, privacy, a11y, i18n)? Ensure a **qualified** reviewer covers that part and say which parts you reviewed.

## 11. Context
- Look beyond the diff: open the whole file/module. Does the change still make sense with the surrounding invariants?
- System-level: does this improve code health, or add a little complexity/debt that compounds across many such PRs? Don't let rot accumulate one "small" change at a time.

## 12. Good Things (don't skip)
- Call out what's done well — especially when the author cleanly addressed earlier feedback. Mentoring value is highest when you reinforce the right behavior, not only the wrong.

---

## Concurrency deep-dive (when threads/async/parallelism are touched)
- **Race conditions:** shared mutable state without a lock / atomic? Check-then-act gaps (TOCTOU)?
- **Deadlocks:** consistent lock ordering? Any lock held across an `await` / blocking I/O / callback?
- **Async correctness:** every awaitable awaited? No fire-and-forget that drops errors? No blocking call (sync I/O, `time.sleep`, CPU loop) inside an async context / event loop?
- **Cancellation & timeouts:** are long ops cancellable and bounded?
- **Idempotency:** safe to retry? (Important for queues, webhooks, payments.)
> These bugs rarely show up when running once — they need careful reading. Prefer concurrency models that make races/deadlocks *unlikely by construction*.

## Performance deep-dive
- **N+1 queries:** a DB/RPC call inside a loop? → batch / `IN` / join / dataloader.
- **Algorithmic cost:** accidental O(n²) over user-controlled n? Nested loops over the same collection?
- **Allocations / copies:** large objects copied in hot paths? Unbounded in-memory buffers on user input?
- **Caching & memoization:** repeated identical work? Cache invalidation correct?
- **Blocking in async:** see concurrency above — the #1 perf killer in event-loop code.
- **Resource lifecycle:** files / sockets / DB connections / cursors closed (context managers / `defer` / `finally`)? Connection pools bounded?
- Don't micro-optimize cold paths — flag perf only where n is real or the path is hot.
