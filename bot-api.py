import telebot
import requests


token = "7787094528:AAHk93KnXzVpqfNAhsYLAcKo9NBFWU16i2g"
bot = telebot.TeleBot(token)
key_api_weath = "ceefc72707b93c05ea9db640edce2047"

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет. Отправь свой город")

@bot.message_handler(content_types=['text'])
def print_weather(message):
    try:
        response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={message.text}&appid={key_api_weath}")
        print(response)
        city = response.json()
        print(city)
        city_lat = city[0]['lat']
        print(city_lat)
        city_lon = city[0]['lon']
        print(city_lon)

        try:
            response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={city_lat}&lon={city_lon}&appid={key_api_weath}&lang=ru")
            weather = response.json()
            print(weather)
            temp = weather['main']['temp'] - 273.15
            message_weather = (
                f"Погода в *{weather['name']}*\n"
                f"Общая погода: *{weather['weather'][0]['description']}*\n"
                f"Температура: *{temp:.0f} °C*\n"
                f"Ветер: *{weather['wind']['speed']} м/с*\n"
                f"Влажность: *{weather['main']['humidity']}%*\n"
                f"Облачность: *{weather['clouds']['all']}%*\n"
            )
            bot.send_message(message.chat.id, message_weather, parse_mode='Markdown')
        except:
            print(response)
            bot.send_message(message.chat.id,"Ошибка при запросе погоды.")
    except:
        bot.send_message(message.chat.id,"Проверьте название города.")

bot.polling(none_stop=True, interval=0)