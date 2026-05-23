import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command


from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from keyboards.menu import main_menu
from keyboards.gender import gender_keyboard
from keyboards.country import country_keyboard

from states.profile_states import ProfileSetup

TOKEN = "8531257365:AAE8w3Z37HA11AmlR7DavXGiQizJL_7bU3I"

bot = Bot(token=TOKEN)
storage = MemoryStorage()

dp = Dispatcher(storage=storage)

waiting_users = []
active_chats = {}
user_profiles = {}


@dp.message(Command("start"))
async def start(message: Message, state: FSMContext):

    user_id = message.from_user.id

    if user_id in user_profiles:

        profile = user_profiles[user_id]

        await message.answer(
            f"✨ Welcome back!\n\n"
            f"👤 Gender: {profile['gender']}\n"
            f"🎂 Age: {profile['age']}\n"
            f"🌍 Country: {profile['country']}",
            reply_markup=main_menu
        )

    else:

        await message.answer(
            "👤 Select your gender:",
            reply_markup=gender_keyboard
        )

        await state.set_state(ProfileSetup.waiting_for_gender)

@dp.message(ProfileSetup.waiting_for_gender)
async def process_gender(message: Message, state: FSMContext):

    gender = message.text

    await state.update_data(gender=gender)

    await message.answer("🎂 Enter your age:")

    await state.set_state(ProfileSetup.waiting_for_age)


@dp.message(ProfileSetup.waiting_for_age)
async def process_age(message: Message, state: FSMContext):

    age = message.text

    if not age.isdigit():
        await message.answer("Please enter valid age.")
        return

    await state.update_data(age=age)

    await message.answer(
        "🌍 Select your country:",
        reply_markup=country_keyboard
    )

    await state.set_state(ProfileSetup.waiting_for_country)


@dp.message(ProfileSetup.waiting_for_country)
async def process_country(message: Message, state: FSMContext):

    country = message.text

    data = await state.get_data()

    user_profiles[message.from_user.id] = {
        "gender": data["gender"],
        "age": data["age"],
        "country": country
    }

    await message.answer(
        f"✅ Profile Saved!\n\n"
        f"👤 Gender: {data['gender']}\n"
        f"🎂 Age: {data['age']}\n"
        f"🌍 Country: {country}",
        reply_markup=main_menu
    )

    await state.clear()

@dp.message(lambda message: message.text == "💬 Chat")
async def button_chat(message: Message):
    await find_chat(message)


@dp.message(lambda message: message.text == "❓ Help")
async def help_button(message: Message):
    await message.answer(
        "Commands:\n"
        "/find - Find stranger\n"
        "/next - Next stranger\n"
        "/stop - Stop chat"
    )


@dp.message(lambda message: message.text == "ℹ️ About")
async def about_button(message: Message):
    await message.answer(
        "Anonymous Chat Bot 🚀\n"
        "Built with Python + aiogram"
    )

@dp.message(lambda message: message.text == "⚙️ Settings")
async def settings_button(message: Message):

    user_id = message.from_user.id

    if user_id not in user_profiles:
        await message.answer("Profile not setup.")
        return

    profile = user_profiles[user_id]

    await message.answer(
        f"⚙️ Settings\n\n"
        f"👤 Gender: {profile['gender']}\n"
        f"🎂 Age: {profile['age']}\n"
        f"🌍 Country: {profile['country']}"
    )

@dp.message(Command("find"))
async def find_chat(message: Message):
    user_id = message.from_user.id

    if user_id in active_chats:
        await message.answer("You are already chatting.")
        return

    if user_id in waiting_users:
        await message.answer("Already searching...")
        return

    waiting_users.append(user_id)

    await message.answer("Searching for stranger...")

    if len(waiting_users) >= 2:
         user1 = waiting_users.pop(0)
         user2 = waiting_users.pop(0)

         active_chats[user1] = user2
         active_chats[user2] = user1

         profile1 = user_profiles.get(user1)
         profile2 = user_profiles.get(user2)

         await bot.send_message(
             user1,
             f"✅ Partner Matched\n\n"
             f"👤 Gender: {profile2['gender']}\n"
             f"🎂 Age: {profile2['age']}\n"
             f"🌍 Country: {profile2['country']}\n\n"
             f"Say hi 👋"
         )

         await bot.send_message(
             user2,
             f"✅ Partner Matched\n\n"
             f"👤 Gender: {profile1['gender']}\n"
             f"🎂 Age: {profile1['age']}\n"
             f"🌍 Country: {profile1['country']}\n\n"
             f"Say hi 👋"
         )
       

@dp.message(Command("next"))
async def next_chat(message: Message):

    user_id = message.from_user.id

    if user_id in active_chats:

        partner = active_chats[user_id]

        del active_chats[user_id]
        del active_chats[partner]

        await bot.send_message(
            partner,
            "❌ Stranger skipped the chat."
        )

        await message.answer(
            "🔄 Finding new stranger..."
        )

        # Search new chat automatically

        if user_id not in waiting_users:
            waiting_users.append(user_id)

        if len(waiting_users) >= 2:

            user1 = waiting_users.pop(0)
            user2 = waiting_users.pop(0)

            active_chats[user1] = user2
            active_chats[user2] = user1

            profile1 = user_profiles.get(user1)
            profile2 = user_profiles.get(user2)

            await bot.send_message(
                user1,
                f"✅ Partner Matched\n\n"
                f"👤 Gender: {profile2['gender']}\n"
                f"🎂 Age: {profile2['age']}\n"
                f"🌍 Country: {profile2['country']}\n\n"
                f"Say hi 👋"
            )

            await bot.send_message(
                user2,
                f"✅ Partner Matched\n\n"
                f"👤 Gender: {profile1['gender']}\n"
                f"🎂 Age: {profile1['age']}\n"
                f"🌍 Country: {profile1['country']}\n\n"
                f"Say hi 👋"
            )

    else:
        await message.answer(
            "You are not chatting with anyone."
        )


@dp.message(Command("stop"))
async def stop_chat(message: Message):
    user_id = message.from_user.id

    if user_id in active_chats:
        partner = active_chats[user_id]

        del active_chats[user_id]
        del active_chats[partner]

        await bot.send_message(user_id, "Chat ended.")
        await bot.send_message(partner, "Stranger disconnected.")

    else:
        await message.answer("You are not in chat.")


@dp.message()
async def forward_messages(message: Message):
    user_id = message.from_user.id

    if user_id in active_chats:
        partner = active_chats[user_id]

        await bot.copy_message(
            chat_id=partner,
            from_chat_id=user_id,
            message_id=message.message_id
        )


async def main():
    print("BOT STARTED")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())