from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import logging
import openai

load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY
# print("Ok")

MODEL_NAME = "gpt-3.5-turbo"

# initialize bot
bot = Bot(token=API_TOKEN) # creating bot object
dispatcher = Dispatcher(bot) # passing the bot object

# In the reference it is getting saved everything
class Reference:
    def __init__(self) -> None:
        self.response = ""

# initializing the reference class
reference = Reference()

# Forget the previous chat
def clear_past():
    reference.response = ""


# Welcome screen message
@dispatcher.message_handler(commands=['start'])
async def welcome(message:types.Message):
    """This handler receives messages with `/start` or `/help `command

    Args:
        message (types.Message): _description_
    """
    await message.reply("Hi!\nI am a Chat Bot! Created by Kunal. How can I assist you?")


# If user is giving "help" command then show me this window
@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi there, I'm a bot created by Kunal! Please follow these commands - 
    /start - to start the conversation.
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)


# Function for clear operation
@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context.")


# Final (Main) Bot
@dispatcher.message_handler()
async def main_bot(message: types.Message):
    """
    A handler to process the user's input and generate a response using the openai API.
    """

    print(f">>> USER: \n\t{message.text}")

    # prompt technique
    response = openai.ChatCompletion.create(
        model = MODEL_NAME,
        messages = [
            {"role": "assistant", "content": reference.response}, # role assistant
            {"role": "user", "content":message.text} # our query
        ]
    )
    reference.response = response['choices'][0]['message']['content'] # response will be in json format so I will extract the content of the response
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response) # send the response to the telegram


if __name__=="__main__":
    executor.start_polling(dispatcher, skip_updates=True)
