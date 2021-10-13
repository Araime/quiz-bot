# Чат-бот для проведения викторин в Telegram и Вконтакте.

Для работы скрипт открывает файл с вопросами, которые потом задаёт пользователю.
Скрипт состоит из нескольких частей: бот для общения в Telegram, бот для общения
в группе во Вконтакте, обработка логов, загрузка словаря с вопросами и ответами.
Бот используют базу данных [Redis](https://redis.com/), сохраняет id пользователя
и заданный ему вопрос, благодаря чему бот помнит, какой вопрос задавал какому 
пользователю. В проект входят: дополнительный telegram-бот для получения 
сообщений об ошибках, отдельный скрипт для загрузки вопросов и ответов. Для 
удобства добавлена клавиатура, которая динамически меняет кнопки, в зависимости 
от этапа диалога.

![vk-bot](vk-quiz.gif)|![tg-bot](tg-quiz.gif)
---------------------|---------------------

[Пример чат-бота telegram](https://t.me/Sheru_support_bot).

## Как установить

### Скачать 

Python3 должен быть уже установлен.
[Скачать](https://github.com/Araime/support-bot/archive/master.zip) этот репозиторий себе на компьютер.

Рекомендуется использовать [virtualenv/venv](https://docs.python.org/3/library/venv.html)
для изоляции проекта.

#### Быстрая настройка venv

Начиная с Python версии 3.3 виртуальное окружение идёт в комплекте в виде модуля
venv. Чтобы его установить и активировать нужно выполнить следующие действия в
командной строке:  

Указать скачанный репозиторий в качестве каталога.
```sh
cd C:\Users\ваш_пользователь\Downloads\папка_репозитория
```
Установить виртуальное окружение в выбранном каталоге.
```sh
Python -m venv env
```
В репозитории появится папка виртуального окружения env  

<a href="https://imgbb.com/"><img src="https://i.ibb.co/Hn4C6PD/image.png" alt="image" border="0"></a>

Активировать виртуальное окружение.
```sh
env\scripts\activate
```
Если всё сделано правильно, вы увидите в командной строке (env) слева от пути 
каталога.  

<a href="https://imgbb.com/"><img src="https://i.ibb.co/MZ72r22/2.png" alt="2" border="0"></a>

#### Установить зависимости

Используйте `pip` (или `pip3`, есть конфликт с Python2) для установки 
зависимостей:

```sh
pip install -r requirements.txt
```

#### Получение токенов, ключей, создание базы данных Redis

1. Создать двух ботов для Telegram, получить их токены у [Отца Ботов](https://telegram.me/BotFather).
   Один для общения, другой для сбора логов.
2. Получить свой chat_id у  телеграм-бота [userinfobot](https://telegram.me/userinfobot).
3. Создайте группу в Vk, она будет доступна во вкладке [управление](https://vk.com/groups?tab=admin). 
   В настройках группы включите отправку сообщений, создайте ключ доступа.
   <a href="https://ibb.co/J278JbK"><img src="https://i.ibb.co/wCW8mbR/8.png" alt="8" border="0"></a>
4. Перейти в «Управление сообществом» -> «Сообщения» -> «Настройки бота» и
   включить «функции бота».  
   <a href="https://imgbb.com/"><img src="https://i.ibb.co/DMvwm6R/8.png" alt="8" border="0"></a>
5. Зарегистрироваться на [Redis](https://redis.com/). Создать новую базу
   данных(new subscription), тип базы - облачный, бесплатный 30 мегабайт. 
   Возьмите оттуда информацию: host, port, пароль от БД. (пример на фото)
   <a href="https://ibb.co/ZxxS7B5"><img src="https://i.ibb.co/sqqCzKn/agent.png" alt="agent" border="0"></a>

#### Переменные окружения

Создайте в корне репозитория файл `.env` и добавьте в него следующие строки:

```sh
TG_DIALOG_BOT=Токен_телеграм_бота
TG_SERVICE_BOT=Токен_бота_логов
TG_CHAT_ID=Чайт_ID_бота_логов
VK_GROUP_TOKEN=Токен_группы_вк
REDIS_HOST=Хост_БД_redis
REDIS_PORT=Порт_БД_redis
REDIS_PASS=Пароль_БД_redis
ENCODING=Тип_кодировки_файла
FILEPATH=Путь_к_файлу_с_вопросами_викторины
```
В папке `questions examples` лежат файлы примеров вопросов, обычный файл `sample.txt`
в кодировке `UTF-8` и 3 файла в кодировке `KOI8-R`.

Пример пути к файлу вопросов для викторины:  
```sh
FILEPATH=C:/Users/Ваш_пользователь/Downloads/Quiz bot/questions examples/baik07ch.txt
```

Пример кодировки:  
```sh
ENCODING=KOI8-R
```

### Запуск локально

Telegram-бот:
```sh
python tg_bot.py
```

Vk-бот:
```sh
python vk_bot.py
```

### Деплой и запуск на Heroku

1. Зарегистрируйтесь на Heroku и создайте приложение (app):  
   
<a href="https://ibb.co/r5mDQ2Z"><img src="https://i.ibb.co/447hFRj/Screenshot-from-2019-04-10-17-43-30.png" alt="Screenshot-from-2019-04-10-17-43-30" border="0"></a><br />  

2. Опубликуйте код репозитория на свой GitHub.  
3. Привяжите свой аккаунт на GitHub к Heroku:  

<a href="https://ibb.co/Hqy7yvP"><img src="https://i.ibb.co/zZgsgc2/123.png" alt="123" border="0"></a>

4. Задеплойте проект на Heroku:  

<a href="https://ibb.co/kgpN9tF"><img src="https://i.ibb.co/1f3Fdkx/5353.jpg" alt="5353" border="0"></a>  

5. В разделе Resources включите ботов vk и telegram:  

<a href="https://ibb.co/n3VbdLj"><img src="https://i.ibb.co/bHyPwKX/666.png" alt="666" border="0"></a>  

6. Перейдите в раздел Settings и в пункте Config Vars укажите из вашего файла .env
   TG_DIALOG_BOT, TG_SERVICE_BOT, TG_CHAT_ID, VK_GROUP_TOKEN, REDIS_HOST, REDIS_PORT,
   REDIS_PASS:  

<a href="https://ibb.co/5x70h7H"><img src="https://i.ibb.co/FqPr4PT/8.png" alt="8" border="0"></a>

7. Задеплоить повторно(пункт 4).  

Вы увидите сообщение о запуске в чате бота-логгера:  

<a href="https://imgbb.com/"><img src="https://i.ibb.co/jWbcXx0/agent.png" alt="agent" border="0"></a>

#### Создания файла с вопросами и ответами

Идеальным примером для создания файла с вопросами и ответами является `sample.txt`, 
в папке `questions examples`. По его образу, с сохранениями пробелов и отступов, 
необходимо создать свой файл и указать к нему путь и кодировку. Если файл будет 
отличаться по структуре, вам придётся переписать скрипт quiz_content_handler под 
свои нужды.

#### Работа с ботом из командной строки

Установить консольный [CLI client](https://devcenter.heroku.com/articles/heroku-cli#download-and-install).

Быстрый старт CLI:

Примечание: для Windows можно открыть командную строку cmd и работать в ней.

Подключение к Heroku:
```sh
heroku login
```
Посмотреть список своих приложений:
```sh
heroku apps
```
Посмотреть логи:
```sh
heroku logs --app=имя_приложения
```
Статус бота:
```sh
heroku ps -a имя_приложения
```

[Руководство по Heroku CLI](https://devcenter.heroku.com/articles/using-the-cli).

### Цель проекта

Код написан в учебных целях, это часть курса по созданию [чат-ботов](https://dvmn.org/modules/chat-bots/)
на сайте веб-разработчиков [Девман](https://dvmn.org/modules/).
