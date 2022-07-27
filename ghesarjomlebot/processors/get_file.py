from django_tgbot.decorators import processor
from django_tgbot.exceptions import ProcessFailure
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from django_tgbot.types.replykeyboardmarkup import ReplyKeyboardMarkup
from django_tgbot.types.keyboardbutton import KeyboardButton
from ..bot import state_manager, TelegramBot
from ..models import TelegramState, TelegramUser, UserPost
from ..Texts import Text

state_manager.set_default_update_types(update_types.Message)


@processor(state_manager, from_states='sending_post', fail=state_types.Keep)
def get_file(bot: TelegramBot, update: Update, state: TelegramState):
    text = update.get_message().get_text()
    chat_id = update.get_chat().get_id()

    if text == "خانه":
        bot.sendMessage(chat_id, Text['greeting_text'], reply_markup=ReplyKeyboardMarkup.a(keyboard=[
            [KeyboardButton.a(text='ارسال پست'), KeyboardButton.a(text="جست و جوی پست")],
        ], resize_keyboard=True))
        state.set_name('said_greetings')

    else:
        file_type = update.get_message().type()
        post = getattr(update.get_message(), file_type)
        acceptable_formats = ['document', 'sticker', 'voice', 'audio', 'video', ]
        if file_type == "photo":
            file_id = post[0].file_id
        elif file_type in acceptable_formats:
            file_id = post.file_id
        else:
            bot.sendMessage(chat_id, "لطفا از فرمت‌های پشتیبانی شده استفاده کنید")
            raise ProcessFailure

        state.set_memory({
                             'file_id': file_id,
                             'file_type': file_type,
        })
        bot.sendMessage(chat_id, 'لطفا کلمات کلیدی مرتبط را وارد کنید. کلمات کلیدی را با "," از هم جدا کنید',
                        reply_markup=ReplyKeyboardMarkup.a(keyboard=[
                            [KeyboardButton.a(text='انصراف')],
                        ], resize_keyboard=True))
        state.set_name('getting_file_caption')


@processor(state_manager, from_states='getting_file_caption', success='said_greetings' , fail=state_types.Keep, message_types=message_types.Text)
def get_caption(bot: TelegramBot, update: Update, state: TelegramState):
    text = update.get_message().get_text()
    chat_id = update.get_chat().get_id()
    user = TelegramUser.objects.get(telegram_id=chat_id)
    file_id = state.get_memory()['file_id']
    file_type = state.get_memory()['file_type']

    if text == 'انصراف':
        bot.sendMessage(chat_id,"حله", reply_markup=ReplyKeyboardMarkup.a(keyboard=[
        [KeyboardButton.a(text='ارسال پست'), KeyboardButton.a(text="جست و جوی پست")],
    ], resize_keyboard=True))


    else:

        post = UserPost.objects.create(description = text, file_id = file_id, OP = user,file_type=file_type)
        post.save()

        bot.sendMessage(chat_id, 'دریافت شد', reply_markup=ReplyKeyboardMarkup.a(keyboard=[
            [KeyboardButton.a(text='ارسال پست'), KeyboardButton.a(text="جست و جوی پست")],
        ], resize_keyboard=True))

@processor(state_manager, from_states='getting_file_caption', exclude_message_types = message_types.Text)
def get_caption_text_fail(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    bot.sendMessage(chat_id,"لطفا یک متن به عنوان مجموعه کلمات کلیدی ارسال کنید")

