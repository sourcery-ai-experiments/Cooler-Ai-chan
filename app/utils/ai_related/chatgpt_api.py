from openai import OpenAI
from app.utils.logger import logger
client = OpenAI()
from dotenv import load_dotenv

load_dotenv() # load openai api key from .env file

def send_to_openai(messages):
    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, temperature=0.6)
    answer = completion.choices[0].message.content
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    total_tokens = completion.usage.total_tokens
    logger.info(f"Prompt tokens: {prompt_tokens}")
    logger.info(f"Completion tokens: {completion_tokens}")
    logger.info(f"Total tokens: {total_tokens}")
    logger.info(f"Response: {answer}")
    return answer, prompt_tokens, completion_tokens, total_tokens

def send_to_openai_vision(question, image_url):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }
        ],
    )
    answer = completion.choices[0].message.content
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    total_tokens = completion.usage.total_tokens
    logger.info(f"Prompt tokens: {prompt_tokens}")
    logger.info(f"Completion tokens: {completion_tokens}")
    logger.info(f"Total tokens: {total_tokens}")
    logger.info(f"Response: {answer}")
    return answer, prompt_tokens, completion_tokens, total_tokens