# import


import discord
from discord import commands


# class
class Jail(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # setupjail
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setupjail(self, ctx):
        guild = ctx.guild
        jailedRole = discord.utils.get(guild.roles, name="Jailed")
        jailedChannel = discord.utils.get(guild.channels, name="jail")
        if jailedChannel or jailedRole:
            embed = discord.Embed(
                description=f"Config exists already or you tampered with it, to reconfigure it please do {prefix_data(ctx.guild.id)}unsetjail and run setupjail again",
                color=color_data())
            embed.set_author(name="Success!")
            successembed = await ctx.send(embed=embed, delete_after=10)
            await successembed.add_reaction("<:HikariCheckmark:821686378579361833>")
        if not jailedRole:
            createmsg = await ctx.send("Setting up Jail Role!")
            await createmsg.add_reaction("<a:HikariLoading:822433462141190166>")
            jailedRole = await guild.create_role(name="Jailed")
            await asyncio.sleep(2)
            await createmsg.delete()
            permmsg = await ctx.send("Setting up Permissions")
            await asyncio.sleep(1)
            await permmsg.add_reaction("<a:HikariLoading:822433462141190166")
            for channel in guild.channels:
                await channel.set_permissions(jailedRole, connect=False, read_messages=False, send_messages=False)


            await permmsg.delete()
            embed = discord.Embed(description="Jailed role created! Please dont rename the role or you will break it!",
                                  color=color_data())
            embed.set_author(name="Success!")
            successembed = await ctx.send(embed=embed, delete_after=15)
            await successembed.add_reaction("<:HikariCheckmark:821686378579361833>")
        if not jailedChannel:
            createmsg = await ctx.send("Setting up Jail Channel!")
            await createmsg.add_reaction("<a:HikariLoading:822433462141190166>")
            await guild.create_text_channel(name="jail")
            channel = discord.utils.get(guild.channels, name='jail')
            await asyncio.sleep(2)
            await createmsg.delete()
            permmsg = await ctx.send("Setting up Permissions")
            await asyncio.sleep(1)
            await permmsg.add_reaction("<a:HikariLoading:822433462141190166")
            await channel.set_permissions(ctx.guild.default_role, read_messages=False)
            await channel.set_permissions(jailedRole, read_messages=True, send_messages=True)
            await permmsg.delete()
            embed = discord.Embed(description="Jailed Channel created!",
                                  color=color_data())
            embed.set_author(name="Success!")
            successembed = await ctx.send(embed=embed, delete_after=10)
            await successembed.add_reaction("<:HikariCheckmark:821686378579361833>")
            await ctx.message.delete()


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unsetupjail(self, ctx):
        guild = ctx.guild
        jailedRole = discord.utils.get(guild.roles, name="Jailed")
        jailedChannel = discord.utils.get(guild.channels, name="jail")
        embed = discord.Embed(description="Fetching data from guild!",
                              color=color_data())
        fetchmsg = await ctx.send(embed=embed, delete_after=10)
        await fetchmsg.add_reaction("<:HikariCheckmark:821686378579361833>")
        await ctx.message.delete()
        await fetchmsg.delete()
        if jailedRole or jailedChannel:
            await asyncio.sleep(2)
            await jailedRole.delete()
            await jailedChannel.delete()
            embed = discord.Embed(description="Deleted all Jail data!",
                                  color=color_data())
            embed.set_author(name="Success!")
            successembed = await ctx.send(embed=embed, delete_after=10)
            await successembed.add_reaction("<:HikariCheckmark:821686378579361833>")
        if not jailedRole or jailedChannel:
            return

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def jail(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        jailedRole = discord.utils.get(guild.roles, name="Jailed")
        if not jailedRole:
            await ctx.send(f"You didn't run the Jail Setup yet! Please run {prefix_data(ctx.guild.id)}setupjail !")
            return
        if jailedRole:
            await member.add_roles(jailedRole, reason=reason)
            embed1 = discord.Embed(color=color_data())
            embed1.set_author(name=f"You got jailed "
                                   f"in {ctx.guild.name}!")
            embed1.add_field(name="Reason:", value=f"{reason}", inline=False)
            await member.send(embed=embed1)
            embed2 = discord.Embed(color=color_data())
            embed2.set_author(name=f"{member.name} got jailed!")
            embed2.add_field(name="Reason:", value=f"{reason}", inline=False)
            await ctx.message.reply(embed=embed2, mention_author=False)

    # Unjail
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unjail(self, ctx, member: discord.Member):
        jailedRole = discord.utils.get(ctx.guild.roles, name="Jailed")
        await member.remove_roles(jailedRole)
        embed1 = discord.Embed(color=color_data())
        embed1.set_author(name=f"You got unjailed on {ctx.guild.name}")
        embed3 = discord.Embed(color=color_data())
        await member.send(embed=embed1)
        embed3.set_author(name=f"{member.name} got unjailed!")
        await ctx.message.reply(embed=embed3, mention_author=False)


def setup(bot):
    bot.add_cog(Jail(bot))
