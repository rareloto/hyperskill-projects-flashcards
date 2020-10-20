import random
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
			# "view": lambda: self.view_cards()
		}
		self.delimiter = ','
		
	def main(self):
		while True:
			action = input(f"Input the action ({', '.join(self.actions)}): \n> ")
			self.actions.get(action, lambda: print("Invalid action. Try again."))()
			print()
			
		# self.view_cards()
	
	def add_card(self):
		# Prompt user for term and definition
		term = input(f"The card: \n> ")
		while term in self.flashcards:
			print(f'The card "{term}" already exists. Try again: ')
			term = input("> ")
		
		definition = input(f"The definition of the card: \n> ")
		while definition in self.flashcards.values():
			print(f'The definition "{definition}" already exists. Try again: ')
			definition = input("> ")
		
		# Add to flashcards
		self.flashcards[term] = definition
		
		print(f'The pair ("{term}":"{definition}") has been added.')
		
	def remove_card(self):
		card = input("Which card? \n> ")
		
		if self.flashcards.pop(card, "Card not found.") != "Card not found.":
			print("The card has been removed.")
		else:
			print(f"Can't remove \"{card}\". There is no such card.")
	
	def import_cards(self):
		filename = input("File name: \n> ")
		cards_loaded = 0
		
		try:
			with open(filename) as f:
				for pair in f:
					term, definition = pair.split(',')[:2]
					self.flashcards[term] = definition.rstrip()
					cards_loaded += 1
			
			print(f"{cards_loaded} cards have been loaded.")
		except Exception:
			print("File not found.")
			
	def export_cards(self):
		if not self.flashcards:
			print("You haven't created any flashcards yet. Try adding one first.")
			return
	
		filename = input("File name: \n> ")
		with open(filename, "w") as f:
			for term, definition in self.flashcards.items():
				f.write(f"{term}{self.delimiter}{definition}\n")
		
		print(f"{len(self.flashcards)} cards have been saved.")
		
	def view_cards(self):
		if not self.flashcards:
			print("You haven't created any flashcards yet. Try adding one first.")
			return
			
		for term, definition in self.flashcards.items():
			print("Card:")
			print(term)
			print("Definition:")
			print(definition)
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
			for term, definition in random.sample(self.flashcards.items(), len(self.flashcards)):
				answer = input(f'Print the definition of "{term}": \n> ')
			
				if answer.casefold() == definition.casefold():
					print("Correct!")
				else:
					key_match = [key for key in self.flashcards \
								 if self.flashcards[key].casefold() == answer.casefold()]
					print(f'Wrong! The right answer is "{definition}".' +
						 (f'\b, but your definition is correct for "{key_match[0]}".' if key_match else ""))
						 
				cards_reviewed += 1
				if cards_reviewed == card_count:
					return
	
	@staticmethod		
	def exit():
		print("Bye bye!")
		sys.exit()


if __name__ == "__main__":
	flashcards = Flashcards()
	flashcards.main()
