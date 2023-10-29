import os
import openai
import telebot

print('Бот запущен!')

openai.api_key = "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"  # Ключ API от OpenAI
bot = telebot.TeleBot('1383349915:AAGc6PJhLpgVR8njl5_k1udJ6HRPQAZOJog')  # Замените на свой токен бота

if not os.path.exists("users"):
    os.mkdir("users")

# Определите путь к файлу с биографией бота
BIO_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bio.txt")

def read_bio_from_file():
    with open(BIO_FILE_PATH, 'r', encoding='utf-8') as file:
        bio = file.read()
    return bio

# Получите биографию бота из файла
BOT_BIO = read_bio_from_file()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Отвечаем на команду /start
    response_text = (
        "Приветик) Я Василиса😻\n"
        "Если тебе не скем пообщаться, то просто напиши мне... Я скучаю😿"
    )
    bot.send_message(chat_id=message.chat.id, text=response_text)

@bot.message_handler(content_types=['text'])
def msg(message):
    if f"{message.chat.id}.txt" not in os.listdir('users'):
        with open(f"users/{message.chat.id}.txt", "x") as f:
            f.write('')

    with open(f'users/{message.chat.id}.txt', 'r', encoding='utf-8') as file:
        oldmes = file.read()

    if message.text == '/clear':
        with open(f'users/{message.chat.id}.txt', 'w', encoding='utf-8') as file:
            file.write('')
        return bot.send_message(chat_id=message.chat.id, text='История сообщений очищена!')

    try:
        send_message = bot.send_message(chat_id=message.chat.id, text='Печатает...')
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=[
                {"role": "system", "content": BOT_BIO},  # Передаем биографию бота как системное сообщение
                {"role": "user", "content": oldmes},
                {"role": "user", "content": f'Предыдущие сообщения: {oldmes}; Запрос: {message.text}'}
            ],
            presence_penalty=0.6
        )

        bot.edit_message_text(
            text=completion.choices[0].message["content"],
            chat_id=message.chat.id,
            message_id=send_message.message_id
        )

        with open(f'users/{message.chat.id}.txt', 'a+', encoding='utf-8') as file:
            file.write(
                message.text.replace('\n', ' ') + '\n' + completion.choices[0].message["content"].replace('\n', ' ') + '\n'
            )

    except Exception as e:
        bot.send_message(chat_id=message.chat.id, text=e)

bot.infinity_polling()