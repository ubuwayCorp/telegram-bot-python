import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import LabeledPrice, PreCheckoutQuery, InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
import os

# === НАСТРОЙКИ ===
TOKEN = "8569944927:AAHlFviZDfXtIw8urohvMgEr8kSG2jUNrsQ"
ADMIN_ID = 8275271557

# Настройка логирования
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# === ВСЕ ТВОИ КЛЮЧИ ===
VPN_KEYS = {
    "austria1": {
        "name": "Австрия 🇦🇹 #1",
        "price": 10,
        "config": "vless://aaaaaabb-4ddd-4eee-9fff-ffffffffffff@afrcloud22.mmv.kr:443?encryption=none&security=tls&type=ws&host=afrcloud22.mmv.kr&path=/138.2.95.61=1111&sni=afrcloud22.mmv.kr#%F0%9F%87%A6%F0%9F%87%B9%20Austria%2C%20Vienna%20%7C%20%F0%9F%8C%90%20Anycast-IP%20%7C%20%5BCloudflare%5D%20%7C%20%5BBL%5D"
    },
    "austria2": {
        "name": "Австрия 🇦🇹 #2",
        "price": 25,
        "config": "vless://9202d12b-42a9-42cd-b7c9-4ba844da635c@afrcloud22.mmv.kr:443?security=tls&type=ws&path=%2F44.208.64.96%3D443&host=afrcloud22.mmv.kr&sni=afrcloud22.mmv.kr&fp=chrome&encryption=none#%F0%9F%87%A6%F0%9F%87%B9%20Austria%2C%20Vienna%20%5BBL%5D"
    },
    "germany1": {
        "name": "Германия 🇩🇪 #1",
        "price": 5,
        "config": "vless://36254425-4c07-428a-828e-8a1924765691@148.251.1.198:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.microsoft.com&fp=chrome&pbk=uf64ptbhMNcLWuwEfOzQB7qgn725h6w9DmKRteQQPwg&sid=176f1837&type=tcp&headerType=none#Germany_Stable"
    },
    "germany2": {
        "name": "Германия 🇩🇪 #2",
        "price": 10,
        "config": "vless://a91e9db3-a3f1-43a4-84b3-316ea3600fac@178.162.242.98:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.samsung.com&fp=chrome&pbk=ckRcueERkPqqjZABwxqni_J_Nbb70Q6k5fEEUAjoImw&type=raw&headertype=none#%F0%9F%87%A9%F0%9F%87%AA%20Germany%2C%20Frankfurt%20am%20Main%20%28Innenstadt%20I%29%20%5BBL%5D"
    },
    "germany3": {
        "name": "Германия 🇩🇪 #3",
        "price": 30,
        "config": "vless://b39aca97-e9f2-4a94-b87f-8748299846cd@144.31.85.153:443/?type=tcp&encryption=none&flow=xtls-rprx-vision&sni=germany.denditop.site&fp=chrome&security=reality&pbk=wgoLhL4pRP0y6fu6He4qW_ElohCM_ANWJF3HEoUhNz4&sid=9c2378562188c3cb#%F0%9F%87%A9%F0%9F%87%AA%20Germany%2C%20Frankfurt%20am%20Main%20%28Innenstadt%20I%29%20%5BBL%5D"
    },
    "finland1": {
        "name": "Финляндия 🇫🇮 #1",
        "price": 20,
        "config": "vless://76bd59cb-82ee-4ce3-9410-f7b19416318f@info.mattesaira.cc:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.techradar.com&fp=chrome&pbk=uf64ptbhMNcLWuwEfOzQB7qgn725h6w9DmKRteQQPwg&sid=43c6f259e156&type=tcp&headerType=none#%F0%9F%87%AB%F0%9F%87%AE%20Finland%20%5B%2ACIDR%5D"
    }
}

# Клавиатура главного меню
def get_main_keyboard():
    buttons = [
        [InlineKeyboardButton(text="🇦🇹 Австрия #1 (10⭐)", callback_data="select_austria1")],
        [InlineKeyboardButton(text="🇦🇹 Австрия #2 (25⭐)", callback_data="select_austria2")],
        [InlineKeyboardButton(text="🇩🇪 Германия #1 (5⭐)", callback_data="select_germany1")],
        [InlineKeyboardButton(text="🇩🇪 Германия #2 (10⭐)", callback_data="select_germany2")],
        [InlineKeyboardButton(text="🇩🇪 Германия #3 (30⭐)", callback_data="select_germany3")],
        [InlineKeyboardButton(text="🇫🇮 Финляндия #1 (20⭐)", callback_data="select_finland1")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Клавиатура для выбранного ключа
def get_key_keyboard(key_id: str):
    buttons = [
        [InlineKeyboardButton(text=f"💳 Оплатить {VPN_KEYS[key_id]['price']} ⭐️", callback_data=f"pay_{key_id}")],
        [InlineKeyboardButton(text="◀️ Меню", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🌟 Здравствуй, я VPN Менеджер.\n"
        "Выбери VPN ключ из списка:",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query(F.data.startswith("select_"))
async def select_key(callback: types.CallbackQuery):
    key_id = callback.data.replace("select_", "")
    
    if key_id not in VPN_KEYS:
        await callback.answer("❌ Ключ не найден", show_alert=True)
        return
        
    key_info = VPN_KEYS[key_id]
    
    await callback.message.edit_text(
        f"🔑 *{key_info['name']}*\n\n"
        f"💰 Цена: {key_info['price']} Telegram Stars\n\n"
        f"Нажмите кнопку ниже для оплаты:",
        reply_markup=get_key_keyboard(key_id),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🌟 Здравствуй, я VPN Менеджер.\n"
        "Выбери VPN ключ из списка:",
        reply_markup=get_main_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("pay_"))
async def send_invoice(callback: types.CallbackQuery):
    key_id = callback.data.replace("pay_", "")
    
    if key_id not in VPN_KEYS:
        await callback.answer("❌ Ключ не найден", show_alert=True)
        return
        
    key_info = VPN_KEYS[key_id]
    
    try:
        await bot.send_invoice(
            chat_id=callback.from_user.id,
            title=f"Покупка {key_info['name']}",
            description=f"Оплата VPN ключа {key_info['name']}",
            payload=f"vpn_{key_id}",
            currency="XTR",
            prices=[LabeledPrice(label=key_info['name'], amount=key_info['price'])],
            provider_token=""
        )
        await callback.answer()
    except Exception as e:
        print(f"Ошибка: {e}")
        await callback.answer("❌ Ошибка оплаты", show_alert=True)

@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def success_payment_handler(message: types.Message):
    payment = message.successful_payment
    key_id = payment.invoice_payload.replace("vpn_", "")
    
    if key_id in VPN_KEYS:
        key_info = VPN_KEYS[key_id]
        user = message.from_user
        
        await message.answer(
            f"✅ *Успешно!*\n\n"
            f"🔑 *Ваш ключ:*\n"
            f"`{key_info['config']}`\n\n"
            f"📱 *Для использования:*\n"
            f"• Windows, Android: скачайте *Hiddify*\n"
            f"• iOS: скачайте *V2Box*\n\n"
            f"Спасибо за покупку! 🎉",
            parse_mode="Markdown"
        )
        
        # Уведомление админу
        admin_message = (
            f"🛒 *НОВАЯ ПОКУПКА!*\n\n"
            f"👤 *Пользователь:*\n"
            f"ID: `{user.id}`\n"
            f"Имя: {user.full_name}\n"
            f"Username: @{user.username if user.username else 'отсутствует'}\n\n"
            f"🔑 *Купленный ключ:* {key_info['name']}\n"
            f"💰 *Цена:* {payment.total_amount} ⭐️\n"
            f"📅 *Дата:* {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
        )
        
        try:
            await bot.send_message(ADMIN_ID, admin_message, parse_mode="Markdown")
        except Exception as e:
            print(f"Ошибка отправки уведомления админу: {e}")
    else:
        await message.answer("❌ Ошибка: ключ не найден")

async def main():
    print("✅ Бот VPN Менеджер запущен на RAILWAY!")
    print(f"🤖 Bot: @VPNManagerRUbot")
    
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
