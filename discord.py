import discord
from discord_webhook import DiscordWebhook
from dotenv import load_dotenv
import os

class Discord:
    def __init__(self):
        load_dotenv()

        self.thread1_webhook = os.getenv('Discord_t1_webhook')
        self.login_webhook = os.getenv('Discord_login_webhook')

    def ThreadsLog(self, message):
        webhook = DiscordWebhook(url=self.thread1_webhook, content=f'{message}')
        response = webhook.execute()
    
    def LoginLog(self, message):
        webhook = DiscordWebhook(url=self.login_webhook, content=f'{message}')
        response = webhook.execute()