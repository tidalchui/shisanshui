global token, battleid

def getcards():

    url = 'https://api.shisanshui.rtxux.xyz/game/open'
    token = '9cea49a4-4ea3-40cc-93cd-25e7e51f7396'
    headers = {'X-Auth-Token': token}
    r = requests.post(url, headers=headers)
    r_data = r.json()['data']
    battleid = r_data['id']
    cards = r_data['card'].split()
    return cards