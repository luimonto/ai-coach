first successfull training generation by the coach:


/plan 
{
  "duration_weeks": 12,
  "overall_objective": "Prepare for a triathlon by building aerobic capacity, swim technique, and bike power while integrating transition skills.",
  "weeks": [
    {
      "week": 1,
      "objective": "Establish baseline endurance in all three disciplines",
      "focus": [
        "Swim technique",
        "Aerobic base cycling",
        "Consistent running volume"
      ],
      "intensity": "Low"
    },
    {
      "week": 2,
      "objective": "Build aerobic foundation and swim comfort",
      "focus": [
        "Swimming endurance",
        "Steady state cycling",
        "Base running"
      ],
      "intensity": "Low"
    },
    {
      "week": 3,
      "objective": "Increase swimming distance and bike duration",
      "focus": [
        "Swim volume",
        "Cycling endurance",
        "Easy running"
      ],
      "intensity": "Low-Moderate"
    },
    {
      "week": 4,
      "objective": "Active recovery and technique refinement",
      "focus": [
        "Swimming form",
        "Recovery cycling",
        "Short easy runs"
      ],
      "intensity": "Low"
    },
    {
      "week": 5,
      "objective": "Introduce strength and power on the bike",
      "focus": [
        "Cycling intervals",
        "Swim speed work",
        "Tempo running"
      ],
      "intensity": "Moderate"
    },
    {
      "week": 6,
      "objective": "Increase aerobic capacity across all disciplines",
      "focus": [
        "Hill repeats (bike)",
        "Interval swimming",
        "Threshold running"
      ],
      "intensity": "Moderate"
    },
    {
      "week": 7,
      "objective": "Introduce transition dynamics",
      "focus": [
        "Brick workouts (Bike-to-Run)",
        "Swim endurance sets",
        "Strength maintenance"
      ],
      "intensity": "Moderate"
    },
    {
      "week": 8,
      "objective": "Build specific strength and stamina",
      "focus": [
        "Longer bike rides",
        "High-volume swim sets",
        "Tempo runs"
      ],
      "intensity": "High"
    },
    {
      "week": 9,
      "objective": "Peak volume and intensity phase",
      "focus": [
        "Max effort intervals",
        "Long endurance bricks",
        "Race pace running"
      ],
      "intensity": "High"
    },
    {
      "week": 10,
      "objective": "Specific race preparation",
      "focus": [
        "Race-pace swimming",
        "Extended bike rides",
        "Speed work"
      ],
      "intensity": "High"
    },
    {
      "week": 11,
      "objective": "Taper phase - volume reduction",
      "focus": [
        "Short high-intensity bursts",
        "Swim technique focus",
        "Maintenance runs"
      ],
      "intensity": "Moderate"
    },
    {
      "week": 12,
      "objective": "Final taper and race readiness",
      "focus": [
        "Active recovery",
        "Race pace familiarity",
        "Mental preparation"
      ],
      "intensity": "Low"
    }
  ]
}

/plan/workout
...

                 Athlete Context
                       │
                       ▼
                ┌─────────────┐
                │ AI Planner  │
                └──────┬──────┘
                       │
                 small JSON
                       │
                       ▼
              Training Plan
                       │
                       ▼
             Python scheduler
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
       Workout 1             Workout 2
             │                   │
             ▼                   ▼
        AI workout            AI workout
             │                   │
             └─────────┬─────────┘
                       ▼
               Garmin Translator
                       │
                       ▼
                    Garmin


User request
     │
     ▼
┌─────────────────────┐
│ Athlete Context      │
│ + user goal          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 1. PLANNER LLM      │
│                     │
│ "What should happen │
│ over 12 weeks?"     │
└──────────┬──────────┘
           │
           ▼
   Small JSON roadmap
   Week 1 → Foundation
   Week 2 → Foundation
   ...
   Week 12 → Taper
           │
           ▼
┌─────────────────────┐
│ Application decides │
│ which workouts need │
│ details              │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 2. DETAILER LLM     │
│                     │
│ ONE workout at a    │
│ time                 │
└──────────┬──────────┘
           │
           ▼
     WorkoutDetail
           │
           ▼
     Garmin payload