from disnake.ext import commands
import disnake
import asyncio
import datetime
import textwrap
from supp import db_human
from supp import dt_human
# supp
async def send_picture(src, message):
    with open(src, 'rb') as f:
        picture = disnake.File(f)
        await message.channel.send(file=picture)
    return

# reminder 
class Timer:
    # __slots__ = ('author', 'name', 'description', 'id', 'created', 'duration', 'extra')

    def __init__(self, *, info):
        self.author = info['author']
        self.event = info['event']
        self.description = info['description']
        self.created = info['created']
        self.expires = info['expires']
        self.extra = info['extra']
        self.id = dt_human.sid()

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

    # async def call(self):
    #     self.bot.dispatch('reminder', str(self.expires))
    
    # async def dispatch(self):
    #     utcnow = datetime.datetime.utcnow()
    #     if self.expires >= utcnow:
    #         to_sleep = (self.expires - utcnow).total_seconds()
    #         await asyncio.sleep(to_sleep)
    #     await self.call()

    def __repr__(self):
        return f'<Timer created={self.created} expires={self.expires} event={self.event}>'

class Reminder():

    def __init__(self, bot):
        self.bot = bot
        self._current_timer = None
        self._task = bot.loop.create_task(self.dispatch_timers())
        self._timers = list()
    
    async def fetch_available_timers(self, num=5):
        query = f"SELECT * FROM reminder LIMIT {num}"
        timers = db_human.Sql().fetch(query)
        self._timers = list()
        for timer_info in timers:
            timer = Timer(info=self._timers[0])
            self._timers.append(Timer(info=timer_info))

    async def call_timer(self, timer):
        # move the timer record from reminder to reminder_arc
        db_human.Sql().execute(f"UPDATE reminder SET status = '0' where event_id = '{timer.event_id}'")
        db_human.Sql().execute(f"INSERT INTO reminder_arc SELECT * FROM reminder where event_id = '{timer.event_id}';")
        db_human.Sql().execute(f"DELETE FROM reminder where event_id = '{timer.event_id}'")

        # dispatch the event
        self.bot.dispatch('timer_complete', timer)

    async def load_timers(self, num=5):
        query = f"SELECT * FROM reminder LIMIT {num}"
        self._timers = db_human.Sql().fetch(query)

    async def dispatch_timers(self):
        try:
            while not self.bot.is_closed():
                if self._timers:
                    timer = self._current_timer = self._timers.pop()
                    now = datetime.datetime.utcnow()

                    if timer.expires >= now:
                        to_sleep = (timer.expires - now).total_seconds()
                        await asyncio.sleep(to_sleep)

                    if len(self._timers) < 2:
                        self.fetch_available_timers()
                    await self.call_timer(timer)
                else:
                    break
        except:
            self._task.cancel()
            self._task = self.bot.loop.create_task(self.dispatch_timers())

    async def create_timer(self, info: dict):

        columns = list(info.items())

        db_human.Sql().insert(table='reminder', columns=columns)
        timer = Timer(info=info)
        # check if this timer is earlier than our currently run timer
        if self._current_timer and timer.expires < self._current_timer.expires:
            # cancel the task and re-run it
            self._timers.append(timer)
            self._task.cancel()
            self._task = self.bot.loop.create_task(self.dispatch_timers())

        return timer

