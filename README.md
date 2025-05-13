# When Comments Lie

A growing collection of short write-ups exploring real-world examples where **code comments mislead**, misunderstand, or outright lie — and what we can learn from them.

Inspired by the principle that **code should explain itself**, this series walks through cases where intentions were good, but assumptions about code behavior didn’t hold up.

## Entry #1: Django ORM – `.all()` vs `.first()`

> _“Using `.all()` instead of `.first()` to avoid an extra database query...”_

Sounds smart, right? But that comment was wrong — and so was the logic that followed.

Read the full write-up → [When Comments Lie: A Case Study in ORM Behavior](./all-vs-first.md)

It covers:
- Lazy vs eager evaluation in Django
- Why `.first()` is not inherently inefficient
- How `select_related()` can collapse two queries into one
- A full runnable test harness to explore the behavior yourself

## About This Series

This repo will serve as a home for:
- 🧾 Clean, runnable examples based on real-world code
- 📊 Honest breakdowns of what the code *actually* does
- 💡 Lessons learned and refactors that clarify intent

New entries will be added over time. If you’ve got a great example of a misleading comment or subtle misunderstanding in production code, feel free to suggest one via [Issues](https://github.com/gmcnickle/when-comments-lie/issues).


