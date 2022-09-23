import os
import discord
from dotenv import load_dotenv
import psycopg

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DB = os.getenv('DATABASE_URL')

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        # Fetch all users and their roles
        
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

    async def on_message(self, message):
        if message.author == client.user:
            return
        
        if message.content.startswith == '$hello':
            response = 'Hello!'
            await message.channel.send(response)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)
