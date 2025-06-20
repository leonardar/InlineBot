import telebot
from spellchecker import SpellChecker

# Замените 'YOUR_API_TOKEN' на ваш токен API от BotFather
API_TOKEN = '7765015743:AAFkS54j5ERLfsz8D1cqAplEU8Ogo9uwM50'

# Создаем объект бота с указанным API токеном
bot = telebot.TeleBot(API_TOKEN)

# Создаем объект SpellChecker для проверки орфографии (русский язык)
spell = SpellChecker(language='ru')

# Обработчик для команд /start и /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать в программу проверки орфографии!")

# Обработчик для всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def check_message(message):
    # Разбиваем сообщение на слова и приводим к нижнему регистру
    mes = message.text.lower().replace(',', '').split()

    # Проверяем на приветствия и отправляем ответ
    if any(word in mes for word in ['привет', 'здравствуйте', 'хай', 'hello', 'hi', 'приветствую']):
        bot.reply_to(message, 'Привет, какое слово ты хочешь проверить?')
        return
    # Проверяем на запрос о проверке орфографии
    elif any(word in mes for word in ['проверка', 'проверить']):
        bot.reply_to(message, 'Введите слово для проверки:')
        bot.register_next_step_handler(message, spell_checker_bot)
        return
    else:
        # Если сообщение не является приветствием или запросом проверки орфографии, проверяем само сообщение
        spell_checker_bot(message)

# Функция для проверки орфографии слова
def spell_checker_bot(message):
    word = message.text.lower()

    # Проверяем, есть ли слово в словаре
    if word in spell:
        bot.reply_to(message, f"Слово '{word}' написано правильно.")
    else:
        # Находим возможные исправления
        corrections = spell.candidates(word)
        bot.reply_to(message, f"Слово '{word}' написано неправильно. Возможно, вы имели в виду: {', '.join(corrections)}")

# Запускаем бота

bot.polling()