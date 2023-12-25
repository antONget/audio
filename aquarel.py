import telebot
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
import keyboards
import main
import googleSheets
import os
from pydub import AudioSegment
import time

# bot = telebot.TeleBot('6689173506:AAFjbmjGd124jwLQyS_XA1VVtCPLvhhgCfE') # test
bot = telebot.TeleBot('6490398143:AAH33JclTur7nlX4dxwtycOFADRjY2x5FyM')
user = {"flag_contact": False, "back": 'None', "phone": 'picture'}


# обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        googleSheets.append_name_start(message.chat.id)
        keyboard = keyboards.start_keyboard()
        bot.send_message(message.from_user.id,
                         text="Здесь вы сможете создать свою персональную аффирмацию за считанные минуты, рассчитать"
                              " и узнать как активировать ваш код богатства, а также заказать картину или записаться"
                              " на офлайн мастер-класс.",
                         reply_markup=keyboard)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Здесь вы сможете создать свою персональную аффирмацию за"
                                               " считанные минуты, рассчитать и узнать как активировать ваш код"
                                               " богатства, а также заказать картину или записаться на офлайн"
                                               " мастер-класс. ")
    elif message.text == "/admin":
        if message.chat.id in [843554518]:
            bot.send_message(chat_id=message.chat.id,
                             text='Вы являетесь администратором и вам доступен расширенный функционал бота!')
            users = googleSheets.get_all_user()
            # users = [843554518, 463672403, 5443784834]
            for i, u in enumerate(users):
                time.sleep(1)
                try:
                    bot.send_message(chat_id=u,
                                     text='На связи Мария Чечина, и я рада вам сообщить о долгожданном старте продаж'
                                          ' нейрокартин «Акварели для цели». Вы получили это сообщение, потому что проявили'
                                          ' интерес к моему уникальному продукту, не имеющему аналогов на рынке.\n\n'
                                          'Приобретая картину, вы получаете целый комплекс практик, направленных для'
                                          ' реализации ваших целей. Это самопрограммирование сознания с научнодоказанным'
                                          ' фундаментом:\n'
                                          '– Работа с телом\n'
                                          '– Медитации\n'
                                          '– Эзотерика с секретной техникой\n'
                                          '– Визуальный стимул, который будет работать с вашим сознанием.\n'
                                          'И это только часть того, что вы получаете!\n\n'
                                          'Успейте стать первым обладателем картины Акварели для цели! Выбирайте сюжет,'
                                          ' который понравился и рисуйте свой уникальный путь к личному успеху и реализации'
                                          ' целей!\n\n'
                                          'Количество картин ограничено!\n'
                                          'Для заказа переходите в раздел «Нейрокартины» или по '
                                          '<a href="https://www.wildberries.ru/catalog/195632159/detail.aspx?targetUrl=GP&size=317794367">ссылке.</a>',
                                     parse_mode='HTML')
                    bot.send_message(chat_id=843554518,
                                     text=f'{i+1}/{len(users)} - Пользователь {u} оповещен!')
                except:
                    bot.send_message(chat_id=843554518,
                                     text=f'{i+1} - Пользователь {u} не оповещен!')
        else:
            bot.send_message(chat_id=message.chat.id,
                             text='Вы не являетесь администратором и вам не доступен расширенный функционал бота!')
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


# обработка записонного голосового сообщения
@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    print("voice_processing")
    # bot.clear_step_handler(message)
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open(f'data/{message.chat.id}new_file.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)
    # link = f"<a href='https://t.me/AntonPon0marev'>технической поддержкой.</a>"
    bot.send_message(chat_id=message.chat.id, text='Немного подождите, ваша аффирмация обрабатывается...⏳\n'
                                                   'Если время ожидания составит более 1 мин, напишите в поддержку.')
    # main.affirmacia(message.chat.id, user["back"])
    main.affirmacia(message.chat.id, user["back"])
    audio = open(f"data/{message.chat.id}aff.mp3", 'rb')

    bot.send_message(843554518, text=f'аффирмация для {message.chat.id} создана')
    bot.send_audio(message.chat.id, audio)
    # bot.send_audio(843554518, audio)
    audio.close()


# обработка отправленного контакта
@bot.message_handler(content_types=['contact'])
def contact(message):
    print("contact")
    if message.contact is not None:  # Если присланный объект <strong>contact</strong> не равен нулю
        if user["phone"] == "picture":
            bot.register_next_step_handler(message, googleSheets.update_phone(message))
        else:
            bot.register_next_step_handler(message, googleSheets.update_phone_master(message))


# обработка нажатия кнопки КОД БОГАТСТВА
@bot.callback_query_handler(func=lambda call: call.data == "codewealth")
def callback_code(call):
    print("callback_code")
    bot.clear_step_handler(call.message)
    bot.send_message(call.message.chat.id,
                     text='Код на богатство (его также называют денежный или финансовый код) 💵- это пароль из цифр;'
                          ' комбинация чисел денежной удачи. Он бывает личный и универсальный. Универсальным '
                          'считается “8888” – его можно использовать каждому человеку в любой ситуации.'
                          '\n'
                          '\n'
                           'Для того, чтобы высчитать и правильно определить ваш личный код успешности,'
                          ' достаточно ввести дату рождения ниже:')
    calendar, step = DetailedTelegramCalendar(locale='ru').build()
    bot.send_message(call.message.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


# обработка выбора даты рождения
@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    print("cal")
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        code = main.codewealth(str(result))
        bot.edit_message_text(f"Ваша дата рождения {result}, Ваш код богатства {code}",
                              c.message.chat.id,
                              c.message.message_id)
        bot.send_message(c.message.chat.id,
                         text="Активацию финансового кода можно произвести любым из способов:\n"
                            "— написать число на картине для исполнения желаний;\n"
                            " — написать число на купюре крупного номинала или найти с такими же цифрами в номере, и носить с собой;\n"
                            "— записать код на бумаге и положить там, где хранятся сбережения;\n"
                            "— добавить цифры кода в пароль на аккаунты, почту или поставить на банковскую карту, телефон и др.\n"
                            "— окружить себя таким числовым сочетание: написать в ежедневнике или на другом видном тебе месте,"
                              " выбрать номер телефона с этими цифрами, указывать их при заключении договоров и др.")


# ПОЛУЧИТЬ АФФИРМАЦИЮ
@bot.callback_query_handler(func=lambda call: call.data == "affermacia")
def callback_affirmacia(call):
    print("callback_affirmacia")
    bot.clear_step_handler(call.message)
    keyboard = keyboards.affirmacia_keyboard()
    bot.send_message(call.message.chat.id,
                     text='Запишите свою персональную аффирмацию и каждое утро начинаете с положительной установки.\n\n'
                          ' — Аффирмацию сформулируйте  в настоящем времени, как будто она уже осуществилась.'
                          ' Аффирмация  должна касаться только вас.\n'
                          '— Исключите в формулировках отрицание (частицу «не»), сконцентрируйтесь на положительном.\n\n'
                          'Например:\n'
                          '«— Я излучаю радость, энергию , счастье, успех.\n'
                          ' — Я денежный магнит! Деньги беспрерывно потоком текут ко мне из разных источников».\n\n'
                          'Выберите фон для вашей аффирмации.',
                     reply_markup=keyboard)


# выбор мелодии волна
@bot.callback_query_handler(func=lambda call: call.data == "volna")
def callback_audio(call):
    print("callback_audio")
    bot.send_message(chat_id=call.message.chat.id, text='Идет загрузка выбранной мелодии...⏳')
    bot.send_audio(chat_id=call.message.chat.id, audio=open('media/волна.mp3', 'rb'))

    user["back"] = 'волна'
    # msg = bot.send_message(chat_id=call.message.chat.id, text='Укажите уровень громкости фона (от -20 до 20)')
    # bot.register_next_step_handler(msg, test_msg)
    bot.send_message(chat_id=call.message.chat.id,
                     text='Запишите и отправьте голосовое сообщение не более 1 мин. Во время записи будьте в хорошем'
                          ' расположении духа, уединитесь, чтобы исключить посторонние'
                          ' звуки. Круче всего получается под одеялом ☺️')


# выбор мелодии гарминия
@bot.callback_query_handler(func=lambda call: call.data == "garmonia")
def callback_audio(call):
    print("callback_audio")
    bot.send_message(chat_id=call.message.chat.id, text='Идет загрузка выбранной мелодии...⏳')
    bot.send_audio(chat_id=call.message.chat.id, audio=open('media/гармония.mp3', 'rb'))

    user["back"] = 'гармония'
    # msg = bot.send_message(chat_id=call.message.chat.id, text='Укажите уровень громкости фона (от -20 до 20)')
    # bot.register_next_step_handler(msg, test_msg)
    bot.send_message(chat_id=call.message.chat.id,
                     text='Запишите и отправьте голосовое сообщение не более 1 мин. Во время записи будьте в хорошем'
                          ' расположении духа, уединитесь, чтобы исключить посторонние'
                          ' звуки. Круче всего получается под одеялом ☺️')


# выбор мелодии релах
@bot.callback_query_handler(func=lambda call: call.data == "relax")
def callback_audio(call):
    print("callback_audio")
    bot.send_message(chat_id=call.message.chat.id, text='Идет загрузка выбранной мелодии...⏳')
    bot.send_audio(chat_id=call.message.chat.id, audio=open('media/релакс.mp3', 'rb'))

    user["back"] = 'релакс'
    # msg = bot.send_message(chat_id=call.message.chat.id, text='Укажите уровень громкости фона (от -20 до 20)')
    # bot.register_next_step_handler(msg, test_msg)
    bot.send_message(chat_id=call.message.chat.id,
                     text='Запишите и отправьте голосовое сообщение не более 1 мин. Во время записи будьте в хорошем'
                          ' расположении духа, уединитесь, чтобы исключить посторонние'
                          ' звуки. Круче всего получается под одеялом ☺️')

# проверка на корректность введенного уровня горомкости мелодии
def test_msg(msg):
    print("test_msg")
    try:
        print(msg.json['text'])
        user["volume"] = int(msg.json['text'])
        bot.send_message(chat_id=msg.chat.id,
                         text='Запишите и отправьте голосовое сообщение. Во время записи будьте в хорошем'
                                ' расположении духа, уединитесь, чтобы исключить посторонние'
                                ' звуки. Круче всего получается под одеялом ☺️')
    except:
        msg = bot.send_message(msg.chat.id, text='Укажите допустимое значение от -20 до 20')
        bot.register_next_step_handler(msg, test_msg)


# обработка нажатия клавиши НЕЕРОКАРТИНА
@bot.callback_query_handler(func=lambda call: call.data == "picture")
def callback_picture(call):
    print("callback_picture")
    bot.clear_step_handler(call.message)
    bot.send_message(call.message.chat.id,
                     text='Нарисуйте свой уникальный путь к успеху! Закажите картину по номерам Акварели'
                          ' для цели на <a href="https://www.wildberries.ru/catalog/195632159/detail.aspx?targetUrl=GP&size=317794367">Wildberries</a>.\n\n'
                          'Во время рисования, вы погружаетесь в гармоничное и восприимчивое состояние для'
                          ' достижения ваших целей. Мозг отсеивает ненужную информацию и сосредотачивается на'
                          ' важном.\n\n'
                          '<a href="https://www.wildberries.ru/catalog/195632159/detail.aspx?targetUrl=GP&size=317794367">ЗАКАЗАТЬ</a>\n\n'
                          'Количество картин ограничено!',
                     parse_mode="Markdown")
    # msg = bot.send_message(call.message.chat.id, text='Укажите ваши имя и фамилию')
    # user["flag_contact"] = True
    # bot.register_next_step_handler(msg, get_contact)


# получение и запись контакта введенного вручную
def get_contact(message):
    print("get_contact")
    if user["flag_contact"]:
        user["phone"] = "picture"
        googleSheets.append_name(message.chat.id, message.text)
        keyboard = keyboards.contact_keyboard()
        msg = bot.send_message(message.chat.id, text='Укажите ваш номер телефона', reply_markup=keyboard)
        bot.register_next_step_handler(msg, picture_finish)
        user["flag_contact"] = False

def get_contact_master(message):
    print("get_contact_master")
    if user["flag_contact"]:
        user["phone"] = "master"
        googleSheets.append_name_master(message.chat.id, message.text)
        keyboard = keyboards.contact_keyboard()
        msg = bot.send_message(message.chat.id, text='Укажите ваш номер телефона', reply_markup=keyboard)
        bot.register_next_step_handler(msg, master_finish)
        user["flag_contact"] = False

# обработка нажатия клавиши МАСТЕР-КЛАСС
@bot.callback_query_handler(func=lambda call: call.data == "masterclass")
def callback_picture(call):
    print("callback_picture")
    bot.clear_step_handler(call.message)
    bot.send_message(call.message.chat.id,
                     text='Расписание находится в процессе формирования. Оставьте свои контактные данные, '
                          'чтобы записаться в лист ожидания.',
                     parse_mode="Markdown")
    msg = bot.send_message(call.message.chat.id, text='Укажите ваши имя и фамилию:')
    bot.register_next_step_handler(msg, get_contact_master)

def picture_finish(message):
    print("picture_finish")
    googleSheets.update_phone(message)
    bot.send_message(message.chat.id, text='Благодарим за проявленный интерес!'
                                           ' О появлении картин вы узнаете в числе первых!')

def master_finish(message):
    print("master_finish")
    googleSheets.update_phone_master(message)
    bot.send_message(message.chat.id, text='Благодарим, вы записаны в лист ожидания.'
                                           ' Мы свяжемся с вами и сообщим о дате ближайшего мастер-класса.')

if __name__ == '__main__':
# bot.polling()
    while True:
        try:
            bot.polling()
        except:
            continue
