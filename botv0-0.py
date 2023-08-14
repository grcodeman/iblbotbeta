from pickle import TRUE
import discord, asyncio
from discord import app_commands

from ibltoken import get_token, get_guild, get_general, get_botcommands

from heightroll import calc_height
from jsroll import roll_js
from viewstats import grab_stats, cached_stats
from viewbank import grab_teamac, grab_teambal, grab_bal, grab_claims
from submitform import submit_ac, submit_claim
from ibldb import add_name, get_name
from viewmr import grab_mr, find_row
from countryroll import roll_country

guild = get_guild()
general = get_general()
botcommands = get_botcommands()

# for stats
default_season = 12

# for mr viewing
info_start = 2
overview_start = 19
att_start = 32

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"We have logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)

# To restrict to main server use as a command argument: , guild=discord.Object(id=guild)

# roll command
@tree.command(name="roll", description="Roll a height using the IBL odds")
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
@tree.command(name="jumpshot", description="Roll a jumpshot (Required for Giant and Athletic)")
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
@tree.command(name="stats", description="View a players stat line")
@app_commands.choices(type=[
    app_commands.Choice(name="Cached (Recommended)", value="cached"),
    app_commands.Choice(name="Live", value="live"),
    ],
    season=[
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
    app_commands.Choice(name="11", value="11"),
    app_commands.Choice(name="12", value="12"),
    app_commands.Choice(name="13", value="13"),
    ])
async def stats(interaction: discord.Interaction, type: app_commands.Choice[str], season: app_commands.Choice[str]=None, player: str=None):
    await interaction.response.defer()
    if (interaction.channel_id == general):
        await interaction.followup.send("Go to <#" + str(botcommands) + ">")
    else:
        if (player == None):
            player = get_name(interaction.user.id)

        if (season == None):
            season = default_season
        else:
            season = season.value

        if (type.value == "live"):
            await interaction.followup.send(grab_stats(season,player))
        elif (type.value == "cached"):
            await interaction.followup.send(cached_stats(season,player))
        else:
            await interaction.followup.send("Process Failed")

# teamac command
@tree.command(name="teamac", description="View a team's AC status")
@app_commands.choices(team=[
    app_commands.Choice(name="76ers", value="76ers"),
    app_commands.Choice(name="Cavs", value="Cavs"),
    app_commands.Choice(name="Nets", value="Nets"),
    app_commands.Choice(name="Rockets", value="Rockets"),
    app_commands.Choice(name="Grizzlies", value="Grizzlies"),
    app_commands.Choice(name="Hawks", value="Hawks"),
    app_commands.Choice(name="Magic", value="Magic"),
    app_commands.Choice(name="Heat", value="Heat"),
    app_commands.Choice(name="Knicks", value="Knicks"),
    app_commands.Choice(name="Lakers", value="Lakers"),
    app_commands.Choice(name="Nuggets", value="Nuggets"),
    app_commands.Choice(name="Sonics", value="Sonics"),
    app_commands.Choice(name="Suns", value="Suns"),
    app_commands.Choice(name="Thunder", value="Thunder"),
    app_commands.Choice(name="Pistons", value="Pistons"),
    app_commands.Choice(name="Warriors", value="Warriors"),
    ],
    teamcu=[
    app_commands.Choice(name="Iowa Wolves", value="Iowa Wolves"),
    app_commands.Choice(name="Sky Hawks", value="Sky Hawks"),
    app_commands.Choice(name="Cleveland Charge", value="Cleveland Charge"),
    app_commands.Choice(name="Santa Cruz Warriors", value="Santa Cruz Warriors"),
    app_commands.Choice(name="Grand Rapid Gold", value="Grand Rapid Gold"),
    app_commands.Choice(name="Stockton Kings", value="Stockton Kings"),
    app_commands.Choice(name="Greensboro Swarm", value="Greensboro Swarm"),
    app_commands.Choice(name="Raptors 905", value="Raptors 905"),
    app_commands.Choice(name="OKC Blue", value="OKC Blue"),
    app_commands.Choice(name="Long Island Nets", value="Long Island Nets"),
    ])
async def teamac(interaction: discord.Interaction, team: app_commands.Choice[str]=None, teamcu: app_commands.Choice[str]=None):
    await interaction.response.defer()
    if (interaction.channel_id == general):
        await interaction.followup.send("Go to <#" + str(botcommands) + ">")
    else:
        selected_team = ""
        if (team != None):
            selected_team = team.value
        elif (teamcu != None):
            selected_team = teamcu.value
        else:
            await interaction.followup.send("Select a team")

        if (selected_team != ""):
            await interaction.followup.send(grab_teamac(selected_team))

# teambal command
@tree.command(name="teambal", description="View a team's XP balance")
@app_commands.choices(team=[
    app_commands.Choice(name="76ers", value="76ers"),
    app_commands.Choice(name="Cavs", value="Cavs"),
    app_commands.Choice(name="Nets", value="Nets"),
    app_commands.Choice(name="Rockets", value="Rockets"),
    app_commands.Choice(name="Grizzlies", value="Grizzlies"),
    app_commands.Choice(name="Hawks", value="Hawks"),
    app_commands.Choice(name="Magic", value="Magic"),
    app_commands.Choice(name="Heat", value="Heat"),
    app_commands.Choice(name="Knicks", value="Knicks"),
    app_commands.Choice(name="Lakers", value="Lakers"),
    app_commands.Choice(name="Nuggets", value="Nuggets"),
    app_commands.Choice(name="Sonics", value="Sonics"),
    app_commands.Choice(name="Suns", value="Suns"),
    app_commands.Choice(name="Thunder", value="Thunder"),
    app_commands.Choice(name="Pistons", value="Pistons"),
    app_commands.Choice(name="Warriors", value="Warriors"),
    ],
    teamcu=[
    app_commands.Choice(name="Iowa Wolves", value="Iowa Wolves"),
    app_commands.Choice(name="Sky Hawks", value="Sky Hawks"),
    app_commands.Choice(name="Cleveland Charge", value="Cleveland Charge"),
    app_commands.Choice(name="Santa Cruz Warriors", value="Santa Cruz Warriors"),
    app_commands.Choice(name="Grand Rapid Gold", value="Grand Rapid Gold"),
    app_commands.Choice(name="Stockton Kings", value="Stockton Kings"),
    app_commands.Choice(name="Greensboro Swarm", value="Greensboro Swarm"),
    app_commands.Choice(name="Raptors 905", value="Raptors 905"),
    app_commands.Choice(name="OKC Blue", value="OKC Blue"),
    app_commands.Choice(name="Long Island Nets", value="Long Island Nets"),
    ])
async def teambal(interaction: discord.Interaction, team: app_commands.Choice[str]=None, teamcu: app_commands.Choice[str]=None):
    await interaction.response.defer()
    if (interaction.channel_id == general):
        await interaction.followup.send("Go to <#" + str(botcommands) + ">")
    else:
        selected_team = ""
        if (team != None):
            selected_team = team.value
        elif (teamcu != None):
            selected_team = teamcu.value
        else:
            await interaction.followup.send("Select a team")

        if (selected_team != ""):
            await interaction.followup.send(grab_teambal(selected_team))

# bal command
@tree.command(name="bal", description="View a player's XP balance")
async def self(interaction: discord.Interaction, player: str=None):
    await interaction.response.defer()
    if (player == None):
        player = get_name(interaction.user.id)
    await interaction.followup.send(grab_bal(player))

# viewclaims command
@tree.command(name="viewclaims", description="View a player's claims for a period")
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
@tree.command(name="ac", description="Submit an Activity Check (Weekly Checkin)")
async def self(interaction: discord.Interaction, player: str=None):
    await interaction.response.defer()
    if (player == None):
        player = get_name(interaction.user.id)
    if (player != "Error"):
        await interaction.followup.send(submit_ac((interaction.user.name + "#" + interaction.user.discriminator),player))
    else:
        await interaction.followup.send("Use `/link` or enter in a name to use")

# link command
@tree.command(name="link", description="Link your player's name to your account")
async def self(interaction: discord.Interaction, player: str):
    await interaction.response.defer()
    add_name(interaction.user.id,player)
    await interaction.followup.send("Linked name to `" + player + "`")

# claim command
@tree.command(name="claim", description="Submit a claim request")
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
    ],
    category=[
        app_commands.Choice(name="Job: Assets", value="Job: Assets"),
        app_commands.Choice(name="Job: Athletic", value="Job: Athletic"),
        app_commands.Choice(name="Job: Auditor", value="Job: Auditor"),
        app_commands.Choice(name="Job: Editor Come Up", value="Job: Editor Come Up"),
        app_commands.Choice(name="Job: Editor IBL", value="Job: Editor IBL"),
        app_commands.Choice(name="Job: ESPN", value="Job: ESPN"),
        app_commands.Choice(name="Job: First Take", value="Job: First Take"),
        app_commands.Choice(name="Job: League Historian", value="Job: League Historian"),
        app_commands.Choice(name="Job: Master Roster", value="Job: Master Roster"),
        app_commands.Choice(name="Job: Stats", value="Job: Stats"),
        app_commands.Choice(name="Job: Streamer Come Up", value="Job: Streamer Come Up"),
        app_commands.Choice(name="Job: Streamer IBL", value="Job: Streamer IBL"),
        app_commands.Choice(name="Job: Sheets", value="Job: Sheets"),
        app_commands.Choice(name="Administrative: Job Leader", value="Administrative: Job Leader"),
        app_commands.Choice(name="Administrative: Mods", value="Administrative: Mods"),
        app_commands.Choice(name="Administrative: Admin", value="Administrative: Admin"),
        app_commands.Choice(name="Management: Head Coach", value="Management: Head Coach"),
        app_commands.Choice(name="Management: GM", value="Management: GM"),
        app_commands.Choice(name="Awards", value="Awards"),
        app_commands.Choice(name="XP Spent", value="XP Spent"),
        app_commands.Choice(name="Misc.", value="Misc."),
        app_commands.Choice(name="Refunds", value="Refunds"),
    ]
    )
async def claim(interaction: discord.Interaction, week: app_commands.Choice[str], category: app_commands.Choice[str], amt: str, desc: str, player: str=None):
    await interaction.response.defer()
    if (player == None):
        player = get_name(interaction.user.id)
    if (player != "Error"):
        await interaction.followup.send(submit_claim(player, week.value, category.value, amt, desc))
    else:
        await interaction.followup.send("Use `/link` or enter in a name to use")

# viewmr command
@tree.command(name="viewmr", description="Grab a value from the Master Roster such as badge level, player info, etc")
@app_commands.choices(info=[
    app_commands.Choice(name="Team", value=str(info_start+0)),
    app_commands.Choice(name="Nat. Pos.", value=str(info_start+1)),
    app_commands.Choice(name="Sec. Pos.", value=str(info_start+2)),
    app_commands.Choice(name="Height", value=str(info_start+3)),
    app_commands.Choice(name="Weight", value=str(info_start+4)),
    app_commands.Choice(name="IBL Archetype", value=str(info_start+5)),
    app_commands.Choice(name="In Game Archetype", value=str(info_start+6)),
    app_commands.Choice(name="Loyalty Years", value=str(info_start+7)),
    app_commands.Choice(name="Contract", value=str(info_start+8)),
    app_commands.Choice(name="Cap Hit", value=str(info_start+9)),
    app_commands.Choice(name="Years", value=str(info_start+10)),
    app_commands.Choice(name="Options", value=str(info_start+11)),
    app_commands.Choice(name="Drafted", value=str(info_start+12)),
    app_commands.Choice(name="Affiliation (Stashed)", value=str(info_start+13)),
    app_commands.Choice(name="Homegrown", value=str(info_start+14)),
    app_commands.Choice(name="Season Joined", value=str(info_start+15)),
    app_commands.Choice(name="Regression Season", value=str(info_start+16)),
    ],
    overview=[
        app_commands.Choice(name="Comparison", value=str(overview_start+0)),
        app_commands.Choice(name="Total Badges", value=str(overview_start+1)),
        app_commands.Choice(name="Hall of Fame", value=str(overview_start+2)),
        app_commands.Choice(name="Gold", value=str(overview_start+3)),
        app_commands.Choice(name="Silver", value=str(overview_start+4)),
        app_commands.Choice(name="Bronze", value=str(overview_start+5)),
        app_commands.Choice(name="Hot Zones", value=str(overview_start+6)),
        app_commands.Choice(name="Inside Scoring", value=str(overview_start+7)),
        app_commands.Choice(name="Outside Scoring", value=str(overview_start+8)),
        app_commands.Choice(name="Playmaking", value=str(overview_start+9)),
        app_commands.Choice(name="Athleticism", value=str(overview_start+10)),
        app_commands.Choice(name="Defending", value=str(overview_start+11)),
        app_commands.Choice(name="Rebounding", value=str(overview_start+12)),
    ],
    att_off=[
        app_commands.Choice(name="Driving Layup", value=str(att_start+0)),
        app_commands.Choice(name="Post Fade", value=str(att_start+1)),
        app_commands.Choice(name="Post Hook", value=str(att_start+2)),
        app_commands.Choice(name="Post Moves", value=str(att_start+3)),
        app_commands.Choice(name="Draw Foul", value=str(att_start+4)),
        app_commands.Choice(name="Close Shot", value=str(att_start+5)),
        app_commands.Choice(name="Mid-Range Shot", value=str(att_start+6)),
        app_commands.Choice(name="Three-Point Shot", value=str(att_start+7)),
        app_commands.Choice(name="Free Throw", value=str(att_start+8)),
        app_commands.Choice(name="Ball Control", value=str(att_start+9)),
        app_commands.Choice(name="Pass IQ", value=str(att_start+10)),
        app_commands.Choice(name="Pass Accuracy", value=str(att_start+11)),
        app_commands.Choice(name="Offensive Rebound", value=str(att_start+12)),
        app_commands.Choice(name="Standing Dunk", value=str(att_start+13)),
        app_commands.Choice(name="Driving Dunk", value=str(att_start+14)),
        app_commands.Choice(name="Shot IQ", value=str(att_start+15)),
        app_commands.Choice(name="Pass Vision", value=str(att_start+16)),
        app_commands.Choice(name="Hands", value=str(att_start+17)),
    ]
    )
async def viewmr(interaction: discord.Interaction, manual: str=None, player: str=None, info: app_commands.Choice[str]=None, overview: app_commands.Choice[str]=None, att_off: app_commands.Choice[str]=None):
    await interaction.response.defer()
    if (player == None):
        player = get_name(interaction.user.id)
    if (player != "Error"):
        num = "1"
        if (manual != None):
            num = find_row(manual)
        elif (info != None):
            num = info.value
        elif (overview != None):
            num = overview.value
        elif (att_off != None):
            num = att_off.value
        

        await interaction.followup.send(grab_mr(player, num))
    else:
        await interaction.followup.send("Use `/link` or enter in a name to use")

# country command
@tree.command(name="country", description="Roll a country")
@app_commands.choices(region=[
    app_commands.Choice(name="America", value="america"),
    app_commands.Choice(name="Europe", value="europe"),
    app_commands.Choice(name="Africa", value="africa"),
    app_commands.Choice(name="Asia", value="asia"),
    app_commands.Choice(name="Oceania", value="oceania"),
    ])
async def roll(interaction: discord.Interaction, region: app_commands.Choice[str]):
    await interaction.response.defer()
    await asyncio.sleep(1)
    rolled = roll_country(region.value)
    await interaction.followup.send("`" + (interaction.user.name + "#" + interaction.user.discriminator) + "` rolled **" + rolled + "**")

# create command


client.run(get_token())