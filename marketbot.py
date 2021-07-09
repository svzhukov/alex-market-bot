#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""Simple inline keyboard bot with multiple CallbackQueryHandlers.

This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined as callback query handler. Then, those functions are
passed to the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot that uses inline keyboard that has multiple CallbackQueryHandlers arranged in a
ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line to stop the bot.
"""
import logging
import configparser
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode, Contact
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)

class Config:
    config = None

    @staticmethod
    def load():
        Config.setup_config()
        Config.set_env_vars()

    @staticmethod
    def setup_config():
        Config.config = configparser.ConfigParser()
        Config.config.read('config.ini')

    @staticmethod
    def set_env_vars():
        try:
            os.environ['DISCORD_BOT_TOKEN'] = Config.config['DEFAULT']['DISCORD_BOT_TOKEN']
            # EventLogger.log("From config.ini", action="load")
        except KeyError:
            raise
            # EventLogger.log("From os", action="load")


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Stages
STATE_GREETING, STATE_KNOW_MORE, STATE_REFERRAL = range(3)

# Callback data
DATA_KNOW_MORE, DATA_MAIN_MENU, DATA_TERMS, DATA_CASHBACK, DATA_CERTIFICATES, DATA_REFERRAL, DATA_INSTRUCTION = range(7)

def start(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            InlineKeyboardButton("Узнать больше", callback_data=str(DATA_KNOW_MORE)),
            InlineKeyboardButton("Как начать", callback_data=str(DATA_REFERRAL)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    msg_hello = "Привет, Меня зовут <b>Alex!</b>\n\nВ этом чате вы найдёте актуальную информацию о сервисе <b>Ai.Marketing</b> и о его роботе <b>MarketBot!</b>" \
                "\n\n<b>Ai.Marketing</b> – рекламный проект, в котором <b>MarketBot</b> (рекламный робот) рассылает за вас рекламу. После регистрации, " \
                "вам доступен подарочный сертификат на 50$! По рекламе покупатели приобретают товары, а сервис и Вы получаете комиссию. "
    update.message.reply_text(msg_hello, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

    # alex = Contact(phone_number='+79648914416', first_name='Alex', user_id=1104051985)

    # Tell ConversationHandler that we're in state `FIRST` now
    return STATE_GREETING


def start_over(update: Update, context: CallbackContext) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Узнать подробнее", callback_data=str(DATA_KNOW_MORE)),
            InlineKeyboardButton("Как начать", callback_data=str(DATA_REFERRAL)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    msg_hello = "Привет, Меня зовут <b>Alex!</b>\n\nВ этом чате вы найдёте актуальную информацию о сервисе <b>Ai.Marketing</b> и о его роботе <b>MarketBot!</b>" \
                "\n\n<b>Ai.Marketing</b> – рекламный проект, в котором <b>MarketBot</b> (рекламный робот) рассылает за вас рекламу. После регистрации, " \
                "вам доступен подарочный сертификат на 50$! По рекламе покупатели приобретают товары, а сервис и Вы получаете комиссию. "

    query.edit_message_text(msg_hello, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    return STATE_GREETING


def know_more(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()

    msg = "После того\, как вы пополните рекламный бюджет\, *MarketBot* проанализирует рынки и отберет трендовые " \
          "продукты и услуги\, из них команда профи выберет наиболее привлекательные предложения с максимальным кэшбэком\. \nСпециалисты запустят " \
          "массированную рекламную кампанию с привязкой по региону\, *48* часов на модерацию \- и пошел заработок\. \n\nТакже можно ознакомиться с [" \
          "презентацией в слайдах](https://clck.ru/SdXm7) и [промо\-видео](https://youtu.be/rs1HZcOtmkY)"

    keyboard = [
        [
            InlineKeyboardButton("Какие условия?", callback_data=str(DATA_TERMS)),
        ],
        [
            InlineKeyboardButton("Подтверждение кэшбэка", callback_data=str(DATA_CASHBACK)),
        ],
        [
            InlineKeyboardButton("Подарочные сертификаты", callback_data=str(DATA_CERTIFICATES)),
        ],
        [
            InlineKeyboardButton("Главное меню", callback_data=str(DATA_MAIN_MENU)),
            InlineKeyboardButton("Хочу начать", callback_data=str(DATA_REFERRAL)),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=msg, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2
    )
    return STATE_KNOW_MORE


def terms(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()

    msg = "Чтобы рекламная компания стартовала\, необходимо пополнить её бюджет\. Можно вносить суммы от 10$ любым удобным способом\. В течении " \
          "*48* часов происходит запуск компании\. [Пополнение\, продажи видео\.](https://youtu.be/7Kt9Pid8UOo)\n\nПримерный [расчет доходности](" \
          "https://imgur.com/a/XJIQuGv)\, если реинвестировать в течении *1\.5* лет"

    keyboard = [
        [
            InlineKeyboardButton("Назад к информации", callback_data=str(DATA_KNOW_MORE)),
            InlineKeyboardButton("Главное меню", callback_data=str(DATA_MAIN_MENU)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=msg, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2
    )
    return STATE_KNOW_MORE


def cashback(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()

    msg = "Каждый раз когда реклама привлекает клиента и он совершает покупку\, вам полагается часть комиссии с продаж в виде кэшбэка\. В " \
          "*MarketBot* всё понятно\, прозрачно и безопасно\. Начните получать доход прямо сейчас\! [Кэшбэки \- видео](https://youtu.be/BqdE-PatOCw)"
    keyboard = [
        [
            InlineKeyboardButton("Назад к информации", callback_data=str(DATA_KNOW_MORE)),
            InlineKeyboardButton("Главное меню", callback_data=str(DATA_MAIN_MENU)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=msg, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2
    )
    # Transfer to conversation state `SECOND`
    return STATE_KNOW_MORE


def certificates(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()

    msg = "Доход при помощи сертификата будет приятным дополнением к вашему собственному доходу\. Отправляйте друзьям свой сертификат и " \
          "получайте 5% отсуммы их рекламных бюджетов\. [Видео про сертификаты](https://youtu.be/VE-ZcgQycMw)"
    keyboard = [
        [
            InlineKeyboardButton("Назад к информации", callback_data=str(DATA_KNOW_MORE)),
            InlineKeyboardButton("Главное меню", callback_data=str(DATA_MAIN_MENU)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=msg, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2
    )
    return STATE_KNOW_MORE
#
# def contact_partner(update: Update, context: CallbackContext) -> int:
#     """Show new choice of buttons"""
#     query = update.callback_query
#     query.answer()
#
#     msg = "информация о сертификатах \.\.\. [сертификаты](https://youtu.be/VE-ZcgQycMw)"
#     keyboard = [
#         [
#             InlineKeyboardButton("Назад к информации", callback_data=str(DATA_KNOW_MORE)),
#             InlineKeyboardButton("Главное меню", callback_data=str(DATA_MAIN_MENU)),
#         ]
#     ]
#
#     update.message.contact
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     query.edit_message_text(
#         text=msg, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2
#     )
#     return STATE_KNOW_MORE


def referral(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Узнать больше", callback_data=str(DATA_KNOW_MORE)),
            InlineKeyboardButton("Подробная инструкция", callback_data=str(DATA_INSTRUCTION)),
        ],
        [
            InlineKeyboardButton("Главное меню", callback_data=str(DATA_MAIN_MENU)),
        ],
    ]
    msg = "Если вы ознакомились со всей информацией и готовы начать сотрудничать с *MarketBot*\, переходите по [ссылке](https://ai.marketing/ru/campaign/tnkqumy8qe)\, " \
          "регистрируйтесь и начинайте получать доход с рекламы уже сегодня\! Более подробная инструкция регистрации по кнопке ниже\."
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=msg, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2
    )
    return STATE_REFERRAL


def instructions(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Узнать больше", callback_data=str(DATA_KNOW_MORE)),
        ],
        [
            InlineKeyboardButton("Главное меню", callback_data=str(DATA_MAIN_MENU)),
        ],
    ]
    msg = "ИНСТРУКЦИЯ:\n1. Переходим по ссылке https://inb.network/#/?ref=65b388b\nи нажимаем \"У меня нет аккаунта, Создать аккаунт!\"\n2. " \
          "Создаем новый аккаунт (Фамилия. Имя пишем на латинице)\n3. Откроется сайт https://inb.network/ уже с вашим именем. Из него надо " \
          "выйти и закрыть.\n4. Для завершения регистрации вам нужно подтвердить свой адрес электронной почты. Идём на почту (письмо может " \
          "попасть и в спам)\n5. После подтверждения заходите в кабинет https://inb.network/\n6. Слева в меню выбираете и нажимаете на " \
          "\"AI.MARKETING\" Вас перекидывает на сайт https://ai.marketing/ru \n7. В правом верхнем углу нажимаете на \"ВХОД\", посредине нажимаете " \
          "на 1-ю картинку (мозги), вводите пароль указанный при регистрации на странице https://inb.network/\n8. Вы попадаете в кабинет " \
          "https://ai.marketing/ru В поле \"Представиться\" указываете имя/логин. Здесь Вам необходимо просмотреть ролик ДО КОНЦА." \
          " (без его просмотра невозможно продолжить регистрацию) и нажимаем \"NEXT\".\n9. После этого нажимаем на вкладку \"Мой робот\" с " \
          "предложением купить рекламу. Нажимаем \"Купить рекламу\".\nВыбираем способ оплаты \"Подарочный сертификат\",\nвставляем этот номер " \
          "сертификата:  8Z9N-P63V-JAR9-MWAF и нажимаем \"Пополнить\"\nПодарочный сертификат успешно погашен ! Поздравляю! Вы" \
          " получили 50$ на ваш рекламный бюджет и через 48 часов Робот автоматически начнёт делать продажи за Вас !\nВаш " \
          "подарочный сертификат для приглашения Вы найдёте в \"строке Кэшбек\", его можно использовать " \
          "неограниченное количество раз.\n\n Если у вас все еще остались вопросы, задайте их Алексу напрямую в телеграм или по электронной почте:\n\n" \
          "+7 964-891-44-16 telegram\nZhukov_Alex82_82@mail.ru"
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=msg, reply_markup=reply_markup
    )
    return STATE_REFERRAL


def main() -> None:
    Config.load()
    updater = Updater("1867330513:AAFlU-xfWSXeZbaoNfeVA6RNVQxqGySI8nE")

    dispatcher = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            STATE_GREETING: [
                CallbackQueryHandler(know_more, pattern='^' + str(DATA_KNOW_MORE) + '$'),
                CallbackQueryHandler(referral, pattern='^' + str(DATA_REFERRAL) + '$'),
                CallbackQueryHandler(referral, pattern='^' + str(DATA_REFERRAL) + '$'),

                ],
            STATE_KNOW_MORE: [
                CallbackQueryHandler(terms, pattern='^' + str(DATA_TERMS) + '$'),
                CallbackQueryHandler(cashback, pattern='^' + str(DATA_CASHBACK) + '$'),
                CallbackQueryHandler(certificates, pattern='^' + str(DATA_CERTIFICATES) + '$'),
                CallbackQueryHandler(know_more, pattern='^' + str(DATA_KNOW_MORE) + '$'),
                CallbackQueryHandler(start_over, pattern='^' + str(DATA_MAIN_MENU) + '$'),
                CallbackQueryHandler(referral, pattern='^' + str(DATA_REFERRAL) + '$'),
                ],
            STATE_REFERRAL: [
                CallbackQueryHandler(know_more, pattern='^' + str(DATA_KNOW_MORE) + '$'),
                CallbackQueryHandler(start_over, pattern='^' + str(DATA_MAIN_MENU) + '$'),
                CallbackQueryHandler(instructions, pattern='^' + str(DATA_INSTRUCTION) + '$'),
                ],
            },
        fallbacks=[CommandHandler('start', start)],
        )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()