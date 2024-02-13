from aiogram import Bot, Dispatcher, types, executor
import asyncio
from db import DataBase
from aiogram.utils.exceptions import *
import random

bot = Bot("Token")
dp = Dispatcher(bot)

db = DataBase("postdb.db", bot)

@dp.message_handler(content_types=["video", "photo", "video_note", "document", "voice"])
async def media_group(message: types.Message):
   id = message.from_user.id
   
   checking = await db.check_db(message)
   await db.check_db(message)
   
   if checking == "dont in base":
      return await message.answer("К сожалению, вы не можете пользоваться этим ботом, так как владелец запретил доступ.")
   
   if db.data[2] == "waitMessage":
      if message.video:
         db.cursor.execute("UPDATE admin_data SET video = ? WHERE user_id = ?", (message.video.file_id, id))
         
      elif message.video_note:
         db.cursor.execute("UPDATE admin_data SET video_note = ? WHERE user_id = ?", (message.video_note[0].file_id, id))
         
      elif message.photo:
         db.cursor.execute("UPDATE admin_data SET photo = ? WHERE user_id = ?", (message.photo[0].file_id, id))
         
      elif message.voice:
         db.cursor.execute("UPDATE admin_data SET voice = ? WHERE user_id = ?", (message.voice[0].file_id, id))
         
      elif message.document:
         db.cursor.execute("UPDATE admin_data SET document = ? WHERE user_id = ?", (message.document[0].file_id, id))
      
      db.conn.commit()
      
      if message.caption:
         db.cursor.execute("UPDATE admin_data SET caption = ? WHERE user_id = ?", (message.caption, id))
         db.conn.commit()
         
      await db.edit_message(message)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
   checking = await db.check_db(message)
   
   list_info = ["Чтобы отправить пост, нужно нажать на '📲Отправить пост'", "Чтобы добавить канал, нажмите на ⚙️Настройки --> ➕Добавить канал", "Если при режиме фонт вы написали/добавили не правильно символ, то фонт не заработает, и те символы которые были написаны, останутся", "Если первым в списке владельцем не вы, то вы можете не ставить пароль, так как пароль проверяется именно у первого в списке владельцев,  пользователя"]
   
   if checking != "dont in base":
      if message.chat.type == "private":
         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
         markup.add("📲Отправить пост")
         markup.add("⚙️Настройки")
         
         await message.answer(f"Приветствую\n\n{random.choice(list_info)}", reply_markup=markup)
   else:
      await message.answer("К сожалению, вы не можете пользоваться этим ботом, так как владелец запретил доступ.")

@dp.message_handler(commands=["help"])
async def help(message: types.Message):
   await message.answer("""
/help - помощь по командам
/html_font - как использовать html фонт
/markdown_font - как использовать MarkDown фонт
/version - версии и новвоведения
__________
/html_font |
-----------------
   """)

@dp.message_handler(commands=["html_font"])
async def html_font(message: types.Message):
   await message.answer("""
<b>жирный</b>
<u>подчёркнутый</u>
<i>курсив</i>
<s>зачёркнутый</s>
<code>моно</code>
<pre><code class='python'>код</code></pre>
<a href='ссылка'></a>

________________
/markdown_font |
--------------------------
""")

@dp.message_handler(commands=["markdown_font"])
async def html_font(message: types.Message):
   await message.answer("""
*жирный*
_курсив_ 
[текст](url)
-зачеркнутый-

________
/version |
-------------
""")

@dp.message_handler(commands=["version"])
async def vesrion(message: types.Message):
   await message.answer("<b>🛠️Название версии: new 0.1(29.01.2024-31.01.2024):</b>\n•Добавлена кнопка '📲Отправить пост'\n•Добавлена кнопка '⚙️Настройки'\n•Добавлена кнопка в редактировании текста '📝Изменить'\n•Добавлена кнопка в редактировании 'Фонт' которая меняет стиль вашего текста\n•Добавлена кнопка в редактировании текста '🔗URL Кнопка' которая делает кнопку с ссылкой\n\n<b>🛠️Название версии: reaction and fix 0.2(2.2.2024-5.2.2024):</b>\n•Добавлена кнопка в редактировании текста '❤️Реакции'\n•Пофикшены баги/неприятности\n•Добавлены/изменены мелкие детали для комфорта\n•Добавлен способ добавления канала в бота через список каналов\n•Добавлена кнопка в редактировании текста '😶‍🌫Скрытый текст', при нажатии на него высветится текст, для подпищиков и не для подпищиков(его можно настроить)\n\n<b>🛠️Название версии: supporting media and other 0.3(7.2.2024-12.2.2024):</b>\n•Добавлена поддержка всей медии\n•Добалена функция, которая рассылает пост, по всем каналам\n•Теперь если отреагировали больше 1000 человек, то счёт будет скорочен на 1к. и более\n•Добавлена поддержка нового фонта 'MarkDown', и был изменён текст у кнопки для фонта\n•Добавлена кнопка в настройках для добавления владельца и удаления владельца\n•Добавлена кнопка в настройках '🔐Поставить пароль' для защиты\n•Исправлены мелкие баги\n\n=====Проект временно преостановлен=====", parse_mode="html")

@dp.message_handler(content_types=["text"])
async def text(message: types.Message):
   id = message.from_user.id
   
   checking = await db.check_db(message)
   await db.check_db(message)
   
   if checking == "dont in base":
      return await message.answer("К сожалению, вы не можете пользоваться этим ботом, так как владелец запретил доступ.")
   
   if message.chat.type == "private":
      if message.text == "📲Отправить пост":
         if db.data[3] == "None":
            return await message.answer("К сожалению, вы ещё не добавили свой канал(⚙️Настройки --> ➕Добавить канал)")
            
         db.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("waitMessage", id))
         db.conn.commit()
         
         db.cursor.execute("UPDATE admin_data SET url_button = ? WHERE user_id = ?", ("None", id))
         db.cursor.execute("UPDATE admin_data SET reaction_button = ? WHERE user_id = ?", ("None", id))
         db.conn.commit()
         
         db.cursor.execute("UPDATE admin_data SET text = ? WHERE user_id = ?", ("None", id))
         db.conn.commit()
         
         db.cursor.execute("UPDATE admin_data SET name_hide_text = ? WHERE user_id = ?", ("None", id))
         db.cursor.execute("UPDATE admin_data SET not_sub_text = ? WHERE user_id = ?", ("None", id))
         db.cursor.execute("UPDATE admin_data SET sub_text = ? WHERE user_id = ?", ("None", id))
         db.conn.commit()
         
         db.cursor.execute("UPDATE admin_data SET caption = ? WHERE user_id = ?", ("None", id))
         db.conn.commit()
         
         db.cursor.execute("UPDATE admin_data SET video = ? WHERE user_id = ?", ("None", id))
         db.conn.commit()
         
         db.cursor.execute("UPDATE admin_data SET video_note = ? WHERE user_id = ?", ("None", id))
         db.conn.commit()
         
         db.cursor.execute("UPDATE admin_data SET voice = ? WHERE user_id = ?", ("None", id))
         db.conn.commit()
         
         db.cursor.execute("UPDATE admin_data SET photo = ? WHERE user_id = ?", ("None", id))
         db.conn.commit()
         
         db.cursor.execute("UPDATE admin_data SET document = ? WHERE user_id = ?", ("None", id))
         db.conn.commit()
            
         markup = types.InlineKeyboardMarkup()
         markup.add(types.InlineKeyboardButton("Отмена", callback_data="cancel"))
            
         await message.answer("Вы можете отправить сюда текст, видео, голосовое сообщение и другую медию, в количестве 1-ой штуки.", reply_markup=markup)
      elif db.data[2] == "waitMessage":
         db.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("None", id))
         db.conn.commit()
         
         db.cursor.execute("UPDATE admin_data SET text = ? WHERE user_id = ?", (message.text, id))
         db.conn.commit()
         
         await db.edit_message(message)
      elif message.text == "⚙️Настройки":
         await db.option(message)
      elif db.data[2] == "waitForwardMessage":
         await message.delete()
         
         await bot.delete_message(chat_id=message.from_user.id, message_id=int(message.message_id) - 1)
         #await bot.delete_message(chat_id=message.from_user.id, message_id=int(message.message_id) - 2)
         
         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
         markup.add("📲Отправить пост")
         markup.add("⚙️Настройки")
         
         try:
            if message.forward_from_chat:
               channel_name = await bot.get_chat(chat_id=int(message.forward_from_chat.id))
               
               db.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("None", id))
               db.conn.commit()
               
               if db.data[3] == "None":
                  db.cursor.execute("UPDATE admin_data SET channel = ? WHERE user_id = ?", (f"{message.forward_from_chat.id}", id))
                  db.conn.commit()
               else:
                  if str(message.forward_from_chat.id) in db.data[3]:
                     await message.answer("Этот канал уже есть в боте", reply_markup=markup)
                  else:
                     db.cursor.execute("UPDATE admin_data SET channel = ? WHERE user_id = ?", (f"|{message.forward_from_chat.id}", id))
                     db.conn.commit()
               
               if str(message.forward_from_chat.id) in db.data[3]:
                  pass
               else:
                  await message.answer(f"Вы успешно добавили {channel_name.title} в бота", reply_markup=markup)
               
               await db.check_db(message)
               
               await db.option(message)
            else:
               await message.reply("Это сообщение не из канала")
         except Exception as e:
            return await message.answer(f"Вы не переслали сообщение из канала, {e}")
      elif db.data[2] == "editMessage":
         db.cursor.execute("UPDATE admin_data SET text = ? WHERE user_id = ?", (message.text, id))
         db.conn.commit()
         
         await message.delete()
         
         await bot.delete_message(chat_id=message.from_user.id, message_id=int(message.message_id) - 1)
         
         await db.edit_message(message)
      elif db.data[2] == "addUrlButton":
         db.cursor.execute("UPDATE admin_data SET text = ? WHERE user_id = ?", ("None", id))
         db.conn.commit()
         
         msg = message.text
         
         await message.delete()
         await bot.delete_message(chat_id=message.from_user.id, message_id=int(message.message_id) - 1)
         
         if "," in msg:
            msg = msg.replace(",", "")
         else:
            pass
         
         if not "|" in msg:
            msg = msg.split("\n")
            
            i = 0
            for mis in msg:
               if mis[int(mis.find("-")) - 1] == " ":
                  mis = mis[:int(mis.find("-")) - 1] + mis[int(mis.find("-")):]
                  msg[i] = mis
               if mis[int(mis.find("-")) + 1] == " ":
                  mis = mis[:int(mis.find("-")) + 1] + mis[int(mis.find("-")) + 2:]
                  msg[i] = mis
               i += 1
            
            msg = ",".join(msg)
         else:
            msg = msg.split("\n")
            
            i = 0
            for mas in msg:
               if mas[-1] == " ":
                  mas = mas[:-1]
                  msg[i] = mas
               if mas[-2] == " ":
                  mas = mas[:-2] + mas[-1]
                  msg[i] = mas
               if mas[0] == " ":
                  msg[i] = mas[1:]
               
               if mas[int(mas.find("-")) - 1] == " ":
                  mas = mas[:int(mas.find("-")) - 1] + mas[int(mas.find("-")):]
                  msg[i] = mas
               if mas[int(mas.find("-")) + 1] == " ":
                  mas = mas[:int(mas.find("-")) + 1] + mas[int(mas.find("-")) + 2:]
                  msg[i] = mas
               i += 1
            
            msg = "".join(msg)
         
         if db.data[5] == "None":
            db.cursor.execute("UPDATE admin_data SET url_button = ? WHERE user_id = ?", (f"{msg}", id))
            db.conn.commit()
         else:
            db.cursor.execute("UPDATE admin_data SET url_button = ? WHERE user_id = ?", (f"{''.join(db.data[5])},{msg}", id))
            db.conn.commit()
         
         await db.edit_message(message)
      elif db.data[2] == "addReactionButton":
         msg = message.text
         
         msg = msg.replace(" ", "")
         
         if db.data[6] == "None":
            db.cursor.execute("UPDATE admin_data SET reaction_button = ? WHERE user_id = ?", (msg, id))
            db.conn.commit()
         else:
            db.cursor.execute("UPDATE admin_data SET reaction_button = ? WHERE user_id = ?", (f"{db.data[6]},{msg}", id))
            db.conn.commit()
         
         await db.edit_message(message)
      elif db.data[2] == "waitHideTextName":
         await bot.delete_message(chat_id=message.from_user.id, message_id=int(message.message_id) - 1)
         
         msg = message.text
         
         if "|" in msg:
            msg = msg.replace("|", "")
         if "," in msg:
            msg = msg.replace(",", "")
         
         db.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("waitNotSubText", id))
         db.conn.commit()
         
         if db.data[7] == "None":
            db.cursor.execute("UPDATE admin_data SET name_hide_text = ? WHERE user_id = ?", (msg, id))
            db.conn.commit()
         else:
            db.cursor.execute("UPDATE admin_data SET name_hide_text = ? WHERE user_id = ?", (f",{msg}", id))
            db.conn.commit()
         
         await message.answer("Вы успешно назначили имя для кнопки.Отправьте сюда текст для тех кто не подписан(до 200 слов)")
      elif db.data[2] == "waitNotSubText":
         await bot.delete_message(chat_id=message.from_user.id, message_id=int(message.message_id) - 1)
         
         msg = message.text
         
         if "|" in msg:
            msg = msg.replace("|", "")
         if "," in msg:
            msg = msg.replace(",", "")
         
         if len(msg) > 200:
            return await message.answer("Увы, но ваш текст привышает лимит в больше 200 слов.")
         
         db.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("waitSubText", id))
         db.conn.commit()
         
         if db.data[8] == "None":
            db.cursor.execute("UPDATE admin_data SET not_sub_text = ? WHERE user_id = ?", (msg, id))
            db.conn.commit()
         else:
            db.cursor.execute("UPDATE admin_data SET not_sub_text = ? WHERE user_id = ?", (f",{msg}", id))
            db.conn.commit()
         
         await message.answer("Вы успешно установили текст для тех кто не подписан в кнопку.Отправьте сюда текст для тех подписан(до 200 слов)")
      elif db.data[2] == "waitSubText":
         await bot.delete_message(chat_id=message.from_user.id, message_id=int(message.message_id) - 1)
         
         msg = message.text
         
         if "|" in msg:
            msg = msg.replace("|", "")
         if "," in msg:
            msg = msg.replace(",", "")
         
         if len(msg) > 200:
            return await message.answer("'Увы, но ваш текст привышает лимит в болше 200 слов.")
         
         db.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("None", id))
         db.conn.commit()
         
         db.cursor.execute("UPDATE admin_data SET sub_text = ? WHERE user_id = ?", (msg, id))
         db.conn.commit()
         
         await db.edit_message(message)
      elif db.data[2] == "GetUserIdForNewOwner":
         if message.forward_origin.id:
            db.cursor.execute("INSERT OR IGNORE INTO admin_data (user_id) VALUES (?)", (message.forward_origin.id))
            db.conn.commit()
            
            db.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("None", id))
            db.conn.commit()
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("📲Отправить пост")
            markup.add("⚙️Настройки")
            
            await message.answer("Вы успешно добавили нового админа", reply_markup=markup)
         else:
             markup = types.InlineKeyboardMarkup()
             markup.add(types.InlineKeyboardButton("Отмена", callback_data="cancel"))
             
             await message.answer("К сожалению, пользователь которого вы переслали, скрыл свою информацию, советую передать информацию через список")
      elif db.data[2] == "GetPassword":
         password = db.cursor.execute("SELECT password FROM admin_data").fetchall()
         
         markup = types.InlineKeyboardMarkup()
         markup.add(types.InlineKeyboardButton("Отмена", callback_data="cancel"))
         
         if message.text == password[0][0]:
             await message.delete()
             
             db.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("GetUserIdForNewOwner", id))
             db.conn.commit()
            
             await message.answer("Вы успешно подтвердили пароль, перешлите сюда сообщение нового владельца", reply_markup=markup)
            
             markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
             btn = types.KeyboardButton("Отправить через список", request_user=types.KeyboardButtonRequestUser(request_id=9876, user_is_bot=False))
         
             markup.add(btn)
         
             await message.answer("Вы также можете отправить из своего списка", reply_markup=markup)
         else:
            await message.answer("Неверный пароль", reply_markup=markup)
      elif db.data[2] == "GetPasswordForDelOwner":
         password = db.cursor.execute("SELECT password FROM admin_data").fetchall()
         
         if message.text == password[0][0]:
            db.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("None", id))
            db.conn.commit()
            
            markup = types.InlineKeyboardMarkup(row_width=1)
         
            for owner in db.cursor.execute("SELECT * FROM admin_data").fetchall():
               markup.add(types.InlineKeyboardButton(f"{owner[0]}", callback_data=f"del_owner {owner[0]}"))
            markup.add(types.InlineKeyboardButton("Отмена", callback_data="cancel"))
            
            await message.answer("Выберите владельца для удаления", reply_markup=markup)
         else:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Отмена", callback_data="cancel"))
            
            await message.answer("Неверный пароль", reply_markup=markup)
      elif db.data[2] == "setPassword":
         db.cursor.execute("UPDATE admin_data SET password = ? WHERE user_id = ?", (message.text, id))
         db.conn.commit()
         
         db.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("None", id))
         db.conn.commit()
         
         print("test")
         
         await db.option(message)
      elif db.data[2] == "GetPasswordForNew":
         password = db.cursor.execute("SELECT password FROM admin_data").fetchall()
         
         markup = types.InlineKeyboardMarkup()
         markup.add(types.InlineKeyboardButton("Отмена", callback_data="cancel"))
         
         if message.text == password[0][0]:
            db.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("setPassword", id))
            db.conn.commit()
            
            await message.answer("Введите будущий пароль", reply_markup=markup)
         else:
            await message.answer("Неверный пароль", reply_markup=markup)

@dp.callback_query_handler(lambda call: call.data.startswith("del_owner "))
async def delete_owner(call: types.CallbackQuery):
   await call.message.delete()
   
   splited = call.data.split("del_owner ")[1]
   
   await db.call_check_db(call)
   
   db.cursor.execute(f"DELETE FROM admin_data WHERE user_id LIKE {splited}")
   db.conn.commit()
   
   await call.answer("Вы успешно удалили владельца")
   
   await db.call_option(call)

@dp.callback_query_handler(lambda call: call.data.startswith("del_channel "))
async def delete_channel(call: types.CallbackQuery):
   await call.message.delete()
   
   splited = call.data.split("del_channel ")[1]
   
   await db.call_check_db(call)
   
   if "|" in db.data[3]:
      channels = db.data[3].replace(f"|{splited}", "")
   else:
      channels = db.data[3].replace(f"{splited}", "")
   
   db.cursor.execute("UPDATE admin_data SET channel = ? WHERE user_id = ?", (channels, call.from_user.id))
   db.conn.commit()
   
   await db.call_check_db(call)
   
   if not db.data[3]:
      db.cursor.execute("UPDATE admin_data SET channel = ? WHERE user_id = ?", ("None", call.from_user.id))
      db.conn.commit()
   
   await call.answer("Вы успешно удалили канал")
   
   await db.call_check_db(call)
   
   await db.call_option(call)

@dp.callback_query_handler(lambda call: call.data.startswith("hide_text "))
async def hide_text(call: types.CallbackQuery):
   hide_text = db.cursor.execute("SELECT * FROM reaction_msg WHERE message_id = ? AND channel_id = ?", (call.message.message_id, call.message.chat.id)).fetchone()
   
   user = await bot.get_chat_member(chat_id=hide_text[1], user_id=call.from_user.id)
   if user.status in ["member", "administrator", "creator"]:
      await call.answer(text=hide_text[8], show_alert=True)
   else:
      await call.answer(text=hide_text[7], show_alert=True)

@dp.callback_query_handler(lambda call: call.data.startswith("reaction "))
async def reaction_call(call: types.CallbackQuery):
   await db.call_check_db(call)
   
   reaction = db.cursor.execute("SELECT * FROM reaction_msg WHERE message_id = ? AND channel_id = ?", (call.message.message_id, call.message.chat.id)).fetchone()
   
   react = call.data.split("reaction ")
   users = reaction[3].split("|")
   
   markup = types.InlineKeyboardMarkup()
   
   sobr = []
   
   if reaction[3] == "None" or reaction[3] != "None":
      for user in users:
         if str(call.from_user.id) in user:
            return await call.answer(f"🚫Вы голосовали ранее...")
      var_emoji = reaction[2].split(",")
      
      for pot in var_emoji:
         if react[1] in pot:
            vars = int(pot[1:])
            pot = f"{pot[0]}{vars+1}"
         sobr.append(pot)
   
      db.cursor.execute("UPDATE reaction_msg SET emoji_and_var = ? WHERE message_id = ? AND channel_id = ?", (",".join(sobr), call.message.message_id, call.message.chat.id))
      db.conn.commit()
   
   reaction = db.cursor.execute("SELECT * FROM reaction_msg WHERE message_id = ? AND channel_id = ?", (call.message.message_id, call.message.chat.id)).fetchone()
   
   if reaction[4] != "None":
      spl = reaction[4].split(",")
         
      btn_row = []
      for btn in spl:
         if not "|" in btn:
            splr = "".join(btn).split("-")
            if not splr:
               pass
            else:
               markup.add(types.InlineKeyboardButton(f"{splr[0]}", url=f"{splr[1]}"))
         else:
            palk = "".join(btn).split("|")
            for palka in palk:
               ch = "".join(palka).split("-")
               
               if not ch:
                  pass
               else:
                  btn_row.append(types.InlineKeyboardButton(f"{ch[0]}", url=f"{ch[1]}"))
               
            markup.add(*btn_row)
   else:
      pass
   
   if db.data[7] != "None":
      markup.add(types.InlineKeyboardButton(f"{db.data[7]}", callback_data=f"hide_text {db.data[7]}"))
   
   if reaction[5] != "None":
      btns_emoji = []
      emoji_and_var = []
         
      sdd = reaction[5].split(",")
      for ceh in sdd:
         if "\n" in ceh:
            for res in ceh.split("\n"):
               for ins in res.split("|"):
                  for emj in reaction[2].split(","):
                     if emj[0] == ins:
                        ins = emj
                        
                        if len(str(ins[1:])) > 3:
                           if len(str(ins[1:])) == 4:
                              formated = f"{ins[1]}.{ins[2]}k"
                           elif len(str(ins[1:])) == 5:
                              formated = f"{ins[1:3]}.{ins[3]}k"
                           elif len(str(ins[1:])) == 6:
                              formated = f"{ins[1:4]}.{ins[4]}k"
                           elif len(str(ins[1:])) == 7:
                              formated = f"{ins[1]}.{ins[2]}m"
                           elif len(str(ins[1:])) == 8:
                              formated = f"{ins[1:3]}.{ins[3]}m"
                           elif len(str(ins[1:])) == 9:
                              formated = f"{ins[1:3]}.{ins[4]}m"
                           ins = f"{ins[0]}{formated}"
                     
                  btns_emoji.append(types.InlineKeyboardButton(f"{ins}", callback_data=f"reaction {ins[0]}"))
                  
                  emoji_and_var.append(f"{ins[0]}")
               markup.add(*btns_emoji)
               btns_emoji = []
         else:
            pdd = ceh.split("|")
               
            for res in pdd:
               for emj in reaction[2].split(","):
                  if emj[0] == res:
                     res = emj
                     
                     if len(str(res[1:])) > 3:
                        if len(str(res[1:])) == 4:
                           formated = f"{res[1]}.{res[2]}k"
                        elif len(str(res[1:])) == 5:
                           formated = f"{res[1:3]}.{res[3]}k"
                        elif len(str(res[1:])) == 6:
                           formated = f"{res[1:4]}.{res[4]}k"
                        elif len(str(res[1:])) == 7:
                           formated = f"{res[1]}.{res[2]}m"
                        elif len(str(res[1:])) == 8:
                           formated = f"{res[1:3]}.{res[3]}m"
                        elif len(str(res[1:])) == 9:
                           formated = f"{res[1:3]}.{res[4]}m"
                        res = f"{res[0]}{formated}"
               
               btns_emoji.append(types.InlineKeyboardButton(f"{res}", callback_data=f"reaction {res[0]}"))
               
               emoji_and_var.append(f"{res[0]}")
               
            markup.add(*btns_emoji)
            btns_emoji = []
      
   if reaction[3] == "None":
      db.cursor.execute("UPDATE reaction_msg SET used_reaction = ? WHERE message_id = ? AND channel_id = ?", (call.from_user.id, call.message.message_id, call.message.chat.id))
      db.conn.commit()
   else:
      db.cursor.execute("UPDATE reaction_msg SET used_reaction = ? WHERE message_id = ? AND channel_id = ?", (f"{reaction[3]}|{call.from_user.id}", call.message.message_id, call.message.chat.id))
      db.conn.commit()
    
   if call.message.caption:
      await bot.edit_message_caption(chat_id=reaction[1], message_id=call.message.message_id, caption=call.message.caption, reply_markup=markup)
   else:
      await bot.edit_message_text(chat_id=reaction[1], message_id=call.message.message_id, text=call.message.text, reply_markup=markup)
      
   await call.answer(f"Вы отреагировали: {pot[0]}")

@dp.callback_query_handler(lambda call: call.data.startswith("sendmsg "))
async def sendmsg(call: types.CallbackQuery):
   await call.message.delete()
   
   splited = call.data.split("sendmsg ")[1]
   
   checking = await db.call_check_db(call)
   await db.call_check_db(call)
   
   if checking == "dont in base":
      return await call.message.answer("К сожалению, вы не можете пользоваться этим ботом, так как владелец запретил доступ.")
   
   markup = types.InlineKeyboardMarkup()
   
   if db.data[5] != "None":
      spl = db.data[5].split(",")
         
      btn_row = []
      for btn in spl:
         if not "|" in btn:
            splr = "".join(btn).split("-")
            if not splr:
               pass
            else:
               markup.add(types.InlineKeyboardButton(f"{splr[0]}", url=f"{splr[1]}"))
         else:
            palk = "".join(btn).split("|")
            for palka in palk:
               ch = "".join(palka).split("-")
               
               if not ch:
                  pass
               else:
                  btn_row.append(types.InlineKeyboardButton(f"{ch[0]}", url=f"{ch[1]}"))
               
            markup.add(*btn_row)
   else:
      pass
   
   if db.data[7] != "None":
      markup.add(types.InlineKeyboardButton(f"{db.data[7]}", callback_data=f"hide_text {db.data[7]}"))
   
   btns_emoji = []
   emoji_and_var = []
   if db.data[6] != "None":
         
      sdd = db.data[6].split(",")
      for ceh in sdd:
         if "\n" in ceh:
            for res in ceh.split("\n"):
               for ins in res.split("|"):
                  btns_emoji.append(types.InlineKeyboardButton(f"{ins}0", callback_data=f"reaction {ins}"))
                  
                  emoji_and_var.append(f"{ins}0")
               markup.add(*btns_emoji)
               btns_emoji = []
         else:
            pdd = ceh.split("|")
               
            for res in pdd:
               btns_emoji.append(types.InlineKeyboardButton(f"{res}0", callback_data=f"reaction {res}"))
               
               emoji_and_var.append(f"{res}0")
               
            markup.add(*btns_emoji)
            btns_emoji = []
   
   if db.data[11] == "None" and db.data[12] == "None" and db.data[13] == "None" and db.data[14] == "None" and db.data[15] == "None":
      try:
         if db.data[4] == 0:
            msg = await bot.send_message(int(splited), db.data[1], parse_mode="html", reply_markup=markup)
         
         elif db.data[4] == 2:
            msg = await bot.send_message(int(splited), db.data[1], parse_mode="markdown", reply_markup=markup)
         
         else:
            msg = await bot.send_message(int(splited), db.data[1], reply_markup=markup)
      
      except Exception as e:
         return await call.message.answer("К сожалению, вы ещё не добавили свой канал(⚙️Настройки --> ➕Добавить канал)")
   else:
      try:
         if db.data[10] != "None":
            caption = db.data[10]
         else:
            caption = None
         
         if db.data[11] != "None":
            msg = await db.bot.send_video(chat_id=int(splited), video=db.data[11], reply_markup=markup, caption=caption)
            
         elif db.data[12] != "None":
            msg = await bot.send_video_note(chat_id=int(splited), video_note=db.data[12], reply_markup=markup, caption=caption)
            
         elif db.data[13] != "None":
            msg = await bot.send_photo(chat_id=int(splited), photo=db.data[13], reply_markup=markup, caption=caption)
               
         elif db.data[14] != "None":
            msg = await bot.send_voice(chat_id=int(splited), voice=db.data[14], reply_markup=markup, caption=caption)
            
         elif db.data[15] != "None":
            msg = await bot.send_document(chat_id=int(splited), document=db.data[15], reply_markup=markup, caption=caption)
            
      except Exception as e:
         return await call.message.answer("К сожалению, вы ещё не добавили свой канал(⚙️Настройки --> ➕Добавить канал)")
   
   if db.data[6] != "None":
      react = db.cursor.execute("SELECT * FROM reaction_msg")
      
      db.cursor.execute("INSERT INTO reaction_msg (message_id, channel_id, emoji_and_var, user_reaction, url_button, reaction_button, name_hide_text, not_sub_text, sub_text) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (msg.message_id, splited, ",".join(emoji_and_var), "None", db.data[5], db.data[6], db.data[7], db.data[8], db.data[9]))
      db.conn.commit()
   
   await call.message.answer("✅Вы успешно опубликовали пост в канал")

@dp.callback_query_handler(lambda call: True)
async def call(call: types.CallbackQuery):
   id = call.from_user.id
   
   checking = await db.call_check_db(call)
   await db.call_check_db(call)
   
   if checking == "dont in base":
      return await call.message.answer("К сожалению, вы не можете пользоваться этим ботом, так как владелец запретил доступ.")
   
   if call.data == "cancel":
      if db.data[2] in ["editMessage", "addUrlButton", "addReactionButton"]:
         await call.message.delete()
         
         await db.call_edit_message(call)
         
         await call.answer("Вы успешно отменили действие.")
      else:
         await call.message.delete()
         
         db.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("None", id))
         db.conn.commit()
         
         await call.answer("Вы успешно отменили действие.")
         
         if call.message.text == "Выберите канал чтобы удалить его" or call.message.text == "Бота нету или он не является администратором в вашем канале, назначьте бота администратором (ему достаточно лишь изменять и писать сообщение) Chat not found" or db.data[2] == "GetUserIdForNewOwner" or db.data[2] == "GetPassword" or db.data[2] == "GetPasswordForDelOwner" or db.data[2] == "setPassword" or db.data[2] == "GetPasswordForNew":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("📲Отправить пост")
            markup.add("⚙️Настройки")
            
            await call.message.answer("Делается меню...", reply_markup=markup)
            
            await db.call_option(call)
   elif call.data == "postMessage":
      if db.data[3] == "None":
         return await call.message.answer("К сожалению, вы ещё не добавили свой канал(⚙️Настройки --> ➕Добавить канал)")
      
      await call.message.delete()
      
      quantity_channel = 0
      for i in db.data[3].split("|"):
         if i:
            quantity_channel += 1
      
      btn_list = []
      if quantity_channel > 1:
         for channel in db.data[3].split("|"):
            try:
               if not channel:
                  pass
               else:
                     
                  channel_name = await bot.get_chat(chat_id=int(channel))
                  
                  btn_list.append(types.InlineKeyboardButton(f"{channel_name.title}", callback_data=f"sendmsg {channel}"))
            except Exception as e:
               return await call.message.answer(f"Бота нету на каком то из каналов, пожалуйста, проверьте, является ли бот администратором в вашем канале {e}")
         
         markup = types.InlineKeyboardMarkup()
         markup.add(*btn_list)
         markup.add(types.InlineKeyboardButton("Отправить это на всех каналах", callback_data="send_all_channel"))
         
         return await call.message.answer("Выберите канал, в котором будете публиковать сообщение.", reply_markup=markup)
      
      markup = types.InlineKeyboardMarkup()
      
      btn_row = []
      if db.data[5] != "None":
         spl = db.data[5].split(",")
            
         for btn in spl:
            if not "|" in btn:
               splr = "".join(btn).split("-")
               if not splr:
                  pass
               else:
                  markup.add(types.InlineKeyboardButton(f"{splr[0]}", url=f"{splr[1]}"))
            else:
               palk = "".join(btn).split("|")
               for palka in palk:
                  ch = "".join(palka).split("-")
                  
                  if not ch:
                     pass
                  else:
                     btn_row.append(types.InlineKeyboardButton(f"{ch[0]}", url=f"{ch[1]}"))
                  
               markup.add(*btn_row)
      else:
         pass
      
      if db.data[7] != "None":
         markup.add(types.InlineKeyboardButton(f"{db.data[7]}", callback_data=f"hide_text {db.data[7]}"))
      
      btns_emoji = []
      emoji_and_var = []
      if db.data[6] != "None":
         
         sdd = db.data[6].split(",")
         for ceh in sdd:
            if "\n" in ceh:
               for res in ceh.split("\n"):
                  for ins in res.split("|"):
                     btns_emoji.append(types.InlineKeyboardButton(f"{ins}0", callback_data=f"reaction {ins}"))
                     
                     emoji_and_var.append(f"{ins}0")
                     
                  markup.add(*btns_emoji)
                  btns_emoji = []
            else:
               pdd = ceh.split("|")
               
               for res in pdd:
                  btns_emoji.append(types.InlineKeyboardButton(f"{res}0", callback_data=f"reaction {res}"))
                  
                  emoji_and_var.append(f"{res}0")
               
               markup.add(*btns_emoji)
               btns_emoji = []
      
      if db.data[11] == "None" and db.data[12] == "None" and db.data[13] == "None" and db.data[14] == "None" and db.data[15] == "None":
         try:
            if db.data[4] == 1:
               msg = await bot.send_message("".join(db.data[3].split("|")).replace(" ", ""), "".join(db.data[1]), parse_mode="html", reply_markup=markup)
            
            elif db.data[4] == 2:
               msg = await bot.send_message("".join(db.data[3].split("|")).replace(" ", ""), "".join(db.data[1]), parse_mode="markdown", reply_markup=markup)
            
            else:
               msg = await bot.send_message("".join(db.data[3].split("|")).replace(" ", ""), "".join(db.data[1]), reply_markup=markup)
          
         except CantParseEntities as e:
            msg = await bot.send_message("".join(db.data[3].split("|")).replace(" ", ""), "".join(db.data[1]), reply_markup=markup)
            
            await call.answer("🚫Такие символы не поддерживаются")
                
         except Exception as e:
            return await call.message.answer("Что то пошло не так, пожалуйста, проверьте, является ли бот администратором в вашем канале")
      else:
         if db.data[10] != "None":
            caption = db.data[10]
         else:
            caption = None
         
         if db.data[11] != "None":
           msg = await db.bot.send_video(chat_id="".join(db.data[3].split("|")).replace(" ", ""), video=db.data[11], caption=caption, reply_markup=markup)
           
         elif db.data[12] != "None":
            msg = await bot.send_video_note(chat_id="".join(db.data[3].split("|")).replace(" ", ""), video_note=db.data[12], caption=caption, reply_markup=markup)
            
         elif db.data[13] != "None":
            msg = await bot.send_photo(chat_id="".join(db.data[3].split("|")).replace(" ", ""), photo=db.data[13], caption=caption, reply_markup=markup)
               
         elif db.data[14] != "None":
            msg = await bot.send_voice(chat_id="".join(db.data[3].split("|")).replace(" ", ""), voice=db.data[14], caption=caption, reply_markup=markup)
            
         elif db.data[15] != "None":
            msg = await bot.send_document(chat_id="".join(db.data[3].split("|")).replace(" ", ""), document=db.data[15], caption=caption, reply_markup=markup)
      
      await call.message.answer("✅Вы успешно опубликовали пост на вашем канале.")
      
      react = db.cursor.execute("SELECT * FROM reaction_msg")
       
      db.cursor.execute("INSERT INTO reaction_msg (message_id, channel_id, emoji_and_var, used_reaction, url_button, reaction_button, name_hide_text, not_sub_text, sub_text) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (msg.message_id, "".join(db.data[3].split("|")).replace(" ", ""), ",".join(emoji_and_var), "None", db.data[5], db.data[6], db.data[7], db.data[8], db.data[9]))
      db.conn.commit()
   elif call.data == "add_channel":
      await call.message.delete()
      
      db.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("waitForwardMessage", id))
      db.conn.commit()
      
      markup = types.InlineKeyboardMarkup()
      markup.add(types.InlineKeyboardButton("Добавить бота в канал", url="https://t.me/animeLiSTOdnianimebot?startchannel=invite"))
      markup.add(types.InlineKeyboardButton("Отмена", callback_data="cancel"))
      
      await call.message.answer("Добавьте бота в ваш канал, затем сделайте его администратором(не обязательно ставить все параметры, главное чтобы он смог отправлять сообщение и изменять), и после этого, перешлите сюда сообщение с вашего канала.", reply_markup=markup)
      
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      
      user_rights = types.ChatAdministratorRights(can_restrict_members=True, can_manage_chat=True, can_promote_members=True)
      
      btn = types.KeyboardButton("Выбрать из списка", 
      request_chat=types.KeyboardButtonRequestChat(
      request_id=123, 
      chat_is_channel=True,
      user_administrator_rights=user_rights))
      
      markup.add(btn)
      await call.message.answer("Вы также можете поделиться чатом из вашего списка", reply_markup=markup)
   elif call.data == "editMessage":
      await call.message.delete()
      
      db.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("editMessage", id))
      db.conn.commit()
      
      markup = types.InlineKeyboardMarkup()
      markup.add(types.InlineKeyboardButton("Отмена", callback_data="cancel"))
      
      await call.message.answer("Отправьте сюда сообщение которое хотите изменить", reply_markup=markup)
   elif call.data == "parsing":
      if db.data[4] == 0:
         db.cursor.execute("UPDATE admin_data SET parse_mode = ? WHERE user_id = ?", (1, id))
         db.conn.commit()
         
      elif db.data[4] == 1:
         db.cursor.execute("UPDATE admin_data SET parse_mode = ? WHERE user_id = ?", (2, id))
         db.conn.commit()
         
      elif db.data[4] == 2:
         db.cursor.execute("UPDATE admin_data SET parse_mode = ? WHERE user_id = ?", (0, id))
         db.conn.commit()
      
      await db.call_edit_message(call)
   elif call.data == "add_url_button":
      await call.message.delete()
      
      db.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("addUrlButton", id))
      db.conn.commit()
      
      markup = types.InlineKeyboardMarkup()
      markup.add(types.InlineKeyboardButton("Отмена", callback_data="cancel"))
      
      await call.message.answer("Отправьте боту список кнопок в таком формате:\n\nБез ряда\n```\nКнопка 1 - https://t.me/odnianime\nКнопка 2 - https://t.me/odnianime```\n\nС рядом\n```\nКнопка 1 - ссылка |\nКнопка 2 - ссылка |\nКнопка 3 - ссылка```\n\n*Внимание, в названии кнопки не допускаются символы для разделения ссылок и кнопок*", reply_markup=markup, parse_mode="markdownv2")
   elif call.data == "reactionMessage":
      await call.message.delete()
      
      db.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("addReactionButton", id))
      db.conn.commit()
      
      markup = types.InlineKeyboardMarkup()
      markup.add(types.InlineKeyboardButton("Отмена", callback_data="cancel"))
      
      await call.message.answer("Отправьте боту список кнопок реакции в таком формате:\n\n```\n👍 | 👎\n```\n\nЕсли хотите добавить несколько кнопок с рядами:\n```\n👍 | 👎\n👍 | 👎\n```", reply_markup=markup)
   elif call.data == "delete_channel":
      await call.message.delete()
      
      if db.data[3] == "None":
         await call.message.answer("К сожалению, вы ещё не добавили свой канал(⚙️Настройки --> ➕Добавить канал)")
         
         return await db.call_option(call)
         
      markup = types.InlineKeyboardMarkup(row_width=3)
      
      for chn in db.data[3].split("|"):
         try:
            if not chn:
               pass
            else:
               channel = await bot.get_chat(chat_id=int(chn))
               
               markup.add(types.InlineKeyboardButton(f"{channel.title}", callback_data=f"del_channel {chn}"))
         except Exception as e:
            if not chn:
               pass
            else:
               channel = "Удалённый канал"
               
               markup.add(types.InlineKeyboardButton(f"{channel}", callback_data=f"del_channel {chn}"))
      
      markup.add(types.InlineKeyboardButton("Отменить", callback_data="cancel"))
      
      await call.message.answer("Выберите канал чтобы удалить его", reply_markup=markup)
   elif call.data == "hideText":
      db.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("waitHideTextName", id))
      db.conn.commit()
      
      markup = types.InlineKeyboardMarkup()
      markup.add(types.InlineKeyboardButton("Отмена", callback_data="cancel"))
      
      await call.message.answer("Отправьте сюда название кнопки", reply_markup=markup)
   elif call.data == "send_all_channel":
      await call.message.delete()
      
      successfull = 0
      all_channel = 0
      
      for channel in db.data[3].split("|"):
            markup = types.InlineKeyboardMarkup()
      
            btn_row = []
            if db.data[5] != "None":
               spl = db.data[5].split(",")
                  
               for btn in spl:
                  if not "|" in btn:
                     splr = "".join(btn).split("-")
                     if not splr:
                        pass
                     else:
                        markup.add(types.InlineKeyboardButton(f"{splr[0]}", url=f"{splr[1]}"))
                  else:
                     palk = "".join(btn).split("|")
                     for palka in palk:
                        ch = "".join(palka).split("-")
                        
                        if not ch:
                           pass
                        else:
                           btn_row.append(types.InlineKeyboardButton(f"{ch[0]}", url=f"{ch[1]}"))
                        
                     markup.add(*btn_row)
            else:
               pass
            
            if db.data[7] != "None":
               markup.add(types.InlineKeyboardButton(f"{db.data[7]}", callback_data=f"hide_text {db.data[7]}"))
            
            btns_emoji = []
            emoji_and_var = []
            if db.data[6] != "None":
               
               sdd = db.data[6].split(",")
               for ceh in sdd:
                  if "\n" in ceh:
                     for res in ceh.split("\n"):
                        for ins in res.split("|"):
                           btns_emoji.append(types.InlineKeyboardButton(f"{ins}0", callback_data=f"reaction {ins}"))
                           
                           emoji_and_var.append(f"{ins}0")
                           
                        markup.add(*btns_emoji)
                        btns_emoji = []
                  else:
                     pdd = ceh.split("|")
                     
                     for res in pdd:
                        btns_emoji.append(types.InlineKeyboardButton(f"{res}0", callback_data=f"reaction {res}"))
                        
                        emoji_and_var.append(f"{res}0")
                     
                     markup.add(*btns_emoji)
                     btns_emoji = []
            
            all_channel += 1
            if db.data[11] == "None" and db.data[12] == "None" and db.data[13] == "None" and db.data[14] == "None" and db.data[15] == "None":
               try:
                  if db.data[4] == 1:
                     msg = await bot.send_message(channel, "".join(db.data[1]), parse_mode="html", reply_markup=markup)
               
                  elif db.data[4] == 2:
                     msg = await bot.send_message(channel, "".join(db.data[1]), parse_mode="markdown", reply_markup=markup)
                  
                  else:
                     msg = await bot.send_message(channel, "".join(db.data[1]), reply_markup=markup)
                  
               except CantParseEntities as e:
                     
                  msg = await bot.send_message(channel, "".join(db.data[1]), reply_markup=markup)
                  
                  await call.answer("🚫Такие символы не поддерживаются")
            else:
               try:
                  if db.data[10] != "None":
                     caption = db.data[10]
                  else:
                     caption = None
                  
                  if db.data[11] != "None":
                    msg = await db.bot.send_video(chat_id=channel, video=db.data[11], caption=caption, reply_markup=markup)
                    
                  elif db.data[12] != "None":
                     msg = await bot.send_video_note(chat_id=channel, video_note=db.data[12], caption=caption, reply_markup=markup)
                     
                  elif db.data[13] != "None":
                     msg = await bot.send_photo(chat_id=channel, photo=db.data[13], caption=caption, reply_markup=markup)
                        
                  elif db.data[14] != "None":
                     msg = await bot.send_voice(chat_id=channel, voice=db.data[14], caption=caption, reply_markup=markup)
                     
                  elif db.data[15] != "None":
                     msg = await bot.send_document(chat_id=channel, document=db.data[15], caption=caption, reply_markup=markup)
               
               except Exception as e:
                  pass
               
               successfull += 1
               
               react = db.cursor.execute("SELECT * FROM reaction_msg")
                
               db.cursor.execute("INSERT INTO reaction_msg (message_id, channel_id, emoji_and_var, used_reaction, url_button, reaction_button, name_hide_text, not_sub_text, sub_text) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (msg.message_id, channel, ",".join(emoji_and_var), "None", db.data[5], db.data[6], db.data[7], db.data[8], db.data[9]))
               db.conn.commit()
            #except Exception as e:
#               await call.answer("Пост не отправился в какаой то канал")
               
      await call.message.answer(f"✅Вы успешно опубликовали пост в каналах {successfull}/{all_channel}")
   elif call.data == "add_owner":
      await call.message.delete()
      
      password = db.cursor.execute("SELECT password FROM admin_data").fetchall()
      
      if password[0][0] == "None":
         db.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("GetUserIdForNewOwner", id))
         db.conn.commit()
         
         markup = types.InlineKeyboardMarkup()
         markup.add(types.InlineKeyboardButton("Отмена", callback_data="cancel"))
         
         await call.message.answer("Перешлите сюда сообщение нового владельца", reply_markup=markup)
         
         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
         btn = types.KeyboardButton("Отправить через список", request_user=types.KeyboardButtonRequestUser(request_id=9876, user_is_bot=False))
         
         markup.add(btn)
         
         await call.message.answer("Вы также можете отправить из своего списка", reply_markup=markup)
      else:
         db.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("GetPassword", id))
         db.conn.commit()
         
         markup = types.InlineKeyboardMarkup()
         markup.add(types.InlineKeyboardButton("Отмена", callback_data="cancel"))
         
         await call.message.answer("Отправьте сюда пароль, чтобы вы смогли добавить нового владельца", reply_markup=markup)
   elif call.data == "del_owner":
      await call.message.delete()
      
      password = db.cursor.execute("SELECT password FROM admin_data").fetchall()
      
      if password[0][0] == "None":
         markup = types.InlineKeyboardMarkup(row_width=1)
         
         for owner in db.cursor.execute("SELECT * FROM admin_data").fetchall():
            markup.add(types.InlineKeyboardButton(f"{owner[0]}", callback_data=f"del_owner {owner[0]}"))
         markup.add(types.InlineKeyboardButton("Отмена", callback_data="cancel"))
         
         await call.message.answer("Выберите владельца для удаления", reply_markup=markup)
      else:
         db.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("GetPasswordForDelOwner", id))
         db.conn.commit()
         
         markup = types.InlineKeyboardMarkup()
         markup.add(types.InlineKeyboardButton("Отмена", callback_data="cancel"))
         
         await call.message.answer("Отправьте сюда пароль, чтобы вы смогли удалить владельца", reply_markup=markup)
   elif call.data == "set_password":
      await call.message.delete()
      
      password = db.cursor.execute("SELECT password FROM admin_data").fetchall()
      
      markup = types.InlineKeyboardMarkup()
      markup.add(types.InlineKeyboardButton("Отмена", callback_data="cancel"))
      
      if password[0][0] == "None":
         db.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("setPassword", id))
         db.conn.commit()
         
         await call.message.answer("Введите будущий пароль", reply_markup=markup)
      else:
         db.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("GetPasswordForNew", id))
         db.conn.commit()
         
         await call.message.answer("Введите текущий пароль", reply_markup=markup)

@dp.message_handler(content_types=["chat_shared"])
async def chat_shared(message: types.Message):
   print(message)
   
   await db.check_db(message)
   
   id = message.from_user.id
   
   markup = types.InlineKeyboardMarkup()
   markup.add(types.InlineKeyboardButton("Отмена", callback_data="cancel"))
   
   if db.data[2] == "waitForwardMessage":
      try:
         channel = await bot.get_chat(message.chat_shared["chat_id"])
      except Exception as e:
         return await message.answer(f"Бота нету или он не является администратором в вашем канале, назначьте бота администратором (ему достаточно лишь изменять и писать сообщение) {e}", reply_markup=markup)
      
      db.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("None", id))
      db.conn.commit()
      
      if db.data[3] == "None":
         db.cursor.execute("UPDATE admin_data SET channel = ? WHERE user_id = ?", (f"{message.chat_shared['chat_id']}", id))
         db.conn.commit()
      else:
         if str(message.chat_shared["chat_id"]) in db.data[3]:
            await message.answer("Этот канал уже есть в боте")
         else:
            db.cursor.execute("UPDATE admin_data SET channel = ? WHERE user_id = ?", (f"{db.data[3]}|{message.chat_shared['chat_id']}", id))
            db.conn.commit()
      
      await message.delete()
      #await bot.delete_message(chat_id=message.from_user.id, message_id=int(message.message_id) - 1)
      #await bot.delete_message(chat_id=message.from_user.id, message_id=int(message.message_id) - 2)
      
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      markup.add("📲Отправить пост")
      markup.add("⚙️Настройки")
      
      await message.answer(f"Вы успешно добавили {channel.title} в бота", reply_markup=markup)
      
      await db.check_db(message)
      
      await db.option(call)

@dp.message_handler(content_types=["user_shared"])
async def user_shared(message: types.Message):
   await db.check_db(message)
   
   id = message.from_user.id
   print(message.user_shared.user_id)
   
   if db.data[2] == "GetUserIdForNewOwner":
      db.cursor.execute("INSERT OR IGNORE INTO admin_data (user_id) VALUES (?)", (message.user_shared.user_id,))
      db.conn.commit()
      
      db.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("None", id))
      db.conn.commit()
      
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      markup.add("📲Отправить пост")
      markup.add("⚙️Настройки")
      
      await message.answer("Вы успешно добавили нового владельца", reply_markup=markup)

if "__main__" == __name__:
   executor.start_polling(dp)
