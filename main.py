import requests
import time

# Токен доступа к Telegram Bot API
TOKEN = '7601054207:AAGP-L-4dLtdEz8s5WbU6dRi73ePf8gd_8E'
# URL для обращения к API Telegram Bot
URL = 'https://api.telegram.org/bot'

# Функция для получения обновлений от Telegram сервера
def get_updates(offset=0):
    # Запрос обновлений с параметром offset
    result = requests.get(f'{URL}{TOKEN}/getUpdates?offset={offset}').json()
    # Возвращаем результат в виде списка обновлений
    return result['result']

# Функция для отправки сообщения пользователю
def send_message(chat_id, text):
    # Отправляем сообщение по указанному chat_id
    requests.get(f'{URL}{TOKEN}/sendMessage?chat_id={chat_id}&text={text}')

# Функция для проверки сообщения и отправки ответа
def check_message(chat_id, message):
    # Перебираем слова в сообщении
    for mes in message.lower().replace(',', '').split():
        # Проверяем на приветствия и отправляем ответ
        if mes in ['привет', 'здравствуйте', 'хай', 'hello', 'hi', 'приветствую']:
            send_message(chat_id, 'Привет :)')
        # Проверяем на запрос о состоянии дел и отправляем ответ
        if mes in ['как дела?', 'как ты?', 'дела?']:
            send_message(chat_id, 'Спасибо, хорошо!')

# Основная функция для запуска бота
def run():
    # Получаем ID последнего сообщения
    update_id = get_updates()[-1]['update_id']
    while True:
        # Задержка перед следующим запросом обновлений
        time.sleep(2)
        # Получаем новые обновления
        messages = get_updates(update_id)
        for message in messages:
            # Проверяем, есть ли новые сообщения
            if update_id < message['update_id']:
                # Обновляем ID последнего сообщения
                update_id = message['update_id']
                # Проверяем и обрабатываем новое сообщение
                check_message(message['message']['chat']['id'], message['message']['text'])

# Точка входа в программу
if __name__ == '__main__':
    run()
