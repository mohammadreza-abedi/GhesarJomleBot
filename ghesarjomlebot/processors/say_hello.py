from django_tgbot.decorators import processor
from django_tgbot.types.update import Update
from ..bot import state_manager
from ..models import TelegramState
from ..bot import TelegramBot
from ..Texts import Text
from django_tgbot.types.replykeyboardmarkup import ReplyKeyboardMarkup
from django_tgbot.types.keyboardbutton import KeyboardButton


@processor(state_manager, success="said_greetings")
def hello_world(bot: TelegramBot, update: Update, state: TelegramState):
    bot.sendMessage(update.get_chat().get_id(), Text['greeting_text'], reply_markup=ReplyKeyboardMarkup.a(keyboard=[
        [KeyboardButton.a(text='ارسال پست'), KeyboardButton.a(text="جست و جوی پست")],
    ], resize_keyboard=True))
