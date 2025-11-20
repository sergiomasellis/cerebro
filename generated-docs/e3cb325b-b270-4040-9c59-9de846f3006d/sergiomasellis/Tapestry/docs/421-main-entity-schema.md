# Main Entity Schema

| Repo    | Doc Type           | Date                | Branch |
|---------|--------------------|---------------------|--------|
| Tapestry| Main Entity Schema | 2025-08-04 19:08    | main   |

This document describes the main data entities for the Tapestry backend, as defined in the SQLAlchemy models (`[backend/app/models/models.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/models/models.py)`) and Pydantic schemas (`[backend/app/schemas/schemas.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/schemas/schemas.py)`). These entities form the core of the application's domain: users, families, calendars, events, chores, points, and goals.

## Overview

Tapestry is a family-oriented calendar and chore management system. The backend models represent:

- **Users**: Individual accounts, each belonging to a family.
- **Families**: Groups of users.
- **Calendars**: Collections of events, can be shared within a family.
- **Events**: Calendar events (appointments, reminders, etc.).
- **Chores**: Tasks assigned to users, with completion tracking and point rewards.
- **Points**: Earned by users for completing chores.
- **Goals**: Rewards or milestones users can work toward by accumulating points.

## Entity-Relationship Diagram

```mermaid
erDiagram
    FAMILY ||--o{ USER : has
    FAMILY ||--o{ CALENDAR : owns
    USER ||--o{ CHORE : assigned
    USER ||--o{ POINT : earns
    USER ||--o{ GOAL : sets
    CALENDAR ||--o{ EVENT : contains
    CHORE ||--o{ POINT : rewards
    FAMILY ||--o{ GOAL : offers

    FAMILY {
        int id PK
        string name
        datetime created_at
    }
    USER {
        int id PK
        string email
        string name
        string role
        int family_id FK
        datetime created_at
        bool is_active
        string hashed_password
    }
    CALENDAR {
        int id PK
        string name
        int family_id FK
        string provider
        string external_id
        datetime created_at
    }
    EVENT {
        int id PK
        int calendar_id FK
        string title
        string description
        datetime start_time
        datetime end_time
        string location
        string color
        bool all_day
        string recurrence
        datetime created_at
    }
    CHORE {
        int id PK
        string title
        string description
        int assigned_to FK (USER)
        int family_id FK
        int points
        string status
        datetime due_date
        datetime completed_at
        datetime created_at
    }
    POINT {
        int id PK
        int user_id FK
        int chore_id FK
        int amount
        datetime awarded_at
    }
    GOAL {
        int id PK
        int user_id FK
        int family_id FK
        string title
        string description
        int target_points
        bool achieved
        datetime created_at
        datetime achieved_at
    }
```

## Entity Details

### Family

- **id**: Primary key
- **name**: Family/group name
- **created_at**: Timestamp

### User

- **id**: Primary key
- **email**: Unique email address
- **name**: Display name
- **role**: Enum (e.g., parent, child, admin)
- **family_id**: Foreign key to Family
- **created_at**: Timestamp
- **is_active**: Boolean
- **hashed_password**: Credential storage

### Calendar

- **id**: Primary key
- **name**: Calendar name
- **family_id**: Foreign key to Family
- **provider**: (optional) e.g., Google, iCal, Alexa
- **external_id**: (optional) Provider-specific ID
- **created_at**: Timestamp

### Event

- **id**: Primary key
- **calendar_id**: Foreign key to Calendar
- **title**: Event title
- **description**: Event details
- **start_time**: Datetime
- **end_time**: Datetime
- **location**: (optional)
- **color**: (optional)
- **all_day**: Boolean
- **recurrence**: (optional) Recurrence rule
- **created_at**: Timestamp

### Chore

- **id**: Primary key
- **title**: Chore name
- **description**: Details
- **assigned_to**: Foreign key to User
- **family_id**: Foreign key to Family
- **points**: Points awarded on completion
- **status**: Enum (e.g., pending, completed)
- **due_date**: Datetime
- **completed_at**: Datetime
- **created_at**: Timestamp

### Point

- **id**: Primary key
- **user_id**: Foreign key to User
- **chore_id**: Foreign key to Chore
- **amount**: Points awarded
- **awarded_at**: Timestamp

### Goal

- **id**: Primary key
- **user_id**: Foreign key to User
- **family_id**: Foreign key to Family
- **title**: Goal title
- **description**: Details
- **target_points**: Points required to achieve
- **achieved**: Boolean
- **created_at**: Timestamp
- **achieved_at**: Datetime

## Notes

- All entities have `created_at` timestamps for auditability.
- Relationships are designed to support multi-user, multi-calendar, and multi-chore scenarios within a family context.
- Points and goals are directly tied to user engagement and gamification.

---

## Primary Sources

- [backend/app/models/models.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/models/models.py) (Last modified: 2025-08-04 19:08)
- [backend/app/schemas/schemas.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/schemas/schemas.py) (Last modified: 2025-08-04 19:08)
- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)
- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) (Last modified: 2025-08-04 19:08)