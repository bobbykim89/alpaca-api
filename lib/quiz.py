import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import os
from openai import OpenAI
from pathlib import Path

load_dotenv()
client = OpenAI()

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
prompt_path = project_root / "lib" / "assets" / "prompts"

# LLM + Formatting utilities


def llm(user_prompt, system_prompt, model="gpt-4o-mini", temperature=0.5):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature
    )
    return response.choices[0].message.content


def load_prompts():
    user_prompt_path = prompt_path / "user_prompt.txt"
    sys_prompt_path = prompt_path / "user_prompt.txt"
    with open(user_prompt_path, "r") as f:
        user_prompt = f.read()
    with open(sys_prompt_path, "r") as f:
        system_prompt = f.read()
    return user_prompt, system_prompt


def format_prompts(user_prompt, system_prompt, career_quiz, user_response):
    qna_user_prompt = user_prompt.format(
        user_response=json.dumps(user_response, indent=2))
    qna_system_prompt = system_prompt.format(
        career_quiz=json.dumps(career_quiz, indent=2))
    return qna_user_prompt, qna_system_prompt


@csrf_exempt
def career_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
        career_quiz = data.get("career_quiz", [])
        user_response = data.get("user_response", [])

        user_prompt_template, system_prompt_template = load_prompts()
        user_prompt, system_prompt = format_prompts(
            user_prompt_template, system_prompt_template, career_quiz, user_response)

        raw_response = llm(user_prompt, system_prompt)
        response = json.loads(raw_response)

        return JsonResponse(response, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
