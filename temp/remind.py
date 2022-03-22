from disnake.ext import commands
import disnake
import asyncio
import datetime
import textwrap


class Timer:
    # __slots__ = ('author', 'name', 'description', 'id', 'created', 'duration', 'extra')

    def __init__(self, *, info, bot):
        self.author = info['author']
        self.name = info['name']
        self.description = info['description']
        self.created = info['created']
        self.duration = info['duration']
        self.extra = info['extra']
        self.id = str(self.created)
        print(self.created, self.duration)
        self.expires = self.created + self.duration
        print(self.created, self.duration)
        self.bot = bot
    
    @property
    def passed(self):
        return None

    @property
    def remaining(self):
        return None
    
    @property
    def author_id(self):
        if self.args:
            return int(self.args[0])
        return None

    async def call(self):
        self.bot.dispatch('reminder', str(self.expires))
    
    async def dispatch(self):
        utcnow = datetime.datetime.utcnow()
        if self.expires >= utcnow:
            to_sleep = (self.expires - utcnow).total_seconds()
            await asyncio.sleep(to_sleep)
        await self.call()

