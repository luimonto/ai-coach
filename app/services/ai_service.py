import json
from datetime import date
from pathlib import Path

from openai import OpenAI

from app.core.config import get_settings
from app.schemas.ai_training_plan import AITrainingPlan
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

    def generate_training_plan(
        self,
        user_goal: str,
        athlete_context: AthleteContext,
    ) -> AITrainingPlan:

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

Create the training plan based on the athlete's
actual recent training history and the requested goal.
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

        message = response.choices[0].message

        raw_output = message.content

        print("========== LLM DEBUG ==========")
        print("CONTENT LENGTH:", len(raw_output or ""))
        print("CONTENT:", repr(raw_output))
        print(
            "REASONING:",
            repr(getattr(message, "reasoning", None))
        )
        print(
            "REFUSAL:",
            repr(getattr(message, "refusal", None))
        )
        print(
            "FINISH:",
            response.choices[0].finish_reason
        )
        print("================================")

        if not raw_output:
            raise ValueError(
                "LLM returned no content"
            )

        try:
            ai_response_data = json.loads(raw_output)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "LLM returned invalid JSON. "
                f"length={len(raw_output)} "
                f"position={exc.pos} "
                f"error={exc.msg}"
            ) from exc

        return AITrainingPlan.model_validate(
            ai_response_data
        )