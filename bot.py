import telebot
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
import keyboards
import main
import googleSheets

bot = telebot.TeleBot('6490398143:AAH33JclTur7nlX4dxwtycOFADRjY2x5FyM')
user = {"volume": 0, "back": 'None'}


# обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
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
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


# обработка записонного голосового сообщения
@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open(f'media/{message.chat.id}new_file.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)
    main.convert_ogg_to_mp3(f'media/{message.chat.id}new_file.ogg', f'media/{message.chat.id}new_file.mp3')
    main.affirmacia(user["volume"], message.chat.id, user["back"])
    audio = open(rf'media/{message.chat.id}аффирмация.mp3', 'rb')
    bot.send_audio(message.chat.id, audio)
    audio.close()


# обработка отправленного контакта
@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:  # Если присланный объект <strong>contact</strong> не равен нулю
        bot.register_next_step_handler(message, googleSheets.update_phone(message))


# обработка нажатия кнопки КОД БОГАТСТВА
@bot.callback_query_handler(func=lambda call: call.data == "codewealth")
def callback_code(call):
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


# ПОЛУЧИТЬ АФФИРМАЦИЮ
@bot.callback_query_handler(func=lambda call: call.data == "affermacia")
def callback_affirmacia(call):
    keyboard = keyboards.affirmacia_keyboard()
    bot.send_message(call.message.chat.id,
                     text='Запишите свою персональную аффирмацию и каждое утро начинаете с установки, которая '
                          'направлена на реализацию вашего желания.'
                        '\n'
                        '\n'
                        'Для записи аффирмации вам потребуется:\n'
                        '— Сформировать ваше желание в настоящем времени, как будто оно уже осуществилось.'
                        ' Желания должно касаться только вас.\n'
                        '— Исключить в формулировках отрицание (частицу «не»), сконцентрироваться на положительном.\n'
                        '— Поставить реалистичную дату реализации. Описать то, что вы чувствуете от реализации желания'
                        'и описать это как можно детальней.'
                        '\n'
                        '\n'
                        'Например: «Я купила 3-комнатную квартиру с панорамными окнами площадью 100 кв.м.'
                        ' в городе Барнауле в прекрасном районе. Вместе с парковочным местом. Осенью 2024 года.'
                        ' У меня дизайнерский ремонт, стильная просторная гардеробная, в моей спальне личная'
                        ' просторная ванная комната. Я счастлива в этой квартире со своей семьей»',
                     reply_markup=keyboard)


# выбор мелодии волна
@bot.callback_query_handler(func=lambda call: call.data == "volna")
def callback_audio(call):
    bot.send_message(chat_id=call.message.chat.id, text='Идет загрузка выбранной мелодии...⏳')
    bot.send_audio(chat_id=call.message.chat.id, audio=open('media/волна.mp3', 'rb'))
    user["back"] = 'волна'
    msg = bot.send_message(chat_id=call.message.chat.id, text='Укажите уровень громкости фона (от -20 до 20)')
    bot.register_next_step_handler(msg, test_msg)


# выбор мелодии гарминия
@bot.callback_query_handler(func=lambda call: call.data == "garmonia")
def callback_audio(call):
    bot.send_message(chat_id=call.message.chat.id, text='Идет загрузка выбранной мелодии...⏳')
    bot.send_audio(chat_id=call.message.chat.id, audio=open('media/гармония.mp3', 'rb'))
    user["back"] = 'гармония'
    msg = bot.send_message(chat_id=call.message.chat.id, text='Укажите уровень громкости фона (от -20 до 20)')
    bot.register_next_step_handler(msg, test_msg)


# выбор мелодии релах
@bot.callback_query_handler(func=lambda call: call.data == "relax")
def callback_audio(call):
    bot.send_message(chat_id=call.message.chat.id, text='Идет загрузка выбранной мелодии...⏳')
    bot.send_audio(chat_id=call.message.chat.id, audio=open('media/релакс.mp3', 'rb'))
    user["back"] = 'релакс'
    msg = bot.send_message(chat_id=call.message.chat.id, text='Укажите уровень громкости фона (от -20 до 20)')
    bot.register_next_step_handler(msg, test_msg)


# проверка на корректность введенного уровня горомкости мелодии
def test_msg(msg):
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
    bot.send_message(call.message.chat.id,
                     text='Совсем скоро вы сможете заказать картины по номерам *Акварели для цели* '
                          'с популярного маркетплэйса Wildberries. Во время рисования, вы погружаетесь в гармоничное '
                          'и восприимчивое состояние для достижения ваших целей. Мозг отсеивает ненужную информацию и '
                          'сосредотачивается на важном.'
                          '\n'
                          '\n'
                          'Узнать о наличии первыми можно заполнив анкету предзаказа.',
                     parse_mode="Markdown")
    msg = bot.send_message(call.message.chat.id, text='Укажите ваши имя и фамилию')
    bot.register_next_step_handler(msg, get_contact)


# получение и запись контакта введенного вручную
def get_contact(message):
    googleSheets.append_name(message.chat.id, message.text)
    keyboard = keyboards.contact_keyboard()
    msg = bot.send_message(message.chat.id, text='Укажите ваш номер телефона', reply_markup=keyboard)
    bot.register_next_step_handler(msg, googleSheets.update_phone)


# обработка нажатия клавиши МАСТЕР-КЛАСС
@bot.callback_query_handler(func=lambda call: call.data == "masterclass")
def callback_picture(call):
    bot.send_message(call.message.chat.id,
                     text='Оставьте свои контактные данные для связи',
                     parse_mode="Markdown")
    msg = bot.send_message(call.message.chat.id, text='Укажите ваши имя и фамилию')
    bot.register_next_step_handler(msg, get_contact)

if __name__ == '__main__':
    # bot.polling()
    while True:
        try:
            bot.polling()
        except:
            continue
