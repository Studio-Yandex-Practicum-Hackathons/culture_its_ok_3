from django.conf import settings
from django.core.management.base import BaseCommand
from telegram import Bot, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)
from telegram.utils.request import Request

from excursion.models import (Exhibit, Journey, Message, Profile,
                              ReviewOnExhibit, ReviewOnRoute, Route)


def log_errors(f):

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            print(error_message)
            raise e

    return inner


@log_errors
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )

    r, _ = Route.objects.get_or_create(title=text)

    reply_text = f'Ваш ID = {chat_id}\n{r.description}'
    update.message.reply_text(
        text=reply_text,
    )


# @log_errors
# def do_count(update: Update, context: CallbackContext):
#     chat_id = update.message.chat_id
#
#     p, _ = Profile.objects.get_or_create(
#         external_id=chat_id,
#         defaults={
#             'name': update.message.from_user.username,
#         }
#     )
#     count = Message.objects.filter(profile=p).count()
#
#     # count = 0
#     update.message.reply_text(
#         text=f'У вас {count} сообщений',
#     )
#
# @log_errors
# def do_next(update: Update, context: CallbackContext):
#     chat_id = update.message.chat_id
#
#     tr = Journey.objects.get(traveler=chat_id)
#     if tr.now_exhibit < Route.objects.get(title=tr.route.title).exhibit.count():
#         ex = Exhibit.objects.get(route__title=tr.route, order=tr.now_exhibit + 1)
#         tr.now_exhibit = tr.now_exhibit + 1
#         tr.save()
#         update.message.reply_text(
#             text=ex.description,
#         )
#     else:
#         tr.delete()
#         update.message.reply_text(
#             text='это было прекрасно',
#         )
#
# @log_errors
# def do_map(update: Update, context: CallbackContext):
#     chat_id = update.message.chat_id
#     number_map = str(update.message.text).split()[1]
#     Journey.objects.filter(traveler=chat_id).delete()
#     print(Route.objects.get(title=number_map).exhibit.count())
#     tr = Journey(
#         traveler=chat_id,
#         route=Route.objects.get(title=number_map),
#         now_exhibit=0
#     )
#     tr.save()
#
#     update.message.reply_text(
#         text='Ну что погнали !',
#     )


TOKEN = '5575568139:AAEuNC2x_yW23LFcefoBmmsc7AZw31abqyA'

class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        # 1 -- правильное подключение
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            request=request,
            token=TOKEN,
            base_url=getattr(settings, 'PROXY_URL', None),
        )
        print(bot.get_me())

        # 2 -- обработчики
        updater = Updater(
            bot=bot,
            use_context=True,
        )

        message_handler = MessageHandler(Filters.text, do_echo)
        updater.dispatcher.add_handler(message_handler)
        updater.dispatcher.add_handler(CommandHandler('count', do_count))
        updater.dispatcher.add_handler(CommandHandler('next', do_next))
        updater.dispatcher.add_handler(CommandHandler('map', do_map))

        # 3 -- запустить бесконечную обработку входящих сообщений
        updater.start_polling()
        updater.idle()
