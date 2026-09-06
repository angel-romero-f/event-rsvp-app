# Mock Interview Guide - Event RSVP App

## Overview

This is a mock interview project for prospective software engineer interns. The interview evaluates the candidate's ability to understand data flow through an unfamiliar codebase and critique code they didn't write.

## Interview Structure

### Phase 1: Codebase Exploration (10-15 minutes)
The candidate explores the base application (main branch) to understand:
- How events are displayed on the listing page
- How RSVPs are created and cancelled
- How capacity enforcement works
- Data flow from frontend → backend → database → response

**Key files to explore:**
- `schema.sql` - database structure
- `app.py` - Flask backend with API endpoints
- `static/js/event.js` - event detail page logic
- `static/js/index.js` - event listing page logic

### Phase 2: Design Thinking (10-15 minutes)
Present the waitlist feature request:

> "When an event reaches capacity, users should be able to join a waitlist. When someone cancels their RSVP, the next person on the waitlist should automatically be promoted to confirmed."

Ask the candidate to explain:
- What data model changes are needed (new status in `rsvps` table)
- What API endpoints need to change (`/rsvp` behavior when full, `/cancel` promotion logic)
- What new information the frontend needs (waitlist count, user's position)
- Edge cases to consider (promotion order, what if promoted user already cancelled?)

### Phase 3: Code Review (15-20 minutes)
Direct candidate to PR #1: https://github.com/angel-romero-f/event-rsvp-app/pull/1

Ask them to review the implementation and identify any issues.

## Planted Bugs

### Bug 1: Off-by-one error in capacity check
**Location:** `app.py:126`

```python
# BUG: Should be < not <=
if confirmed_count <= event['capacity']:
```

**Impact:** Allows one extra person past capacity. If capacity is 5 and there are 5 confirmed, the 6th person will be confirmed instead of waitlisted.

**How to catch:**
- The requirement says "when event reaches capacity" but `<=` means "when event reaches or exceeds capacity"
- Testing with a capacity-5 event: after 5 people RSVP, the 6th should be waitlisted, but they'll be confirmed
- Database would show 6 confirmed RSVPs for a capacity-5 event

### Bug 2: Missing waitlist promotion
**Location:** `app.py:153-161`

```python
# BUG: No call to promote_from_waitlist()
cursor.execute('''
    UPDATE rsvps
    SET status = 'cancelled'
    WHERE user_id = ? AND event_id = ?
''', (CURRENT_USER_ID, event_id))

# Missing: promote_from_waitlist(event_id, db)
```

**Impact:** When someone cancels, their spot opens up, but no one is promoted from the waitlist. The feature request explicitly says promotion should be automatic.

**How to catch:**
- The PR description mentions "automatic promotion" but there's no code that triggers it
- The helper function `promote_from_waitlist()` exists but is never called
- Testing: Cancel an RSVP when waitlist has people → spots_remaining increases but waitlist person stays waitlisted

### Bug 3: Nondeterministic waitlist promotion
**Location:** `app.py:18-19`

```python
# BUG: Missing ORDER BY created_at
cursor.execute('''
    SELECT user_id
    FROM rsvps
    WHERE event_id = ? AND status = 'waitlisted'
    LIMIT 1
''', (event_id,))
```

**Impact:** Without `ORDER BY created_at`, the database could return any waitlisted person, not necessarily the first one who joined. This makes promotion unfair and unpredictable.

**How to catch:**
- Waitlists should be FIFO (first in, first out)
- SQLite doesn't guarantee row order without ORDER BY
- Testing with multiple waitlisted users could show inconsistent promotion order
- Code review: "How do we know which person joined the waitlist first?"

### Bug 4: Frontend doesn't handle waitlisted state
**Location:** `static/js/event.js:40-47`

```javascript
// BUG: No check for event.current_user_rsvp === 'waitlisted'
let buttonHtml = '';
if (event.current_user_rsvp === 'confirmed') {
    buttonHtml = '<button id="action-btn" class="btn btn-danger">Cancel RSVP</button>';
} else if (event.spots_remaining > 0) {
    buttonHtml = '<button id="action-btn" class="btn btn-success">RSVP</button>';
} else {
    buttonHtml = '<button id="action-btn" class="btn btn-warning">Join Waitlist</button>';
}
```

**Impact:** If a user is already on the waitlist, the button will show "Join Waitlist" again instead of "Leave Waitlist". Clicking it would re-RSVP them (setting status to waitlisted again, which is harmless but confusing).

**How to catch:**
- The backend returns `current_user_rsvp` which can be `'confirmed'`, `'cancelled'`, `'waitlisted'`, or `null`
- The frontend only checks for `'confirmed'` and `null` (implicitly)
- Testing: Join waitlist, then reload page → button still says "Join Waitlist" instead of "Leave Waitlist"
- There's a `/leave-waitlist` endpoint but no way to trigger it from the UI

## Expected Candidate Performance

### Strong Performance
- Identifies 3-4 bugs during review
- Explains the impact of each bug clearly
- Suggests how to test for the bugs
- Asks clarifying questions about requirements
- Points out the unused `promote_from_waitlist()` function
- Mentions the missing ORDER BY as a fairness/correctness issue

### Acceptable Performance
- Identifies 2 bugs
- Understands the data flow well enough to explain where the code breaks
- Can articulate what *should* happen vs what *does* happen

### Weak Performance
- Focuses only on style/formatting issues
- Can't explain the impact of bugs they find
- Doesn't connect backend bugs to user-facing behavior
- Misses the logic bugs entirely

## Setup Instructions

**Requirements:** Python 3.7+

1. Clone the repository:
```bash
git clone https://github.com/angel-romero-f/event-rsvp-app.git
cd event-rsvp-app
```

2. Run setup:
```bash
./setup.sh
```

3. Run the app:
```bash
./run.sh
```

4. Open http://localhost:5000

**Note:** The app uses only standard Flask features and Python's built-in sqlite3. The setup script creates a virtual environment to avoid any conflicts with system packages.

## Tips for Interviewers

- Don't immediately confirm or deny bug reports - ask candidates to explain their reasoning
- If stuck, ask guiding questions: "What happens when someone cancels? Walk me through the code."
- Pay attention to *how* they navigate the codebase, not just what they find
- Strong candidates will use `git diff main...feature/waitlist` to see changes
- Very strong candidates might try to actually run the code and test it
