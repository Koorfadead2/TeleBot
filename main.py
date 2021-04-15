import telebot
from urllib.request import Request, urlopen
import requests
import sqlite3 as sq
from telebot import types
from bs4 import BeautifulSoup
bot = telebot.TeleBot("TOKEN", parse_mode=None)
user_data = {}
connect = sq.connect('users.db', check_same_thread = False)
cursor = connect.cursor()
root = "https://www.google.ru/"
link = "https://www.google.ru/search?q=science&newwindow=1&sxsrf=ALeKk01Ngn4IWnWF8SVTFptniZpcQccjZA:1618486759300&source=lnms&tbm=nws&sa=X&ved=2ahUKEwiy5PGClYDwAhXPxIsKHXj2COsQ_AUoAnoECAEQBA&biw=1920&bih=964"
req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
def news(link):
	with requests.Session() as c:
		soup = BeautifulSoup(webpage, 'html.parser')
		for item in soup.find_all('div', attr = {'class': 'kCrYT'}):
			raw_link = item.find('a', href=True)['href']
			link = raw_link.split("/url?q=")[1].split('&sa=U&')[0]
		return link


count = [0, 0, 0, 0, 0]


@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, f'Здравствуйте, {message.from_user.first_name}. Это новостной бот. Для ознакомления с командами - /help')

@bot.message_handler(commands=['help'])
def help_msg(message):
	bot.reply_to(message, "Все доступные команды")
	bot.send_message(message.chat.id, "/start - начало диалога, /subscribe - подписаться на рассылку, /unsub - отписаться от рассылки, /news - новостные категории")

@bot.message_handler(commands=['subscribe'])
def registration(message):
	f_name = ', '.join({message.from_user.first_name})
	if not message.from_user.username:
		username = message.from_user.id
	else:
		username = '@' + ', '.join({message.from_user.username})
	chat_id = message.from_user.id
	cursor.execute('''SELECT username FROM user_id WHERE username = ?''', (username,))
	exists = cursor.fetchall()
	if not exists:
		bot.send_message(message.chat.id, "Вы подписались на рассылку")
		cursor.execute('''INSERT INTO user_id (first_name, username, chat_id) VALUES (?,?,?)''', (f_name, username, chat_id))
		connect.commit()
	else:
		bot.send_message(message.chat.id, "Вы уже подписаны")

@bot.message_handler(commands=['unsub'])
def unregistr(message):
	f_name = ', '.join({message.from_user.first_name})
	if not message.from_user.username:
		username = message.from_user.id
	else:
		username = '@' + ', '.join({message.from_user.username})
	chat_id = message.from_user.id
	cursor.execute('''SELECT username FROM user_id WHERE username = ?''', (username,))
	exists = cursor.fetchall()
	if exists:
		bot.send_message(message.chat.id, "Вы отписались")
		cursor.execute('''DELETE FROM user_id WHERE first_name = ? AND username = ? AND chat_id = ?''', (f_name, username, chat_id, ))
		connect.commit()
	else:
		bot.send_message(message.chat.id, "Вы не подписаны")

@bot.message_handler(commands=['delete'])
def delete(message):
	chat_id = message.chat.id
	cursor.execute('''SELECT username FROM user_id WHERE chat_id = ?''', (chat_id,))
	exists = cursor.fetchall()
	if exists:
		cursor.execute('''UPDATE user_id SET categ_id = NULL WHERE chat_id = ?''', (chat_id,) )
		connect.commit()
		bot.send_message(message.chat.id, "История поиска успешно удалена")
	else:
		bot.send_message(message.chat.id, "Ты кто? ПОДПИШИСЬ!")

@bot.message_handler(commands=['news'])
def send_news(message):
	cursor.execute('''SELECT title FROM categories''',)
	items = cursor.fetchall()
	markup_inline = types.InlineKeyboardMarkup()
	item_cat0 = types.InlineKeyboardButton(text=str(', '.join(items[0])), callback_data='science')
	item_cat1 = types.InlineKeyboardButton(text=str(', '.join(items[1])), callback_data='business')
	item_cat2 = types.InlineKeyboardButton(text=str(', '.join(items[2])), callback_data='cars')
	item_cat3 = types.InlineKeyboardButton(text=str(', '.join(items[3])), callback_data='family')
	item_cat4 = types.InlineKeyboardButton(text=str(', '.join(items[4])), callback_data='health')
	markup_inline.add(item_cat0, item_cat1, item_cat2, item_cat3, item_cat4)
	bot.send_message(message.chat.id, 'Выберите категорию', reply_markup=markup_inline
	)

@bot.callback_query_handler(func=lambda call: True)
def answer(call):
	chat_id = call.message.chat.id
	if call.data == 'science':
		count[0] += 1
		link = "https://www.google.ru/search?q=science&newwindow=1&sxsrf=ALeKk01Ngn4IWnWF8SVTFptniZpcQccjZA:1618486759300&source=lnms&tbm=nws&sa=X&ved=2ahUKEwiy5PGClYDwAhXPxIsKHXj2COsQ_AUoAnoECAEQBA&biw=1920&bih=964"
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
		bot.send_message(call.message.chat.id, str(news(link)))

	elif call.data == 'business':
		count[1] += 1
		link = "https://www.google.ru/search?q=business&newwindow=1&sxsrf=ALeKk01Ngn4IWnWF8SVTFptniZpcQccjZA:1618486759300&source=lnms&tbm=nws&sa=X&ved=2ahUKEwiy5PGClYDwAhXPxIsKHXj2COsQ_AUoAnoECAEQBA&biw=1920&bih=964"
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
		bot.send_message(call.message.chat.id, str(news(link)))

	elif call.data == 'cars':
		count[2] += 1
		link = "https://www.google.ru/search?q=cars&newwindow=1&sxsrf=ALeKk01Ngn4IWnWF8SVTFptniZpcQccjZA:1618486759300&source=lnms&tbm=nws&sa=X&ved=2ahUKEwiy5PGClYDwAhXPxIsKHXj2COsQ_AUoAnoECAEQBA&biw=1920&bih=964"
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
		bot.send_message(call.message.chat.id, str(news(link)))

	elif call.data == 'family':
		count[3] += 1
		link = "https://www.google.ru/search?q=family&newwindow=1&sxsrf=ALeKk01Ngn4IWnWF8SVTFptniZpcQccjZA:1618486759300&source=lnms&tbm=nws&sa=X&ved=2ahUKEwiy5PGClYDwAhXPxIsKHXj2COsQ_AUoAnoECAEQBA&biw=1920&bih=964"
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
		bot.send_message(call.message.chat.id, str(news(link)))

	elif call.data == 'health':
		count[4] += 1
		link = "https://www.google.ru/search?q=health&newwindow=1&sxsrf=ALeKk01Ngn4IWnWF8SVTFptniZpcQccjZA:1618486759300&source=lnms&tbm=nws&sa=X&ved=2ahUKEwiy5PGClYDwAhXPxIsKHXj2COsQ_AUoAnoECAEQBA&biw=1920&bih=964"
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
		bot.send_message(call.message.chat.id, str(news(link)))
	for i in range(len(count)):
		if count[i] == 3:
			cursor.execute('''UPDATE user_id SET categ_id = (SELECT categ_id FROM categories WHERE categ_id = ?) WHERE chat_id = ?''',(i+1,chat_id,))
			connect.commit()
			count[i] = 0

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	file = open('file.txt', 'a')
	file.write(message.text + " |" + "ID " + str(message.from_user.id) + '\n')
	file.close()

bot.polling()
connect.close()