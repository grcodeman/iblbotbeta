import gspread

gc = gspread.service_account(filename="sheets-test-343522-8a764f8b82da.json")

sh = gc.open_by_key("1kMjNXd9vgc4BybQYhByucby4TIi6_QuWXMZ951ms3f0")

def grab_teamac(team):
    ws = sh.worksheet('Bank')
    string = ""
    try:
        # locates the team cell and starts the string
        c = ws.find(team)
        string += "**" + team + " AC:**\n"

        # loops through team list
        for i in range(5):
            string += ws.cell(c.row + i, 2).value
            string += " = "
            string += ws.cell(c.row + i, 29).value
            string += "\n"
    except:
        string = "Process Failed"
    return string

def grab_teambal(team):
    ws = sh.worksheet('Bank')
    string = ""
    try:
        # locates the team cell and starts the string
        c = ws.find(team)
        string += "**" + team + " Bal:**\n"

        # loops through team list
        for i in range(5):
            string += ws.cell(c.row + i, 2).value
            string += " = "
            string += ws.cell(c.row + i, 4).value
            string += "XP\n"
    except:
        string = "Process Failed"
    return string

def grab_bal(player):
    ws = sh.worksheet('Bank')
    string = ""
    try:
        # locates the player cell and pulls their xp value
        c = ws.find(player)
        string += player + ": **" + ws.cell(c.row, 4).value + "XP**"
    except:
        string = "Process Failed"
    return string

def grab_claims(week, player):
    ws = sh.worksheet('Claim View')
    string = ""
    amt_approved = 0
    amt_denied = 0
    amt_pending = 0

    # finds all matching cells for the player and period combination
    c = ws.findall(player + "-" + week)
    string += "__**" + player + " " + week + " claims**__" + "\n"

    # loops through the claims list
    for i in c:

        # grabs the concat
        concat = (ws.cell(i.row, 11).value).split("?")

        # displays the information
        string += "Time: __" + str(concat[0]) + "__ "
        string += "Cat: __" + str(concat[3]) + "__ "
        amount = str(concat[4])
        string += "Amount: __" + amount + "XP__ "
        string += "Desc: __" + str(concat[5]) + "__ "
        string += "\n"

        # displays the status
        status = str(concat[6])
        if (status == "Yes"):
            string += "🟢 " + amount + "XP **Approved** by " + str(concat[7])
            amt_approved += int(amount)
        elif (status == "No"):
            string += "🔴 " + amount + "XP **Denied** by " + str(concat[7]) + " Reason: " + str(concat[8])
            amt_denied += int(amount)
        else:
            string += "🟡 " + amount + "XP **Pending**"
            amt_pending += int(amount)
        string += "\n"
    
    # displays the summary
    string += "**Summary:**\n" + "🟢 " + str(amt_approved) + "XP 🔴" + str(amt_denied) + "XP 🟡" + str(amt_pending) + "XP"

    return string
