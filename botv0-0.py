import discord, asyncio
from discord import app_commands

from heightroll import calc_height
from viewstats import grab_stats
from viewbank import grab_teamac
from viewbank import grab_teambal
from viewbank import grab_bal

guild = 1004183670086713445
general = 1004183672720720016
botcommands = 1017795880553824359

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        if not self.synced:
            await tree.sync(guild = discord.Object(id = guild))
            self.synced = True
        print(f"We have logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)

# roll command
@tree.command(name="roll", description="Roll a height using the IBL odds", guild=discord.Object(id=guild))
@app_commands.choices(archetype=[
    app_commands.Choice(name="Tiny", value="tiny"),
    app_commands.Choice(name="Skilled", value="skilled"),
    app_commands.Choice(name="Athletic", value="athletic"),
    app_commands.Choice(name="Giant", value="giant"),
    ], 
    position = [
    app_commands.Choice(name="PG", value="pg"),
    app_commands.Choice(name="SG", value="sg"),
    app_commands.Choice(name="SF", value="sf"),
    app_commands.Choice(name="PF", value="pf"),
    app_commands.Choice(name="C", value="c"),
    ])
async def roll(interaction: discord.Interaction, archetype: app_commands.Choice[str], position: app_commands.Choice[str]):
    await interaction.response.defer()
    await asyncio.sleep(2)
    await interaction.followup.send(calc_height(position.value,archetype.value))

# stats command
@tree.command(name="stats", description="View a players stat line", guild=discord.Object(id=guild))
@app_commands.choices(season=[
    app_commands.Choice(name="1", value="1"),
    app_commands.Choice(name="2", value="2"),
    app_commands.Choice(name="3", value="3"),
    app_commands.Choice(name="4", value="4"),
    app_commands.Choice(name="5", value="5"),
    app_commands.Choice(name="6", value="6"),
    app_commands.Choice(name="7", value="7"),
    app_commands.Choice(name="8", value="8"),
    app_commands.Choice(name="9", value="9"),
    app_commands.Choice(name="10", value="10"),
    ])
async def stats(interaction: discord.Interaction, season: app_commands.Choice[str], player: str):
    await interaction.response.defer()
    if (interaction.channel_id == general):
        await interaction.followup.send("Go to <#" + str(botcommands) + ">")
    else:
        await interaction.followup.send(grab_stats(season.value,player))

# teamac command
@tree.command(name="teamac", description="View a team's AC status", guild=discord.Object(id=guild))
@app_commands.choices(team=[
    app_commands.Choice(name="76ers", value="76ers"),
    app_commands.Choice(name="Raptors", value="Raptors"),
    app_commands.Choice(name="Wizards", value="Wizards"),
    app_commands.Choice(name="Rockets", value="Rockets"),
    app_commands.Choice(name="Grizzlies", value="Grizzlies"),
    app_commands.Choice(name="Hawks", value="Hawks"),
    app_commands.Choice(name="Magic", value="Magic"),
    app_commands.Choice(name="Clippers", value="Clippers"),
    app_commands.Choice(name="Knicks", value="Knicks"),
    app_commands.Choice(name="Lakers", value="Lakers"),
    app_commands.Choice(name="Nuggets", value="Nuggets"),
    app_commands.Choice(name="Sonics", value="Sonics"),
    app_commands.Choice(name="Suns", value="Suns"),
    app_commands.Choice(name="Thunder", value="Thunder"),
    app_commands.Choice(name="Bucks", value="Bucks"),
    app_commands.Choice(name="Warriors", value="Warriors"),
    app_commands.Choice(name="Iowa Wolves", value="Iowa Wolves"),
    app_commands.Choice(name="Sky Hawks", value="Sky Hawks"),
    app_commands.Choice(name="Cleveland Charge", value="Cleveland Charge"),
    app_commands.Choice(name="Santa Cruz Warriors", value="Santa Cruz Warriors"),
    app_commands.Choice(name="Grand Rapid Gold", value="Grand Rapid Gold"),
    app_commands.Choice(name="Stockton Kings", value="Stockton Kings"),
    app_commands.Choice(name="The Hive", value="The Hive"),
    app_commands.Choice(name="Raptors 905", value="Raptors 905"),
    ])
async def viewac(interaction: discord.Interaction, team: app_commands.Choice[str]):
    await interaction.response.defer()
    if (interaction.channel_id == general):
        await interaction.followup.send("Go to <#" + str(botcommands) + ">")
    else:
        await interaction.followup.send(grab_teamac(team.value))

# teambal command
@tree.command(name="teambal", description="View a team's XP balance", guild=discord.Object(id=guild))
@app_commands.choices(team=[
    app_commands.Choice(name="76ers", value="76ers"),
    app_commands.Choice(name="Raptors", value="Raptors"),
    app_commands.Choice(name="Wizards", value="Wizards"),
    app_commands.Choice(name="Rockets", value="Rockets"),
    app_commands.Choice(name="Grizzlies", value="Grizzlies"),
    app_commands.Choice(name="Hawks", value="Hawks"),
    app_commands.Choice(name="Magic", value="Magic"),
    app_commands.Choice(name="Clippers", value="Clippers"),
    app_commands.Choice(name="Knicks", value="Knicks"),
    app_commands.Choice(name="Lakers", value="Lakers"),
    app_commands.Choice(name="Nuggets", value="Nuggets"),
    app_commands.Choice(name="Sonics", value="Sonics"),
    app_commands.Choice(name="Suns", value="Suns"),
    app_commands.Choice(name="Thunder", value="Thunder"),
    app_commands.Choice(name="Bucks", value="Bucks"),
    app_commands.Choice(name="Warriors", value="Warriors"),
    app_commands.Choice(name="Iowa Wolves", value="Iowa Wolves"),
    app_commands.Choice(name="Sky Hawks", value="Sky Hawks"),
    app_commands.Choice(name="Cleveland Charge", value="Cleveland Charge"),
    app_commands.Choice(name="Santa Cruz Warriors", value="Santa Cruz Warriors"),
    app_commands.Choice(name="Grand Rapid Gold", value="Grand Rapid Gold"),
    app_commands.Choice(name="Stockton Kings", value="Stockton Kings"),
    app_commands.Choice(name="The Hive", value="The Hive"),
    app_commands.Choice(name="Raptors 905", value="Raptors 905"),
    ])
async def viewbal(interaction: discord.Interaction, team: app_commands.Choice[str]):
    await interaction.response.defer()
    if (interaction.channel_id == general):
        await interaction.followup.send("Go to <#" + str(botcommands) + ">")
    else:
        await interaction.followup.send(grab_teambal(team.value))

# bal command
@tree.command(name="bal", description="View a player's XP balance", guild=discord.Object(id=guild))
async def self(interaction: discord.Interaction, player: str):
    await interaction.response.defer()
    await interaction.followup.send(grab_bal(player))

client.run('MTAwNDE3ODMzOTU4NzcwMjgyNQ.GhXiJZ.gbWQp_wtpIxVHr9gtQcbpi6IIKpJIZSobwpYbc')