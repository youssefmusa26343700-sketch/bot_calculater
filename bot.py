import logging
import math
import re
from fractions import Fraction
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

user_data = {}

# -----------------------
# لوحة احترافية مع زر الكسر
# -----------------------
def build_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("(", callback_data="("),
            InlineKeyboardButton(")", callback_data=")"),
            InlineKeyboardButton("√", callback_data="SQRT"),
            InlineKeyboardButton("𝑎⁄𝑏", callback_data="FRAC"),
            InlineKeyboardButton("⌫", callback_data="BACK"),
            InlineKeyboardButton("AC", callback_data="AC")
        ],
        [
            InlineKeyboardButton("7", callback_data="7"),
            InlineKeyboardButton("8", callback_data="8"),
            InlineKeyboardButton("9", callback_data="9"),
            InlineKeyboardButton("÷", callback_data="/")
        ],
        [
            InlineKeyboardButton("4", callback_data="4"),
            InlineKeyboardButton("5", callback_data="5"),
            InlineKeyboardButton("6", callback_data="6"),
            InlineKeyboardButton("×", callback_data="*")
        ],
        [
            InlineKeyboardButton("1", callback_data="1"),
            InlineKeyboardButton("2", callback_data="2"),
            InlineKeyboardButton("3", callback_data="3"),
            InlineKeyboardButton("−", callback_data="-")
        ],
        [
            InlineKeyboardButton("0", callback_data="0"),
            InlineKeyboardButton(".", callback_data="."),
            InlineKeyboardButton("=", callback_data="="),
            InlineKeyboardButton("+", callback_data="+")
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# -----------------------
# تقييم العملية مع دعم الكسور
# -----------------------
def evaluate_expression(expr):
    try:
        expr = expr.replace("÷", "/").replace("×", "*").replace("−", "-")

        # √(9) → math.sqrt(9)
        expr = re.sub(r'√\((.*?)\)', r'math.sqrt(\1)', expr)

        # تحويل الأرقام إلى Fraction
        tokens = re.split(r'(\D)', expr)
        new_expr = ""

        for t in tokens:
            if t.isdigit():
                new_expr += f"Fraction({t})"
            else:
                new_expr += t

        result = eval(new_expr)
        return str(result)

    except:
        return "خطأ ❌"


# -----------------------
# start
# -----------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id] = ""
    await update.message.reply_text(
        "🧮 **PRO Calculator (Fractions)**\n\n`0`",
        parse_mode="Markdown",
        reply_markup=build_keyboard()
    )


# -----------------------
# الأزرار
# -----------------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if user_id not in user_data:
        user_data[user_id] = ""

    data = query.data

    if data == "AC":
        user_data[user_id] = ""

    elif data == "BACK":
        user_data[user_id] = user_data[user_id][:-1]

    elif data == "SQRT":
        user_data[user_id] += "√("

    elif data == "FRAC":
        user_data[user_id] += "/"

    elif data == "=":
        user_data[user_id] = evaluate_expression(user_data[user_id])

    else:
        user_data[user_id] += data

    text = user_data[user_id] if user_data[user_id] else "0"

    await query.edit_message_text(
        f"🧮 **PRO Calculator (Fractions)**\n\n`{text}`",
        parse_mode="Markdown",
        reply_markup=build_keyboard()
    )


# -----------------------
# تشغيل
# -----------------------
def main():
    app = ApplicationBuilder().token("PUT_YOUR_BOT_TOKEN").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("Calculator Running...")
    app.run_polling()


if __name__ == "__main__":
    main()
