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
                
                    cur.execute("INSERT INTO members (username, display_name) VALUES (%s, %s)", ([member.name+member.discriminator, m.display_name]))
                    for role in m.roles:
                        cur.execute("INSERT INTO roles (name) VALUES (%s) ON CONFLICT DO NOTHING", ([role.name]))
                        cur.execute("INSERT INTO member_to_role_map (member_username, role_name) VALUES (%s, %s)", (member.name+member.discriminator, role.name))
                    conn.commit()

def get_roles_for_user_by_display_name(display_name):
    like_pattern = '{}%'.format(display_name)
    with psycopg.connect(DB) as conn:
        with conn.cursor() as cur:
            cur.execute("""select username, display_name, role_name from members 
inner join member_to_role_map on members.username = member_to_role_map.member_username 
where display_name like (%s)""", (like_pattern, ))
            rows = cur.fetchall()
            cur.close()
            return rows

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
            after_command = message.content.split('$time ')[1]
            print(after_command)

            if after_command != '':
                member_roles = get_roles_for_user_by_display_name(after_command)
                for role in member_roles:
                    role_name = role[2]
                    if role_name.startswith("UTC"):
                        offset = role_name.split("UTC")[1]
                        now_utc = datetime.datetime.now(datetime.timezone.utc)
                        local = now_utc + datetime.timedelta(hours=int(offset))
                        local_string = datetime.datetime.strftime(local, "%Y-%m-%d %H:%M")
                        response = f'The datetime for {role[1]} is **{local_string}** (Role: {role_name})'
                        await message.channel.send(response)
                        return

                # no UTC roles
                await message.channel.send('Couldn\'t find timezone role for user.')
            else:
                # TODO: Print some common timezones for active members
                now = datetime.datetime.now(datetime.timezone.utc)
                local = now + datetime.timedelta(hours=11)
                response = datetime.datetime.strftime(local, "%Y-%m-%d %H:%M:%S")
                await message.channel.send(response)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)
