from telebot import types


def start_keyboard():
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_picture = types.InlineKeyboardButton(text='Нейрокартины', callback_data='picture')
    key_codewealth = types.InlineKeyboardButton(text='Код богатства', callback_data='codewealth')
    keyboard.add(key_picture, key_codewealth)  # добавляем кнопку в клавиатуру
    key_masterclass = types.InlineKeyboardButton(text='Запись на мастер-класс', callback_data='masterclass')
    key_affermacia = types.InlineKeyboardButton(text='Создать аффирмацию', callback_data='affermacia')
    keyboard.add(key_masterclass, key_affermacia)
    return keyboard

def affirmacia_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    key_forest = types.InlineKeyboardButton(text='Волна', callback_data='volna')
    key_bird = types.InlineKeyboardButton(text='Гармония', callback_data='garmonia')
    key_sea = types.InlineKeyboardButton(text='Релакс', callback_data='relax')
    keyboard.add(key_forest, key_bird, key_sea)
    return keyboard

def contact_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True) #Подключаем клавиатуру
    button_phone = types.KeyboardButton(text="Отправить телефон", request_contact=True) #Указываем название кнопки, которая появится у пользователя
    keyboard.add(button_phone) #Добавляем эту кнопку
    return keyboard