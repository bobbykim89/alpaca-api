import json
from openai import OpenAI
from dotenv import load_dotenv


# load environment vars and connect to openAI
load_dotenv()
client = OpenAI()

# set up functions
def llm(user_prompt,system_prompt="you are a helpful assistant",model="gpt-4o-mini",temperature=0.5):
    ''' this function calls the openAI api and feeds it user/system prompts'''
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature,
        )
    return response.choices[0].message.content

def load_prompts(user_prompt_filename="user_prompt.txt",system_prompt_filename="system_prompt.txt"):
    '''read the prompts from the txt files'''
    with open(user_prompt_filename, "r") as f:
        QNA_USER_PROMPT = f.read()

    with open(system_prompt_filename, "r") as f:
        QNA_SYSTEM_PROMPT = f.read()

    return QNA_USER_PROMPT, QNA_SYSTEM_PROMPT


def load_quiz_files(quiz_filename="career_quiz.json",responses_filename="user_response.json"):
    '''load the original quiz and answer selections if needed'''
    with open(quiz_filename, "r") as f:
        career_quiz = json.load(f)

    with open(responses_filename, "r") as f:
        user_response = json.load(f)

    return career_quiz, user_response


def format_prompts(QNA_USER_PROMPT,QNA_SYSTEM_PROMPT,career_quiz=[],user_response=[]):
    '''this function formats both the user and system prompt given quizz/answer selections so far'''

    # format the quiz and the answer
    qna_user_prompt = QNA_USER_PROMPT.format(user_response=json.dumps(user_response, indent=2))
    qna_system_prompt = QNA_SYSTEM_PROMPT.format(career_quiz=json.dumps(career_quiz, indent=2))

    return qna_user_prompt, qna_system_prompt



# set up fake JSON input
data = {
    'career_quiz': [],
    'user_response': []
}

# load the prompts
QNA_USER_PROMPT, QNA_SYSTEM_PROMPT = load_prompts()

# read any input data from the system
if not (data['career_quiz'] and data['user_response']):
    # load the initial career quiz and response
    career_quiz, user_response = load_quiz_files()
else:
    career_quiz = data['career_quiz']
    user_response = data['user_response']


# format prompts and get response
qna_user_prompt, qna_system_prompt = format_prompts(QNA_USER_PROMPT,QNA_SYSTEM_PROMPT,career_quiz,user_response)
response = llm(user_prompt = qna_user_prompt,system_prompt=qna_system_prompt,model="gpt-4o-mini",temperature=0.5)

# extract new question
new_question = json.loads(response)

# pretend the user selected and answer
new_response = {
    "id": new_question['id'],
    "question": new_question['question'],
    "selections": [new_question['options'][i] for i in [0]]
}

# append to the career quiz and the user_response
career_quiz.append(new_question)
user_response.append(new_response)

# output the updated career quiz and user_response as json bits
data = {
    'career_quiz': career_quiz,
    'user_response': user_response
}