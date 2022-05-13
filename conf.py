TOKEN = "5225036392:AAHUYdCMnJZ3deIJdCsnKWPFOnDR1y-Ri8M"

import mysql.connector
import telebot
import mysql.connector
from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup,KeyboardButton,ReplyKeyboardMarkup


users = {}

bot = telebot.TeleBot(TOKEN)


class Files:
    users = []
    users_info = {}
    def __init__(self):
       self.chat_id = ""
       self.fio = ""
       self.group = ""
       self.phone = ""

    def add_chat_id(self,chat_id):
        if chat_id not in Files.users:
            Files.users.append(chat_id)
            Files.users_info= {str(chat_id) : {} }
        self.chat_id = chat_id


    def add_fio(self,fio,chat_id):
        if chat_id in Files.users:
            Files.users_info[str(chat_id)].update(fio = fio)          
        return self.__dict__

    def add_group(self,group,chat_id):
        if chat_id in Files.users:
            Files.users_info[str(chat_id)].update(group = group)       
        return self.__dict__
        
    def add_phone(self,phone,chat_id):
        if chat_id in Files.users:
            Files.users_info[str(chat_id)].update(phone = phone)
        return self.__dict__
        
    def get_user(self,chat_id):
        return Files.users_info[str(chat_id)]

    def clear_user(self):
        self.chat_id = ""
        self.fio = ""
        self.phone = ""
        self.group = ""

    def __str__(self):
        return users

    def create_button(self, message):
        name = message.from_user.first_name
        abs = f'Salom {name} botga xush kelibsiz'        
        keyboard = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text="Familiya Ism", callback_data="fio")
        button2 = InlineKeyboardButton(text="Telefon",callback_data="tel")
        button3 = InlineKeyboardButton(text="Grux", callback_data="group")
        keyboard.add(button1, button2, button3)
        bot.send_message(message.chat.id, text=abs, reply_markup=keyboard)        
    
        
    def create_post(self,id):
        keyboard = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text="Post", callback_data="post")
        button2 = InlineKeyboardButton(text="My posts", callback_data = 'watch')
        keyboard.add(button1, button2)
        bot.send_message(id, text="Yangi Postni qo'shish\Postlarni korish", reply_markup=keyboard)
        

    def add_start_user_fio(self, start_user_fio):
        if chat_id in Files.users:
            Files.users_info[str(chat_id)].update(start_user_fio = start_user_fio)            
        return self.__dict__
    
class Posts():

    def __init__(self):
        self.image_id = ""
        self.text = ""
        self.user_id = 0
    
    def add_user_id(self,id):
        self.user_id = id
        return self.__dict__

    def get_posts(self):
        return self.__dict__
    
    def add_image_id(self,image_id):
        self.image_id = image_id
        return self.__dict__
    
    def add_text(self,text):
        self.text = text
        return self.__dict__
    
    def check_post(self):
        if (len(self.image_id) > 0 and len(self.text) > 0 ):
            return 1
        else:
            return 0
    
    #after insert to base
    def clear_item(self):
        self.image_id = ""
        self.text = ""

class Send_Post():
    def connect_to_base(self,user,password,database):
        mydb = mysql.connector.connect(
        host="localhost",
        user=user,
        password=password,
        database=database,
        )
        return mydb
    



