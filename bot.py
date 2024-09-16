import random
import clickhouse_connect
import logging
import datetime
from asyncio import Queue
import environ
import os

# импорт API Telegramm
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Poll, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

# подключение к БД
#client = clickhouse_connect.get_client(host='localhost', username='root', password='password')
client = clickhouse_connect.get_client(host=os.environ.get('CL_DB_HOST')
                         , database=os.environ.get('CL_SCHEMA')
                         , user=os.environ.get('CL_USER')
                         , password=os.environ.get('CL_PASSWORD'))

# Ведение журнала логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Этапы/состояния разговора
FIRST, SECOND, THIRD, FOURTH = range(4)
# Данные обратного вызова
ONE, TWO, THREE, FOUR = range(4)


async def quizMed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Пользователь %s работает с test_obstetrics_and_gynecology_2022", update.effective_chat.username)
    # возьмем выборку
    result = client.query('SELECT * from test_obstetrics_and_gynecology_2022 order by rand() limit 1')
    # блок для определения рандомом массива
    randanswer = random.sample(range(2, 6), 4)
    # блок чтобы найти корректный ответ
    if randanswer[0] == 2:
        r = 0
    elif randanswer[1] == 2:
        r = 1
    elif randanswer[2] == 2:
        r = 2
    elif randanswer[3] == 2:
        r = 3
        # Вопрос викторины и ответы
    questions = result.result_rows[0][1][:299]
    answer = [str(result.result_rows[0][randanswer[0]])
        , str(result.result_rows[0][randanswer[1]])
        , str(result.result_rows[0][randanswer[2]])
        , str(result.result_rows[0][randanswer[3]])]
    keyboard = [
        [
            InlineKeyboardButton("Следующий", callback_data=str(FIRST)),
            InlineKeyboardButton("Закончили", callback_data=str(THIRD)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # посылаем сообщение с викториной, правильный ответ указывается
    # в `correct_option_id`, представляет собой индекс `answer`
    message = await update.effective_message.reply_poll(
        questions, answer, type=Poll.QUIZ, correct_option_id=r
        , reply_markup=reply_markup
    )


async def quizMed2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Пользователь %s работает с Anatomy_kollok7", update.effective_chat.username)
    question = client.query(r"SELECT num_q,name from Anatomy_kollok7 where what = 'q' order by rand() limit 1")
    questions = question.result_rows[0][1] #q_name 2 column
    num_q = question.result_rows[0][0]
    randanswers = client.query(r"SELECT name,correct from Anatomy_kollok7 where what = 'a' and num_q = '%i' order by rand()",{num_q})
    #print(randanswers.result_rows)
    #print(randanswers.result_rows[0][1])
    # возьмем выборку
    # блок чтобы найти корректный ответ
    r_list =''
    if randanswers.result_rows[0][1]:
        r = 0
        r_list = ' 1'
    if randanswers.result_rows[1][1]:
        r = 1
        r_list = r_list + ',2'
    if randanswers.result_rows[2][1]:
        r = 2
        r_list = r_list + ',3'
    if randanswers.result_rows[3][1]:
        r = 3
        r_list = r_list + ',4'
    if randanswers.result_rows[4][1]:
        r = 4
        r_list = r_list + ',5'
        # Вопрос викторины и ответы
    #questions = result.result_rows[0][1][:299]
    answer = [  randanswers.result_rows[0][0]
                ,randanswers.result_rows[1][0]
                ,randanswers.result_rows[2][0]
                ,randanswers.result_rows[3][0]
                ,randanswers.result_rows[4][0]
              ]
    keyboard = [
        [
            InlineKeyboardButton("Следующий", callback_data=str(FOURTH)),
            InlineKeyboardButton("Закончили", callback_data=str(THIRD)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # посылаем сообщение с викториной, правильный ответ указывается
    # в `correct_option_id`, представляет собой индекс `answer`
    message = await update.effective_message.reply_poll(
        questions, answer, type=Poll.QUIZ, correct_option_id=r
        , reply_markup=reply_markup, allows_multiple_answers=True
        , explanation='Правильные ответы'+r_list
    )


async def quizMed2_old(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    question = client.query(r"SELECT num_q,name from Anatomy_kollok7 where what = 'q' order by rand() limit 1")
    questions = question.result_rows[0][1] #q_name 2 column
    num_q = question.result_rows[0][0]
    randanswers = client.query(r"SELECT name,correct from Anatomy_kollok7 where what = 'a' and num_q = '%i' order by rand()",{num_q})
    print(randanswers.result_rows)
    print(randanswers.result_rows[0][1])
    # возьмем выборку
    # блок чтобы найти корректный ответ
    r = ''
    if randanswers.result_rows[0][1]:
        r = '1'
    if randanswers.result_rows[1][1]:
        r = r +',2'
    if randanswers.result_rows[2][1]:
        r = r +',3'
    if randanswers.result_rows[3][1]:
        r = r +',4'
    if randanswers.result_rows[4][1]:
        r = r +',5'
    print(r)
        # Вопрос викторины и ответы
    #questions = result.result_rows[0][1][:299]
    answer = [  randanswers.result_rows[0][0][:100]
                ,randanswers.result_rows[1][0][:100]
                ,randanswers.result_rows[2][0][:100]
                ,randanswers.result_rows[3][0][:100]
                ,randanswers.result_rows[4][0][:100]
              ]
    # посылаем сообщение с викториной, правильный ответ указывается
    # в `correct_option_id`, представляет собой индекс `answer`
    message = await context.bot.send_poll(update.effective_chat.id,
        questions, answer, is_anonymous=True, allows_multiple_answers=True,)
    # Save some info about the poll the bot_data for later use in receive_poll_answer
    payload = {
        message.poll.id: {
            "questions": answer,
            "message_id": message.message_id,
            "chat_id": update.effective_chat.id,
            "answers": 0,
        }
    }
    context.bot_data.update(payload)


async def quizSchool(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Пользователь %s работает с quizSchool", update.effective_chat.username)
    # возьмем выборку
    result = client.query('SELECT * from school order by rand() limit 1')
    # блок для определения рандомом массива
    randanswer = random.sample(range(2, 6), 4)
    # блок чтобы найти корректный ответ
    if randanswer[0] == 2:
        r = 0
    elif randanswer[1] == 2:
        r = 1
    elif randanswer[2] == 2:
        r = 2
    elif randanswer[3] == 2:
        r = 3
        # Вопрос викторины и ответы
    questions = 'Сколько будет ' + str(result.result_rows[0][0]) + ' умножить на ' + str(
        result.result_rows[0][1]) + ' ?'
    answer = [str(result.result_rows[0][randanswer[0]])
        , str(result.result_rows[0][randanswer[1]])
        , str(result.result_rows[0][randanswer[2]])
        , str(result.result_rows[0][randanswer[3]])]

    """Show new choice of buttons"""
    #query = update.callback_query
    #await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("Следующий", callback_data=str(SECOND)),
            InlineKeyboardButton("Закончили", callback_data=str(THIRD)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # посылаем сообщение с викториной, правильный ответ указывается
    # в `correct_option_id`, представляет собой индекс `answer`
    message=await update.effective_message.reply_poll(
        questions, answer, type=Poll.QUIZ, correct_option_id=r
        , reply_markup=reply_markup
    )


# функция обратного вызова
async def echo(update, context):
    # добавим в начало полученного сообщения строку 'ECHO: '
    text = 'Для запуска бота введите команду /start. Если вызов не выполняется, закройте предыдущие сессии командой /cancel.'
    # `update.effective_chat.id` - определяем `id` чата,
    # откуда прилетело сообщение
    await context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    """Send a message when the command /start is issued."""
    #user = update.effective_user
    user = update.message.from_user
    logger.info("Пользователь %s начал разговор", user.username)
    await update.message.reply_html(
        rf"Привет {user.mention_html()}!",
        #reply_markup=ForceReply(selective=False),

    )
    # Создаем `InlineKeyboard`, где каждая кнопка имеет
    # отображаемый текст и строку `callback_data`
    # Клавиатура - это список строк кнопок, где каждая строка,
    # в свою очередь, является списком `[[...]]`
    keyboard = [
        [InlineKeyboardButton("ВУЗ.МЕД. Анатомия Коллок 7", callback_data=str(FOURTH)), ],
        [InlineKeyboardButton("ВУЗ.МЕД. ГОСА (Вопросы 2022)", callback_data=str(FIRST)), ],
        [InlineKeyboardButton("Школа. Таблица умножения до 10", callback_data=str(SECOND)), ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # для версии 20.x необходимо использовать оператор await
    await update.message.reply_text('Пожалуйста, выберите:', reply_markup=reply_markup)
    # Сообщаем `ConversationHandler`, что сейчас находимся в состоянии `FIRST`
    return FIRST


async def buttonContMed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # запускаем ГОСА Мед тест
    await quizMed(update, context)

async def buttonContMed2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # запускаем ГОСА Мед тест
    await quizMed2(update, context)

async def buttonContSch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # запускаем школьные
    await quizSchool(update, context)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Возвращает `ConversationHandler.END`, который говорит
    `ConversationHandler` что разговор окончен"""
    logger.info("Пользователь %s закончил общение"
                , update.effective_chat.username)
    text = 'Пока 👋  Увидимся!'
    #update.effective_chat.id` - определяем `id` чата,
    # откуда прилетело сообщение
    await context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main() -> None:
    #my_queue = Queue()
    # updater = Updater('6293904097:AAHngmkhZfg-MkUCJLhXH7jGuQGNA4vcPME')
    #updater = Updater('6204220687:AAHgEjFYMkTWJRpAWSnGS7qn9Dm3HP93b4w', update_queue=my_queue)
    #dispatcher = updater.dispatcher
    #TG_TOKEN= env('TG_TOKEN')
    TG_TOKEN = os.environ.get('TG_TOKEN')
    print(TG_TOKEN)
    application = Application.builder().token(TG_TOKEN).build()

    # обработчик любой команды
    # говорим обработчику `MessageHandler`, если увидишь текстовое
    # сообщение (фильтр `Filters.text`)  и это будет не команда
    # (фильтр ~Filters.command), то вызови функцию `echo()`
    echo_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)

    # echo_handler = MessageHandler(Filters.text & (~Filters.command), quiz)
    # регистрируем обработчик `echo_handler` в экземпляре `dispatcher`
    #dispatcher.add_handler(echo_handler)
    application.add_handler(echo_handler)
    # прописываем обработчик при нажатии start
    start_command = CommandHandler("start", start)
    # dispatcher.add_handler(start_command)
    #application.add_handler(start_command)

    # Настройка обработчика разговоров с состояниями `FIRST` и `SECOND`
    # Используем параметр `pattern` для передачи `CallbackQueries` с
    # определенным шаблоном данных соответствующим обработчикам
    # ^ - означает "начало строки"
    # $ - означает "конец строки"
    # Таким образом, паттерн `^ABC$` будет ловить только 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[start_command],
        states={  # словарь состояний разговора, возвращаемых callback функциями
            FIRST: [
                CallbackQueryHandler(buttonContMed, pattern="^" + str(FIRST) + "$"),
                CallbackQueryHandler(buttonContSch, pattern="^" + str(SECOND) + "$"),
                CallbackQueryHandler(buttonContMed2, pattern="^" + str(FOURTH) + "$"),
                CallbackQueryHandler(cancel, pattern="^" + str(THIRD) + "$")
           ],
        },
        #fallbacks=[CommandHandler('start', start)],
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Добавляем `ConversationHandler` в диспетчер, который
    # будет использоваться для обработки обновлений
    # dispatcher.add_handler(conv_handler)
    application.add_handler(conv_handler)

    #application.add_handler(CommandHandler("help", help_command))


    #updater.start_polling()
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    #updater.idle()
    #application.idle()


if __name__ == "__main__":

    main()