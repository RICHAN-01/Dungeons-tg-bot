import telebot
from telebot import types
import random

token = ''
bot = telebot.TeleBot(token)

hp = damage = xp = 0
lvl = 1
revival_token = 1
race_dict = {
    'Стрелок': {'здоровье': 100, 'урон': 10},
    'Силач': {'здоровье': 130, 'урон': 12}
}


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_1 = 'Начать игру'
    btn_2 = 'Об игре'
    markup.add(btn_1, btn_2)
    return markup


def ne_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_1 = 'Сыграть ещё раз'
    btn_2 = 'Об игре'
    markup.add(btn_1, btn_2)
    return markup


def death_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_1 = 'Использовать жетон возрождения 🪙'
    btn_2 = 'Сыграть ещё раз'
    btn_3 = 'Об игре'
    markup.add(btn_1, btn_2), btn_3
    return markup


def make_race_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for race in race_dict.keys():
        markup.add(types.KeyboardButton(text=race))
    return markup


def start_quest():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = 'Погнали!'
    btn2 = 'Вернуться в главное меню'
    markup.add(btn1, btn2)
    return markup


def combat():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    attack_btn = 'Атаковать'
    run_btn = 'Убежать'
    main_menu_btn = 'Вернуться в главное меню'
    markup.add(attack_btn, run_btn, main_menu_btn)
    return markup


@bot.message_handler(commands=['start'])
def start_menu(message):
    bot.send_message(message.chat.id, "  Добро пожаловать в игру 'Подземелья  '.\nГотов сыграть?",
                     reply_markup=main_menu())
    bot.send_sticker(chat_id=message.chat.id,
                     sticker='CAACAgIAAxkBAAEIwWdkStqjPTHXwTlCrkDOSMCnOURMMAACXBMAAlyt6Us8jhSGeWB0Ty8E')


@bot.message_handler(content_types=['text'])
def main(message):
    global hp, damage, xp, lvl, victim, revival_token, hp_2, damage_2

    def create_enemy():
        rnd_name = random.choice(enemy_name)
        rnd_hp = random.randint(50, 80)
        rnd_damage = random.randint(5, 8)
        return [rnd_name, rnd_hp, rnd_damage]

    if message.text == 'Об игре':
        bot.send_message(message.chat.id, text="Это игра подземелья.", reply_markup=main_menu())
    elif message.text == 'Начать игру':
        bot.send_message(message.chat.id, text='Выбери своего персонажа', reply_markup=make_race_menu())
        bot.send_sticker(chat_id=message.chat.id,
                         sticker='CAACAgIAAxkBAAEIwXtkSt4JkiPAsu8hoJjrCEbv6YlCcwACxwQAArbWYTJeqZswTKC1ky8E')
    if message.text == 'Силач':
        hp = race_dict['Силач']['здоровье']
        damage = race_dict['Силач']['урон']
        damage_2 = 12
        hp_2 = 130
        bot.send_message(message.chat.id, f'Твой герой: Силач\n Твоё здоровье: {hp}\n Твой урон: {damage}')
        bot.send_message(message.chat.id, text="Ну что ж, идём в подземелья?", reply_markup=start_quest())
    if message.text == 'Стрелок':
        hp = race_dict['Стрелок']['здоровье']
        damage = race_dict['Стрелок']['урон']
        damage_2 = 10
        hp_2 = 100
        bot.send_message(message.chat.id, f'Твой герой: Стрелок\n Твоё здоровье: {hp}\n Твой урон: {damage}')
        bot.send_message(message.chat.id, text="Ну что ж, идём в подземелья?", reply_markup=start_quest())
    if message.text == 'Погнали!':
        event = random.randint(1, 3)
        if event == 1:
            bot.send_message(message.chat.id, text='Ты никого не встретил. Идём дальше?',
                             reply_markup=start_quest())
        else:
            victim = create_enemy()
            bot.send_message(message.chat.id, text=f'Ты встретил {victim[0]}.\n Его здоровье: {victim[1]}, а '
                                                   f'урон: {victim[2]}.\n Что будешь делать?',
                             reply_markup=combat())
    if message.text == 'Атаковать':
        if damage_2 == 12:
            bot.send_message(message.chat.id, text='⚔️')
            victim[1] -= damage
            if victim[1] > 0 < hp:
                bot.send_message(message.chat.id, text=f'Здоровье {victim[0]}: {victim[1]}')
            elif victim[1] <= 0 < hp:
                bot.send_message(message.chat.id, text=f'Враг повержен.\n Твоё здоровье: {hp}\nПродолжим наш путь?',
                                 reply_markup=start_quest())
                xp += 10 * lvl
                if xp >= lvl * 30:
                    lvl += 1
                    damage += 0.3
                    hp_2 += 3
                    hp = hp_2
                    bot.send_message(message.chat.id, text=f'Молодец! Теперь у тебя {lvl} уровень.\n'
                                                           f'Уровень здоровья был повышен до {hp} , '
                                                           f'а урон до {damage}\n'
                                                           f'Тебе осталось {30 * lvl - xp} опыта до нового уровня!',
                                     reply_markup=start_quest())
            if victim[1] > 0:
                hp -= victim[2]
                if hp > 0:
                    bot.send_message(message.chat.id, text=f'Тебя атаковали!\nТвоё здоровье: {hp}')
                    bot.send_message(message.chat.id, text='Что делаем дальше?', reply_markup=combat())
                if hp <= 0:
                    bot.send_message(message.chat.id, text=f'Ты был повержен...\nЧто будешь делать?.',
                                     reply_markup=death_menu())
                    bot.send_sticker(chat_id=message.chat.id,
                                     sticker='CAACAgIAAxkBAAEIz_lkUDEPdIJ7in8lcMYmwDzNMQNaZAACWRYAAvvJCUhqRXSe4-8aPC8E')
        if damage_2 == 10:
            bot.send_message(message.chat.id, text='🏹')
            victim[1] -= damage
            if victim[1] > 0 < hp:
                bot.send_message(message.chat.id, text=f'Здоровье {victim[0]}: {victim[1]}')
            elif victim[1] <= 0 < hp:
                bot.send_message(message.chat.id, text=f'Враг повержен.\n Твоё здоровье: {hp}\nПродолжим наш путь?',
                                 reply_markup=start_quest())
                xp += 10
                if xp >= lvl * 30:
                    lvl += 1
                    damage += 0.5
                    hp_2 += 5
                    hp = hp_2
                    bot.send_message(message.chat.id, text=f'Молодец! Теперь у тебя {lvl} уровень.\n'
                                                           f'Уровень здоровья был повышен до {hp} , '
                                                           f'а урон до {damage}\n'
                                                           f'Тебе осталось {30 * lvl - xp} опыта до нового уровня!',
                                     reply_markup=start_quest())
    if message.text == 'Убежать':
        plan = random.randint(1, 3)
        if plan == 1:
            bot.send_message(message.chat.id, text=f'Ты успешно убежал от {victim[0]}. Продолжим наш путь?',
                             reply_markup=start_quest())
        elif plan == 2 or 3:
            hp -= victim[2]
            if hp > 0:
                bot.send_message(message.chat.id, text=f"О нет! Монстр настиг тебя и теперь твоё здоровье равно {hp}.\n"
                                                       f"Что будешь делать?", reply_markup=combat())
            elif hp <= 0:
                bot.send_message(message.chat.id, text=f'В этот раз тебе не повезло и ты был повержен.'
                                                       f"Если ты нажмёшь 'Сыграть ещё раз', твой уровень и опыт будут"
                                                       f" обнулены\n"
                                                       f"Что будешь делать?", reply_markup=death_menu())
                bot.send_sticker(chat_id=message.chat.id,
                                 sticker='CAACAgIAAxkBAAEIz_NkUDBl5SVORWNQv0e0YeuuqfTI9QAC3BYAAo7I0Uq39QafTeynUS8E')
    if message.text == 'Использовать жетон возрождения 🪙':
        revival_token -= 1
        if revival_token < 0:
            bot.send_message(message.chat.id, text=f'У тебя не осталось жетонов возрождения.\n'
                                                   f'Твой уровень и опыт были обнулены.'
                                                   f' Что будешь делать?', reply_markup=ne_main_menu())
        elif revival_token >= 0:
            hp = hp_2
            bot.send_message(message.chat.id, text=f'Ты использовал жетон возрождения\n'
                                                   f'У тебя осталось {revival_token} жетонов\n'
                                                   f'Твоё здоровье было восстановлено до {hp}\n'
                                                   f'Что будешь делать?', reply_markup=combat())
    if message.text == 'Вернуться в главное меню':
        hp = 0
        damage_2 = 0
        damage = 0
        xp = 0
        lvl = 1
        bot.send_message(message.chat.id, "  Добро пожаловать в игру 'Подземелья  '.\nГотов сыграть?",
                         reply_markup=main_menu())
        bot.send_sticker(chat_id=message.chat.id,
                         sticker='CAACAgIAAxkBAAEIwWdkStqjPTHXwTlCrkDOSMCnOURMMAACXBMAAlyt6Us8jhSGeWB0Ty8E')
    if message.text == 'Сыграть ещё раз':
        hp = damage = xp = damage_2 = 0
        lvl = 1
        bot.send_message(message.chat.id, text='Выбери своего персонажа', reply_markup=make_race_menu())
        bot.send_sticker(chat_id=message.chat.id,
                         sticker='CAACAgIAAxkBAAEIwXtkSt4JkiPAsu8hoJjrCEbv6YlCcwACxwQAArbWYTJeqZswTKC1ky8E')


enemy_name = ['Гоблина', 'Орка', 'Зомби', 'Кентавра', 'Огра']

bot.polling(non_stop=True)
