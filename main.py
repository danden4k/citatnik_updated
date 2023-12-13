import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, Updater, CommandHandler, CallbackQueryHandler, Filters,MessageHandler

# Создаем список цитат
quotes = ['Стремитесь не к успеху, а к ценностям, которые он дает. Альберт Эйнштейн',
        'Сложнее всего начать действовать, все остальное зависит только от упорства. Амелия Эрхарт',
        'Логика может привести Вас от пункта А к пункту Б, а воображение — куда угодно.Альберт Эйнштейн',
        'Начинать всегда стоит с того, что сеет сомнения.Борис Стругацкий',
        'Наука — это организованные знания, мудрость — это организованная жизнь .Иммануил Кант',
        'Вы никогда не пересечете океан, если не наберетесь мужества потерять берег из виду. Христофор Колумб',
        ' Два самых важных дня в твоей жизни: день, когда ты появился на свет, и день, когда понял, зачем. Марк Твен',
        'Есть только один способ избежать критики: ничего не делайте, ничего не говорите и будьте никем. Аристотель',
        ' Стоит только поверить, что вы можете – и вы уже на полпути к цели.',
          ]

# Обработчик команды /start
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Случайная цитата", callback_data='random')],
        [InlineKeyboardButton("Добавить свою цитату", callback_data='add')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        'Привет! Я телеграм бот-цитатник. '
        'Нажми на кнопку "случайная цитата", чтобы получить случайную цитату.'
        'Нажми на кнопку "Добавить свою цитату", добавить свою цитату в базу данных бота.',
    )
    update.message.reply_text('Выберите действие:', reply_markup=reply_markup)

# Обработчик кнопок
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == 'random':
        quote = random.choice(quotes)
        query.answer()
        query.edit_message_text(text=quote)
    elif query.data == 'add':
        query.answer()
        query.edit_message_text(text='Введите свою цитату:')
        context.user_data['adding_quote'] = True

# Обработчик текстовых сообщений
def text_message(update: Update, context: CallbackContext):
    if 'adding_quote' in context.user_data:
        quote = update.message.text
        if quote not in quotes:
            quotes.append(quote)
            update.message.reply_text('Цитата успешно добавлена!')
        else:
            update.message.reply_text('Цитата уже существует!')
        del context.user_data['adding_quote']

def main():
    updater = Updater('6869651621:AAHBelZoJL3STrC42khK9UPYwq20tdFj9xc')
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, text_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()