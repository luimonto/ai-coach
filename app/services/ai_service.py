import json
from datetime import date
from pathlib import Path

from openai import OpenAI

from app.core.config import get_settings
from app.schemas.coach import TrainingSchedule
from app.schemas.coach import AthleteContext


class AIService:

    def __init__(self, client: OpenAI):
        self.client = client
        self.settings = get_settings()

        prompt_path = (
            Path(__file__).resolve().parent.parent
            / "prompts"
            / "ai_coach_system.txt"
        )

        self.system_prompt = prompt_path.read_text(
            encoding="utf-8"
        )

    def generate_schedule(self, user_goal: str, athlete_context: AthleteContext) -> TrainingSchedule:

        date_context = (
            f"Today's date is {date.today().isoformat()}. "
            f"Schedule relative to this date."
        )

        athlete_context_json = athlete_context.model_dump_json(exclude_none=False)

        user_prompt = f"""
            ATHLETE CONTEXT:
            {athlete_context_json}

            ATHLETE REQUEST:
            {user_goal}

            Today's date is {date.today().isoformat()}.
            Schedule relative to this date.
        """

        response = self.client.chat.completions.create(
            model=self.settings.model,
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt,
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

        raw_output = response.choices[0].message.content

        if not raw_output:
            raise ValueError("Empty response from AI model.")

        ai_response_data = json.loads(raw_output)

        if (
            isinstance(ai_response_data, dict)
            and ai_response_data.get("error") == "unsupported_topic"
        ):
            raise ValueError("unsupported_topic")

        return TrainingSchedule.model_validate(ai_response_data)