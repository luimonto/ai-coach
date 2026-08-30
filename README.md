                    ┌──────────────────────┐
                    │       FastAPI        │
                    │   Coach Endpoints    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    WorkoutService    │
                    │  Orchestration layer │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼──────────────────┐
             ▼                 ▼                  ▼
      ┌─────────────┐  ┌──────────────┐  ┌──────────────┐
      │ PostgreSQL  │  │    Garmin    │  │  AIService   │
      │             │  │              │  │              │
      │ User        │  │ Activities   │  │ Planner      │
      │ TrainingPlan│  │ Workouts     │  │ Detailer     │
      │ Weeks       │  │ Completed    │  │              │
      │ Feedback    │  │ Scheduled    │  │              │
      └─────────────┘  └──────────────┘  └──────────────┘


                         ┌──────────────┐
                         │    User      │
                         └──────┬───────┘
                                │
                         "Prepare me for
                          a triathlon"
                                │
                                ▼
                     ┌─────────────────────┐
                     │    Coach API        │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │   WorkoutService    │
                     └──────────┬──────────┘
                                │
                  ┌─────────────┼──────────────┐
                  ▼             ▼              ▼
             PostgreSQL      Garmin         AIService
                  │             │              │
                  │             │        ┌─────┴─────┐
                  │             │        ▼           ▼
                  │             │    Planner      Detailer
                  │             │
                  ▼             ▼
             Plan State      Actual Data
                  │
                  └──────────────┐
                                 ▼
                         Coaching Decision
                                 │
                                 ▼
                         Next Workout/Week