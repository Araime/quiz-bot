import os
import re


def get_quiz_content(folder):
    directory = f'{os.getcwd()}/{folder}'
    files_sheet = sorted(os.listdir(directory))
    files_content = []
    quiz_content = {}

    for quiz_file in files_sheet:
        if quiz_file.endswith('.txt'):
            with open(f'{directory}/{quiz_file}', 'r', encoding='UTF-8') as file:
                files_content.extend(file.read().split('\n\n'))

    for part in files_content:
        if 'Вопрос' in part:
            question_content = re.split(':', part, maxsplit=1)
            question = question_content[1].replace('\n', ' ')
        if 'Ответ' in part:
            answer_content = re.split(':', part, maxsplit=1)
            answer = answer_content[1].replace('\n', ' ')
            quiz_content[question] = answer
    return quiz_content


def get_answer(question, quiz_content):
    answer = quiz_content[question]
    answer = answer.replace('.', ' ').replace('"', '').split('(')[0]
    return answer
