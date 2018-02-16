import requests
import json
import re
import random
import os
from sys import argv, exit

class builder:

	def __init__(self):
		
		if os.path.exists('champions.json'):
			with open('champions.json', 'r') as champ_file:
				champs = json.load(champ_file)

			self.top = champs[0]
			self.jungle = champs[1]
			self.mid = champs[2]
			self.adc = champs[3]
			self.support = champs[4]

			
		else:
			with open("champions.json", 'w') as champ_file:
				json.dump([[],[],[],[],[]],champ_file)

			self.top = []
			self.jungle = []
			self.mid = []
			self.adc = []
			self.support = []
		
	def add(self, *_):
		inp = input("Select role to Add champions <top, jungle, mid, support, adc>\n>>> ")
		if inp not in ('top', 'jungle', 'mid', 'adc', 'support'):
			print("Not a valid role")
			return
		champ = input("Adding champions to {}\nType <exit> to leave\n>>> ".format(inp))
		while champ != 'exit':
			getattr(self, inp).append(champ)
			champ = input(">>> ")
		with open("champions.json", 'w') as champ_file:
				json.dump([self.top, self.jungle, self.mid, self.adc, self.support],champ_file)
		self.__init__()
		
	def remove(self, *_):
		inp = input("Select role to Add champions <top, jungle, mid, support, adc>\n>>> ")
		if inp not in ('top', 'jungle', 'mid', 'adc', 'support'):
			print("Not a valid role")
			return
		champ = input("Adding champions to {}\nType <exit> to leave\n>>> ".format(inp))
		while champ != 'exit':
			try:
				getattr(self, inp).remove(champ)
			except Exception:
				print("Champion Not Found!")
			champ = input(">>> ")
		with open("champions.json", 'w') as champ_file:
				json.dump([self.top, self.jungle, self.mid, self.adc, self.support],champ_file)
		self.__init__()
		
	def list(self, *_):
		inp = input("Select role to Add champions <top, jungle, mid, support, adc>\n>>> ")
		print("\n-----{}-----\n".format(inp.upper()))
		for champ in getattr(self, inp):
			print(champ)
		print("\n-----END-----\n")
		
	def build(self, inp, *_):
		try:
			champion = random.choice(getattr(self, inp))
		except AttributeError:
			champion, inp = inp, ''
		except IndexError:
			print("Role <{}> is empty!".format(inp))
			return


		addr = "http://www.probuilds.net/champions/details/{}".format(champion)
		session = requests.Session()
		html = session.get(addr)

		popular = re.findall("'item-name gold'>([\w\s']+?)<\/div>[\w\W]+?'popularity green'>([\d\.]+?%)+?<\/div>",html.text)

		if not popular:
			print("Invalid Champion/Role <{}>".format(inp))
			return

		print("\n{}".format(champion.upper()))
		print("\n---ITEMS---\n")
		for i, items in enumerate(popular):
			if i in [6, 10]:
				print()


			print("{} --- {}".format(items[0], items[1]))


		addr_runes = "http://champion.gg/champion/{}/{}?".format(champion, inp)
		html = session.get(addr_runes)
		runes = re.findall('color=[\w\W]+?>([\w ]+?)<\/div>',html.text)
		print("\n---RUNES---\n")
		for i, rune in enumerate(runes):
			print() if i == 8 else None
			print(rune)
	
	def exit(self, *_):
		print("Goodbye!")
		exit(0)
	
	def main(self, *_):

		while True:
			inp = input("\n\n\nOptions are:\nadd\nremove\nlist\nexit\n\nType the champion name/role to get a build\n>>> ")
			try:
				getattr(self, inp, self.build)(inp)
			except Exception:
				self.build(inp)
		



if __name__ == '__main__':
	os.chdir(os.path.dirname(os.path.realpath(__file__)))
	try:
		builder().main()
	except KeyboardInterrupt:
		print("Goodbye!")
		exit(0)

