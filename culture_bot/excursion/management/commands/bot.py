from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.utils.request import Request


from excursion.models import Message, Profile, Route, Exhibit, ReviewOnExhibit, ReviewOnRoute, Journey


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

    # m = Message(
    #     profile=p,
    #     text=text,
    # )
    # m.save()

    reply_text = f'Ваш ID = {chat_id}\n{r.description}'
    update.message.reply_text(
        text=reply_text,
    )


@log_errors
def do_count(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )
    count = Message.objects.filter(profile=p).count()

    # count = 0
    update.message.reply_text(
        text=f'У вас {count} сообщений',
    )

@log_errors
def do_next(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    tr = Journey.objects.get(traveler=chat_id)
    ex = Exhibit.objects.get(route__title='1', order=tr.now_exhibit+1)
    tr.now_exhibit = tr.now_exhibit + 1
    tr.save()
    update.message.reply_text(
        text=ex.description,
    )

@log_errors
def do_map(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    tr = Journey(
        traveler=chat_id,
        route=Route.objects.get(title='1'),
        now_exhibit=0
    )
    tr.save()

    update.message.reply_text(
        text='Ну что погнали !',
    )


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
        updater.dispatcher.add_handler(CommandHandler('map_1', do_map))

        # 3 -- запустить бесконечную обработку входящих сообщений
        updater.start_polling()
        updater.idle()
