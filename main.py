import telebot
from token import TOKEN
from telebot import types
from komunbot.db import init_db, add_message, get_messages, get_message, set_messages_worker_user
from komunbot.petitiondb import init_petition_db, add_petition
from komunbot.usersdatabase import init_user_db, register_user, get_user, get_user_id
from komunbot.workers import init_workers_db, add_workers, сhoose_workers, get_positions, get_user_positions, get_workers
from komunbot.indexesdatabase import init_indexes_db, write_indexes


bot = telebot.TeleBot(TOKEN)
init_db()
init_petition_db()
init_user_db()
init_indexes_db()
init_workers_db()

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id,
                     "Доброго дня, {0.first_name}!\nЯ комунальний бот  - <b>{1.first_name}</b>, "
                     "Мій господар поручив мені дізнаватися про всі події та повідомляти його про них для їх усунення.\n"
                     "<b>Прошу зареєструатись. Для цього потрібно записати таким чином: \n"
                     "/registration (Прізвище), (Ім'я), (Номер квартири)</b>\n \n "
                     "Для перегляду основного набору команд введіть /help".format(
                         message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=["registration"])
def regatration(message):
    user_data = get_user(message.from_user.id)
    if user_data:
        bot.send_message(message.chat.id, 'Користувач уже зареєстрований')
    else:
        try:
            answer = message.text
            answer = str(answer)
            answer = answer.replace('/registration', '')
            new_answer = answer.split(',')
            prizvuche = new_answer[0]
            name = new_answer[1]
            home = new_answer[2]
            register_user(user_id = message.from_user.id,
                          username = message.from_user.first_name,
                          first_name = name,
                          last_name = prizvuche,
                          flat = home)
            bot.send_message(message.chat.id, 'Користувачa зареєстрованo')
        except IndexError:
            bot.send_message(message.chat.id, 'Повідомлення не записано . Перевірте форму запису!')



@bot.message_handler(commands=["help"])
def help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id,
                     "В мої функії входить:\n \n"
                     "Повідомляти госпдаря про події,що сталися   \n "
                     "<b>Записувати потрібно таким чином </b>: \n"
                     "/komunmessage (що сталося) , (де саме) \n \n"
                     "Повідомляти вас про події,які стануться та можу передавти петиції господарю \n "
                     "<b>Записувати потрібно таким чином:</b> \n"
                     "/bossmessage (петиція)\n \n"
                     "Зчитувати ваші показники за світло,гарячу та холодну воду, газ \n"
                     "<b>Записувати потрібно таким чином:</b> \n " 
                     "/indexes (показники за світло),(показники за холодну воду),(показники за гарячу воду),(показники за газ)\n \n"
                     "Для того щоб перейти до меню функцій для персоналу викличіть /headhelp"
                     , parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=["komunmessage"], content_types=["text"])
def kmessage(message):
    answer = message.text
    answer = str(answer)
    answer = answer.replace('/komunmessage', '')
    new_answer = answer.split(',')
    try:
        answer_text = str(new_answer[0])
        answer_adres = str(new_answer[1])
        add_message(user_id=message.from_user.id,
                    first_name=message.from_user.first_name,
                    adres=answer_adres,
                    text=answer_text)
        bot.send_message(message.chat.id, 'Повідомлення записано')
    except IndexError:
        bot.send_message(message.chat.id, 'Повідомлення не записано . Перевірте форму запису! /help')


@bot.message_handler(commands=["indexes"], content_types=["text"])
def indexes(message):
    try:
        answer = message.text
        answer = str(answer)
        answer = answer.replace('/indexes', '')
        new_answer = answer.split(',')
        indexes_data = get_user(message.from_user.id)
        l = new_answer[0]
        c = new_answer[1]
        h = new_answer[2]
        g = new_answer[3]
        write_indexes(user_id = message.from_user.id,
                  username= message.from_user.first_name,
                  light= l,
                  cold_water= c ,
                  hot_water= h ,
                  gas= g)
        bot.send_message(message.chat.id, 'Показники записано')
    except:
        bot.send_message(message.chat.id, 'Показники не записано . Перевірте форму запису! /help')


@bot.message_handler(commands=["headhelp"], content_types=["text"])
def headhelp(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id,
                     "В мої функії входить:\n \n"
                     "Повідомляти користувачів про події \n "
                     "<b>Записувати потрібно таким чином:</b> \n"
                     "/headmessage (повідомлення) \n \n "
                     "Для того,щоб опублікувати заявку про проблему: \n "
                     "<b>Записувати потрібно таким чином:</b> \n"
                     "/approve_message (id заявки) \n\n"
                     "Для показу не оброблених заявок: \n"
                     "/not_addoption_messages \n \n"
                     "Для показу усіх робітників: \n "
                     "/showworkers\n \n"
                     "Для того, щоб зареєструватись введіть ключ реєстрації \n " #ключ = "/Vylutsa_Shevchenka"
                     , parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=["Vylutsa_Shevchenka"], content_types=["text"])
def registration(message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    items = []
    for position_id, position_name in get_positions():
        items.append(types.InlineKeyboardButton(position_name, callback_data=f'set_position_{position_id}'))
    markup.add(*items)
    bot.send_message(message.chat.id, 'Оберіть професію', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('set_position'))
def set_position(call):
    user_id = int(call.from_user.id)
    position_id = ((call.data).replace('set_position', ''))

    user_positions = get_user_positions(user_id=user_id)
    for _id, name in user_positions:
        if _id == position_id:
            bot.answer_callback_query(callback_query_id=call.id, text='Дана посада вже була додана!')
            return

    add_workers(user_id=int(call.from_user.id), position_id= call.data)
    bot.answer_callback_query(callback_query_id=call.id, text='Посада додана!')


@bot.callback_query_handler(func=lambda call: call.data.startswith('approve_message'))
def approve_message_user(call):
    message_id, user_id = call.data.replace('approve_message', '').split('_')
    set_messages_worker_user(message_id, user_id)
    bot.answer_callback_query(callback_query_id=call.id, text='Заявка передана!')


@bot.message_handler(commands=["showworkers"], content_types=["text"])
def show_workers(message):
    if message.from_user.id not in head:
        bot.send_message(message.chat.id, 'Доступ заборонено!')
        return

    workers = get_workers()
    items = []
    for user_id, first_name, last_name, position_name in workers:
        items.append(f'{last_name} {first_name}: {position_name}')
    bot.send_message(message.chat.id, '\n'.join(items))


@bot.message_handler(commands=["not_addoption_messages"], content_types=["text"])
def show_not_addoption_messages(message):
    if message.from_user.id not in head:
        bot.send_message(message.chat.id, 'Доступ заборонено!')
        return

    messages = get_messages()
    if messages:
        items = []
        for _id, first_name, last_name, text, adres in messages:
            items.append(f'#{_id}, {last_name} {first_name}: {text}')
        bot.send_message(message.chat.id, '\n'.join(items))
    else:
        bot.send_message(message.chat.id, 'Немає повідомлень!')


@bot.message_handler(commands=["approve_message"], content_types=["text"])
def approve_message(message):
    if message.from_user.id not in head:
        bot.send_message(message.chat.id, 'Доступ заборонено!')
        return

    answer = message.text
    answer = str(answer)
    message_id = answer.replace('/approve_message', '').strip()
    try:
        message_id = int(message_id)
    except ValueError:
        bot.send_message(message.chat.id, 'Вкажіть ІД повідомлення')
        return

    user_message = get_message(message_id=message_id)
    if not user_message:
        bot.send_message(message.chat.id, 'Повідомлення не знайдено')
        return

    bot.send_message(message.chat.id, f'Повідомлення №{user_message.id}\n{user_message.text}')

    markup = types.InlineKeyboardMarkup(row_width=3)
    items = []
    for user_id, first_name, last_name, position_name in get_workers():
        items.append(types.InlineKeyboardButton(f'{first_name} {last_name}: {position_name}',
                                                callback_data=f'approve_message_{message_id}_{user_id}'))
    markup.add(*items)
    bot.send_message(message.chat.id, 'Оберіть виконавця', reply_markup=markup)


@bot.message_handler(commands=["headmessage"], content_types=["text"])
def headmessage(message):
    count = 0
    for j in head:
        answer = message.text
        answer = str(answer)
        answer = answer.replace('/headmessage', '')
        if answer == '':
            bot.send_message(message.chat.id, 'Повідомлення не записано . Перевірте форму запису! /help')
            break
        if message.from_user.id == j:
            id = get_user_id()
            count += 1
            for user in id:
                s = str(user)
                s = s.replace("(", "")
                s = s.replace(",", "")
                s = s.replace(")", "")
                bot.send_message(int(s), answer)
        else:
            bot.send_message("Вам не надано права керівника")


head = [770746424]


@bot.message_handler(commands=["bossmessage"], content_types=["text"])
def boss(message):
    answer = message.text
    answer = str(answer)
    answer = answer.replace('/bossmessage', '')
    try:
        if answer == '':
            bot.send_message(message.chat.id, 'Повідомлення не записано . Перевірте форму запису! /help')
        else:
            add_petition(user_id=message.from_user.id,
                         first_name=message.from_user.first_name,
                         petition=answer)
            bot.send_message(message.chat.id, 'Повідомлення записано')
    except:
        bot.send_message(message.chat.id, 'Повідомлення не записано . Перевірте форму запису! /help')


if __name__ == '__main__':
    bot.infinity_polling()
bot.polling()
