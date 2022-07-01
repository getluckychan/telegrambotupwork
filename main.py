import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot('5395238480:AAH-77uvOL1pSA110SxEJ-ZaHLF8I60fTNE')

questions = []
id_of_new_users = []
checked_id = []
chat_id = int
all_users = {}
rule = str

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type == 'private' and message.from_user.id == 360809721:
        bot.send_message(message.from_user.id, 'Lets get started')
        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('Add question')
        itembtn2 = types.KeyboardButton('Show all questions')
        itembtn3 = types.KeyboardButton('Delete question')
        itembtn4 = types.KeyboardButton('Ban someone')
        itembtn5 = types.KeyboardButton('Add rules')
        itembtn6 = types.KeyboardButton('Delete rules')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)
        bot.send_message(message.chat.id, "Choose one letter:", reply_markup=markup)


def gen_markup1():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Approve", callback_data="cb_yes"),
               InlineKeyboardButton("Deny", callback_data="cb_no"))
    return markup


def gen_markup2():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1

    for i in questions:
        markup.add(InlineKeyboardButton(f'{i}', callback_data=f'{i}'))
    return markup


def gen_markup3():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    items = all_users.items()
    for i in items:
        markup.add(InlineKeyboardButton(f'{i[1]}', callback_data=i[0]))
    return markup


@bot.message_handler(content_types=["new_chat_members"])
def handler_new_member(message):
    user_name = message.from_user.username
    id_of_new_users.append(message.from_user.id)
    all_users.update({message.from_user.id: f'@{message.from_user.username}'})
    b = ""
    bot.send_message(message.chat.id, f'{id_of_new_users}')
    for i in questions:
        b += f'{i[1:]}\n'
    bot.send_message(message.chat.id, f'Hi, @{user_name}!, '
                                      f'\nPlease answer for this questions: \n'
                                      f'{b}\n'
                                      f'Please, start your message with "My answer is:" and write it in one message')


@bot.message_handler(content_types=["left_chat_members"])
def handler_lest_member(message):
    all_users.pop(message.from_user.id)


@bot.message_handler(content_types=["text"])
def check_massage(message):
    global chat_id
    chat_id = message.chat.id
    if message.chat.type == 'private' and message.from_user.id == 360809721 and message.text == 'Ban someone':
        bot.reply_to(message, 'Who do you want to ban?', reply_markup=gen_markup3())

    if message.chat.type == 'private' and message.from_user.id == 360809721 and message.text == 'Add question':
        bot.reply_to(message, 'Write a question started with #')
    elif message.chat.type == 'private' and message.from_user.id == 360809721 and '#' in message.text:
        questions.append(message.text)
    elif message.chat.type == 'private' and message.from_user.id == 360809721 and message.text == 'Show all questions':
        try:
            b = ""
            v = 0
            for i in questions:
                v += 1
                b += f'{v}: {i}\n'
            bot.reply_to(message, f'{b}')
        except:
            bot.reply_to(message, 'There is no questions')

    elif message.chat.type == 'private' and message.from_user.id == 360809721 and message.text == 'Delete question':
        bot.reply_to(message, 'What question you want to delete?', reply_markup=gen_markup2())
    for i in id_of_new_users:
        if message.from_user.id == i and 'My answer is' in message.text:
            checked_id.append(message.from_user.id)
            bot.send_message(message.chat.id, f'{checked_id}')
            bot.send_message(360809721, f'Answer from @{message.from_user.username}'
                                        f'\n{message.text}',
                             reply_markup=gen_markup1())
            bot.delete_message(message.chat.id, message.message_id)
        elif message.from_user.id == i and 'My answer is' not in message.text:
            bot.delete_message(message.chat.id, message.message_id)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_yes":
        try:
            id_of_new_users.remove(checked_id[0])
            checked_id.pop(0)
            bot.answer_callback_query(call.id, "User is allowed to chat")
        except ValueError:
            bot.answer_callback_query(call.id, "Can`t find this user")
    elif call.data == "cb_no":
        try:
            id_of_new_users.remove(checked_id[0])
            bot.kick_chat_member(chat_id, checked_id[0])
            checked_id.pop(0)
            bot.answer_callback_query(call.id, "User is not allowed to chat")
        except ValueError:
            bot.answer_callback_query(call.id, "Can`t find this user")
    for i in questions:
        if i == call.data:
            questions.remove(i)
            bot.answer_callback_query(call.id, f'Question "{call.data}" was deleted')
    for key in all_users:
        if key == call.data:
            bot.ban_chat_member(chat_id, key, revoke_messages=True)
            all_users.pop(key)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
