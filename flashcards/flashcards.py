from io import StringIO
import argparse
import random
import json
import sys

class Flashcards:
	def __init__(self):
		self.flashcards = {}
		self.actions = {
			"add": lambda: self.add_card(), 
			"remove": lambda: self.remove_card(), 
			"import": lambda: self.import_cards(), 
			"export": lambda: self.export_cards(), 
			"ask": lambda: self.review_cards(), 
			"exit": lambda: self.exit(),
			"log": lambda: self.log(),
			"hardest card": lambda: self.hardest_card(),
			"reset stats": lambda: self.reset_stats(),
			# "view": lambda: self.view_cards()
		}
		self.args = None
		
	def main(self):
		parser = argparse.ArgumentParser()
		parser.add_argument("--import_from", help="import cards from file")
		parser.add_argument("--export_to", help="export cards to file")
		self.args = parser.parse_args()
		
		if self.args.import_from:
			self.import_cards(self.args.import_from)
			print()
	
		while True:
			action = input(f"Input the action ({', '.join(self.actions)}): \n> ")
			self.actions.get(action, lambda: print("Invalid action. Try again."))()
			print()
	
	def add_card(self):
		# Prompt user for term and definition
		term = input(f"The card: \n> ")
		while term in self.flashcards:
			print(f'The card "{term}" already exists. Try again: ')
			term = input("> ")
		
		definition = input(f"The definition of the card: \n> ")
		definitions = [self.flashcards[term]['definition'] for term in self.flashcards]
		while definition in definitions:
			print(f'The definition "{definition}" already exists. Try again: ')
			definition = input("> ")
		
		# Add to flashcards
		self.flashcards[term] = { 'definition': definition, 'mistakes': 0 }
		
		print(f'The pair ("{term}":"{definition}") has been added.')
		
	def remove_card(self):
		card = input("Which card? \n> ")
		
		if self.flashcards.pop(card, "Card not found.") != "Card not found.":
			print("The card has been removed.")
		else:
			print(f"Can't remove \"{card}\". There is no such card.")
	
	def import_cards(self, filename=None):
		if not filename:
			filename = input("File name: \n> ")
		
		try:
			with open(filename) as f_import:
				imported_cards = json.load(f_import)
				self.flashcards.update(imported_cards)
				
			print(f"{len(imported_cards)} cards have been loaded.")
		except FileNotFoundError:
			print("File not found.")
			
	def export_cards(self, filename=None):
		if not self.flashcards:
			print("You haven't created any cards yet. 0 cards exported.")
			return
	
		if not filename:
			filename = input("File name: \n> ")
			
		with open(filename, "w") as f_export:
			json.dump(self.flashcards, f_export)
		
		print(f"{len(self.flashcards)} cards have been saved.")
		
	def view_cards(self):
		if not self.flashcards:
			print("You haven't created any flashcards yet. Try adding one first.")
			return
			
		for term, values in self.flashcards.items():
			definition, mistakes = values['definition'], values['mistakes']
			print("Card:")
			print(term)
			print("Definition:")
			print(definition)
			print("Mistakes:")
			print(mistakes)
			print()
			
	def review_cards(self):
		if not self.flashcards:
			print("You haven't created any flashcards yet. Try adding one first.")
			return
	
		card_count = 0
		while True:
			try:
				card_count = int(input("How many times to ask? \n> "))
				if card_count < 1:
					raise ValueError
				else:
					break
			except ValueError:
				print(f"Please enter a whole number (1, 2, 3, ...).")
		
		cards_reviewed = 0
		while cards_reviewed < card_count:
			for term, values in random.sample(self.flashcards.items(), len(self.flashcards)):
				definition, mistakes = values['definition'], values['mistakes']
				
				answer = input(f'Print the definition of "{term}": \n> ')
			
				if answer.casefold() == definition.casefold():
					print("Correct!")
				else:
					key_match = [key for key in self.flashcards \
								 if self.flashcards[key]['definition'].casefold() == answer.casefold()]
					print(f'Wrong! The right answer is "{definition}".' +
						 (f'\b, but your definition is correct for "{key_match[0]}".' if key_match else ""))
					self.flashcards[term]['mistakes'] += 1
						 
				cards_reviewed += 1
				if cards_reviewed == card_count:
					return
	
	def exit(self):
		if self.args.export_to:
			self.export_cards(self.args.export_to)
		
		print("Bye bye!")
		sys.exit()
		
	def log(self):
		log = StringIO("Log:\n")
		log.write("Test")
		...
		
		filename = input("File name: \n> ")
		with open(filename, 'w') as f_log:
			for line in log:
				f_log.write(line)

		print("The log has been saved.")
		
	def hardest_card(self):
		if not self.flashcards:
			print("There are no cards with errors.")
			return
			
		highest_mistakes = max([values['mistakes'] for term, values in self.flashcards.items()])
		hardest_card = [card for card in self.flashcards \
						if self.flashcards[card]['mistakes'] == highest_mistakes]

		if highest_mistakes == 0:
			print("There are no cards with errors.")
		else:
			linking_verb = 'is' if len(hardest_card) == 1 else 'are'
			s_ending = 's' if len(hardest_card) > 1 else ''
			pronoun = 'it' if len(hardest_card) == 1 else 'them'
			replace_chars = {'[': '', ']': '', "'": '"'}
			trans_table = f"{hardest_card}".maketrans(replace_chars)
			print(f"The hardest card{s_ending} {linking_verb} " \
				  f"{hardest_card}. ".translate(trans_table) 
				  + f"You have {highest_mistakes} error{'s' if highest_mistakes > 1 else ''} " \
				    f"answering {pronoun}.")
		
	def reset_stats(self):
		if not self.flashcards:
			print("You haven't created any flashcards yet. Try adding one first.")
			return
			
		self.flashcards = {
			term: {
				'definition': self.flashcards[term]['definition'],
				'mistakes': 0
			}
			for term in self.flashcards
		}
		print("Card statistics has been reset.")
		

if __name__ == "__main__":
	flashcards = Flashcards()
	flashcards.main()
