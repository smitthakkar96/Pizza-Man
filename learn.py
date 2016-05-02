import telebot
from telebot import types
from geopy.geocoders import Nominatim

TOKEN = '168743027:AAEnNqtlAGIQ8zG-Rb8BaKs8k0G8Cxky1rY'
geolocator = Nominatim()
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,"message")

# @bot.message_handler(func=lambda m: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)



@bot.message_handler(regexp="keyboard")
def keyboard(message):
    markup = types.ReplyKeyboardMarkup(selective=True)
    markup.one_time_keyboard = True
    itembtn1 = types.KeyboardButton('a')
    itembtn2 = types.KeyboardButton('v')
    itembtn3 = types.KeyboardButton('d')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.reply_to(message, "Choose one letter:", reply_markup=markup)


@bot.message_handler(regexp="message")
def geolocation(location):
    print type(location)
    print location
    bot.reply_to(location,"thanks")

@bot.message_handler(content_types=["location"])
def reciveLocation(message):
    print message
    location_data = message.location
    location_decode = geolocator.reverse(str(location_data.latitude)+","+str(location_data.longitude))
    bot.reply_to(message,str(location_decode.address))

try:
	bot.polling()
except:
	print "error"
	bot.polling()
