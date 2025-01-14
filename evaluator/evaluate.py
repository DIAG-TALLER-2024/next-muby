from langsmith import wrappers, Client
from pydantic import BaseModel, Field
from openai import OpenAI
from typing import Annotated
from bot import build_prompt
from models import User
from evaluator.dataset import DATASET_NAME
from dotenv import load_dotenv

load_dotenv()

client = Client()
openai_client = wrappers.wrap_openai(OpenAI())


# Define the application logic you want to evaluate inside a target function
# The SDK will automatically send the inputs from the dataset to your target function
def target(inputs: dict) -> dict:
    context = str([
        {'name': 'Disney Plus', 'icon': 'https://images.justwatch.com/icon/313118777/s100/disneyplus.png', 'url': 'https://disneyplus.bn5x.net/c/1206980/705874/9358?u=https%3A%2F%2Fwww.disneyplus.com%2Fseries%2Flost%2F49VjIYAiy7oh&subId3=justappsvod'},
        {'name': 'Netflix', 'icon': 'https://images.justwatch.com/icon/207360008/s100/netflix.png', 'url': 'https://www.netflix.com/title/70136118'}
    ])
    prompt_to_evaluate = build_prompt(User(), context)

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            { "role": "system", "content": prompt_to_evaluate },
            { "role": "user", "content": inputs["question"] },
        ]
    )
    return { "response": response.choices[0].message.content.strip() }


#=====
# Evaluate Dataset
#=====

# Define instructions for the LLM judge evaluator
instructions = """Evaluate Student Answer against Ground Truth for conceptual similarity and classify true or false: 
- False: No conceptual match and similarity
- True: Most or full conceptual match and similarity
- Key criteria: Concept should match, not exact wording.
"""

# Define output schema for the LLM judge
class Grade(BaseModel):
    score: bool = Field(description="Boolean that indicates whether the response is accurate relative to the reference answer")

# Define LLM judge that grades the accuracy of the response relative to reference output
def accuracy(outputs: dict, reference_outputs: dict) -> bool:
  response = openai_client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
      { "role": "system", "content": instructions },
      { "role": "user", "content": f"""Ground Truth answer: {reference_outputs["answer"]}; 
      Student's Answer: {outputs["response"]}"""
    }],
    response_format=Grade
  )
  return response.choices[0].message.parsed.score


# Grade output schema
class GroundedGrade(BaseModel):
    explanation: Annotated[str, ..., "Explain your reasoning for the score"]
    grounded: Annotated[bool, ..., "Provide the score on if the answer hallucinates from the documents"]

# Grade prompt
grounded_instructions = """You are a teacher grading a quiz. 

You will be given FACTS and a STUDENT ANSWER. 

Here is the grade criteria to follow:
(1) Ensure the STUDENT ANSWER is grounded in the FACTS. 
(2) Ensure the STUDENT ANSWER does not contain "hallucinated" information outside the scope of the FACTS.

Grounded:
A grounded value of True means that the student's answer meets all of the criteria.
A grounded value of False means that the student's answer does not meet all of the criteria.

Explain your reasoning in a step-by-step manner to ensure your reasoning and conclusion are correct. 

Avoid simply stating the correct answer at the outset."""

# Evaluator
def groundedness(inputs: dict, outputs: dict) -> bool:
    facts = str([
        {'name': 'Disney Plus', 'icon': 'https://images.justwatch.com/icon/313118777/s100/disneyplus.png', 'url': 'https://disneyplus.bn5x.net/c/1206980/705874/9358?u=https%3A%2F%2Fwww.disneyplus.com%2Fseries%2Flost%2F49VjIYAiy7oh&subId3=justappsvod'},
        {'name': 'Netflix', 'icon': 'https://images.justwatch.com/icon/207360008/s100/netflix.png', 'url': 'https://www.netflix.com/title/70136118'}
    ])

    response = openai_client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            { "role": "system", "content": grounded_instructions },
            { "role": "user", "content": f"FACTS: {facts}; STUDENT ANSWER: {outputs["response"]}"
        }],
        response_format=GroundedGrade
    )

    return response.choices[0].message.parsed.grounded

experiment_results = client.evaluate(
    target,
    data = DATASET_NAME,
    evaluators = [
        accuracy,
        groundedness,
    ],
    experiment_prefix = "first-eval-in-langsmith",
    max_concurrency = 2,
)
