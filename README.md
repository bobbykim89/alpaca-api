# ALPACA-API

A Django REST Framework (DRF) based API for career guidance questionnaires and recommendations.

## Overview

ALPACA-API provides an intelligent questionnaire system that helps users discover career paths and educational programs through a series of adaptive questions. The API generates contextual follow-up questions and provides personalized career recommendations based on user responses.

## Base URLs

- **Questionnaire**: `/api/ai/questionnaire/`
- **Program Recommendations**: `/api/ai/recommendation/`

## Endpoints

### GET /api/ai/questionnaire/

Retrieves the first question of the questionnaire to begin the career assessment process.

#### Response

Returns a JSON object containing the initial question with the following structure:

```json
{
  "id": 1,
  "question": "What type of program are you most interested in right now?",
  "options": [
    "Bachelor's degree",
    "Graduate degree (e.g., Master's or PhD)",
    "Certificate or short-term credential",
    "I'm just exploring for now"
  ],
  "multiple_answers": false
}
```

#### Response Fields

- `id` (integer): Unique identifier for the question
- `question` (string): The question text presented to the user
- `options` (array): List of available answer options
- `multiple_answers` (boolean): Indicates whether multiple options can be selected

#### Example Request

```bash
curl -X GET https://alpaca-api.vercel.app/api/ai/questionnaire/
```

### POST /api/ai/questionnaire/

Submits previous question responses and receives the next question. After the 10th answer, returns comprehensive career recommendations based on the complete assessment.

#### Request Body

Send a JSON object containing all previous questions and corresponding user answers:

```json
{
  "questions": [
    {
      "id": 1,
      "question": "What type of program are you most interested in right now?",
      "options": [
        "Bachelor's degree",
        "Graduate degree (e.g., Master's or PhD)",
        "Certificate or short-term credential",
        "I'm just exploring for now"
      ],
      "multiple_answers": false
    }
  ],
  "answers": [
    {
      "id": 1,
      "question": "What type of program are you most interested in right now?",
      "selections": ["Graduate degree (e.g., Master's or PhD)"]
    }
  ]
}
```

#### Request Fields

- `questions` (array): List of all questions presented so far
  - `id` (integer): Question identifier
  - `question` (string): The question text
  - `options` (array): Available answer options
  - `multiple_answers` (boolean): Whether multiple answers were allowed
- `answers` (array): List of user responses to questions
  - `id` (integer): Question identifier
  - `question` (string): The question text
  - `selections` (array): User's selected answer(s)

#### Response

**For questions 1-10**: Returns the next question in the same format as the GET request.

**After 10th answer**: Returns career recommendations:

```json
{
  "message": "Submission received",
  "data": {
    "career_recommendations": [
      "Data Scientist",
      "Software Engineer",
      "Research Scientist",
      "Systems Analyst",
      "Technical Project Manager",
      "Machine Learning Engineer",
      "Cybersecurity Analyst",
      "DevOps Engineer",
      "UX/UI Designer"
    ],
    "reasoning": "Based on your interests in Technology and Science, along with your skills in analytical thinking and technical abilities, careers in data science, software development, and research are well-suited to help you advance in your field while making a positive impact."
  }
}
```

#### Example Request

```bash
curl -X POST http://your-domain.com/api/ai/questionnaire/ \
  -H "Content-Type: application/json" \
  -d '{
    "questions": [
      {
        "id": 1,
        "question": "What type of program are you most interested in right now?",
        "options": [
          "Bachelor'\''s degree",
          "Graduate degree (e.g., Master'\''s or PhD)",
          "Certificate or short-term credential",
          "I'\''m just exploring for now"
        ],
        "multiple_answers": false
      }
    ],
    "answers": [
      {
        "id": 1,
        "question": "What type of program are you most interested in right now?",
        "selections": ["Graduate degree (e.g., Master'\''s or PhD)"]
      }
    ]
  }'
```

### POST /api/ai/recommendation/

Generates personalized ASU Online program recommendations based on a selected career and user's questionnaire responses. Returns up to 3 relevant program recommendations with detailed reasoning.

#### Request Body

Send a JSON object containing the user's answers and selected career:

```json
{
  "answers": [
    {
      "id": 1,
      "question": "What type of program are you most interested in right now?",
      "selections": ["Graduate degree (e.g., Master's or PhD)"]
    }
  ],
  "selected_career": "Software Engineer"
}
```

#### Request Fields

- `answers` (array): List of user responses from the questionnaire
  - `id` (integer): Question identifier
  - `question` (string): The question text
  - `selections` (array): User's selected answer(s)
- `selected_career` (string): Career chosen from the recommendations

#### Response

Returns up to 3 ranked ASU Online program recommendations:

```json
{
  "message": "Submission received",
  "data": [
    {
      "rank": 1,
      "degree_name": "Online Master of Science in Engineering Science – Software Engineering",
      "reasoning": "This degree aligns perfectly with your interest in software development and enhances your programming skills, preparing you for leadership roles in the field.",
      "url": "<degree program url>"
    },
    {
      "rank": 2,
      "degree_name": "Online Master of Science in Information Technology (IT)",
      "reasoning": "This degree will equip you with a broad range of IT skills, making it ideal for advancing your career in technology and software engineering.",
      "url": "<degree program url>"
    },
    {
      "rank": 3,
      "degree_name": "Online Master of Computer Science – Big Data Systems",
      "reasoning": "This program focuses on big data and analytics, which complements your analytical thinking skills and interests in innovative technology solutions.",
      "url": "<degree program url>"
    }
  ]
}
```

#### Response Fields

- `message` (string): Status message
- `data` (array): List of program recommendations
  - `rank` (integer): Recommendation ranking (1-3)
  - `degree_name` (string): Full name of the ASU Online program
  - `reasoning` (string): Explanation for why this program matches the user's profile
  - `url` (string): Direct link to the program page

#### Example Request

```bash
curl -X POST http://your-domain.com/api/ai/recommendation/ \
  -H "Content-Type: application/json" \
  -d '{
    "answers": [
      {
        "id": 1,
        "question": "What type of program are you most interested in right now?",
        "selections": ["Graduate degree (e.g., Master'\''s or PhD)"]
      }
    ],
    "selected_career": "Software Engineer"
  }'
```

### POST /api/ai/questionnaire/

Submits previous question responses and receives the next question. After the 10th answer, returns comprehensive career recommendations based on the complete assessment.

#### Request Body

Send a JSON object containing all previous questions and corresponding user answers:

```json
{
  "questions": [
    {
      "id": 1,
      "question": "What type of program are you most interested in right now?",
      "options": [
        "Bachelor's degree",
        "Graduate degree (e.g., Master's or PhD)",
        "Certificate or short-term credential",
        "I'm just exploring for now"
      ],
      "multiple_answers": false
    }
  ],
  "answers": [
    {
      "id": 1,
      "question": "What type of program are you most interested in right now?",
      "selections": ["Graduate degree (e.g., Master's or PhD)"]
    }
  ]
}
```

#### Request Fields

- `questions` (array): List of all questions presented so far
  - `id` (integer): Question identifier
  - `question` (string): The question text
  - `options` (array): Available answer options
  - `multiple_answers` (boolean): Whether multiple answers were allowed
- `answers` (array): List of user responses to questions
  - `id` (integer): Question identifier
  - `question` (string): The question text
  - `selections` (array): User's selected answer(s)

#### Response

**For questions 1-9**: Returns the next question in the same format as the GET request.

**After 10th answer**: Returns career recommendations:

```json
{
  "message": "Submission received",
  "data": {
    "career_recommendations": [
      "Data Scientist",
      "Software Engineer",
      "Research Scientist",
      "Systems Analyst",
      "Technical Project Manager",
      "Machine Learning Engineer",
      "Cybersecurity Analyst",
      "DevOps Engineer",
      "UX/UI Designer"
    ],
    "reasoning": "Based on your interests in Technology and Science, along with your skills in analytical thinking and technical abilities, careers in data science, software development, and research are well-suited to help you advance in your field while making a positive impact."
  }
}
```

#### Example Request

```bash
curl -X POST http://your-domain.com/api/ai/questionnaire/ \
  -H "Content-Type: application/json" \
  -d '{
    "questions": [
      {
        "id": 1,
        "question": "What type of program are you most interested in right now?",
        "options": [
          "Bachelor'\''s degree",
          "Graduate degree (e.g., Master'\''s or PhD)",
          "Certificate or short-term credential",
          "I'\''m just exploring for now"
        ],
        "multiple_answers": false
      }
    ],
    "answers": [
      {
        "id": 1,
        "question": "What type of program are you most interested in right now?",
        "selections": ["Graduate degree (e.g., Master'\''s or PhD)"]
      }
    ]
  }'
```

## Technology Stack

- **Framework**: Django 5.2.4
- **API Framework**: Django REST Framework 3.16.0
- **Language**: Python 3.8+
- **AI Integration**: OpenAI 1.93.0
- **Vector Database**: Qdrant Client 1.14.3
- **Database**: PostgreSQL (via psycopg 3.2.9)

## Dependencies

```
annotated-types==0.7.0
anyio==4.9.0
asgiref==3.9.0
certifi==2025.6.15
charset-normalizer==3.4.2
distro==1.9.0
dj-database-url==3.0.1
Django==5.2.4
djangorestframework==3.16.0
grpcio==1.73.1
h11==0.16.0
h2==4.2.0
hpack==4.1.0
httpcore==1.0.9
httpx==0.28.1
hyperframe==6.1.0
idna==3.10
jiter==0.10.0
numpy==2.3.1
openai==1.93.0
portalocker==2.10.1
protobuf==6.31.1
psycopg==3.2.9
psycopg-binary==3.2.9
pydantic==2.11.7
pydantic_core==2.33.2
python-dotenv==1.1.1
qdrant-client==1.14.3
requests==2.32.4
sniffio==1.3.1
sqlparse==0.5.3
tqdm==4.67.1
typing-inspection==0.4.1
typing_extensions==4.14.0
urllib3==2.5.0
whitenoise==6.9.0
```

## Getting Started

### Prerequisites

- Python 3.8+
- Django 4.0+
- Django REST Framework

### Installation

1. Clone the repository
```bash
git clone https://github.com/bobbykim89/alpaca-api.git
cd alpaca-api
```

2. Install dependencies
```bash
python -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
```

3. Run migrations
```bash
python manage.py migrate
```

4. Start the development server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/ai/questionnaire/`

## Usage Flow

### Complete Assessment Process

1. **Start Assessment**: Make a GET request to `/api/ai/questionnaire/` to retrieve the first question
2. **Continue Assessment**: Make POST requests to `/api/ai/questionnaire/` with accumulated questions and answers
3. **Complete Assessment**: After the 10th answer, receive career recommendations
4. **Get Program Recommendations**: Use POST `/api/ai/recommendation/` with selected career to get ASU Online program suggestions

### Adaptive Intelligence

- **Dynamic Questions**: Each question is generated based on previous responses
- **AI-Powered Matching**: Uses OpenAI for intelligent career matching
- **Vector Search**: Leverages Qdrant for semantic program recommendations
- **Personalized Results**: Tailored recommendations based on individual profiles

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful request
- `400 Bad Request`: Invalid request format or missing required fields
- `404 Not Found`: Endpoint not found
- `500 Internal Server Error`: Server-side error

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.