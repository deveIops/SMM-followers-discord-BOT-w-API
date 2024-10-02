import discord
from discord.ext import commands
from discord.ui import Button, View

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Créer un ticket", style=discord.ButtonStyle.primary)
    async def create_ticket(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)  

        guild = interaction.guild  
        author = interaction.user
        base_channel_name = f"ticket-{author.name.lower()}"

        existing_channel = discord.utils.get(guild.text_channels, name=base_channel_name)
        if existing_channel:
            await interaction.followup.send("Vous avez déjà un ticket ouvert.", ephemeral=True)
            return

        channel_name = base_channel_name
        counter = 1
        while discord.utils.get(guild.text_channels, name=channel_name):
            channel_name = f"{base_channel_name}-{counter}"
            counter += 1

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            author: discord.PermissionOverwrite(read_messages=True)
        }
        channel = await guild.create_text_channel(name=channel_name, overwrites=overwrites)

        await channel.send(f"Bonjour {author.mention}, merci d'avoir créé un ticket. Un membre de notre équipe vous assistera bientôt.")
        await interaction.followup.send(f"Votre ticket a été créé: {channel.mention}", ephemeral=True)

class TicketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ticket(self, ctx):
        embed = discord.Embed(
            title="TikTok",
            description="Cliquez sur le bouton ci-dessous pour créer un ticket.",
            color=discord.Color.from_rgb(255, 255, 255)
        )
        view = TicketView()
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def close(self, ctx):
        if ctx.channel.name.startswith("ticket-"):
            await ctx.channel.delete()
        else:
            await ctx.send("Cette commande ne peut être utilisée que dans un ticket.")

async def setup(bot):
    await bot.add_cog(TicketCog(bot))
