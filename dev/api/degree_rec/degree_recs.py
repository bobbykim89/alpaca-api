import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import os
from openai import OpenAI
from qdrant_client import QdrantClient, models

# set up connection to OpenAI
load_dotenv()
client = OpenAI()

# set up connection to qDrant
api_key = os.getenv("QDRANT_API_KEY")

qdrant_client = QdrantClient(
    url="https://1497c57a-fec5-4169-8998-262cd4f287dc.us-west-1-0.aws.cloud.qdrant.io:6333", 
    api_key=api_key,
)


# LLM + Formatting utilities
def llm(user_prompt, system_prompt, model="gpt-4o-mini", temperature=0.5):
    """ llm function to call openAI with our specific prompts"""
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
    """load the txt files with the user//system prompts """
    with open("degrees_user_prompt.txt", "r") as f:
        user_prompt = f.read()
    with open("degrees_system_prompt.txt", "r") as f:
        system_prompt = f.read()
    return user_prompt, system_prompt

def generate_user_profile(quiz_answers):
    """ based on the json bit with the quiz answers, concatenate all into a string """
    user_profile = []
    for answer in quiz_answers:
        user_profile.append(answer["question"] + " " + ", ".join(answer["selections"]))
    return "; ".join(user_profile)

def search(selected_career,user_profile, limit=1,collection_name = "degree-information",model_handle = "jinaai/jina-embeddings-v2-small-en"):
    """ This function is for searching amongst all the careers listed per degree"""
    results = qdrant_client.query_points(
        collection_name=collection_name,
        prefetch=[
            models.Prefetch(
                query=models.Document(text=selected_career,model=model_handle),
                using="career_vector",
                limit=20,
            ),
            models.Prefetch(
                query=models.Document(text=user_profile,model=model_handle),
                using="description_vector",
                limit=20,
            ),
        ],
        query=models.FusionQuery(fusion=models.Fusion.RRF),
        limit=limit,
        with_payload=True
    )

    return results

def format_hits_response(hits):
    """Format the results into text to plug into chatGPT"""
    recommended_degrees_data = []
    for hit in hits.points:
        degree_data = {}
        degree_data["degree_title"] = hit.payload['degreeTitle']
        degree_data["url"] = hit.payload['url']
        degree_data["careers"] = hit.payload['careers']
        degree_data["degree_description"] = hit.payload['shortDescription']
        recommended_degrees_data.append(degree_data)

    return json.dumps(recommended_degrees_data,indent=2)

@csrf_exempt
def career_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        # obtain user quiz answers and career selection (only 1)
        data = json.loads(request.body)
        career_selected = data.get("career_selected", "")
        quiz_answers = data.get("degree_answers", [])

        #generate user profile
        user_profile = generate_user_profile(quiz_answers)

        # get top 5 hits for degrees
        hits = search(career_selected,user_profile,limit=5)

        # format the data
        recommended_degrees = format_hits_response(hits)

        USER_PROMPT, system_prompt = load_prompts()
        user_prompt = USER_PROMPT.format(career_selection=career_selected,career_quiz=user_profile,degrees_data=recommended_degrees)

        # get chatGPT response of top 3 degree recs
        raw_response = llm(user_prompt, system_prompt)
        response = json.loads(raw_response)

        return JsonResponse(response, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
