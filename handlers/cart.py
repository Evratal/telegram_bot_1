from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database import get_cart, clear_cart, add_order, update_order_status
from payments import create_payment, check_payment_status
from config import OWNER_CHAT_ID

router = Router()


def format_cart(cart_items) -> str:
    """Форматирует корзину для отображения"""
    if not cart_items:
        return "🛒 Ваша корзина пуста"

    text = "🛒 **Ваша корзина:**\n\n"
    total = 0

    for item in cart_items:
        price = item["price"] * item["quantity"]
        total += price
        text += f"• {item['name']} × {item['quantity']} = **{price:,} ₽**\n".replace(",", " ")

    text += f"\n💰 **Итого: {total:,} ₽**".replace(",", " ")
    return text


@router.message(F.text == "🛒 Корзина")
async def show_cart(message: Message):
    """Показывает корзину пользователя"""
    cart_items = get_cart(message.from_user.id)
    text = format_cart(cart_items)

    if cart_items:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🗑 Очистить корзину", callback_data="clear_cart")],
                [InlineKeyboardButton(text="✅ Оформить заказ", callback_data="checkout")]
            ]
        )
    else:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🛍 Перейти к витрине", callback_data="go_shop")]
            ]
        )

    await message.answer(text, reply_markup=kb, parse_mode="Markdown")


@router.callback_query(F.data == "clear_cart")
async def clear_cart_callback(callback: CallbackQuery):
    """Очищает корзину"""
    clear_cart(callback.from_user.id)
    await callback.answer("🗑 Корзина очищена!", show_alert=True)
    try:
        await callback.message.edit_text("🛒 Ваша корзина пуста")
    except Exception as e:
        print(f"Не удалось обновить сообщение: {e}")


@router.callback_query(F.data == "go_shop")
async def go_shop_callback(callback: CallbackQuery):
    """Возвращает к витрине"""
    await callback.answer()
    try:
        await callback.message.edit_text(
            "🛍️ **Наша витрина услуг:**\n\n"
            "Выберите услугу ниже 👇"
        )
    except Exception as e:
        print(f"Не удалось обновить сообщение: {e}")


@router.callback_query(F.data == "checkout")
async def checkout(callback: CallbackQuery):
    """Оформление заказа"""
    user_id = callback.from_user.id
    cart_items = get_cart(user_id)

    if not cart_items:
        await callback.answer("Корзина пуста!", show_alert=True)
        return

    total = sum(item["price"] * item["quantity"] for item in cart_items)

    # Создаём описание заказа
    items_text = ", ".join([f"{item['name']} × {item['quantity']}" for item in cart_items])

    # Создаём платёж
    payment = create_payment(total, f"Заказ: {items_text}", user_id)

    if "confirmation" in payment:
        payment_url = payment["confirmation"]["confirmation_url"]
        payment_id = payment["id"]

        # Сохраняем заказ в БД
        add_order(user_id, items_text, total, payment_id)

        # Отправляем ссылку на оплату
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💳 Оплатить", url=payment_url)],
                [InlineKeyboardButton(text="✅ Я оплатил", callback_data=f"paid_{payment_id}")]
            ]
        )

        try:
            await callback.message.edit_text(
                f"💰 **Ваш заказ:**\n\n{items_text}\n\n"
                f"**Сумма:** {total:,.0f} ₽\n\n"
                "Нажмите кнопку ниже для оплаты 👇",
                reply_markup=kb,
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Не удалось обновить сообщение: {e}")
    else:
        await callback.answer("Ошибка при создании платежа. Попробуйте позже.", show_alert=True)


@router.callback_query(F.data.startswith("paid_"))
async def paid_callback(callback: CallbackQuery, bot: Bot):
    payment_id = callback.data.split("_")[1]
    status = check_payment_status(payment_id)

    if status == "succeeded":
        update_order_status(payment_id, "paid")
        clear_cart(callback.from_user.id)

        # Отправляем уведомление владельцу
        try:
            await bot.send_message(
                OWNER_CHAT_ID,
                f"✅ **Новый оплаченный заказ!**\n\n"
                f"Пользователь: @{callback.from_user.username or callback.from_user.first_name}\n"
                f"ID: {callback.from_user.id}\n\n"
                f"Заказ: {payment_id}"
            )
            print(f"Уведомление отправлено в {OWNER_CHAT_ID}")
        except Exception as e:
            print(f"Ошибка отправки уведомления: {e}")

        try:
            await callback.message.edit_text(
                "✅ **Оплата прошла успешно!**\n\n"
                "Мы получили ваш заказ и скоро свяжемся с вами.\n"
                "Спасибо за доверие! 🙌"
            )
        except Exception as e:
            print(f"Не удалось обновить сообщение: {e}")

    elif status == "pending":
        await callback.answer("⏳ Платёж ещё не завершён. Проверьте, что вы оплатили.", show_alert=True)
    else:
        await callback.answer("❌ Платёж не найден или отклонён. Попробуйте ещё раз.", show_alert=True)


@router.callback_query(F.data == "show_cart")
async def show_cart_callback(callback: CallbackQuery):
    """Показывает корзину по кнопке 'Перейти в корзину'"""
    cart_items = get_cart(callback.from_user.id)
    text = format_cart(cart_items)

    if cart_items:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🗑 Очистить корзину", callback_data="clear_cart")],
                [InlineKeyboardButton(text="✅ Оформить заказ", callback_data="checkout")]
            ]
        )
    else:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🛍 Перейти к витрине", callback_data="go_shop")]
            ]
        )

    try:
        await callback.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    except Exception as e:
        print(f"Не удалось обновить сообщение: {e}")
