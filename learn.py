import telebot
from telebot import types
from geopy.geocoders import Nominatim
from models import *
import unicodedata

TOKEN = '168743027:AAEnNqtlAGIQ8zG-Rb8BaKs8k0G8Cxky1rY'
geolocator = Nominatim()
bot = telebot.TeleBot(TOKEN)

pizza_list = []
pizza_text_list = []

def getPizzaMarkUp():
    markup = types.ReplyKeyboardMarkup(selective=False,row_width=3)
    markup.one_time_keyboard = True
    markup.resize_keyboard = True
    for t in pizza_text_list:
        markup.add(types.KeyboardButton(t))
    return markup

pizzas = session.query(Pizza)
for p in pizzas:
    pizza = {"name":p.name,"image_url":p.image_url,"id":p.id}
    pizza_list.append(pizza)
    pizza_text_list.append(p.name)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # name = message.first_name + message.last_name

    global_name = message.from_user.first_name + " " + message.from_user.last_name

    row = session.query(User).filter_by(id=int(message.from_user.id))
    print row.count()
    if row.count() > 0:
            bot.reply_to(message,"Welcome " + message.from_user.first_name + " " + message.from_user.last_name + " how may I help you ?")
    else:
        u = User(int(message.from_user.id),message.from_user.first_name+" "+message.from_user.last_name,None,None,None,None)
        session.add(u)
        session.flush()
        markup = types.ReplyKeyboardMarkup(selective=True)
        markup.one_time_keyboard = True
        markup.resize_keyboard = True
        location_btn = types.KeyboardButton('Send Location',request_location=True)
        markup.row(location_btn)
        bot.reply_to(message,"Can we have your geo location ?",reply_markup=markup)
# @bot.message_handler(func=lambda m: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)

user_id = 0
global_name = "anonymous"
global_pizza = "cheese pizza"

@bot.message_handler(commands=["order"])
def order_when_command(message):
   bot.reply_to(message,"Please select your Pizza",reply_markup=getPizzaMarkUp())

@bot.message_handler(func = lambda message:message.text in pizza_text_list)
def send_image_and_confirmation(message):
    cid = message.chat.id
    text = message.text
    index = pizza_text_list.index(text)
    pizza = pizza_list[index]
    bot.send_photo(cid, open(pizza["image_url"], 'rb'))
    markup = types.ReplyKeyboardMarkup(selective=False,row_width=3)
    markup.one_time_keyboard = True
    markup.resize_keyboard = True
    yes_btn = types.KeyboardButton("Confirm")
    no_btn = types.KeyboardButton("Cancel")
    markup.add(yes_btn,no_btn)
    user = session.query(User).filter_by(id=int(message.from_user.id)).first()
    bot.reply_to(message,"Good choice you want the " + pizza["name"] + "\n shall I have this delivered to " + user.location,reply_markup=markup)

@bot.message_handler(func = lambda message:message.text.lower() in ["confirm","cancel"])
def finish(message):
    if message.text.lower() == "confirm":
        user = session.query(User).filter_by(id=int(message.from_user.id)).first().id
        text = message.text
        index = pizza_text_list.index(global_pizza)
        pizza = pizza_list[index]["id"]
        order = Orders(None,user,pizza,None)
        session.add(order)
        session.flush()
        bot.reply_to(message,"Thank you sir your pizza will be delivered within 30 mins.")
    else:
        # import pdb;pdb.set_trace()
        bot.reply_to(message,"No problem " + message.from_user.first_name + " " + message.from_user.last_name + " we have cancelled your order. Would you like to order something else ?",reply_markup=getPizzaMarkUp())

@bot.message_handler(regexp="keyboard")
def keyboard(message):
    print "send keyboard"
    markup = types.ReplyKeyboardMarkup(selective=False)
    markup.one_time_keyboard = True
    markup.resize_keyboard = True
    itembtn2 = types.KeyboardButton('Contact Number',request_contact=True)
    itembtn3 = types.KeyboardButton('Location',request_location=True)
    markup.add(itembtn2, itembtn3)
    bot.reply_to(message, "Choose one letter:", reply_markup=markup)


@bot.message_handler(regexp="message")
def geolocation(location):
    print type(location)
    print location
    bot.reply_to(location,"thanks")

@bot.message_handler(content_types=["contact"])
def reciveContact(message):
    print message.contact.phone_number
    print message.contact.first_name
    print message.contact.last_name
    user = session.query(User).filter_by(id=int(message.from_user.id)).first()
    user.contact_number = message.contact.phone_number
    session.begin()
    session.commit()
    bot.reply_to(message,"Thanks " + message.from_user.first_name + " " + message.from_user.last_name + "\n would you like to have a Pizza ?",reply_markup=getPizzaMarkUp())

@bot.message_handler(func = lambda message:message.text.lower() in ["i want pizza","can i have pizza ?","can i have pizza","pizza","order pizza","pizza","pizza list"])
def order(message):
    print "order now"
    markup = getPizzaMarkUp()
    bot.reply_to(message,"Please select your Pizza ?",reply_markup=markup)

@bot.message_handler(content_types=["location"])
def reciveLocation(message):
        import pdb;pdb.set_trace()
        user = session.query(User).filter_by(id=int(message.from_user.id)).first()
        if user.location == "Earth" or user.location == None:
            location_data = message.location
            location_decode = geolocator.reverse(str(location_data.latitude)+","+str(location_data.longitude))
            user.location = location_decode.address.encode('ascii','ignore')
            user.latitude = float(location_data.latitude)
            user.longitude = float(location_data.longitude)
            session.begin()
            session.commit()
            bot.reply_to(message,"Thanks "+message.from_user.first_name + " " + message.from_user.last_name+" your location \""+str(user.location) + "\" has been added successfully")
            markup = types.ReplyKeyboardMarkup(selective=False)
            markup.one_time_keyboard = True
            markup.resize_keyboard = True
            itembtn2 = types.KeyboardButton('Send Contact Number',request_contact=True)
            markup.add(itembtn2)
            bot.reply_to(message, "Can we have your contact number too ?", reply_markup=markup)

try:
    print "started"
    bot.polling()
except:
    print "error"
    print "started"
    bot.polling()
