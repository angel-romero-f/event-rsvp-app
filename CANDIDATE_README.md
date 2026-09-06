# Event RSVP App - Interview Exercise

Welcome! This exercise will test your ability to understand an unfamiliar codebase and review code critically.

## Getting Started

**Requirements:** Python 3.7+

1. Run the setup script:
```bash
./setup.sh
```

2. Run the application:
```bash
./run.sh
```

3. Open http://localhost:5000 in your browser

## Phase 1: Explore the Application (10-15 minutes)

Your first task is to explore the working application and understand how it works.

**Things to try:**
- Browse the event listing page
- Click on an event to see details
- RSVP to an event and observe what changes
- Cancel your RSVP
- Try to RSVP to the "Database Design" event (it's full)

**Questions to answer for yourself:**
- How is event data structured? (Check `schema.sql`)
- What happens when you click "RSVP"? Trace the request from button click to database.
- How does the app enforce capacity limits?
- Where is the current user ID defined? (Hint: there's no real authentication)

## Phase 2: Design a New Feature (10-15 minutes)

**Feature Request: Waitlist Functionality**

When an event reaches capacity, users should be able to join a waitlist. When someone cancels their RSVP, the next person on the waitlist should automatically be promoted to confirmed status.

**Your task:**
Explain at a high level how you would implement this feature. You don't need to write code - just describe:

1. What changes to the database schema are needed?
2. What new data does the API need to return?
3. How should the RSVP endpoint behave when an event is full?
4. What happens when someone cancels? What code triggers the promotion?
5. What edge cases should we handle?

## Phase 3: Code Review (15-20 minutes)

A team member has already implemented the waitlist feature in **Pull Request #1**.

Your task is to review the implementation and identify any issues.

**Access the PR:**
- View it on GitHub: https://github.com/angel-romero-f/event-rsvp-app/pull/1
- Or checkout locally: `git fetch && git checkout feature/waitlist`
- See the changes: `git diff main...feature/waitlist`

**Review checklist:**
- Does the implementation match the requirements?
- Are there any logic errors or bugs?
- What edge cases are not handled correctly?
- If you find an issue, explain:
  - Where the bug is (file and line number)
  - What the code currently does
  - What it should do instead
  - How this would impact users

**Testing the feature:**
To test the waitlist branch:
```bash
git checkout feature/waitlist
source venv/bin/activate
python seed.py  # Reset database with new seed data
python app.py
```

The Database Design event (event #3) should now be completely full. Try joining the waitlist and testing the functionality.

## Tips

- Use `git diff` to see exactly what changed
- Read the PR description - does the implementation deliver what's promised?
- Trace the data flow: button click → fetch() → Flask route → database → response → UI update
- Think about what happens in different scenarios (event full, multiple waitlisted users, etc.)
- Don't just look for syntax errors - look for logic errors

## What We're Evaluating

- **Code comprehension:** Can you trace data flow through an unfamiliar codebase?
- **Critical thinking:** Can you identify gaps between requirements and implementation?
- **Communication:** Can you clearly explain technical issues?
- **Attention to detail:** Do you notice subtle logic errors?

Good luck!
