import logging
import os
import random

import redis
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater)

from logs_handler import configure_handler
from quiz_content_handler import get_quiz_content, get_answer

logger = logging.getLogger('tg_bot')
NEW_QUESTION, CHECK_ANSWER = range(2)
QUIZ_CONTENT = get_quiz_content()


def start(update, context: CallbackContext):
    custom_keyboard = [['Новый вопрос', 'Выход']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    update.message.reply_text(
        'Добрый день! Я - бот для проведения викторин. Чтобы начать, нажмите "Новый вопрос"'
        'для завершения нажмите "Выхода"',
        reply_markup=reply_markup
    )
    return NEW_QUESTION


def cancel(update, context: CallbackContext):
    update.message.reply_text('До свидания!', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def error(update, context: CallbackContext):
    logger.exception('Бот "%s" поймал ошибку "%s"', update, context.error)


def handle_new_question_request(update, context: CallbackContext):
    chat_id = update.message.chat_id
    question = random.choice(list(QUIZ_CONTENT.keys()))
    redcon.set(chat_id, question)
    custom_keyboard = [['Сдаться', 'Мой счёт', 'Выход']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    update.message.reply_text(
        question,
        reply_markup=reply_markup
    )
    return CHECK_ANSWER


def handle_solution_attempt(update, context: CallbackContext):
    chat_id = update.message.chat_id
    question = redcon.get(chat_id).decode('utf8')
    correct_answer = get_answer(question, QUIZ_CONTENT).lower()
    user_message = update.message.text
    user_message = user_message.replace('.', '').lower()
    if user_message in correct_answer:
        custom_keyboard = [['Новый вопрос', 'Мой счёт', 'Выход']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
        update.message.reply_text(
            'Поздравляю! Это правильный ответ! Чтобы продолжить, выберите "Новый вопрос"',
            reply_markup=reply_markup
        )
        return NEW_QUESTION
    else:
        custom_keyboard = [['Сдаться', 'Выход']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
        update.message.reply_text(
            'Неправильно, попробуйте снова',
            reply_markup=reply_markup
        )
        return CHECK_ANSWER


def handle_correct_answer(update, context: CallbackContext):
    chat_id = update.message.chat_id
    question = redcon.get(chat_id).decode('utf8')
    correct_answer = get_answer(question, QUIZ_CONTENT)
    custom_keyboard = [['Новый вопрос', 'Мой счёт', 'Выход']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    update.message.reply_text(
        f'Правильный ответ: {correct_answer}',
        reply_markup=reply_markup
    )
    return NEW_QUESTION


if __name__ == '__main__':
    load_dotenv()

    redcon = redis.Redis(
        host=os.getenv('REDIS_HOST'),
        port=os.getenv('REDIS_PORT'),
        password=os.getenv('REDIS_PASS'),
        db=0)

    configure_handler(logger, os.getenv('TG_SERVICE_BOT'), os.getenv('TG_CHAT_ID'))

    logger.info('tg_bot запущен!')
    updater = Updater(os.getenv('TG_DIALOG_BOT'))
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NEW_QUESTION: [
                MessageHandler(Filters.regex('Новый вопрос'), handle_new_question_request),
                MessageHandler(Filters.regex('Сдаться'), handle_correct_answer),
                MessageHandler(Filters.regex('Выход'), cancel)
            ],
            CHECK_ANSWER: [
                MessageHandler(Filters.regex('Новый вопрос'), handle_new_question_request),
                MessageHandler(Filters.regex('Сдаться'), handle_correct_answer),
                MessageHandler(Filters.regex('Выход'), cancel),
                MessageHandler(Filters.text, handle_solution_attempt)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()
