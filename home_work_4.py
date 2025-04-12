import telebot

token = ""

bot = telebot.TeleBot(token)
dimas_name = "Dima"

@bot.message_handler(content_types=["text"])
def echo(message):
    if dimas_name.lower() in message.text.lower():
        bot.send_message(message.chat.id, "Ба! Знакомые все лица!")
    else:
        bot.send_message(message.chat.id, message.text)

bot.polling(none_stop=True)
