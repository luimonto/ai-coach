                         ┌──────────────┐
                         │    Client    │
                         └──────┬───────┘
                                │
                                │ POST /v1_router
                                ▼
                         ┌──────────────┐
                         │   FastAPI    │
                         │    Router    │
                         └──────┬───────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │   WorkoutService    │
                     └──────┬────────┬─────┘
                            │        │
                 ┌──────────┘        └───────────┐
                 ▼                               ▼
          ┌─────────────┐                ┌───────────────┐
          │ AIService   │                │ GarminService │
          └──────┬──────┘                └───────┬───────┘
                 │                               │
                 ▼                               ▼
          ┌─────────────┐                ┌───────────────┐
          │   Ollama    │                │ Garmin Connect│
          │   llama3    │                └───────────────┘
          └─────────────┘



                     FastAPI
                        │
                        ▼
                 ┌─────────────┐
                 │   main.py   │
                 └──────┬──────┘
                        │
                        ▼
                ┌───────────────┐
                │   v1/router   │
                └───────┬───────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
      /health        /workouts     /coach
                                    /schedule
          │             │             │
          ▼             ▼             ▼
       Health       Workout       AI Coach
       Service      Service       Service
                        │             │
                        ▼             ▼
                    Garmin        OpenAI
                     Client        Client