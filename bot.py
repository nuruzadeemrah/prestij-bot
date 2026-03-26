import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8718873171:AAE6ASUHMh84VUh4-RU5Z1gagjZyln9ZPP0"
MANAGER_USERNAME = "@manager_prestij"  # Menecer username-ini dəyiş

# Kataloq məhsulları - istədiyin qədər əlavə edə bilərsən
CATALOG = {
    "men": {
        "name": "👔 Kişi geyimləri",
        "items": [
            {"name": "Kişi köynəyi", "price": "1500 руб", "desc": "Klassik üslub, müxtəlif rənglər"},
            {"name": "Kişi şalvarı", "price": "2000 руб", "desc": "Rahat material, müxtəlif ölçülər"},
            {"name": "Kişi kurtka", "price": "3500 руб", "desc": "İsti, yüksək keyfiyyət"},
        ]
    },
    "women": {
        "name": "👗 Qadın geyimləri",
        "items": [
            {"name": "Qadın paltar", "price": "2500 руб", "desc": "Müasir dizayn"},
            {"name": "Qadın bluzkası", "price": "1200 руб", "desc": "Yüngül material"},
            {"name": "Qadın kurtka", "price": "3000 руб", "desc": "Stilliş və isti"},
        ]
    },
    "kids": {
        "name": "🧒 Uşaq geyimləri",
        "items": [
            {"name": "Uşaq kostyumu", "price": "1800 руб", "desc": "Yumşaq material"},
            {"name": "Uşaq köynəyi", "price": "800 руб", "desc": "Rəngli və şən"},
        ]
    }
}

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛍 Каталог", callback_data="catalog")],
        [InlineKeyboardButton("📍 Наш адрес", callback_data="address")],
        [InlineKeyboardButton("👩‍💼 Связаться с менеджером", callback_data="manager")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Добро пожаловать в *Магазин Престиж*!\n\n"
        "🏪 Мы предлагаем широкий выбор одежды для всей семьи.\n"
        "🚚 Доставка по всей Губахе!\n\n"
        "Выберите нужный раздел 👇",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

if data == "catalog":
    await query.edit_message_text(
        "🛍 *Наш каталог*\n\nНажмите кнопку ниже чтобы просмотреть все товары 👇",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("👗 Перейти в каталог", url="https://t.me/prestij_magazin")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_main")]
        ]),
        parse_mode="Markdown"
    )
    elif data.startswith("cat_"):
        cat_key = data.replace("cat_", "")
        cat = CATALOG[cat_key]
        text = f"{cat['name']}\n\n"
        keyboard = []
        for i, item in enumerate(cat["items"]):
            text += f"• *{item['name']}* — {item['price']}\n  {item['desc']}\n\n"
            keyboard.append([InlineKeyboardButton(
                f"🛒 Заказать: {item['name']}", callback_data=f"order_{cat_key}_{i}"
            )])
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="catalog")])
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif data.startswith("order_"):
        parts = data.split("_")
        cat_key = parts[1]
        item_index = int(parts[2])
        item = CATALOG[cat_key]["items"][item_index]
        await query.edit_message_text(
            f"✅ Вы выбрали: *{item['name']}*\nЦена: {item['price']}\n\n"
            f"Для оформления заказа напишите нашему менеджеру {MANAGER_USERNAME}\n"
            f"Укажите товар и ваш адрес доставки.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("👩‍💼 Написать менеджеру", url=f"https://t.me/{MANAGER_USERNAME.replace('@', '')}")],
                [InlineKeyboardButton("🔙 Назад в каталог", callback_data="catalog")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "address":
        await query.edit_message_text(
            "📍 *Наш адрес*\n\n"
            "🏙 Город: Губаха\n"
            "🏪 Магазин Престиж\n\n"
            "📞 По всем вопросам обращайтесь к менеджеру.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("👩‍💼 Связаться", callback_data="manager")],
                [InlineKeyboardButton("🔙 Назад", callback_data="back_main")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "manager":
        await query.edit_message_text(
            f"👩‍💼 *Наш менеджер*\n\n"
            f"Напишите нам напрямую: {MANAGER_USERNAME}\n\n"
            f"Мы ответим как можно быстрее! 😊",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💬 Написать", url=f"https://t.me/{MANAGER_USERNAME.replace('@', '')}")],
                [InlineKeyboardButton("🔙 Назад", callback_data="back_main")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "back_main":
        keyboard = [
            [InlineKeyboardButton("🛍 Каталог", callback_data="catalog")],
            [InlineKeyboardButton("📍 Наш адрес", callback_data="address")],
            [InlineKeyboardButton("👩‍💼 Связаться с менеджером", callback_data="manager")],
        ]
        await query.edit_message_text(
            "👋 Добро пожаловать в *Магазин Престиж*!\n\n"
            "🏪 Мы предлагаем широкий выбор одежды для всей семьи.\n"
            "🚚 Доставка по всей Губахе!\n\n"
            "Выберите нужный раздел 👇",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot işə düşdü!")
    app.run_polling()

if __name__ == "__main__":
    main()
