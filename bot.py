import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# লগিং সেটআপ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# সরাসরি টোকেন এবং এপিআই কি এখানে বসানো হলো
TELEGRAM_TOKEN = '9062966168:AAG-TZh3iONmRi8ygX4eg52teNfiIlChwYE'
GEMINI_KEY = 'AQ.Ab8RN6JQgqEDj8jJ6HtpjR3ft_DL1t0kThLVA0rlhN_WhdxhIw'

# জেমিনি কনফিগারেশন
genai.configure(api_key=GEMINI_KEY)
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 2048,
}
model = genai.GenerativeModel(
    model_name="gemini-1.5pro",
    generation_config=generation_config
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if not user_text:
        return

    try:
        # জেমিনি থেকে রেসপন্স নেওয়া
        response = model.generate_content(user_text)
        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("দুঃখিত, এই প্রম্পট থেকে কোনো উত্তর তৈরি করা সম্ভব হয়নি।")
    except Exception as e:
        logging.error(f"Error generating content: {e}")
        await update.message.reply_text("দুঃখিত, এই মুহূর্তে আমি উত্তর দিতে পারছি না।")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # টেক্সট মেসেজ হ্যান্ডলার
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(echo_handler)
    
    print("Bot is running...")
    application.run_polling()
    
