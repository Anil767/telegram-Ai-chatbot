import os
from google import genai
from telegram.ext import ApplicationBuilder, MessageHandler, filters

client = genai.Client()
histories = {}

async def reply(update, context):
    if not update.message or not update.effective_user:
        return
    uid = update.effective_user.id
    history = histories.setdefault(uid, [])
    history.append({"role": "user", "parts": [{"text": update.message.text}]})
    response = await client.aio.models.generate_content(
        model="gemini-3.5-flash",
        contents=history[-20:],
        config={"system_instruction": "You are a helpful assistant. Reply in the user's language."},
    )
    text = response.text
    history.append({"role": "model", "parts": [{"text": text}]})
    await update.message.reply_text(text)

app =ApplicationBuilder().token(os.environ["TELEGRAM_TOKEN"]).connect_timeout(30).read_timeout(30).write_timeout(30).build()
app.add_handler(MessageHandler(filters.TEXT, reply))
app.run_polling()