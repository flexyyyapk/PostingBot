from aiogram import Bot, types
import asyncio
import sqlite3
from aiogram.utils.exceptions import *

class DataBase:
   def __init__(self, db, bot):
      self.conn = sqlite3.connect(db)
      self.cursor = self.conn.cursor()
      
      self.bot = bot
      
      self.cursor.execute("""CREATE TABLE IF NOT EXISTS admin_data(
      user_id INTEGER PRIMARY KEY,
      text TEXT DEFAULT 'None',
      room TEXT DEFAULT 'None',
      channel TEXT DEFAULT 'None',
      parse_mode INTEGER DEFAULT 0,
      url_button TEXT DEFAULT 'None',
      reaction_button TEXT DEFAULT 'None',
      name_hide_text TEXT DEFAULT 'None',
      not_sub_text TEXT DEFAULT 'None',
      sub_text TEXT DEFAULT 'None',
      caption TEXT DEFAULT 'None',
      video TEXT DEFAULT 'None',
      video_note TEXT DEFAULT 'None',
      photo TEXT DEFAULT 'None',
      voice TEXT DEFAULT 'None',
      document TEXT DEFAULT 'None',
      password TEXT DEFAULT 'None'
      )""")
      
      self.cursor.execute("""CREATE TABLE IF NOT EXISTS reaction_msg(
      message_id INTEGER,
      channel_id INTEGER,
      emoji_and_var TEXT,
      used_reaction TEXT,
      url_button TEXT,
      reaction_button TEXT,
      name_hide_text TEXT,
      not_sub_text TEXT,
      sub_text TEXT,
      PRIMARY KEY (message_id, channel_id)
      )""")
      
      self.conn.commit()
   async def check_db(self, message):
      self.data = self.cursor.execute("SELECT * FROM admin_data WHERE user_id = ?", (message.from_user.id,)).fetchone()
      
      self.reac = self.cursor.execute("SELECT * FROM reaction_msg").fetchone()
      
      if not self.data:
         return "dont in base"
      else:
         return "all ok"
   async def call_check_db(self, call):
      self.data = self.cursor.execute("SELECT * FROM admin_data WHERE user_id = ?", (call.from_user.id,)).fetchone()
      
      self.reac = self.cursor.execute("SELECT * FROM reaction_msg").fetchone()
      
      if not self.data:
         return "dont in base"
      else:
         return "all ok"
   async def edit_message(self, message):
      await self.check_db(message)
      
      self.id = message.from_user.id
      
      if self.data[3] == "None":
         return await message.answer("К сожалению, вы ещё не добавили свой канал(⚙️Настройки --> ➕Добавить канал)")
      
      if any(keys in self.data[2] for keys in ["editMessage", "addUrlButton", "addReactionButton"]):
         pass
      else:
         if self.data[11] == "None" and self.data[12] == "None" and self.data[13] == "None" and self.data[14] == "None" and self.data[15] == "None":
            await message.delete()
            await self.bot.delete_message(chat_id=message.from_user.id, message_id=int(message.message_id) - 1)
            
            await self.bot.delete_message(chat_id=message.from_user.id, message_id=int(message.message_id) - 2)
      
      if any(keys in self.data[2] for keys in ["addUrlButton", "addReactionButton", "None"]):
         pass
      else:
         if self.data[11] == "None" and self.data[12] == "None" and self.data[13] == "None" and self.data[14] == "None" and self.data[15] == "None":
            #self.cursor.execute("UPDATE admin_data SET text = ? WHERE user_id = ?", (message.text, self.id))
            #self.conn.commit()
            pass
         else:
            pass
      
      self.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("None", self.id))
      self.conn.commit()
      
      await self.check_db(message)
      
      markup = types.InlineKeyboardMarkup()
      
      if self.data[5] != "None":
         self.spl = self.data[5].split(",")
         
         self.btn_row = []
         for btn in self.spl:
            if not "|" in btn:
               self.splr = "".join(btn).split("-")
               if not self.splr:
                  pass
               else:
                  markup.add(types.InlineKeyboardButton(f"{self.splr[0]}", url=f"{self.splr[1]}"))
            else:
               self.palk = "".join(btn).split("|")
               for palka in self.palk:
                  self.ch = "".join(palka).split("-")
                  
                  if not self.ch:
                     pass
                  else:
                     self.btn_row.append(types.InlineKeyboardButton(f"{self.ch[0]}", url=f"{self.ch[1]}"))
                  
               markup.add(*self.btn_row)
      
      if self.data[7] != "None":
         for rec in self.data[7].split(","):
            markup.add(types.InlineKeyboardButton(f"{''.join(rec)}", callback_data="example"))
      
      btns_emoji = []
      if self.data[6] != "None":
         self.sdd = self.data[6].split(",")
         for ceh in self.sdd:
            if "\n" in ceh:
               for res in ceh.split("\n"):
                  for ins in res.split("|"):
                     btns_emoji.append(types.InlineKeyboardButton(f"{ins}", callback_data="exampl"))
                  markup.add(*btns_emoji)
                  btns_emoji = []
            else:
               self.pdd = ceh.split("|")
               
               for res in self.pdd:
                  btns_emoji.append(types.InlineKeyboardButton(f"{res}", callback_data="exampl"))
               
               markup.add(*btns_emoji)
               btns_emoji = []
      
      if self.data[1] != "None" or self.data[10] != "None":
         markup.add(types.InlineKeyboardButton("📝Изменить", callback_data="editMessage"))
      
      if self.data[4] == 1:
         markup.add(types.InlineKeyboardButton("🟢Фонт: html", callback_data="parsing"))
      elif self.data[4] == 2:
         markup.add(types.InlineKeyboardButton("🟢Фонт: MarkDown", callback_data="parsing"))
      else:
         markup.add(types.InlineKeyboardButton("🔴Фонт: выкл", callback_data="parsing"))
      
      markup.add(types.InlineKeyboardButton("🔗URL Кнопка", callback_data="add_url_button"))
      
      markup.add(types.InlineKeyboardButton("❤️Реакции", callback_data="reactionMessage"))
      
      if self.data[7] == "None":
         markup.add(types.InlineKeyboardButton("😶‍🌫Скрытый текст", callback_data="hideText"))
      
      markup.add(types.InlineKeyboardButton("💬Запостить", callback_data="postMessage"))
      if self.data[11] == "None" and self.data[12] == "None" and self.data[13] == "None" and self.data[14] == "None" and self.data[15] == "None":
         if self.data[4] == 1:
            
            try:
               
               await message.answer(f"{self.data[1]}", reply_markup=markup, parse_mode="html")
            
            except CantParseEntities as e:
               
               await message.answer(f"{self.data[1]}", reply_markup=markup)
         elif self.data[4] == 2:
            
            try:
               
               await message.answer(f"{self.data[1]}", reply_markup=markup, parse_mode="markdownv2")
            
            except CantParseEntities as e:
               
               await message.answer(f"{self.data[1]}", reply_markup=markup)
            
         else:
            await message.answer(f"{self.data[1]}", reply_markup=markup)
               
      else:
         if self.data[10] != "None":
            self.caption = self.data[10]
         else:
            self.caption = None
         
         if self.data[11] != "None":
           await self.bot.send_video(chat_id=message.chat.id, video=self.data[11], caption=self.caption, reply_markup=markup)
           
         elif self.data[12] != "None":
            await self.bot.send_video_note(chat_id=message.chat.id, video_note=self.data[12], caption=self.caption, reply_markup=markup)
         elif self.data[13] != "None":
            await self.bot.send_photo(chat_id=message.chat.id, photo=self.data[13], caption=self.caption, reply_markup=markup)
         elif self.data[14] != "None":
            await self.bot.send_voice(chat_id=message.chat.id, voice=self.data[14], caption=self.caption, reply_markup=markup)
         elif self.data[15] != "None":
            await self.bot.send_document(chat_id=message.chat.id, document=self.data[15], caption=self.caption, reply_markup=markup)
   async def call_edit_message(self, call):
      await self.call_check_db(call)
      
      self.id = call.from_user.id
      
      if self.data[3] == "None":
         return await call.message.answer("К сожалению, вы ещё не добавили свой канал(⚙️Настройки --> ➕Добавить канал)")
      
      self.cursor.execute("UPDATE admin_data SET room = ? WHERE user_id = ?", ("None", self.id))
      self.conn.commit()
      
      await self.call_check_db(call)
      
      markup = types.InlineKeyboardMarkup()
      
      btns_emoji = []
      if self.data[6] != "None":
         self.sdd = self.data[6].split(",")
         for ceh in self.sdd:
            if "\n" in ceh:
               for res in ceh.split("\n"):
                  for ins in res.split("|"):
                     btns_emoji.append(types.InlineKeyboardButton(f"{ins}", callback_data="exampl"))
                  markup.add(*btns_emoji)
                  btns_emoji = []
            else:
               self.pdd = ceh.split("|")
               
               for res in self.pdd:
                  btns_emoji.append(types.InlineKeyboardButton(f"{res}", callback_data="exampl"))
               
               markup.add(*btns_emoji)
               btns_emoji = []
      
      if self.data[5] != "None":
         self.spl = self.data[5].split(",")
         
         self.btn_row = []
         for btn in self.spl:
            if not "|" in btn:
               self.splr = "".join(btn).split("-")
               if not self.splr:
                  pass
               else:
                  markup.add(types.InlineKeyboardButton(f"{self.splr[0]}", url=f"{self.splr[1]}"))
            else:
               self.palk = "".join(btn).split("|")
               for palka in self.palk:
                  self.ch = "".join(palka).split("-")
                  
                  if not self.ch:
                     pass
                  else:
                     self.btn_row.append(types.InlineKeyboardButton(f"{self.ch[0]}", url=f"{self.ch[1]}"))
                  
               markup.add(*self.btn_row)
      
      if self.data[1] != "None" or self.data[10] != "None":
         markup.add(types.InlineKeyboardButton("📝Изменить", callback_data="editMessage"))
      
      if self.data[4] == 1:
         markup.add(types.InlineKeyboardButton("🟢Фонт: html", callback_data="parsing"))
      elif self.data[4] == 2:
         markup.add(types.InlineKeyboardButton("🟢Фонт: MarkDown", callback_data="parsing"))
      elif self.data[4] == 0:
         markup.add(types.InlineKeyboardButton("🔴Фонт: выкл", callback_data="parsing"))
      
      markup.add(types.InlineKeyboardButton("🔗URL Кнопка", callback_data="add_url_button"))
      
      if self.data[7] == "None":
         markup.add(types.InlineKeyboardButton("😶‍🌫Скрытый текст", callback_data="hideText"))
      
      markup.add(types.InlineKeyboardButton("❤️Реакции", callback_data="reactionMessage"))
      
      markup.add(types.InlineKeyboardButton("💬Запостить", callback_data="postMessage"))
       
      if self.data[11] == "None" and self.data[12] == "None" and self.data[13] == "None" and self.data[14] == "None" and self.data[15] == "None":
         if self.data[4] == 1:
            
            try:
               await call.message.edit_text(f"{self.data[1]}", reply_markup=markup, parse_mode="html")
               
            except CantParseEntities as e:
               
               await call.message.edit_text(f"{self.data[1]}", reply_markup=markup)
               
               await call.answer("🚫Такие символы не поддерживаются")
         
         elif self.data[4] == 2:
            
            try:
               await call.message.edit_text(f"{self.data[1]}", reply_markup=markup, parse_mode="markdownv2")
               
            except CantParseEntities as e:
               
               await call.message.edit_text(f"{self.data[1]}", reply_markup=markup)
               
               await call.answer("🚫Такие символы не поддерживаются")
         
         else:
            await call.message.edit_text(f"{self.data[1]}", reply_markup=markup)
      else:
        if self.data[10] != "None":
           self.caption = db.data[10]
        else:
           self.caption = None
        
        if self.data[11] != "None":
           await self.bot.send_video(chat_id=message.chat.id, video=self.data[11], caption=self.caption, reply_markup=markup)
           
        elif self.data[12] != "None":
               await self.bot.send_video_note(chat_id=message.chat.id, video_note=self.data[12], caption=self.caption, reply_markup=markup)
        elif self.data[13] != "None":
               await self.bot.send_photo(chat_id=message.chat.id, photo=self.data[13], caption=self.caption, reply_markup=markup)
        elif self.data[14] != "None":
               await self.bot.send_voice(chat_id=message.chat.id, voice=self.data[14], caption=self.caption, reply_markup=markup)
        elif self.data[15] != "None":
               await self.bot.send_document(chat_id=message.chat.id, document=self.data[15], caption=self.caption, reply_markup=markup)
   async def option(self, message):
      print("test")
      
      self.markup = types.InlineKeyboardMarkup()
      self.markup.add(types.InlineKeyboardButton("➕Добавить канал", callback_data="add_channel"))
            
      self.markup.add(types.InlineKeyboardButton("➖Удалить канал", callback_data="delete_channel"))
            
      self.markup.add(types.InlineKeyboardButton("➕👤Добавить владельца", callback_data="add_owner"))
            
      self.markup.add(types.InlineKeyboardButton("➖👤Убрать владельца", callback_data="del_owner"))
      
      self.markup.add(types.InlineKeyboardButton("🔐Поставить пароль", callback_data="set_password"))
      
      self.is_channel = "Нету"
      if self.data[3] == "None":
         self.is_channel = "Нету"
      else:
         self.is_channel = ""
               
         for chann in self.data[3].split("|"):
            if chann:
               try:
                  await self.bot.get_chat(chat_id=int(chann))
                        
                  self.chakis = await self.bot.get_chat(chat_id=int(chann))
                        
                  self.is_channel += f"{self.chakis.title}\n"
               except Exception as e:
                  self.is_channel += "(Пустой канал)\n"
      
      self.owners = ""
      for owner in self.cursor.execute("SELECT user_id FROM admin_data").fetchall():
         owner = str(owner).replace(",", "")
         owner = str(owner).replace("(", "")
         owner = str(owner).replace(")", "")
         
         self.owners += f"{owner}\n"
      
      self.status_password = "🔓Нету"
      if self.data[16] == "None":
         pass
      else:
         self.status_password = "🔒Стоит"
      
      await message.answer(f"Статус пароля: {self.status_password}\n\nВаши каналы: {self.is_channel}\n\nВладельцы: {self.owners}", reply_markup=self.markup)
   async def call_option(self, call):
      self.markup = types.InlineKeyboardMarkup()
      self.markup.add(types.InlineKeyboardButton("➕Добавить канал", callback_data="add_channel"))
            
      self.markup.add(types.InlineKeyboardButton("➖Удалить канал", callback_data="delete_channel"))
            
      self.markup.add(types.InlineKeyboardButton("➕👤Добавить владельца", callback_data="add_owner"))
            
      self.markup.add(types.InlineKeyboardButton("➖👤Убрать владельца", callback_data="del_owner"))
      
      self.markup.add(types.InlineKeyboardButton("🔐Поставить пароль", callback_data="set_password"))
      
      self.is_channel = "Нету"
      if self.data[3] == "None":
         self.is_channel = "Нету"
      else:
         self.is_channel = ""
               
         for chann in self.data[3].split("|"):
            if chann:
               try:
                  await self.bot.get_chat(chat_id=int(chann))
                        
                  self.chakis = await self.bot.get_chat(chat_id=int(chann))
                        
                  self.is_channel += f"{self.chakis.title}\n"
               except Exception as e:
                  self.is_channel += "(Пустой канал)\n"
      
      self.owners = ""
      for owner in self.cursor.execute("SELECT user_id FROM admin_data").fetchall():
         owner = str(owner).replace(",", "")
         owner = str(owner).replace("(", "")
         owner = str(owner).replace(")", "")
         
         self.owners += f"{owner}\n"
      
      self.status_password = "🔓Нету"
      if self.data[16] == "None":
         pass
      else:
         self.status_password = "🔒Стоит"
      
      await call.message.answer(f"Статус пароля: {self.status_password}\n\nВаши каналы: {self.is_channel}\n\nВладельцы: {self.owners}", reply_markup=self.markup)
