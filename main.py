from uuid import uuid4
import telebot
from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup,KeyboardButton,ReplyKeyboardMarkup,KeyboardButton
from telebot import types
from conf import TOKEN,Files, Posts,bot 
import json
import mysql.connector
import time
my_uuid = Files()
my_post = Posts()



def connect_to_base(user,password,database):
    mydb = mysql.connector.connect(
    host="localhost",
    user=user,
    password=password,
    database=database,
    )
    return mydb


def add_start_user(message):
    name = message.from_user.first_name
    telegram_id = message.chat.id

    
    mydb = connect_to_base("root","","pedagogika")

    mycursor = mydb.cursor()    
    
    sql = f"INSERT INTO users(fio,telegram) VALUES ( %s, %s )"
    val = (name, telegram_id)

    mycursor.execute(sql, val)
    mydb.commit()

def scan_start_user(message):
    mydb = connect_to_base("root","","pedagogika")
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT count(*) FROM users where telegram =  {str(message.chat.id)}")
    myresult = mycursor.fetchone()
    if myresult[0] <= 0:
        name = message.from_user.first_name 
        asd = f'salom {name} bot xush kelibsiz!\nBu bot Uzini maxsulotini sotish uchun kerak buladi.'

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        button = KeyboardButton(text='Registraciya')
        keyboard.add(button)
      
        bot.send_message(message.chat.id, asd,  reply_markup=keyboard)
        add_start_user(message)
        
    elif myresult[0]>0:
        mycursor_S = mydb.cursor()
        mycursor_S.execute(f"SELECT * FROM users where telegram =  {str(message.chat.id)}")
        myresult_s = mycursor.fetchall()

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        button = KeyboardButton(text='Registraciya')
        keyboard.add(button)
      
        bot.send_message(message.chat.id, "Qaytganingizdan xursandman!",  reply_markup=keyboard)

        
        for i in myresult_s:
            print(i)
            if i[5] == 'user':
                my_uuid.create_post(message.chat.id)
                
                                                
        
        #my_uuid.create_post(message.chat.id)
            

    


def crete_users_button(message):
    mydb = connect_to_base("root","","pedagogika")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM users where types = 'user'")
    myresult = mycursor.fetchall()
    for i in myresult:
        keyboard = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text=f"{i[1]}\n{i[3]}", callback_data=f"users{i[2]}")
        keyboard.add(button1)
        bot.send_message(message.chat.id, text=f"Admin lovizimi berish {i[1]}", reply_markup=keyboard)


    
def proverka_nomer(message):
    mydb = connect_to_base("root","","pedagogika")
    my_cursor = mydb.cursor()
    my_cursor.execute(f"SELECT * FROM users where telegram = '{message.chat.id}'")
    myresult = my_cursor.fetchall()
    for i in myresult:
        if len(i[3]) < 7 and len(i[4]) < 5:
            bot.send_message(message.chat.id , 'Iltimos registraciyadan uting')
            my_uuid.create_button(message)

            
        else:
            bot.send_message(message.chat.id, 'siz alla qachon registraciyadan utgan siz')
            my_uuid.create_post(message.chat.id)
            

        
    
        

def admin_scan(message):
    mydb = connect_to_base("root","","pedagogika")
    my_cursor = mydb.cursor()
    my_cursor.execute(f"SELECT * FROM users where telegram = {message.chat.id} and types = 'admin'")
    myresult = my_cursor.fetchall()
    bot.send_message(message.chat.id, 'salom!\nSiz /admin komandasini tanladiz')
    crete_users_button(message)
    
        
def scan_user(message):
    mydb = connect_to_base("root","","pedagogika")
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM users where telegram =  {str(message.chat.id)}")
    myresult = mycursor.fetchone()
    for i in myresult:
        if i[3] <= 0 and i[4] <=0:
            bot.send_message(message.chat.id, 'registraciyadan utishga tugri kiladi')
            
        else:
            bot.send_message(message.chat.id, 'siz registraciyadan alla qachon utgan siz')
            

        
    
def spam_info():
    mydb = connect_to_base("root","","pedagogika")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT distinct(telegram),fio, phone, gname ,types FROM users WHERE types = 'client'")
    myresult = mycursor.fetchall()

    
    for i in myresult:
        print(i[0])    
        my_post_cursor = mydb.cursor()
        #sql = "SELECT pp.*,(select phone from users where telegram = pp.user_id) as phone  FROM posts  pp where pp.state = 'select' and  pp.id not in (Select post_id FROM post_send) and pp.user_id not in(SELECT telegram FROM post_send)"
        sql = f"SELECT pp.*,(select phone from users where telegram = pp.user_id) as phone FROM posts pp WHERE pp.id not in (SELECT post_id FROM post_send WHERE telegram in ('{i[0]}'))"

        my_post_cursor.execute(sql)
        mypost = my_post_cursor.fetchall()
       

        for y in mypost:                
            
            mycursor_s = mydb.cursor()
            posts_s = my_post.get_posts()
            sql = "INSERT INTO post_send (telegram, post_id) VALUES (%s, %s)"
            val = (i[0], y[0])
        
            mycursor_s.execute(sql, val)
            mydb.commit()
                
                
            photos = y[2]
            text = y[3]
            cont = y[6]
            price = y[5]
            #print(cont)
            #time.sleep(0.3)
            bot.send_photo(int(i[0]) , photos, caption = f'{text} Maxsulot narxi: {price}\n Murojat uchun : {cont}')
        



"""def proverca_post_send(post_id, telegram):
    mydb = connect_to_base("root","","pedagogika")
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM posts pp WHERE pp.id not in (Select post_id FROM post_send) and pp.user_id not in(SELECT telegram FROM post_send)")
    myresult = mycursor.fetchall()
   """ 
    
        
        
    
         

                
                #bot.send_photo(call.from_user.id , photos, caption)
            

            
    


def create_admin_button(message,id):
        keyboard = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text="select", callback_data=f"select{id}")
        button2 = InlineKeyboardButton(text="delete", callback_data=f"dalete{id}")
        keyboard.add(button1, button2)
        bot.send_message(message.chat.id,"Amallardan birini tanlang",reply_markup = keyboard)


def admin_function(message):
    mydb = connect_to_base("root","","pedagogika")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM posts")
    myresult = mycursor.fetchall()

    for i in myresult:
        if i[4] == 'new':
            photos = i[2]
            text  = i[3]
            bot.send_photo(message.chat.id, photos, caption = text)
            create_admin_button(message,i[0])

        


def admin_pages(message):
        asd = 'salom, adminkaga xush kelibsiz'
        admin_function(message)    
        bot.send_message(message.chat.id, asd)





def add_post():
    mydb = connect_to_base("root","","pedagogika")
    mycursor = mydb.cursor()
    post = my_post.get_posts()
    sql = "INSERT INTO posts(user_id, image_id, text , prise ) VALUES (%s, %s, %s, %s)"    
    val = (post["user_id"], post["image_id"], post["text"], post['prise'])
    mycursor.execute(sql, val)
    mydb.commit()
    my_post.clear_item()

def add_user(id):
    mydb = connect_to_base("root","","pedagogika")
    mycursor = mydb.cursor()    
    user = my_uuid.users_info[str(id)]
    sql = f"UPDATE users SET fio = '{user['fio']}', phone = '{user['phone']}', gname = '{user['group']}', types = 'user' WHERE telegram = '{id}' "
    mycursor.execute(sql)
    mydb.commit()    
    my_uuid.clear_user()
    

def add_fio(message):
    my_uuid.add_chat_id(message.chat.id)
    my_uuid.add_fio(message.text, message.chat.id)
    check_user(message.chat.id)
    asd = 'sizning FIO qabul qilindi'
    bot.send_message(message.chat.id , asd)

def add_phone(message):
    my_uuid.add_chat_id(message.chat.id)
    my_uuid.add_phone(message.contact.phone_number, message.chat.id)
    check_user(message.chat.id)
    print(my_uuid.users_info)
    asd = 'sizning telefon qabul qilindi'
    bot.send_message(message.chat.id , asd, reply_markup=telebot.types.ReplyKeyboardRemove())

def add_group(message):
    my_uuid.add_chat_id(message.chat.id)
    my_uuid.add_group(message.text,message.chat.id)
    check_user(message.chat.id)
    print(my_uuid.users_info)
    asd = 'sizning grupa qabul qilindi'
    bot.send_message(message.chat.id , asd)


  
    

def add_text_post(message):
    my_uuid.add_text_post(message.text)
    asd = 'sizning postngiz!'
    bot.send_message(message.chat.id , asd)



def check_user(id):
    user = my_uuid.get_user(id)
    my_keys = list(user.keys())
    print(my_keys)
    if "fio" in my_keys and "group" in my_keys and "phone" in my_keys:
        if (len(user["fio"]) > 7 and len(user["phone"]) > 10 and len(user["group"]) > 5):
            bot.send_message(id, "Siz registratsiyadan to'liq o'tdiz endi ma'lumot junatsangiz ham bo'ladi!")
            my_uuid.create_post(id)
            add_user(id)


def add_post_text(message):
    text = message.text
    my_post.add_user_id(message.chat.id)
    my_post.add_image_id(text)
    if message.text is not None:
        add_post()
    else:
        bot.send_message(message.chat.id , 'siz text junatmadiz!')

def add_text_Photo(message):
    my_post.add_text(message.text)
    my_post.add_user_id(message.chat.id)
    state = my_post.check_post()
    bot.send_message(message.chat.id, 'Iltimos postning narxini kiriting')
    bot.register_next_step_handler(message, add_prise)

def add_prise(message):
    my_post.add_user_id(message.chat.id)
    my_post.add_prise(message.text)
    state = my_post.check_post()
    bot.send_message(message.chat.id, 'Post xaqida xamma kerakli malumot olindi, yaqin orada shu post terqatiladi')
    if state == 1:
        add_post()

    
    


@bot.message_handler(commands=['start', 'help', 'admin', 'reg'])
def send_welcome(message):
    
    if (message.text == '/start'):
        mydb = connect_to_base("root","","pedagogika")
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT distinct(telegram),fio, phone,gname ,types FROM users WHERE telegram = '{message.chat.id}'")
        myresult = mycursor.fetchall()
        if len(myresult) > 0:
            if myresult[0][4] == 'admin':
                print('admin')
                admin_pages(message)
            elif myresult[0][4] == 'user':
                scan_start_user(message)
                keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            else:
                print('user')
                scan_start_user(message)

                keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
                button = KeyboardButton(text='Registraciya')
                keyboard.add(button)
                bot.send_message(message.from_user.id, "hu yaqin orada yangi postlar chiqadi!", reply_markup=keyboard)

                
        elif len(myresult) <= 0:
            scan_start_user(message)
            
                
    elif message.text == '/admin':
        admin_scan(message)
    elif message.text == '/reg':
        proverka_nomer(message)
        

@bot.message_handler(content_types=['text'])
def proverka(message):
    if message.text == 'Familiya Ism':
        name = message.from_user.first_name
        asd = f'{name} familiya va ismingizni kiriting'
        # bot.register_next_step_handler(fioread,message)
        bot.send_message(message.chat.id, asd)
    elif message.text == 'Registraciya':
        proverka_nomer(message)
    
       
@bot.callback_query_handler(func=lambda call: True)
def inline_answer(call):
    
    if (call.data == 'fio'):
        bot.send_message(call.from_user.id,"FIO kiriting!")
        bot.register_next_step_handler(call.message,add_fio)
    elif(call.data == 'tel'):
        name = call.from_user.first_name
        asd = f'{name} telefon raqamingizni bilan bulishing!'
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        button = KeyboardButton(text='Nomer telefoni tashash', request_contact=True)
        keyboard.add(button)
        bot.send_message(call.from_user.id,text=asd, reply_markup=keyboard)
    elif(call.data == 'group'):
        bot.send_message(call.from_user.id,"Guruhni kiriting!")
        bot.register_next_step_handler(call.message,add_group)
    elif(call.data == "post"):
        bot.send_message(call.from_user.id,"Iltimos Postni Rasm ko'rinishida kiriting!")

    elif call.data[:6] == 'select':
        mydb = connect_to_base("root","","pedagogika")
        mycursor = mydb.cursor()
        update_sql = f"UPDATE posts SET state = 'select' WHERE id = {call.data[6:8]}"
        mycursor.execute(update_sql)
        mydb.commit()
        bot.send_message(call.from_user.id, 'Siz tanlagan post tarqatildi')
        spam_info()

    elif call.data[:6] == 'dalete':
        mydb = connect_to_base("root","","pedagogika")
        mycursor = mydb.cursor()
        sql = f"UPDATE posts SET state = 'delete' WHERE id = {call.data[6:8]} "
        mycursor.execute(sql)
        mydb.commit(call)
        bot.send_message(call.from_user.id, "Bu postni hechkim ko'rolmaydi")
        print('delete')
    elif call.data == 'watch':
            mydb = connect_to_base("root","","pedagogika")
            my_post_cursor = mydb.cursor()
            my_post_cursor.execute(f"SELECT * FROM posts where user_id = {str(call.from_user.id)}")
            mypost = my_post_cursor.fetchall()
            for y in mypost:
                photos = y[2]
                text = y[3]
                time.sleep(0.3)
                bot.send_photo(call.from_user.id , photos, caption = text)
                
    elif call.data[:5] == 'users':
        mydb = connect_to_base("root","","pedagogika")
        mycursor = mydb.cursor()
        sql = f"UPDATE users SET types = 'admin' WHERE telegram = {call.data[5::]} "
        mycursor.execute(sql)
        mydb.commit()
        
                

        
        




@bot.message_handler(content_types=['contact'])
def number_user(message):
    add_phone(message)


@bot.message_handler(content_types=['photo'])
def post_qiish(message):
    global my_post 
    asd = "Sizning rasmingiz qabul qilindi! Iltimos post xaqida malumot to'ldiring"
    bot.send_message(message.chat.id , asd)   
    photo = message.json["photo"][-1]["file_id"]
    my_post.add_user_id(message.chat.id)
    my_post.add_image_id(photo)
    state = my_post.check_post()

    bot.register_next_step_handler(message, add_text_Photo)
    


bot.polling()
