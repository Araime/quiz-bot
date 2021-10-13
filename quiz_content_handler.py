import os
import random
import re

from dotenv import load_dotenv

load_dotenv()


def get_quiz_content():
    encoding = os.getenv('ENCODING')
    filepath = os.getenv('FILEPATH')
    quiz_content = {}

    with open(filepath, 'r', encoding=encoding) as file:
        content = file.read().split('\n\n')

    for part in content:
        if 'Вопрос' in part:
            question_content = re.split(':', part, maxsplit=1)
            question = question_content[1].replace('\n', ' ')
        if 'Ответ' in part:
            answer_content = re.split(':', part, maxsplit=1)
            answer = answer_content[1].replace('\n', ' ')
            quiz_content[question] = answer
    return quiz_content


def get_question(quiz_content):
    question = random.choice(list(quiz_content.keys()))
    return question


def get_answer(question, quiz_content):
    answer = quiz_content[question]
    answer = answer.replace('.', '').replace('"', '').split('(')[0]
    return answer
