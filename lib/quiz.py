import json
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
from collections import defaultdict

load_dotenv()

# LLM + Formatting utilities


class QuizClass:
    open_ai_client: OpenAI
    prompt_path: Path

    def __init__(self):
        self.open_ai_client = OpenAI()
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent
        self.prompt_path = project_root / "lib" / "assets" / "prompts"

    def _llm(self, user_prompt: str, system_prompt: str, model="gpt-4o-mini", temperature=0.5):
        response = self.open_ai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content

    def _load_prompts(self) -> tuple[str, str]:
        user_prompt_path = self.prompt_path / "user_prompt.txt"
        sys_prompt_path = self.prompt_path / "system_prompt.txt"
        with open(user_prompt_path, "r") as f:
            user_prompt = f.read()
        with open(sys_prompt_path, "r") as f:
            system_prompt = f.read()
        return user_prompt, system_prompt

    def _format_prompts(self, career_quiz, user_response) -> tuple[str, str]:
        user_prompt, system_prompt = self._load_prompts()
        context = defaultdict(str, {
            'user_response': json.dumps(user_response, indent=2),
            'career_quiz': json.dumps(career_quiz, indent=2),
        })
        qna_user_prompt = user_prompt.format_map(context)
        qna_system_prompt = system_prompt.format_map(context)

        return qna_user_prompt, qna_system_prompt

    def run_questionnaire(self, questions, answers):
        user_prompt, system_prompt = self._format_prompts(
            career_quiz=questions, user_response=answers)
        raw_responze = self._llm(
            user_prompt=user_prompt, system_prompt=system_prompt)
        response = json.loads(raw_responze)

        return response
