import telebot

from extensions import ConvertionExeption, CryptoConverter
TOKEN = '5974240081:AAF1_GKwUJaycDrG17yifedEGGvW8u8E1Ok'
keys={
    'евро' : 'EUR',
    'рубль' : 'RUB',
    'йена' :'JPY',
    'доллар' : 'USD',
}
bot=telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help (message: telebot.types.Message):
    text= 'Чтобы начать работу, введите команду в следующем формате: \n<имя валюты> \
<в какую валюту перевести>\
<количество переводимой валюты>\n Увидеть список всех доступных валют: /value'
    bot.reply_to(message, text)
@bot.message_handler(commands=['value']) # какие валюты можно получить
def value (message: telebot.types.Message):
    text= "Доступные валюты:"
    for key in keys.keys():
            text="\n".join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        value = message.text.split(" ")
        if len(value) != 3:
            raise ConvertionExeption('Слишком много параметров')
        quote, base, amount = value
        total_base = CryptoConverter.convert(quote,base,amount)
    except ConvertionExeption as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Неудалось обработать команду\n{e}')
    else:
        text = f'{amount} {quote} - {total_base * float(amount)} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()


