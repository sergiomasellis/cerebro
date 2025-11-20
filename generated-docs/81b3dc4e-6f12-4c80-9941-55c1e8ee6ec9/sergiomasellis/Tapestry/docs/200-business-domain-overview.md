# Domain & Business Rules

| Repo    | Doc Type                | Date                | Branch |
|---------|------------------------|---------------------|--------|
| Tapestry | Domain & Business Rules | 2025-08-04 19:08    | main   |

---

## Overview

Tapestry is a family-oriented calendar and task management application. Its domain model centers on families, users, chores, points, goals, and events. The following outlines the core business rules, entity relationships, and domain flows that govern the application's behavior.

---

## Core Domain Entities

### 1. Family

- **Definition:** A group of users (typically a household) sharing a calendar, chores, and point system.
- **Business Rules:**
  - Each user belongs to one or more families.
  - Families can invite new members via email or code.
  - Family membership determines access to shared data (events, chores, points, goals).

### 2. User

- **Definition:** An individual account, typically a parent or child.
- **Business Rules:**
  - Users authenticate via username/password (with optional admin/master password).
  - Each user has a role (e.g., parent, child) that may affect permissions.
  - Users can view and interact with family data according to their role.

### 3. Chore

- **Definition:** A recurring or one-off task assigned to a user or unassigned within a family.
- **Business Rules:**
  - Chores can be created, updated, deleted, or marked as complete.
  - Chores may be generated automatically via AI (LangGraph pipeline).
  - Completion of a chore awards points to the assigned user.
  - Chores can have due dates, recurrence, and descriptions.

### 4. Points

- **Definition:** A gamified scoring system to incentivize task completion.
- **Business Rules:**
  - Points are awarded upon chore completion.
  - Points are tracked per user within a family context.
  - Points contribute to a family leaderboard.

### 5. Goal

- **Definition:** A reward or milestone that users can work toward by accumulating points.
- **Business Rules:**
  - Goals are created by parents (or admins) and visible to all family members.
  - Goals have a point threshold and a description (e.g., "Movie Night: 100 points").
  - When a user reaches a goal, it is marked as achieved, and the user may receive a prize.

### 6. Event

- **Definition:** Calendar entries for appointments, reminders, or family activities.
- **Business Rules:**
  - Events are visible to all family members.
  - Events can be created, updated, or deleted by authorized users.
  - Events may be imported from external calendars (iCal, Google, Alexa).

---

## Domain Flows

### Family Creation & Membership

1. **Create Family:** A user (parent) creates a new family group.
2. **Invite Members:** The family owner invites other users via email or code.
3. **Join Family:** Invited users accept and join the family, gaining access to shared data.

### Chore Lifecycle

1. **Chore Creation:** Parent or AI pipeline creates a chore, optionally assigning it to a user.
2. **Assignment:** Chores can be reassigned among family members.
3. **Completion:** Assigned user marks the chore as complete.
4. **Point Award:** System awards points to the user for completion.
5. **Leaderboard Update:** Family leaderboard reflects updated point totals.

### Goal Progression

1. **Goal Setup:** Parent defines a goal with a point threshold.
2. **Point Accumulation:** Users earn points by completing chores.
3. **Goal Achievement:** When a user reaches the threshold, the goal is marked as achieved for that user.
4. **Reward:** Parent may grant the associated prize.

### Event Management

1. **Event Creation:** Any family member (with permission) adds an event to the shared calendar.
2. **Event Sync:** External calendars can be linked and synchronized.
3. **Event Notification:** Users receive reminders for upcoming events.

---

## Permissions & Roles

- **Parent/Admin:** Can manage families, invite members, create/assign chores, set goals, and manage events.
- **Child/Member:** Can view family data, complete chores, view points/goals, and add/view events (with possible restrictions).

---

## AI-Driven Chore Generation

- The backend integrates an AI pipeline (LangGraph) to suggest or auto-generate chores based on family routines and history.
- AI-generated chores follow the same lifecycle as manually created chores.

---

## Invariants & Constraints

- A user cannot earn points for chores they did not complete.
- Points cannot be manually edited; they are only awarded via chore completion.
- Each event, chore, and goal is scoped to a family.
- Deleting a family removes all associated data (events, chores, points, goals).

---

## Primary Sources

- [[README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md)](./[README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md)) (Last modified: 2025-08-04 19:08)
- [[backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md)](./[backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md)) (Last modified: 2025-08-04 19:08)
- [[backend/app/models/models.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/models/models.py)](./[backend/app/models/models.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/models/models.py)) (see file for latest modification date)
- [[backend/app/schemas/schemas.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/schemas/schemas.py)](./[backend/app/schemas/schemas.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/schemas/schemas.py)) (see file for latest modification date)
