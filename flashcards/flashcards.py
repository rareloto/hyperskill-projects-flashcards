


class Flashcards:
    def __init__(self):
        self.flashcards = {}
        
    def main(self):
        num_of_cards = int(input("Input the number of cards: \n> "))
        
        for i in range(num_of_cards):
            term = input(f"The term for card #{i+1}: \n>")
            while term in self.flashcards:
                print(f'The term "{term}" already exists. Try again: ')
                term = input("> ")
            
            definition = input(f"The definition for card #{i+1}: \n> ")
            while definition in self.flashcards.values():
                print(f'The definition "{definition}" already exists. Try again: ')
                definition = input("> ")
            
            self.flashcards[term] = definition
        
        self.review_flashcards()   
        # self.view_flashcards()
        
    def view_flashcards(self):
        for term, definition in self.flashcards.items():
            print("Card:")
            print(self.terms)
            print("Definition:")
            print(self.definitions)
            
    def review_flashcards(self):
        for term, definition in self.flashcards.items():
            answer = input(f'Print the definition of "{term}": \n> ')
            evaluation = "Correct!" if answer == definition \
            else f'Wrong! The right answer is "{definition}".'
            key_match = [key for key in self.flashcards if self.flashcards[key] == answer]
            evaluation += f'\b, but your definition is correct for "{key_match}."' \
                if key_match else ""
            
            print(evaluation)


if __name__ == "__main__":
    flashcards = Flashcards()
    flashcards.main()
