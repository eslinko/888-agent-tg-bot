import openai
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from config.settings import TELEGRAM_TOKEN, AI_API_KEY

# Настройка OpenAI API
openai.api_key = AI_API_KEY

# Словарь для хранения состояния беседы каждого пользователя
user_sessions = {}

# Основное меню с кнопками
async def menu(update: Update, context: CallbackContext) -> None:
    """Отображение главного меню."""
    reply_keyboard = [
        ["📋 My complaints", "👥 Groups"],
        ["✍️ Raise complaint", "👤 Profile"]
    ]
    await update.message.reply_text(
        "Choose from the menu:",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True, one_time_keyboard=False
        )
    )

# Обработчики для пунктов меню
def my_complaints(update: Update, context: CallbackContext) -> None:
    """Показывает список жалоб пользователя."""
    update.message.reply_text("📋 Here you can see your complaints.")

def groups(update: Update, context: CallbackContext) -> None:
    """Показывает доступные группы."""
    update.message.reply_text("👥 Here you can see your groups.")

def raise_complaint(update: Update, context: CallbackContext) -> None:
    """Позволяет подать жалобу."""
    update.message.reply_text("✍️ Write a description of your complaint, and I will help you.")

def profile(update: Update, context: CallbackContext) -> None:
    """Отображает профиль пользователя."""
    update.message.reply_text("👤 This is your profile. Here you can see your information.")

# Обработчик для всех пунктов меню
async def handle_menu_selection(update: Update, context: CallbackContext) -> None:
    """Обрабатывает выбор пользователя из меню."""
    text = update.message.text
    if text == "📋 My complaints":
        await update.message.reply_text("📋 Here you can see your complaints.")
    elif text == "👥 Groups":
        await update.message.reply_text("👥 Here you can see your groups.")
    elif text == "✍️ Raise complaint":
        await update.message.reply_text("✍️ Write a description of your complaint, and I will help you.")
    elif text == "👤 Profile":
        await update.message.reply_text("👤 This is your profile. Here you can see your information.")

async def start(update: Update, context: CallbackContext) -> None:
    """Приветствие при запуске бота."""
    user_id = update.message.from_user.id
    user_sessions[user_id] = []  # Инициализация нового диалога
    await update.message.reply_text("Hey! I'm your #dogecomplaints assistant. Use the menu to navigate.")
    await menu(update, context)  # Показываем меню сразу после приветствия

async def reset(update: Update, context: CallbackContext) -> None:
    """Сброс диалога для пользователя."""
    user_id = update.message.from_user.id
    user_sessions[user_id] = []  # Сбрасываем историю сообщений
    await update.message.reply_text("Dialog reset. Start chatting again!")

def chat_with_openai(user_id: int, user_message: str) -> str:
    """Отправка сообщения модели OpenAI и получение ответа с учетом истории."""
    # История сообщений для текущего пользователя
    user_history = user_sessions.get(user_id, [])
    
    # Добавляем сообщение пользователя в историю
    user_history.append({"role": "user", "content": user_message})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты умный и дружелюбный помощник."}
            ] + user_history,  # История сообщений включается в запрос
            max_tokens=1000,
            temperature=0.7,
        )
        # Получаем ответ модели
        ai_response = response["choices"][0]["message"]["content"].strip()
        
        # Добавляем ответ модели в историю
        user_history.append({"role": "assistant", "content": ai_response})
        
        # Сохраняем обновленную историю
        user_sessions[user_id] = user_history
        
        return ai_response
    except Exception as e:
        return f"An error occurred while querying OpenAI: {e}"

async def handle_message(update: Update, context: CallbackContext) -> None:
    """Обработка сообщений от пользователя."""
    user_id = update.message.from_user.id
    user_message = update.message.text
    await update.message.reply_text("Processing request...")
    
    # Вызов OpenAI API с учетом истории сообщений
    ai_response = chat_with_openai(user_id, user_message)
    update.message.reply_text(ai_response)

def main():
    """Запуск Telegram-бота."""
    # Создаем приложение
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reset", reset))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_selection))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
