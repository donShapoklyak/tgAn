from aiogram import Router, F
from aiogram import types
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link, decode_payload
import keyboards.handlers_kb as kb
from States.States import LinkAnswer
from main import bot
import database as db

router = Router()


@router.message(Command('start'), StateFilter("*"))
async def process_start_command(message: Message, state: FSMContext, command: Command = None):
    await state.clear()
    await state.set_state(None)
    await db.update(message.from_user.id, message.from_user.first_name)
    photo = types.FSInputFile("./bot_media/welcome.jpg")
    # photo = "AgACAgIAAxkBAAMZZcvXgtme7i7TuxCXRX9zTo2Eyp8AAtDYMRvpYWBKVnSZzz7N35wBAAMCAAN3AAM0BA"
    link = await create_start_link(bot, str(message.from_user.id), encode=True)
    inline_share_text = "\nОтправь мне анонимную валентинку!💌"
    inline_link = f'https://t.me/share/url?url={link}&text={inline_share_text}'
    text = (
        f"👀 Привет!\n💌 Я Бот <b>Анонимная валентинка!</b>\n\nЧтобы тебе отправили валентинку, поделись "
        f"ссылкой:\n\n<code>{link}</code>"
    )
    await message.answer_photo(photo=photo, caption=text, reply_markup=await kb.anon_share(inline_link))
    if command.args:  # if user redirect from referral link
        args = command.args
        reference = int(decode_payload(args))  # it's user id
        del_message = await message.reply(text="💞 Напиши валентинку")
        await state.set_state(LinkAnswer.getAnswer)
        await state.update_data(receiver_id=reference)
        await state.update_data(del_message_id=del_message.message_id)
        print(del_message.message_id)


@router.message(StateFilter(LinkAnswer.getAnswer))
async def handler(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Только текстом еще раз напиши 🤗")
        return
    await message.reply("Отправлено")
    link = await create_start_link(bot, str(message.from_user.id), encode=True)
    user_anon = link.split('=')[1]
    user_data = await state.get_data()
    receiver_id = user_data["receiver_id"]
    del_message_id = user_data["del_message_id"]
    await bot.delete_message(message.chat.id, del_message_id)
    text = f"🎁 Валентинка от <b>{user_anon}</b>:\n\n{message.html_text}"
    user_id = str(message.from_user.id)
    inline_kb = await kb.answer_button(user_id)
    photo = types.FSInputFile("./bot_media/notification.png")
    # photo = "AgACAgIAAxkBAAMoZcvX7SHOrgT55GAQDcLsoFf4lkIAAhbZMRvpYWBKzST80K08ZfgBAAMCAAN3AAM0BA"
    await bot.send_photo(photo=photo, chat_id=receiver_id, caption=text, reply_markup=inline_kb)
    await state.clear()
    await state.set_state(None)


@router.callback_query(F.data.split("_")[0] == "answer", StateFilter(None))
async def send_random_value(callback: types.CallbackQuery, state: FSMContext):
    receiver_id = callback.data.split("_")[1]
    del_message = await callback.message.reply(text="💛 Напиши ответ")
    await state.set_state(LinkAnswer.getAnswer)
    await state.update_data(receiver_id=receiver_id)
    await state.update_data(del_message_id=del_message.message_id)


@router.message(F.text, StateFilter(None))
async def handler(message: Message):
    await message.answer(
        text=f"""Вы перешли не по ссылке.\nНажмите /start чтобы вернуться 😉""")


@router.message(StateFilter(None))
async def handler(message: Message):
    await message.answer(
        text=f"""Я вас не понимаю 😥""")
