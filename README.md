# AI Coach API

The API owns coaching data and does not connect to Garmin. A mobile or web
client is responsible for reading the athlete's Garmin data and synchronizing
completed activities to the API, ideally once each night.

```text
Client / device Garmin integration
                |
                | POST /api/v1/activities/sync
                v
          PostgreSQL activity cache (latest 20)
                |
                v
         Coach plan and workout endpoints
                |
                v
             AI coaching service
```

## Activity sync

`POST /api/v1/activities/sync` accepts up to 50 normalized activities for one
athlete. The API creates the athlete record when needed, upserts records by
`external_id` plus `garmin_activity_id`, and retains the 20 most recent
activities for that athlete.

```json
{
  "external_id": "athlete-123",
  "activities": [
    {
      "garmin_activity_id": 123456789,
      "activity_name": "Morning Run",
      "sport_type_key": "running",
      "start_time": "2026-09-07T07:30:00",
      "duration_seconds": 1800,
      "distance_meters": 5000,
      "average_heart_rate": 145,
      "max_heart_rate": 166,
      "calories": 420
    }
  ]
}
```

Coach endpoints read only this local cache. No Garmin email, password, or
server-side Garmin session is required.
