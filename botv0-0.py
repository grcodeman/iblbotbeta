from pickle import TRUE
import discord, asyncio
from discord import app_commands

from ibltoken import get_token
from ibltoken import get_guild
from ibltoken import get_general
from ibltoken import get_botcommands

from heightroll import calc_height
from jsroll import roll_js
from viewstats import grab_stats
from viewbank import grab_teamac
from viewbank import grab_teambal
from viewbank import grab_bal
from viewbank import grab_claims
from submitform import submit_ac
from ibldb import add_name
from ibldb import get_name

guild = get_guild()
general = get_general()
botcommands = get_botcommands()

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
    app_commands.Choice(name="Random", value="random"),
    ], 
    position = [
    app_commands.Choice(name="PG", value="pg"),
    app_commands.Choice(name="SG", value="sg"),
    app_commands.Choice(name="SF", value="sf"),
    app_commands.Choice(name="PF", value="pf"),
    app_commands.Choice(name="C", value="c"),
    app_commands.Choice(name="Random", value="random"),
    ])
async def roll(interaction: discord.Interaction, archetype: app_commands.Choice[str], position: app_commands.Choice[str]):
    await interaction.response.defer()
    await asyncio.sleep(1)
    await interaction.followup.send(calc_height(position.value,archetype.value))

# jumpshot command
@tree.command(name="jumpshot", description="Roll a jumpshot (Required for Giant and Athletic)", guild=discord.Object(id=guild))
@app_commands.choices(type=[
    app_commands.Choice(name="5'10-6'4", value="guard"),
    app_commands.Choice(name="6'5-6'9", value="wing"),
    app_commands.Choice(name="6'10-7'3", value="big"),
    ])
async def roll(interaction: discord.Interaction, type: app_commands.Choice[str]):
    await interaction.response.defer()
    await asyncio.sleep(1)
    rolled = roll_js(type.value)
    await interaction.followup.send("`" + (interaction.user.name + "#" + interaction.user.discriminator) + "` rolled a " + type.name + " Jumpshot: **" + rolled + "**")

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
async def stats(interaction: discord.Interaction, season: app_commands.Choice[str], player: str=None):
    await interaction.response.defer()
    if (interaction.channel_id == general):
        await interaction.followup.send("Go to <#" + str(botcommands) + ">")
    else:
        if (player == None):
            player = get_name(interaction.user.id)
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
async def self(interaction: discord.Interaction, player: str=None):
    await interaction.response.defer()
    if (player == None):
        player = get_name(interaction.user.id)
    await interaction.followup.send(grab_bal(player))

# viewclaims command
@tree.command(name="viewclaims", description="View a player's claims for a period", guild=discord.Object(id=guild))
@app_commands.choices(week=[
    app_commands.Choice(name="Week 1", value="Week 1"),
    app_commands.Choice(name="Week 2", value="Week 2"),
    app_commands.Choice(name="Week 3", value="Week 3"),
    app_commands.Choice(name="Week 4", value="Week 4"),
    app_commands.Choice(name="Week 5", value="Week 5"),
    app_commands.Choice(name="Week 6", value="Week 6"),
    app_commands.Choice(name="Pre Season", value="Pre Season"),
    app_commands.Choice(name="All Star Break", value="All Star Break"),
    app_commands.Choice(name="Post Season", value="Post Season"),
    ])
async def viewclaims(interaction: discord.Interaction, week: app_commands.Choice[str], player: str=None):
    await interaction.response.defer()
    if (interaction.channel_id == general):
        await interaction.followup.send("Go to <#" + str(botcommands) + ">")
    else:
        if (player == None):
            player = get_name(interaction.user.id)
        await interaction.followup.send(grab_claims(week.value, player))

# ac command
@tree.command(name="ac", description="Submit an Activity Check (Weekly Checkin)", guild=discord.Object(id=guild))
async def self(interaction: discord.Interaction, player: str=None):
    await interaction.response.defer()
    if (player == None):
        player = get_name(interaction.user.id)
    await interaction.followup.send(submit_ac((interaction.user.name + "#" + interaction.user.discriminator),player))

# link command
@tree.command(name="link", description="Link your player's name to your account", guild=discord.Object(id=guild))
async def self(interaction: discord.Interaction, player: str):
    await interaction.response.defer()
    add_name(interaction.user.id,player)
    await interaction.followup.send("Linked name to `" + player + "`")

client.run(get_token())