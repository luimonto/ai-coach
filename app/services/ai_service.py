import json
from datetime import date
from pathlib import Path

from openai import OpenAI

from app.core.config import get_settings
from app.schemas.coach import AthleteContext
from app.schemas.training_plan import (
    TrainingPlanSchema,
    WeeklyPlan,
    WorkoutDetail
)

class AIService:

    def __init__(self, client: OpenAI):

        self.client = client
        self.settings = get_settings()

        prompt_path = (
            Path(__file__).resolve().parent.parent
            / "prompts"
        )

        self.planner_prompt = (
            prompt_path
            / "ai_coach_planner.txt"
        ).read_text(encoding="utf-8")

        self.detailer_prompt = (
            prompt_path
            / "ai_workout_detailer.txt"
        ).read_text(encoding="utf-8")

    def _get_raw_response(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> dict:

        response = self.client.chat.completions.create(
            model=self.settings.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0.1,
            response_format={
                "type": "json_object"
            },
        )

        message = response.choices[0].message

        content = message.content

        print("========== LLM DEBUG ==========")
        print("CONTENT:", repr(content))
        print(
            "REASONING:",
            repr(
                getattr(
                    message,
                    "reasoning",
                    None,
                )
            ),
        )
        print(
            "REFUSAL:",
            repr(
                getattr(
                    message,
                    "refusal",
                    None,
                )
            ),
        )
        print("================================")

        if not content:
            raise ValueError(
                "LLM returned no content"
            )

        try:
            return json.loads(content)

        except json.JSONDecodeError as exc:

            raise ValueError(
                "LLM returned invalid JSON. "
                f"length={len(content)} "
                f"position={exc.pos} "
                f"line={exc.lineno} "
                f"column={exc.colno} "
                f"error={exc.msg}"
            ) from exc

    def generate_training_roadmap(
        self,
        user_goal: str,
        athlete_context: AthleteContext,
    ) -> TrainingPlanSchema:

        today = date.today().isoformat()

        athlete_context_json = (
            athlete_context.model_dump_json(
                exclude_none=False
            )
        )

        user_prompt = f"""
        ATHLETE CONTEXT:
        {athlete_context_json}
        ATHLETE REQUEST:
        {user_goal}
        TODAY:
        {today}
        Create the high-level training roadmap.
        Do NOT create individual workouts.
        Do NOT provide exercises.
        Do NOT provide sets or repetitions.
        Focus only on weekly progression.
        """

        data = self._get_raw_response(
            self.planner_prompt,
            user_prompt,
        )

        return TrainingPlanSchema.model_validate(
            data
        )

    def expand_workout_details(
        self,
        roadmap_week: WeeklyPlan,
        athlete_context: AthleteContext,
    ) -> WorkoutDetail:

        athlete_context_json = (
            athlete_context.model_dump_json(
                exclude_none=False
            )
        )

        roadmap_json = (
            roadmap_week.model_dump_json()
        )

        user_prompt = f"""
        ATHLETE CONTEXT:
        {athlete_context_json}

        SELECTED ROADMAP WEEK:
        {roadmap_json}

        Generate ONE representative workout
        for this training phase.

        The workout must be consistent with:

        - athlete fitness
        - athlete goals
        - recent training
        - the selected week's objective
        - the selected week's focus
        - the selected week's intensity

        Return ONLY the WorkoutDetail JSON object.
        """

        data = self._get_raw_response(
            self.detailer_prompt,
            user_prompt,
        )

        return WorkoutDetail.model_validate(data)