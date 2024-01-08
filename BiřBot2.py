import datetime
import logging
import re
from token import token

import bs4
import requests
import telebot
from telebot import types, TeleBot

l_1 = logging
l_2 = logging

l_1.basicConfig(filename='bot.log', level=logging.DEBUG,
                format=' %(asctime)s - %(levelname)s - %(message)s')

l_2.basicConfig(filename='bot_info.log', level=logging.INFO,
                format=' %(asctime)s - %(levelname)s - %(message)s')


bot: TeleBot = telebot.TeleBot(token)

trz = float(31.1035)

# Курс доллара
page_usd = 'https://www.sberometer.ru/cbr/'

page_html = requests.get(page_usd).text
soup_usd = bs4.BeautifulSoup(page_html, 'lxml')
s = soup_usd.findAll('tr')
s_2 = s[2].getText('/')
s_3 = s[3].getText('/')
USD = None
if s_2.split('/')[1] == datetime.datetime.now().strftime("%d.%m.%Y"):
    USD = s_2.split('/')[4]
if s_3.split('/')[1] == datetime.datetime.now().strftime("%d.%m.%Y"):
    USD = s_3.split('/')[4]
if USD is None:
    USD = s_2.split('/')[4]

usd = float(USD[:USD.index('.') + 3])

# Родий
page_rh = 'https://autokatrecycle.ru/wp-content/themes/autokat/bot_telegram_export.php'
cookies = {'beget': 'begetok'}

page_rh_html = requests.get(url=page_rh, cookies=cookies).text
soup_rh = bs4.BeautifulSoup(page_rh_html, 'lxml')
s_1 = soup_rh.findAll('tr')

rh_bid_str = s_1[3].getText()
rh_b = re.findall(r'\d+', rh_bid_str)
rh_bid = float(rh_b[0])
# rh_ask_str = s_1[4].getText()
# rh_a = re.findall(r'\d+', rh_ask_str)
# rh_ask = float(rh_a[0])
ba = (rh_bid+4450) / 2

# Платина
page_pt_html = requests.get(url=page_rh, cookies=cookies).text
soup_pt = bs4.BeautifulSoup(page_pt_html, 'lxml')
s_2 = soup_pt.findAll('tr')
pt_str = s_2[1].getText()
ptt = re.findall(r'\d+', pt_str)
Pt = float(ptt[0])

# Палладий
page_pd_html = requests.get(url=page_rh, cookies=cookies).text
soup_pd = bs4.BeautifulSoup(page_pd_html, 'lxml')
s_3 = soup_pd.findAll('tr')
pd_str = s_3[2].getText()
pdd = re.findall(r'\d+', pd_str)
Pd = float(pdd[0])

PT = str(((Pt * usd) / trz)).split('.')[0]  # рубли по 100%
PD = str(((Pd * usd) / trz)).split('.')[0]
RAV = str(((ba * usd) / trz)).split('.')[0]
RA = str(((rh_bid * usd) / trz)).split('.')[0]

#Металл
imp_ch = re.findall(r'\d+', s_1[8].getText())
bmv_ch = re.findall(r'\d+', s_1[7].getText())
lex_ch = re.findall(r'\d+', s_1[12].getText())
inf_ch = re.findall(r'\d+', s_1[11].getText())
lan_ch = re.findall(r'\d+', s_1[9].getText())
ros_ch = re.findall(r'\d+', s_1[6].getText())
com_ch = re.findall(r'\d+', s_1[10].getText())

imp_v = re.findall(r'\d+', s_1[15].getText())
bmv_v = re.findall(r'\d+', s_1[14].getText())
lex_v = re.findall(r'\d+', s_1[19].getText())
inf_v = re.findall(r'\d+', s_1[18].getText())
lan_v = re.findall(r'\d+', s_1[16].getText())
ros_v = re.findall(r'\d+', s_1[13].getText())
com_v = re.findall(r'\d+', s_1[17].getText())


M = {'Импорт': [imp_ch[0], imp_v[0], imp_v[0]],
     'БМВ': [bmv_ch[0], bmv_v[0], bmv_v[0]],
     'Лексус': [lex_ch[0], lex_v[0], lex_v[0]],
     'Инфинити': [inf_ch[0], inf_v[0], inf_v[0]],
     'Ланос': [lan_ch[0], lan_v[0], lan_v[0]],
     'Россия': [ros_ch[0], ros_v[0], ros_v[0]],
     'Коммерция': [com_ch[0], com_v[0], com_v[0]]}


def catalog_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    count_lme = types.KeyboardButton(text="Посчитать биржу по заданным процентам")
    qotes = types.KeyboardButton(text="Котировки на сегодняшний день")
    price = types.KeyboardButton(text="Узнать стоимость за кг")
    metalls = types.KeyboardButton(text="Цены на металл")
    vm = types.KeyboardButton(text="Узнать цену за кг (ВМ)")
    keyboard.add(count_lme, qotes, price, metalls, vm)
    return keyboard


action = 'send_lme'
date = datetime.datetime.now().date().strftime("%d.%m.%Y")
admins = {'Александр Фоменко': 1504242703,
          'Александр Синицын': 181705237,
          'Бессалов Влад': 1237806382,
          'Илья Холькин': 2112612237,
          'Юрий Мирошниченко': 1905616218,
          'Пётр Любанов': 2119047734,
          'Андрей Таболкин': 1922175393,
          'Артём Анисимов': 2131618033,
          'Вагиф Джафаров': 5429292590,
          'Евгений Максименко': 5220388533,
          'Денис Бабенко': 5510839168,
          'Иван Плеских': 5251867994,
          'Михаил Харламов': 5011405787,
          'Киреев Антон': 5235872523,
          'Евгений Кошкинцев': 1948567221,
          'Дмитрий Младёнов': 2007108125,
          'Дмитрий Толдинов': 296804081,
          'Иван Никитин': 313266323,
          'Александр Мокряков': 1860462432,
          }


@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(chat_id=message.chat.id, text='Выберите действие', reply_markup=catalog_keyboard())


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(chat_id=message.chat.id, text='Чтобы воспользоваться ботом, выберите одно из действий, '
                                                   'предлагаемых после нажатия /start\n\n'
                                                   'Порядок элементов везде один и тот же - '
                                                   'платина, палладий, родий\n\n'
                                                   'Каждую команду необходимо вызывать заново - например, если после '
                                                   'расчёта стоимоимости необходимо посчитать её ещё раз, но с другими'
                                                   ' вводными - нужно вызвать эту команду заново через /start\n\n'
                                                   'Важно строго соблюдать форматы ввода, описанные в шаблонах '
                                                   '\n\n'
                                                   '1) При выборе расчёта биржи по заданным процентам:\n'
                                                   '- 75 - биржа в круг по 75, родий середина\n'
                                                   '- 75/78/80 - биржа по 75 процентов на платину, 78 - на палладий и '
                                                   '80 - на родий, родий середина\n'
                                                   '- 75/родий бид - биржа по 75 в круг, родий bid\n'
                                                   '- 75/78/80/родий бид - биржа по соответствующим процентам, родий bid\n\n'
                                                   '2) При выборе расчёта стоимости за кг:\n'
                                                   '- при выборе любой еденицы измерения на месте отсутствующего показателя\n'
                                                   'ставится один символ 0\n'
                                                   '- при выборе еденицы измерения % порядковым разделителем должна '
                                                   'быть строго точка, а не запятая:\n\n'
                                                   '0.015 - верно\n'
                                                   '0,015 - не верно'
                                                   '')


@bot.message_handler(content_types=['text'])
def send(message):
    global action
    try:
        if message.text == 'Посчитать биржу по заданным процентам':
            action = send_lme
            l_2.info(f'{message.from_user.first_name} {message.from_user.last_name} / {message.text} / '
                     f'{message.from_user.id} / {message.from_user.username}')
            bot.send_message(chat_id=message.chat.id, text='Введите процент LME в формате\n\n '
                                                           'ХХ если биржа вкруг,\n\n ХХ/ХХ/ХХ если '
                                                           'проценты различны\n\nЕсли необходим '
                                                           'родий по цене bid - введите "XX/родий бид"\n\n'
                                                           'Чтобы узнать биржу для ВМ - введите "Вм"\n\n'
                                                           'Чтобы узнать биржу для приёмки МСК в субботу - '
                                                           'введите "Суббота приёмка"')

        if message.text == 'Котировки на сегодняшний день':
            l_2.info(f'{message.from_user.first_name} {message.from_user.last_name} / {message.text} / '
                     f'{message.from_user.id} / {message.from_user.username}')
            bot.send_message(chat_id=message.chat.id, text='Выберете цену родия:\n\n'
                                                           '1 - rh bid\n2 - rh (bid+ask)÷2')
            action = send_rh
        if message.text == 'Узнать стоимость за кг':
            l_2.info(f'{message.from_user.first_name} {message.from_user.last_name} / {message.text} / '
                     f'{message.from_user.id} / {message.from_user.username}')
            bot.send_message(chat_id=message.chat.id, text='Выберите еденицы измерения\n\n'
                                                           '1 - PPM\n2 - %')

            action = cost_lme
        if message.text == 'Цены на металл':
            l_2.info(f'{message.from_user.first_name} {message.from_user.last_name} / {message.text} / '
                     f'{message.from_user.id} / {message.from_user.username}')
            bot.send_message(chat_id=message.chat.id, text='Выберите категорию\n\n'
                                                           '1 - Частник\n'
                                                           '2 - Крупный\n'
                                                           '3 - Vip')
            action = cost_metalls
        if message.text == 'Узнать цену за кг (ВМ)':
            l_2.info(f'{message.from_user.first_name} {message.from_user.last_name} / {message.text} / '
                     f'{message.from_user.id} / {message.from_user.username}')
            if message.from_user.id in admins.values():
                action = cost_lme_vm
            else:
                bot.send_message(chat_id=message.chat.id, text='Извините, эта функция доступна только администраторам')
                return None
        action(message)
    except TypeError:
        bot.send_message(chat_id=message.chat.id, text='Некорректное ! Перепроверьте ввод!')


def send_lme(message):
    l_2.info(f'{message.from_user.first_name} {message.from_user.last_name} / {message.text} / '
             f'{message.from_user.id} / {message.from_user.username}')
    try:
        if len(message.text) <= 2 and message.text != 'Вм':
            procent = int(message.text) / 100
            PT_1 = str(int(PT) * procent).split('.')[0]
            PD_1 = str(int(PD) * procent).split('.')[0]
            RH_1 = str(int(RAV) * procent).split('.')[0]
            bot.send_message(message.chat.id, text=f'Биржа по {message.text} родий середина на '
                                                   f'{date}')
            bot.send_message(message.chat.id, text=f'Pt = {PT_1} руб/гр\nPd = {PD_1} руб/гр\nRh = {RH_1} руб/гр')
        elif 2 < len(message.text) <= 8:
            procent_pt = int(str(message.text).split('/')[0]) / 100
            procent_pd = int(str(message.text).split('/')[1]) / 100
            procent_rh = int(str(message.text).split('/')[2]) / 100
            PT_1 = str(int(PT) * procent_pt).split('.')[0]

            PD_1 = str(int(PD) * procent_pd).split('.')[0]

            RH_1 = str(int(RAV) * procent_rh).split('.')[0]
            bot.send_message(message.chat.id, text=f'Биржа по {message.text} родий середина на '
                                                   f'{date}')
            bot.send_message(message.chat.id, text=f'Pt = {PT_1} руб/гр\nPd = {PD_1} руб/гр\nRh = {RH_1} руб/гр')
        elif 'Вм' in message.text:
            if message.from_user.id in admins.values():
                PT_1 = str(float(PT) * 0.73).split('.')[0]
                PD_1 = str(float(PD) * 0.73).split('.')[0]
                RH_1 = str(float(RAV) * 0.68).split('.')[0]
                bot.send_message(message.chat.id, text=f'Биржа для ВМ на '
                                                       f'{date}\n\n'
                                                       f'Котировки\n\nPt = {str(Pt).split(".")[0]} \nPd = '
                                                       f'{str(Pd).split(".")[0]}\nRh = {str(ba).split(".")[0]}\n'
                                                       f'Курс доллара = {usd}\n\n'
                                                       f'Цена для расчётов\n\n'
                                                       f'Pt = {PT_1} руб/гр\nPd = {PD_1} руб/гр\nRh = {RH_1} руб/гр')
            else:
                bot.send_message(chat_id=message.chat.id, text='Извините, эта функция доступна только администраторам')
                return None
        elif 'Суббота приёмка' in message.text:
            if message.from_user.id in admins.values():
                PT_1 = str(int(PT) * 0.7).split('.')[0]
                PD_1 = str(int(PD) * 0.7).split('.')[0]
                RH_1 = str(int(RA) * 0.68).split('.')[0]
                bot.send_message(message.chat.id, text=f'Биржа для приёмки МСК на субботу '
                                                       f'{date}\n\n'
                                                       f'Котировки\n\nPt = {str(Pt).split(".")[0]} \nPd = '
                                                       f'{str(Pd).split(".")[0]}\nRh = {str(rh_bid).split(".")[0]}\n'
                                                       f'Курс доллара = {usd}\n\n'
                                                       f'Цена для расчётов\n\n'
                                                       f'Pt = {PT_1} руб/гр\nPd = {PD_1} руб/гр\nRh = {RH_1} руб/гр')
            else:
                bot.send_message(chat_id=message.chat.id, text='Извините, эта функция доступна только администраторам')
                return None
        elif 'родий бид' in message.text:
            if len(str(message.text).split('/')) == 2:
                procent = int(str(message.text).split('/')[0]) / 100
                PT_1 = str(int(PT) * procent).split('.')[0]

                PD_1 = str(int(PD) * procent).split('.')[0]

                RH_1 = str(int(RA) * procent).split('.')[0]
                bot.send_message(message.chat.id, text=f'Биржа по {message.text} на '
                                                       f'{date}')
                bot.send_message(message.chat.id,
                                 text=f'Pt = {PT_1} руб/гр\nPd = {PD_1} руб/гр\nRh = {RH_1} руб/гр')
            elif len(str(message.text).split('/')) == 4:
                procent_pt = int(str(message.text).split('/')[0]) / 100
                procent_pd = int(str(message.text).split('/')[1]) / 100
                procent_rh = int(str(message.text).split('/')[2]) / 100
                PT_1 = str(int(PT) * procent_pt).split('.')[0]

                PD_1 = str(int(PD) * procent_pd).split('.')[0]

                RH_1 = str(int(RA) * procent_rh).split('.')[0]
                bot.send_message(message.chat.id, text=f'Биржа по {message.text} на '
                                                       f'{date}')
                bot.send_message(message.chat.id,
                                 text=f'Pt = {PT_1} руб/гр\nPd = {PD_1} руб/гр\nRh = {RH_1} руб/гр')
        elif message.text == 'Посчитать биржу по заданным процентам':
            pass
    except (ValueError, IndexError):
        bot.send_message(chat_id=message.chat.id, text='Некорректное значение! Перепроверьте ввод!')


def send_rh(message):
    s = ['1', '2', 'Котировки на сегодняшний день']
    l_2.info(f'{message.from_user.first_name} {message.from_user.last_name} / {message.text} / '
             f'{message.from_user.id} / {message.from_user.username}')
    if message.text == '1':
        bot.send_message(message.chat.id, text=f'Котировки на {date}:'
                                               f'\n\nPt = {str(Pt).split(".")[0]}\nPd = {str(Pd).split(".")[0]}'
                                               f'\nRh = {str(rh_bid).split(".")[0]}\nКурс доллара = {usd}')
    elif message.text == '2':
        bot.send_message(message.chat.id, text=f'Котировки на {date}:'
                                               f'\n\nPt = {str(Pt).split(".")[0]}\nPd = {str(Pd).split(".")[0]}'
                                               f'\nRh = {str(ba).split(".")[0]}\nКурс доллара = {usd}')
    if message.text not in s:
        bot.send_message(chat_id=message.chat.id, text='Некорректное значение! Перепроверьте ввод!')


@bot.message_handler(content_types=['text'])
def func_1(message):
    l_2.info(f'{message.from_user.first_name} {message.from_user.last_name} / {message.text} / '
             f'{message.from_user.id} / {message.from_user.username}')
    try:
        global action
        msc = message.text

        @bot.message_handler(content_types=['text'])
        def func_3(message):
            l_2.info(f'{message.from_user.first_name} {message.from_user.last_name} / {message.text} /'
                     f' {message.from_user.id} / {message.from_user.username}')
            try:
                nonlocal PT_1, PD_1, RH_1
                pt = int(str(message.text).split('/')[0]) / 1000
                pd = int(str(message.text).split('/')[1]) / 1000
                rh = int(str(message.text).split('/')[2]) / 1000
                cost = pt * int(PT_1) + pd * int(PD_1) + rh * int(RH_1)
                cost_int = str(cost).split('.')[0]
                bot.send_message(chat_id=message.chat.id, text=f'Показатели: {str(pt * 1000).split(".")[0]}/'
                                                               f'{str(pd * 1000).split(".")[0]}/'
                                                               f'{str(rh * 1000).split(".")[0]}\n\n'
                                                               f'Стоимость по {msc} на '
                                                               f'{date} - '
                                                               f'{cost_int} руб/кг')
            except (ValueError, IndexError):
                bot.send_message(chat_id=message.chat.id, text='Некорректное значение! Перепроверьте ввод!')

        try:
            if len(message.text) <= 2:
                procent = int(message.text) / 100
                PT_1 = str(int(PT) * procent).split('.')[0]
                PD_1 = str(int(PD) * procent).split('.')[0]
                RH_1 = str(int(RAV) * procent).split('.')[0]
                bot.send_message(chat_id=message.chat.id, text=f'Введите показатели в формате Х/Х/Х\n\nЕсли '
                                                               f'какой-то показатель отсутствует - на его месте '
                                                               f'введите 0')

                action = func_3
            elif 2 < len(message.text) <= 8:
                procent_pt = int(str(message.text).split('/')[0]) / 100
                procent_pd = int(str(message.text).split('/')[1]) / 100
                procent_rh = int(str(message.text).split('/')[2]) / 100
                PT_1 = str(int(PT) * procent_pt).split('.')[0]

                PD_1 = str(int(PD) * procent_pd).split('.')[0]

                RH_1 = str(int(RAV) * procent_rh).split('.')[0]
                bot.send_message(chat_id=message.chat.id, text=f'Введите показатели в формате Х/Х/Х\n\nЕсли '
                                                               f'какой-то показатель отсутствует - на его месте '
                                                               f'введите 0')

                action = func_3
            elif 'родий бид' in message.text:
                if len(str(message.text).split('/')) == 2:
                    procent = int(str(message.text).split('/')[0]) / 100
                    PT_1 = str(int(PT) * procent).split('.')[0]

                    PD_1 = str(int(PD) * procent).split('.')[0]

                    RH_1 = str(int(RA) * procent).split('.')[0]
                    bot.send_message(chat_id=message.chat.id, text=f'Введите показатели в формате Х/Х/Х\n\nЕсли '
                                                                   f'какой-то показатель отсутствует - на его месте '
                                                                   f'введите 0')

                    action = func_3
                elif len(str(message.text).split('/')) == 4:
                    procent_pt = int(str(message.text).split('/')[0]) / 100
                    procent_pd = int(str(message.text).split('/')[1]) / 100
                    procent_rh = int(str(message.text).split('/')[2]) / 100
                    PT_1 = str(int(PT) * procent_pt).split('.')[0]

                    PD_1 = str(int(PD) * procent_pd).split('.')[0]

                    RH_1 = str(int(RA) * procent_rh).split('.')[0]
                    bot.send_message(chat_id=message.chat.id, text=f'Введите показатели в формате Х/Х/Х\n\nЕсли '
                                                                   f'какой-то показатель отсутствует - на его месте '
                                                                   f'введите 0')

                    action = func_3
        except (ValueError, IndexError):
            bot.send_message(chat_id=message.chat.id, text='Некорректное значение! Перепроверьте ввод!')
    except (ValueError, IndexError):
        bot.send_message(chat_id=message.chat.id, text='Некорректное значение! Перепроверьте ввод!')


@bot.message_handler(content_types=['text'])
def func_2(message):
    l_2.info(f'{message.from_user.first_name} {message.from_user.last_name} / {message.text} / '
             f'{message.from_user.id} / {message.from_user.username}')
    try:
        global action
        msc = message.text

        @bot.message_handler(content_types=['text'])
        def func_4(message):
            l_2.info(f'{message.from_user.first_name} {message.from_user.last_name} / {message.text} / '
                     f'{message.from_user.id} / {message.from_user.username}')
            try:
                nonlocal PT_1, PD_1, RH_1
                pt = float(str(message.text).split('/')[0]) * 10
                pd = float(str(message.text).split('/')[1]) * 10
                rh = float(str(message.text).split('/')[2]) * 10
                cost = pt * int(PT_1) + pd * int(PD_1) + rh * int(RH_1)
                cost_int = str(cost).split('.')[0]
                bot.send_message(chat_id=message.chat.id, text=f'Показатели: {pt / 10}/'
                                                               f'{pd / 10}/'
                                                               f'{rh / 10}\n\n'
                                                               f'Стоимость по {msc} на '
                                                               f'{date} - '
                                                               f'{cost_int} руб/кг')
            except (ValueError, IndexError):
                bot.send_message(chat_id=message.chat.id, text='Некорректное значение! Перепроверьте ввод!')

        try:
            if len(message.text) <= 2:
                procent = int(message.text) / 100
                PT_1 = str(int(PT) * procent).split('.')[0]
                PD_1 = str(int(PD) * procent).split('.')[0]
                RH_1 = str(int(RAV) * procent).split('.')[0]
                bot.send_message(chat_id=message.chat.id, text=f'Введите показатели в формате Х/Х/Х\n\nЕсли '
                                                               f'какой-то показатель отсутствует - на его месте '
                                                               f'введите 0\n\nПри использовании показателей в '
                                                               f'процентах'
                                                               f' в качестве порядкового разделителя используйте точку')

                action = func_4
            elif 2 < len(message.text) <= 8:
                procent_pt = int(str(message.text).split('/')[0]) / 100
                procent_pd = int(str(message.text).split('/')[1]) / 100
                procent_rh = int(str(message.text).split('/')[2]) / 100
                PT_1 = str(int(PT) * procent_pt).split('.')[0]

                PD_1 = str(int(PD) * procent_pd).split('.')[0]

                RH_1 = str(int(RAV) * procent_rh).split('.')[0]
                bot.send_message(chat_id=message.chat.id, text=f'Введите показатели в формате Х/Х/Х\n\nЕсли '
                                                               f'какой-то показатель отсутствует - на его месте '
                                                               f'введите 0')

                action = func_4
            elif 'родий бид' in message.text:
                if len(str(message.text).split('/')) == 2:
                    procent = int(str(message.text).split('/')[0]) / 100
                    PT_1 = str(int(PT) * procent).split('.')[0]

                    PD_1 = str(int(PD) * procent).split('.')[0]

                    RH_1 = str(int(RA) * procent).split('.')[0]
                    bot.send_message(chat_id=message.chat.id, text=f'Введите показатели в формате Х/Х/Х\n\nЕсли '
                                                                   f'какой-то показатель отсутствует - на его месте '
                                                                   f'введите 0')

                    action = func_4
                elif len(str(message.text).split('/')) == 4:
                    procent_pt = int(str(message.text).split('/')[0]) / 100
                    procent_pd = int(str(message.text).split('/')[1]) / 100
                    procent_rh = int(str(message.text).split('/')[2]) / 100
                    PT_1 = str(int(PT) * procent_pt).split('.')[0]

                    PD_1 = str(int(PD) * procent_pd).split('.')[0]

                    RH_1 = str(int(RA) * procent_rh).split('.')[0]
                    bot.send_message(chat_id=message.chat.id, text=f'Введите показатели в формате Х/Х/Х\n\nЕсли '
                                                                   f'какой-то показатель отсутствует - на его месте '
                                                                   f'введите 0')

                    action = func_4
        except (ValueError, IndexError):
            bot.send_message(chat_id=message.chat.id, text='Некорректное значение! Перепроверьте ввод!')
    except (ValueError, IndexError):
        bot.send_message(chat_id=message.chat.id, text='Некорректное значение! Перепроверьте ввод!')


def cost_lme(message):
    global action
    e = ['1', '2', 'Узнать стоимость за кг']
    l_2.info(f'{message.from_user.first_name} {message.from_user.last_name} / {message.text} / {message.from_user.id} / '
             f'{message.from_user.username}')
    if message.text == '1':
        bot.send_message(message.chat.id, text=f'Введите процент LME в формате '
                                               'ХХ если биржа вкруг, ХХ/ХХ/ХХ если '
                                               'проценты различны\n\nЕсли необходим '
                                               'родий по цене bid - введите "XX/родий бид"')
        action = func_1
    if message.text == '2':
        bot.send_message(chat_id=message.chat.id, text=f'Введите процент LME в формате '
                                                       'ХХ если биржа вкруг, ХХ/ХХ/ХХ если '
                                                       'проценты различны\n\nЕсли необходим '
                                                       'родий по цене bid - введите "XX/родий бид"')
        action = func_2
    if message.text not in e:
        bot.send_message(chat_id=message.chat.id, text='Некорректное значение! Перепроверьте ввод!')


def cost_metalls(message):
    c = ['1', '2', '3', 'Цены на металл']
    l_2.info(f'{message.from_user.first_name} {message.from_user.last_name} / {message.text} / {message.from_user.id} / '
             f'{message.from_user.username}')
    if message.text == '1':
        bot.send_message(chat_id=message.chat.id, text=f'Цены на металлические катализаторы на {date} в'
                                                       f' категории Частник')
        bot.send_message(chat_id=message.chat.id, text=f'{date}\n\n'
                                                       f'Импорт - {M["Импорт"][0]} руб/кг\n'
                                                       f'БМВ - {M["БМВ"][0]} руб/кг\n'
                                                       f'Лексус - {M["Лексус"][0]} руб/кг\n'
                                                       f'Инфинити - {M["Инфинити"][0]} руб/кг\n'
                                                       f'Ланос - {M["Ланос"][0]} руб/кг\n'
                                                       f'Россия - {M["Россия"][0]} руб/кг\n'
                                                       f'Коммерция - {M["Коммерция"][0]} руб/кг\n')
    elif message.text == '2':
        bot.send_message(chat_id=message.chat.id, text=f'Цены на металлические катализаторы на {date} в'
                                                       f' категории Крупный')
        bot.send_message(chat_id=message.chat.id, text=f'{date}\n\n'
                                                       f'Импорт - {M["Импорт"][1]} руб/кг\n'
                                                       f'БМВ - {M["БМВ"][1]} руб/кг\n'
                                                       f'Лексус - {M["Лексус"][1]} руб/кг\n'
                                                       f'Инфинити - {M["Инфинити"][1]} руб/кг\n'
                                                       f'Ланос - {M["Ланос"][1]} руб/кг\n'
                                                       f'Россия - {M["Россия"][1]} руб/кг\n'
                                                       f'Коммерция - {M["Коммерция"][1]} руб/кг\n')
    elif message.text == '3':
        bot.send_message(chat_id=message.chat.id, text=f'Цены на металлические катализаторы на {date} в'
                                                       f' категории Vip')
        bot.send_message(chat_id=message.chat.id, text=f'{date}\n\n'
                                                       f'Импорт - {M["Импорт"][2]} руб/кг\n'
                                                       f'БМВ - {M["БМВ"][2]} руб/кг\n'
                                                       f'Лексус - {M["Лексус"][2]} руб/кг\n'
                                                       f'Инфинити - {M["Инфинити"][2]} руб/кг\n'
                                                       f'Ланос - {M["Ланос"][2]} руб/кг\n'
                                                       f'Россия - {M["Россия"][2]} руб/кг\n'
                                                       f'Коммерция - {M["Коммерция"][2]} руб/кг\n')
    if message.text not in c:
        bot.send_message(chat_id=message.chat.id, text='Некорректное значение! Перепроверьте ввод!')


def cost_lme_vm(message):
    global action, PT, PD, RAV
    l_2.info(f'{message.from_user.first_name} {message.from_user.last_name} / {message.text} / {message.from_user.id} / '
             f'{message.from_user.username}')

    @bot.message_handler(content_types=['text'])
    def funk_5(message):
        l_2.info(f'{message.from_user.first_name} {message.from_user.last_name} / {message.text} / '
                 f'{message.from_user.id} / {message.from_user.username}')
        try:
            ptvm_1 = int(PT) * 0.73
            pdvm_1 = int(PD) * 0.73
            rvm_1 = int(RAV) * 0.68
            ptvm_2 = int(PT) * 0.6
            pdvm_2 = int(PD) * 0.6
            rvm_2 = int(RAV) * 0.6
            pt = int(str(message.text).split('/')[0]) / 1000
            pd = int(str(message.text).split('/')[1]) / 1000
            rh = int(str(message.text).split('/')[2]) / 1000
            cost = pt * ptvm_1 + pd * pdvm_1 + rh * rvm_1
            cost_int = str(cost).split('.')[0]
            cost_1 = pt * ptvm_2 + pd * pdvm_2 + rh * rvm_2
            cost_int_1 = str(cost_1).split('.')[0]
            bot.send_message(chat_id=message.chat.id, text=f'Показатели: {str(pt * 1000).split(".")[0]}/'
                                                           f'{str(pd * 1000).split(".")[0]}/'
                                                           f'{str(rh * 1000).split(".")[0]}\n\n'
                                                           f'Стоимость по 73/73/68 (родий середина) на '
                                                           f'{date} - '
                                                           f'{cost_int} руб/кг\n\nСтоимость по 60 вкруг (родий '
                                                           f'середина) '
                                                           f'на {date} - {cost_int_1} руб/кг')
        except (ValueError, IndexError):
            bot.send_message(chat_id=message.chat.id, text='Некорректное значение! Перепроверьте ввод!')

    bot.send_message(chat_id=message.chat.id, text=f'Введите показатели в формате \n\nХ/Х/Х\n\nЕсли '
                                                   f'какой-то показатель отсутствует - на его месте '
                                                   f'введите 0\n\nПримеры ввода:\n\n150/1500/150\n0/150/2000')
    action = funk_5


bot.polling(none_stop=True)
