import json
from dotenv import load_dotenv
import os
from openai import OpenAI
from qdrant_client import QdrantClient, models
from pathlib import Path
import requests

load_dotenv()


class DegreeRecommendation:
    openai_client = OpenAI
    qd_client = QdrantClient
    prompt_path = Path
    jina_url = str
    jina_api_key = str

    def __init__(self):
        self.openai_client = OpenAI()
        qd_api_key = os.getenv("QDRANT_API_KEY")
        qd_url = os.getenv("QDRANT_URL")
        self.qd_client = QdrantClient(
            url=qd_url,
            api_key=qd_api_key
        )
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent
        self.prompt_path = project_root / "lib" / "assets" / "prompts"
        self.jina_api_key = os.getenv("JINA_API_KEY")
        self.jina_url = "https://api.jina.ai/v1/embeddings"

    def get_jina_embedding(self, text):
        headers = {
            "Authorization": f"Bearer {self.jina_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "jina-embeddings-v2-small-en",
            "input": [text]
        }
        response = requests.post(
            self.jina_url,
            headers=headers,
            json=data,
            timeout=30
        )
        if response.status_code == 200:
            result = response.json()
            return result["data"][0]["embedding"]
        else:
            raise Exception(
                f"Jina API error: {response.status_code} - {response.text}")

    def llm(self, user_prompt, system_prompt, model="gpt-4o-mini", temperature=0.5):
        """ llm function to call openAI with our specific prompts"""
        response = self.openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content

    def load_prompts(self) -> tuple[str, str]:
        """load the txt files with the user|system prompts """
        degrees_user_prompt_path = self.prompt_path / "degrees_user_prompt.txt"
        degrees_system_prompt_path = self.prompt_path / "degrees_system_prompt.txt"
        with open(degrees_user_prompt_path, "r") as f:
            user_prompt = f.read()
        with open(degrees_system_prompt_path, "r") as f:
            system_prompt = f.read()
        return user_prompt, system_prompt

    def generate_user_profile(self, quiz_answers) -> str:
        """ based on the json bit with the quiz answers, concatenate all into a string """
        user_profile = []
        for answer in quiz_answers:
            user_profile.append(answer["question"] +
                                " " + ", ".join(answer["selections"]))
        return "; ".join(user_profile)

    def search(self, selected_career: str, user_profile: str, limit: int = 1, collection_name="degree-information", model_handle="jinaai/jina-embeddings-v2-small-en"):
        """ This function is for searching amongst all the careers listed per degree"""
        # results = self.qd_client.query_points(
        #     collection_name=collection_name,
        #     prefetch=[
        #         models.Prefetch(
        #             query=models.Document(
        #                 text=selected_career, model=model_handle),
        #             using="career_vector",
        #             limit=20,
        #         ),
        #         models.Prefetch(
        #             query=models.Document(
        #                 text=user_profile, model=model_handle),
        #             using="description_vector",
        #             limit=20,
        #         ),
        #     ],
        #     query=models.FusionQuery(fusion=models.Fusion.RRF),
        #     limit=limit,
        #     with_payload=True
        # )
        career_vector = self.get_jina_embedding(selected_career)
        profile_vector = self.get_jina_embedding(user_profile)
        results = self.qd_client.query_points(
            collection_name=collection_name,
            prefetch=[
                models.Prefetch(query=career_vector,
                                using='career_vector', limit=20),
                models.Prefetch(query=profile_vector,
                                using='description_vector', limit=20)
            ],
            query=models.FusionQuery(fusion=models.Fusion.RRF),
            limit=limit,
            with_payload=True
        )

        return results

    def format_hits_response(self, hits):
        """Format the results into text to plug into chatGPT"""
        recommended_degrees_data = []
        for hit in hits.points:
            degree_data = {}
            degree_data["degree_title"] = hit.payload['degreeTitle']
            degree_data["careers"] = hit.payload['careers']
            degree_data["degree_description"] = hit.payload['shortDescription']
            recommended_degrees_data.append(degree_data)

        return json.dumps(recommended_degrees_data, indent=2)

    def format_prompt(self, career: str, career_quiz: str, degrees) -> tuple[str, str]:
        raw_user_prompt, syetem_prompt = self.load_prompts()
        user_prompt = raw_user_prompt.format(
            career_selection=career, career_quiz=career_quiz, degrees_data=degrees)

        return user_prompt, syetem_prompt

    def recommend_degree_program(self, selected_career: str, quiz_answers: list) -> tuple[list, str]:

        # generate user profile
        user_profile = self.generate_user_profile(quiz_answers=quiz_answers)

        # get top 5 hits for degrees
        hits = self.search(selected_career=selected_career,
                           user_profile=user_profile, limit=5)

        # format data
        recommended_degrees = self.format_hits_response(hits=hits)

        user_prompt, system_prompt = self.format_prompt(
            career=selected_career, career_quiz=user_profile, degrees=recommended_degrees)

        raw_response = self.llm(
            user_prompt=user_prompt, system_prompt=system_prompt)
        response = json.loads(raw_response)

        return response, user_profile
