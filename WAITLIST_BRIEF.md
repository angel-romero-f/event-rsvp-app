# Product Brief: Event Waitlist

**Author:** Product Team
**Status:** In Development

## Problem

When an event reaches capacity, users currently see a disabled "Event Full" button with no way to express interest. They have to keep checking back manually to see if a spot opens up. This leads to frustration and lower engagement.

## Goal

Allow users to join a waitlist when an event is full, so they can automatically get a spot if someone cancels.

## Requirements

### Joining the waitlist
- When a user tries to RSVP to an event that is at capacity, they should be added to a waitlist instead of being rejected
- The UI should clearly indicate that they are joining a waitlist, not getting a confirmed spot
- Users should be able to see their position in the waitlist (e.g. "You are #3 on the waitlist")

### Automatic promotion
- When a confirmed attendee cancels their RSVP, the next person on the waitlist should automatically be promoted to confirmed status
- Promotion should be fair: first person to join the waitlist gets promoted first (FIFO)

### Leaving the waitlist
- Users should be able to voluntarily leave the waitlist if they're no longer interested

### Visibility
- The event detail page should show how many people are on the waitlist
- The event listing page behavior does not need to change — events at capacity should still show as "Full"

## Out of Scope

- Email notifications when promoted from waitlist
- Expiring waitlist spots (e.g. "confirm within 24 hours")
- Waitlist caps
