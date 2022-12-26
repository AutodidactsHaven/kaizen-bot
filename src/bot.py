import os
import datetime
import discord
from dotenv import load_dotenv
import psycopg

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DB = os.getenv('DATABASE_URL')

def populate_db():
    # Connect to an existing database
    with psycopg.connect(DB) as conn:
            # Open a cursor to perform database operations
            with conn.cursor() as cur:
                cur.execute("DELETE FROM member_to_role_map")
                cur.execute("DELETE FROM members")
                for member in client.guilds[0].members:
                    m = client.guilds[0].get_member(member.id)
                    print(m)
                
                    cur.execute("INSERT INTO members (username) VALUES (%s)", ([member.name+member.discriminator]))
                    for role in m.roles:
                        cur.execute("INSERT INTO roles (name) VALUES (%s) ON CONFLICT DO NOTHING", ([role.name]))
                        cur.execute("INSERT INTO member_to_role_map (member_username, role_name) VALUES (%s, %s)", (member.name+member.discriminator, role.name))
                    conn.commit()

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        # Fetch all users and their roles
        populate_db()

    async def on_message(self, message):
        if message.author == client.user:
            return
        
        if message.content.startswith('$hello'):
            response = 'Hello!'
            await message.channel.send(response)

        if message.content.startswith('$time'):
            if message.mentions:
                mentioned_member = message.mentions[0]
                member_info = client.guilds[0].get_member(mentioned_member.id)
                for role in member_info.roles:
                    if role.name.startswith("UTC"):
                        offset = role.name.split("UTC")[1]
                        now_utc = datetime.datetime.now(datetime.timezone.utc)
                        local = now_utc + datetime.timedelta(hours=int(offset))
                        local_string = datetime.datetime.strftime(local, "%Y-%m-%d %H:%M")
                        response = f'The datetime for {member_info.name} is **{local_string}** (Role: {role.name})'
                        await message.channel.send(response)
                        return

                # no UTC roles
                await message.channel.send('Couldn\'t find timezone role for user.')

                # TODO:
                # fetch roles for member from database
                # get UTC role if there is one
                # add the +/- UTC offset to the current time
                # send response
            else:
                # Print some common timezones for active members
                now = datetime.datetime.now(datetime.timezone.utc)
                local = now + datetime.timedelta(hours=11)
                response = datetime.datetime.strftime(local, "%Y-%m-%d %H:%M:%S")
                await message.channel.send(response)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)
