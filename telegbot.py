import telebot
import os
import asyncio
import emailFunc
from threading import Timer
from emailFunc import filenames
from emailFunc import save_all_file


bot = telebot.TeleBot('')


@bot.message_handler(commands = ['start'])
def start(message):
    global fakemess
    fakemess = message
    bot.send_message(message.chat.id, f"Для работы бота вам необходимо создать ключ для сторонних приложений "
                                      f"(информацию можно найти в гугле,"
                                      f"это не сложно).")



@bot.message_handler(commands = ['check'])
def check(message):
    save_all_file()
    bot.send_message(message.chat.id, f"найдено {len(filenames)} непрочитанных сообщений")


@bot.message_handler(commands=['send'])
def send(message):
    for i in filenames:
        with open("documents/"+i, "rb") as file:
            f = file.read()
        if i[len(i)-4:len(i)] == ".png" or i[len(i)-4:len(i)] == ".jpg" or i[len(i)-5:len(i)] == ".jpeg":
            bot.send_message(message.chat.id,"От: \n"+emailFunc.from_who+"\n"+"Тема: \n"+emailFunc.title)
            bot.send_message(message.chat.id,"Текст письма: "+"\n"+emailFunc.letter)
            bot.send_photo(message.chat.id, f)
        else:
            bot.send_message(message.chat.id, "От: " + emailFunc.from_who + "\n" + "Тема: " + emailFunc.title)
            bot.send_document(message.chat.id, f)
        os.remove("documents/"+i)
        filenames.remove(i)
    bot.send_message(message.chat.id, f"осталось {len(filenames)} непрочитанных сообщений")

from threading import Timer

def checker():
    Timer(300, checker).start()
    try:
        save_all_file()
        if len(filenames)>0:
            send(fakemess)
        else:
            print("нет новых увед")

    except NameError:
        print("нет id")
checker()

bot.polling(none_stop=True, interval=0)