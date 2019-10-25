import requests
import json
import sys
first = 0
second = 0
third = 0

global token, battleid
cards = sys.argv[1]
cards = cards.split()

# cards = "$2 #6 *2 #A $10 &7 #10 &8 $7 *7 $A *K #K".split()
# cards = ['$6', '&3', '&8', '$5', '#3', '#2', '*9', '$9', '*8', '#J', '*4', '$2', '$Q']
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
	for r in cards:
		if cards.count(r) == 2:
			return r
	return None

def two_pair(cards):
	cards.sort(key=getvalue)

	strcards = "".join(list(filter(str.isdigit, " ".join(cards))))
	lowpair = judge_pair(strcards)
	pair = judge_pair(list(reversed(strcards)))
	if lowpair and pair != lowpair:
		return list(map(int, [lowpair, pair]))
	else:
		return None

def getlevel(fivecards):
	fivecards.sort(key=getvalue)
	strcards = " ".join(fivecards)
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
			if (i == 0 and fivecards[3][1] == fivecards[4][1]) or (i == 2 and fivecards[0][1] == fivecards[1][1]):  # 葫芦
				return [2, getvalue(fivecards[2])]
			else:
				if fivecards[0][0] == fivecards[1][0] and fivecards[0][0] == fivecards[2][0] and fivecards[0][0] == \
						fivecards[3][0] and fivecards[0][0] == fivecards[4][0]:  # 同花
					return [3, getvalue(fivecards[4])]
				else:  # 三条
					return [5, getvalue(fivecards[i])]
	if fivecards[0][0] == fivecards[1][0] and fivecards[0][0] == fivecards[2][0] and fivecards[0][0] == fivecards[3][
		0] and fivecards[0][0] == fivecards[4][0]:  # 同花
		return [3, getvalue(fivecards[4])]
	if two_pair(fivecards):
		if min(two_pair(fivecards)) + 1 == max(two_pair(fivecards)):
			return [6, max(two_pair(fivecards))]  # 连对
		else:
			return [7, max(two_pair(fivecards))]  # 两对
	values = list(filter(str.isdigit, strcards))
	if judge_pair(values):
		return [8, int(judge_pair(values))] # 一对
	return [99, getvalue(fivecards[4])] # 散牌

def getsecondlevel(cards):
	cards.reverse()
	secondlevel = [100, 0]
	global second
	for i0 in range(0, 4):
		for i1 in range(i0+1, 5):
			for i2 in range(i1+1, 6):
				for i3 in range(i2+1, 7):
					for i4 in range(i3+1, 8):
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
	for i0 in range(0, 4):
		for i1 in range(i0+1, 5):
			for i2 in range(i1+1, 6):
				for i3 in range(i2+1, 7):
					for i4 in range(i3+1, 8):
						newlevel = getlevel([cards[i0], cards[i1], cards[i2], cards[i3], cards[i4]])
						if newlevel[0] == secondlevel[0]:
							first = [item for item in cards if item not in [cards[i0], cards[i1], cards[i2], cards[i3], cards[i4]]]
							first = " ".join(first)
							values = list(filter(str.isdigit, first))
							if judge_pair(values):
								secondlevel = newlevel
								second = [cards[i0], cards[i1], cards[i2], cards[i3], cards[i4]]

	return second

def getpostcards(cards):
	thirdlevel = [100, 0]
	global second
	global third
	for i0 in range(0, 9):
		for i1 in range(i0+1, 10):
			for i2 in range(i1+1, 11):
				for i3 in range(i2+1, 12):
					for i4 in range(i3+1, 13):
						currentcards = [cards[i0], cards[i1], cards[i2], cards[i3], cards[i4]]
						newlevel = getlevel(currentcards)
						if newlevel[0] < thirdlevel[0]:
							third = currentcards
							thirdlevel = newlevel
							eightcards = [item for item in cards if item not in currentcards]
							secondlevel = getsecondlevel(eightcards)
						elif newlevel[0] == thirdlevel[0]:
							eightcards = [item for item in cards if item not in currentcards]
							newsecondlevel = getsecondlevel(eightcards)
							if newsecondlevel[0] < secondlevel[0] or (newsecondlevel[0] == secondlevel[0] and newsecondlevel[1] > secondlevel[1]):
								third = currentcards
								thirdlevel = newlevel
								secondlevel = newsecondlevel
							elif newlevel[1] > thirdlevel[1]:
								third = currentcards
								thirdlevel = newlevel
								secondlevel = newsecondlevel
	eightcards = [item for item in cards if item not in third]
	second = getsecond(eightcards)
	first = list(set(cards) - set(second) - set(third))
	first.sort(key=getvalue)
	first = ' '.join(first)
	second = ' '.join(second)
	third = ' '.join(third)
	thecards = [first, second, third]
	return thecards

def postcards():
	thefinalcards = {
		"id": id,
		"card": getpostcards(cards)
	}
	print(thefinalcards[cards])

# 出牌
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
    cards = getpostcards(cards)
print(cards)
game_submit(cards)

