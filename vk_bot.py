import logging
import os
import random

import redis
import vk_api as vk
from dotenv import load_dotenv
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType

from logs_handler import configure_handler
from quiz_content_handler import get_quiz_content, get_answer

logger = logging.getLogger('vk_bot')


def start(event, vk_api):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Закончить', color=VkKeyboardColor.PRIMARY)

    vk_api.messages.send(
        user_id=event.user_id,
        message='Добрый день! Я - бот для проведения викторин. Чтобы начать, нажмите "Новый вопрос",'
                'для выхода нажмите "Закончить"',
        random_id=random.randint(1, 1000),
        keyboard=keyboard.get_keyboard()
    )


def cancel(event, vk_api):
    keyboard = VkKeyboard(one_time=True)

    vk_api.messages.send(
        user_id=event.user_id,
        message='До свидания!',
        random_id=random.randint(1, 1000),
        keyboard=keyboard.get_empty_keyboard()
    )


def handle_new_question_request(event, vk_api, redcon, quiz_content):
    user_id = event.user_id
    message = random.choice(list(quiz_content.keys()))
    redcon.set(user_id, message)

    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button('Мой счёт', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Закончить', color=VkKeyboardColor.PRIMARY)

    vk_api.messages.send(
        user_id=user_id,
        message=message,
        random_id=random.randint(1, 1000),
        keyboard=keyboard.get_keyboard()
    )


def handle_solution_attempt(event, vk_api, redcon, quiz_content):
    user_id = event.user_id
    question = redcon.get(user_id).decode('utf8')
    correct_answer = get_answer(question, quiz_content).lower()
    user_message = event.text
    user_message = user_message.replace('.', '').lower()
    if user_message in correct_answer:
        message = 'Поздравляю! Это правильный ответ! Чтобы продолжить, выберите "Новый вопрос"'
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Мой счёт', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Закончить', color=VkKeyboardColor.PRIMARY)
    else:
        message = 'Неправильно, попробуйте снова'
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_button('Закончить', color=VkKeyboardColor.PRIMARY)

    vk_api.messages.send(
        user_id=user_id,
        message=message,
        random_id=random.randint(1, 1000),
        keyboard=keyboard.get_keyboard()
    )


def handle_correct_answer(event, vk_api, redcon, quiz_content):
    user_id = event.user_id
    question = redcon.get(user_id).decode('utf8')
    correct_answer = get_answer(question, quiz_content)

    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Мой счёт', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Закончить', color=VkKeyboardColor.PRIMARY)

    vk_api.messages.send(
        user_id=user_id,
        message=f'Правильный ответ: {correct_answer}',
        random_id=random.randint(1, 1000),
        keyboard=keyboard.get_keyboard()
    )


if __name__ == '__main__':
    load_dotenv()

    quiz_content = get_quiz_content(os.getenv('FOLDER'))

    redcon = redis.Redis(
        host=os.getenv('REDIS_HOST'),
        port=os.getenv('REDIS_PORT'),
        password=os.getenv('REDIS_PASS'),
        db=0)

    configure_handler(logger, os.getenv('TG_SERVICE_BOT'), os.getenv('TG_CHAT_ID'))

    logger.info('vk_bot запущен!')
    vk_session = vk.VkApi(token=os.getenv('VK_GROUP_TOKEN'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            # noinspection PyBroadException
            try:
                if event.text == 'Начать':
                    start(event, vk_api)
                elif event.text == 'Новый вопрос':
                    handle_new_question_request(event, vk_api, redcon, quiz_content)
                elif event.text == 'Сдаться':
                    handle_correct_answer(event, vk_api, redcon, quiz_content)
                elif event.text == 'Мой счёт':
                    pass
                elif event.text == 'Закончить':
                    cancel(event, vk_api)
                else:
                    handle_solution_attempt(event, vk_api, redcon, quiz_content)
            except Exception:
                logger.exception('vk_bot поймал ошибку: ')
