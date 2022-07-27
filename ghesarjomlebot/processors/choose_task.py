from django_tgbot.decorators import processor
from django_tgbot.exceptions import ProcessFailure
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from django_tgbot.types.replykeyboardmarkup import ReplyKeyboardMarkup
from django_tgbot.types.keyboardbutton import KeyboardButton
from ..bot import state_manager, TelegramBot
from ..models import TelegramState, TelegramUser
from ..Texts import Text

state_manager.set_default_update_types(update_types.Message)


@processor(state_manager, from_states='said_greetings', fail=state_types.Keep, message_types=message_types.Text)
def choose_task(bot: TelegramBot, update: Update, state: TelegramState):
    print("choose task def ran")
    text = update.get_message().get_text()
    chat_id = update.get_chat().get_id()

    if text == 'ارسال پست':
        bot.sendMessage(chat_id, Text['sending_post'], reply_markup=ReplyKeyboardMarkup.a(keyboard=[[
            KeyboardButton.a(text='خانه')
        ]], resize_keyboard=True))
        state.set_name('sending_post')

    elif text == 'جست و جوی پست':
        bot.sendMessage(chat_id, Text['searching_post'], reply_markup=ReplyKeyboardMarkup.a(keyboard=[[
            KeyboardButton.a(text='خانه')
        ]], resize_keyboard=True))
        state.set_name('searching_post')

    else:
        bot.sendMessage(update.get_chat().get_id(), Text['not_supported'], reply_markup=ReplyKeyboardMarkup.a(keyboard=[
            [KeyboardButton.a(text='ارسال پست'), KeyboardButton.a(text="جست و جوی پست")],
        ], resize_keyboard=True))
