import json, colorama

from discord.ext import commands
from discord import Embed


class SendAlert(commands.Bot):
    
    def __init__(self, error, project_path):
        super().__init__('/')

        self.project_path = project_path

        self.token = self.get_token()
        self.error = error
                
        @self.event
        async def on_ready():
            self.init_all()
            await self.send_error()
            print(f'{colorama.Fore.RED}/!\ Alerte envoyée{colorama.Fore.RESET}')
            await self.close()
        
        self.run(self.token)


    def init_all(self):
        self.init_embed()
        self.init_user()
        
    
    def init_embed(self):
        self.embed = Embed(
            color=0xA90000,
            description=f"""```py\n{self.error}```"""
        )
        
        self.embed.set_author(icon_url="https://cdn.discordapp.com/attachments/963473510544572476/999698093333282847/filigrane.png", name="Une erreur s'est produite")
    
    
    def init_user(self):
        guild_id = 481207830595108875
        self.guild = self.get_guild(guild_id)
        
        channel_id = 876151055577145344
        self.channel = self.guild.get_channel(channel_id)
        
            
    def get_token(self):
        with open(self.project_path + 'assets/tools/other/statistics.json', 'r') as file_object:
            json_file = json.load(file_object)
        
        token = json_file['bot']['token']
        return token

                
    async def send_error(self):
        await self.channel.send(embed=self.embed, content="<@399592144157016065>")

