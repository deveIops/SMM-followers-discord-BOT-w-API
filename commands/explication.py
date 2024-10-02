import discord
from discord.ext import commands

class ExplicationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ex')
    async def send_explication(self, ctx):
        tiktok_emoji = self.bot.get_emoji(1270918142998085644)
        if not tiktok_emoji:
            await ctx.send("L'emoji personnalisé TikTok n'a pas été trouvé.")
            return
        
        message = (
            f"{tiktok_emoji} **Voici le prix des followers tiktok de ce serveur ! **\n\n"
            "Pour obtenir **1000 followers** vous devez dépenser **34 centimes.**\n"
            "Il vous suffit de faire le calcul pour les autres paliers d'abonnées.\n\n"
            "Merci d'envoyer le nom d'utilisateur de votre tiktok et de **vous mettre en public** si vous souhaitez passer commande chez nous.\n\n"
            ":warning: **Aucun mot de passe vous sera demandé.**"
        )
        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(ExplicationCog(bot))
