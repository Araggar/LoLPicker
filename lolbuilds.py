import requests
import json
import re
import random
import os
from sys import argv, exit

class builder:
	def main(self, role):

		if not os.path.exists('champions.json'):
			with open("champions.json", 'w') as champ_file:
				json.dump([[],[],[],[],[]],champ_file)
		


		self.top = []
		self.jungle = []
		self.mid = []
		self.adc = []
		self.support = []

		
		if role in ('add', 'Add'):
			inp = input("Select role to Add champions <top, jungle, mid, support, adc>\n>>> ")
			if inp not in ('top', 'jungle', 'mid', 'adc', 'support'):
				print("Not a valid role")
				exit(1)
			champ = input("Adding champions to {}\nType <exit> to leave\n>>> ".format(inp))
			while champ != 'exit':
				getattr(self, inp).append(champ)
				champ = input(">>> ")
			exit(0)



		try:
			champions = {
				'top' : self.top,
				'jungle' : self.jungle,
				'mid' : self.mid,
				'adc' : self.adc,
				'support' : self.support
			}
			champion = random.choice(champions[role])
		except KeyError:
			champion, role = role, ''
		except IndexError:
			print("Role <{}> is empty!".format(role))
			exit(1)


		addr = "http://www.probuilds.net/champions/details/{}".format(champion)
		session = requests.Session()
		html = session.get(addr)

		popular = re.findall("'item-name gold'>([\w\s']+?)<\/div>[\w\W]+?'popularity green'>([\d\.]+?%)+?<\/div>",html.text)

		if not popular:
			print("Invalid Champion/Role <{}>".format(role))
			exit(1)

		print("\n---ITEMS---\n")
		for i, items in enumerate(popular):
			if i in [6, 10]:
				print()


			print("{} --- {}".format(items[0], items[1]))


		addr_runes = "http://champion.gg/champion/{}/{}?".format(champion, role)
		html = session.get(addr_runes)
		runes = re.findall('color=[\w\W]+?>([\w ]+?)<\/div>',html.text)
		print("\n---RUNES---\n")
		for i, rune in enumerate(runes):
			print() if i == 8 else None
			print(rune)


if __name__ == '__main__':
	os.chdir(os.path.dirname(os.path.realpath(__file__)))
	try:
		if argv[1] == '-h':
			raise IndexError
		builder().main(argv[1])
	except IndexError:
		print("Usage\npython {} Champion/Role/Add/Remove/Show".format(argv[0]))
		exit(1)


