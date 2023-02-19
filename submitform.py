import requests

ac_url = 'https://docs.google.com/forms/d/e/1FAIpQLSfQlPPjtoBi5KCJXV4dXJZZ6N4A-l94ObfTNKvYXHdxVMBAZg/formResponse'
claim_url = 'https://docs.google.com/forms/d/1nvbk8ha-h4uca9r54PSyz9_76Ygtc_cRfcY7vQYv8Z4/formResponse'

def submit_ac (user, player):
    try:
        form_data = {'entry.1352780092':str(user),
                    'entry.2136729267':str(player),
                    'draftResponse':[],
                    'pageHistory':0}
        user_agent = {'Referer':'https://docs.google.com/forms/d/e/1FAIpQLSfQlPPjtoBi5KCJXV4dXJZZ6N4A-l94ObfTNKvYXHdxVMBAZg/viewform','User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36"}
        r = requests.post(ac_url, data=form_data, headers=user_agent)
        if str(r.status_code) == '200':
            return "AC Submitted: `" + str(user) + "` `" + str(player) + "`"
        else:
            return 'Failed to submit AC'
    except:
        return "Error"

def submit_claim (player, week, category, amount, desc):
    try:
        form_data = {'entry.193036250':str(player),
            'entry.947899703':str(week),
            'entry.578622649':str(category),
            'entry.1603733274':str(amount),
            'entry.908077022':str(desc),
            'draftResponse':[],
            'pageHistory':0}
        user_agent = {'Referer':'https://docs.google.com/forms/d/1nvbk8ha-h4uca9r54PSyz9_76Ygtc_cRfcY7vQYv8Z4/viewform','User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36"}
        r = requests.post(claim_url, data=form_data, headers=user_agent)
        if str(r.status_code) == '200':
            return "Claim Submitted: `" + str(player) + "` `" + str(week) + "` `" + str(category) + "` `" + str(amount) + "XP" + "` `" + str(desc) + "`"
        else:
            return 'Failed to submit claim'
    except:
        return "Error"