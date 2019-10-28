import requests
import json

first = 0
second = 0
third = 0


def login(username, password):
    global token
    url = "http://api.revth.com/auth/login"
    headers = {"Content-Type": "application/json"}
    data = {
        "username": username,
        "password": password
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    status = r.json()['status']
    if status == 0:
        print('login successfully')
        token = r.json()['data']['token']
        print(token)
    else:
        print('login failed!')


def startbattle():
    global token, battleid
    url = 'http://api.revth.com/game/open'
    headers = {'X-Auth-Token': token}
    r = requests.post(url, headers=headers)
    r_data = r.json()['data']
    battleid = r_data['id']
    return r_data['card'].split()


def game_submit(submit_card):
    url = "http://api.revth.com/game/submit"
    data = {
        'id': battleid,
        'card': submit_card
    }
    headers = {
        'Content-Type': "application/json",
        'X-Auth-Token': token
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    status = r.json()['status']
    if status == 0:
        print('submit successfully')
    else:
        print('game_submit failed!')
        print(r.text)


login("test817926", "817926")
for i in range(1000000):
    cards = startbattle()
    # cards = ['$A', '#10', '$9', '$10', '*9', '#7', '#A', '#Q', '*4', '&K', '$Q', '#2', '$2']
    print(cards)


    # cards = ['$6', '&3', '&8', '$5', '#3', '#2', '*9', '$9', '*8', '#J', '*4', '$2', '$Q']
    # def test():
    #     cards = [
    #         ['*J', '#Q', '#J', '*7', '*5', '#4', '*8', '#10', '*6', '&5', '#A', '$3', '*4'],
    #         ['$2', '*3', '$6', '$9', '*4', '$7', '$3', '*6', '*J', '&Q', '#10', '#3', '&4'],
    #         ['$10', '*6', '*4', '#J', '$K', '$3', '&9', '*5', '$7', '&A', '*J', '&Q', '&2'],
    #         ['$J', '*9', '$6', '$9', '$8', '&4', '$A', '#9', '&A', '&9', '$5', '*Q', '*10'],
    #         ['$A', '#A', '&6', '*10', '$6', '#7', '*3', '&2', '&9', '$8', '&8', '$5', '&5'],
    #         ['$10', '*8', '*A', '*4', '#8', '#J', '#7', '&2', '$2', '#2', '#5', '*6', '&Q'],
    #         ['*2', '#J', '$3', '#6', '#Q', '#9', '$K', '$J', '*3', '*A', '$10', '$A', '&7'],
    #         ['#7', '&5', '&3', '*A', '#2', '$8', '$9', '*5', '&7', '*8', '#4', '&2', '*3'],
    #         ['&K', '*Q', '$3', '#J', '&A', '$6', '#4', '$8', '&4', '#Q', '*8', '#9', '*3'],
    #         ['*Q', '$6', '&J', '#7', '#10', '*8', '#8', '&6', '*A', '#A', '&8', '&7', '$5'],
    #         ['$K', '*4', '&K', '&7', '#K', '#Q', '$Q', '*10', '#10', '$5', '&2', '*Q', '&10']
    #     ]
    #     for i in cards:
    #         i.sort(key=getvalue)
    #         finalcards = getpostcards(i)
    #         print(finalcards)
    def getsuit(card):
        return card[0]


    def getvalue(x):
        if x[1] == "1":
            return 10
        if x[1] == 'J':
            return 11
        if x[1] == 'Q':
            return 12
        if x[1] == 'K':
            return 13
        if x[1] == 'A':
            return 14
        else:
            return ord(x[1]) - 48


    cards.sort(key=getvalue)


    def judge_pair(cards):
        cards = list(map(getvalue, cards))
        # strcards = "".join(list(filter(str.isalnum, " ".join(cards))))
        for r in cards:
            if cards.count(r) == 2:
                return r
        return None


    def two_pair(cards):
        cards.sort(key=getvalue)
        lowpair = judge_pair(cards)
        pair = judge_pair(list(reversed(cards)))
        if lowpair and pair != lowpair:
            return list(map(int, [lowpair, pair]))
        else:
            return None


    def getlevel(fivecards):
        fivecards.sort(key=getvalue)
        for i in range(4):
            if getvalue(fivecards[i]) + 1 != getvalue(fivecards[i + 1]):  # 顺子
                break
            if i == 3:
                if fivecards[0][0] == fivecards[1][0] and fivecards[0][0] == fivecards[2][0] and fivecards[0][0] == \
                        fivecards[3][0] and fivecards[0][0] == fivecards[4][0]:  # 同花顺
                    return [0, getvalue(fivecards[4])]
                else:  # 普通顺子
                    return [4, getvalue(fivecards[4])]
        for i in range(2):
            if fivecards[i][1] == fivecards[i + 1][1] and fivecards[i][1] == fivecards[i + 2][1] and fivecards[i][1] == \
                    fivecards[i + 3][1]:  # 炸弹
                return [1, getvalue(fivecards[2])]
        for i in range(3):
            if fivecards[i][1] == fivecards[i + 1][1] and fivecards[i][1] == fivecards[i + 2][1]:
                if (i == 0 and fivecards[3][1] == fivecards[4][1]) or (
                        i == 2 and fivecards[0][1] == fivecards[1][1]):  # 葫芦
                    return [2, getvalue(fivecards[2])]
                else:
                    if fivecards[0][0] == fivecards[1][0] and fivecards[0][0] == fivecards[2][0] and fivecards[0][0] == \
                            fivecards[3][0] and fivecards[0][0] == fivecards[4][0]:  # 同花
                        return [3, getvalue(fivecards[4]), getvalue(fivecards[3]), getvalue(fivecards[2]),
                                getvalue(fivecards[1]), getvalue(fivecards[0])]
                    else:  # 三条
                        return [5, getvalue(fivecards[i])]
        if fivecards[0][0] == fivecards[1][0] and fivecards[0][0] == fivecards[2][0] and fivecards[0][0] == \
                fivecards[3][
                    0] and fivecards[0][0] == fivecards[4][0]:  # 同花
            return [3, getvalue(fivecards[4]), getvalue(fivecards[3]), getvalue(fivecards[2]), getvalue(fivecards[1]),
                    getvalue(fivecards[0])]
        if two_pair(fivecards):
            if min(two_pair(fivecards)) + 1 == max(two_pair(fivecards)):
                return [6, max(two_pair(fivecards))]  # 连对
            else:
                return [7, max(two_pair(fivecards))]  # 两对
        if judge_pair(fivecards):
            return [8, judge_pair(fivecards)]  # 一对
        return [99, getvalue(fivecards[4])]  # 散牌


    def getsecondlevel(cards):
        cards.reverse()
        secondlevel = [100, 0]
        global second
        for i0 in range(0, 4):
            for i1 in range(i0 + 1, 5):
                for i2 in range(i1 + 1, 6):
                    for i3 in range(i2 + 1, 7):
                        for i4 in range(i3 + 1, 8):
                            newlevel = getlevel([cards[i0], cards[i1], cards[i2], cards[i3], cards[i4]])
                            if newlevel[0] <= secondlevel[0]:
                                secondlevel = newlevel
                                second = [cards[i0], cards[i1], cards[i2], cards[i3], cards[i4]]
        return secondlevel


    def getsecond(cards):
        cards.reverse()
        secondlevel = getsecondlevel(cards)
        global first
        global second
        first = ["*0", "*0", "*0"]
        for i0 in range(0, 4):
            for i1 in range(i0 + 1, 5):
                for i2 in range(i1 + 1, 6):
                    for i3 in range(i2 + 1, 7):
                        for i4 in range(i3 + 1, 8):
                            currentcards = [cards[i0], cards[i1], cards[i2], cards[i3], cards[i4]]
                            newlevel = getlevel(currentcards)
                            if newlevel[0] < secondlevel[0]:
                                secondlevel = newlevel
                                second = currentcards
                                first = [item for item in cards if item not in currentcards]
                            elif newlevel[0] == secondlevel[0]:
                                newfirst = [item for item in cards if item not in currentcards]
                                if judge_pair(newfirst):
                                    if (getlevel(currentcards)[0] == 8 and judge_pair(newfirst) <
                                        getlevel(currentcards)[1]) or getlevel(currentcards)[0] < 8:
                                        secondlevel = newlevel
                                        second = currentcards
                                        first = [item for item in cards if item not in currentcards]
                                else:
                                    newfirst = list(map(getvalue, newfirst))
                                    if newfirst > list(map(getvalue, first)):
                                        secondlevel = newlevel
                                        second = currentcards
                                        first = [item for item in cards if item not in currentcards]

        return second


    def getpostcards(cards):
        thirdlevel = [100, 0]
        global second
        global third
        for i0 in range(0, 9):
            for i1 in range(i0 + 1, 10):
                for i2 in range(i1 + 1, 11):
                    for i3 in range(i2 + 1, 12):
                        for i4 in range(i3 + 1, 13):
                            currentcards = [cards[i0], cards[i1], cards[i2], cards[i3], cards[i4]]
                            newlevel = getlevel(currentcards)
                            if newlevel[0] < thirdlevel[0]:
                                third = currentcards
                                thirdlevel = newlevel
                                eightcards = [item for item in cards if item not in currentcards]
                                secondlevel = getsecondlevel(eightcards)
                            elif newlevel[0] == thirdlevel[0] and thirdlevel[0] != 99:
                                eightcards = [item for item in cards if item not in currentcards]
                                newsecondlevel = getsecondlevel(eightcards)
                                if newsecondlevel[0] < secondlevel[0] or (
                                        newsecondlevel[0] == secondlevel[0] and newsecondlevel[1] > secondlevel[1]):
                                    third = currentcards
                                    thirdlevel = newlevel
                                    secondlevel = newsecondlevel
                                elif newlevel[1] > thirdlevel[1]:
                                    third = currentcards
                                    thirdlevel = newlevel
                                    secondlevel = newsecondlevel
        eightcards = [item for item in cards if item not in third]
        second = getsecond(eightcards)
        if getlevel(second)[0] == getlevel(third)[0] == 3:
            if second > third:
                second, third = third, second
        if getlevel(second)[0] < getlevel(third)[0] or (
                getlevel(second)[0] == getlevel(third)[0] and getlevel(second)[1] > getlevel(third)[1]):
            second, third = third, second
        first = list(set(cards) - set(second) - set(third))
        first.sort(key=getvalue)
        first = ' '.join(first)
        second = ' '.join(second)
        third = ' '.join(third)
        thecards = [first, second, third]
        return thecards


    cards = getpostcards(cards)
    print(cards)
    game_submit(cards)
    # test()
