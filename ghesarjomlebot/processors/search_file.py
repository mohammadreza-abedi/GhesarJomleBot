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


@processor(state_manager, from_states='searching_post', fail=state_types.Keep)
def search_file(bot: TelegramBot, update: Update, state: TelegramState):
    print("search file def ran")
    text = update.get_message().get_text()
    chat_id = update.get_chat().get_id()
    user = TelegramUser.objects.get(telegram_id=chat_id)

    if text == "خانه":
        bot.sendMessage(chat_id, Text['greeting_text'], reply_markup=ReplyKeyboardMarkup.a(keyboard=[
            [KeyboardButton.a(text='ارسال پست'), KeyboardButton.a(text="جست و جوی پست")],
        ], resize_keyboard=True))
        state.set_name('said_greetings')
    else:
        search_key_words = text.split(",")
        post_results = []
        user_posts = UserPost.objects.filter(OP=user)

        for post in user_posts:
            caption_key_words = post.description.split(",")
            caption_key_words = [word.strip() for word in caption_key_words]

            for key_word in search_key_words:
                if key_word in caption_key_words:
                    post_results.append(post)
        if not post_results:
            bot.sendMessage(chat_id,'نتیجه ای یافت نشد')
            raise ProcessFailure

        for post in post_results:
            if post.file_type == 'document':
                bot.sendDocument(chat_id,post.file_id,reply_markup=ReplyKeyboardMarkup.a(keyboard=[
                [KeyboardButton.a(text='ارسال پست'), KeyboardButton.a(text="جست و جوی پست")],
            ], resize_keyboard=True))
            elif post.file_type == 'sticker':
                bot.sendSticker(chat_id,post.file_id,reply_markup=ReplyKeyboardMarkup.a(keyboard=[
                [KeyboardButton.a(text='ارسال پست'), KeyboardButton.a(text="جست و جوی پست")],
            ], resize_keyboard=True))
            elif post.file_type == 'voice':
                bot.sendVoice(chat_id,post.file_id,reply_markup=ReplyKeyboardMarkup.a(keyboard=[
                [KeyboardButton.a(text='ارسال پست'), KeyboardButton.a(text="جست و جوی پست")],
            ], resize_keyboard=True))
            elif post.file_type == 'audio':
                bot.sendAudio(chat_id,post.file_id,reply_markup=ReplyKeyboardMarkup.a(keyboard=[
                [KeyboardButton.a(text='ارسال پست'), KeyboardButton.a(text="جست و جوی پست")],
            ], resize_keyboard=True))
            elif post.file_type == 'video':
                bot.sendVideo(chat_id,post.file_id,reply_markup=ReplyKeyboardMarkup.a(keyboard=[
                [KeyboardButton.a(text='ارسال پست'), KeyboardButton.a(text="جست و جوی پست")],
            ], resize_keyboard=True))

        state.set_name('said_greetings')


@processor(state_manager, from_states='getting_search_caption', exclude_message_types=message_types.Text)
def sending_searched_post_fail(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    bot.sendMessage(chat_id, "لطفا یک متن به عنوان مجموعه کلمات کلیدی ارسال کنید")
