import requests

ac_url = 'https://docs.google.com/forms/d/e/1FAIpQLSfQlPPjtoBi5KCJXV4dXJZZ6N4A-l94ObfTNKvYXHdxVMBAZg/formResponse'
claim_url = ''

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
            return 'Failed to submit'
    except:
        return "Error"