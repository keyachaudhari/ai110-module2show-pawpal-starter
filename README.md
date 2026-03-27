# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
    
## Smarter Scheduling

This project adds a few simple improvements to make the scheduler more helpful and easy to understand:

- Sorting by time: tasks with a scheduled time are shown earliest first; tasks without a time appear at the end.
- Filtering: easily show only incomplete tasks or tasks for a specific pet to focus on what matters.
- Recurring tasks: tasks can be set to "daily" or "weekly" and when marked complete a next occurrence is created using datetime.timedelta.
- Conflict detection: the scheduler detects overlapping scheduled tasks and can return a short warning message without crashing the program.

These changes are intentionally simple and beginner-friendly so you can read and extend the logic easily.

## Testing PawPal+

- Run the test suite:

  python -m pytest

- What the tests cover (brief):
  - Task completion behavior
  - Adding tasks to a pet
  - Sorting tasks by scheduled time
  - Recurring tasks (daily recurrence creation)
  - Conflict detection for overlapping tasks

- Confidence: ★★★☆☆ (3/5) — a small, focused test suite that checks core scheduling behaviors; run the tests locally to see current results.
