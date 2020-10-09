


class Flashcards:
    def __init__(self):
        self.terms = []
        self.definitions = []
        
    def main(self):
        num_of_cards = int(input("Input the number of cards: \n> "))
        
        for i in range(num_of_cards):
            term = input(f"The term for card #{i+1}: \n>")
            definition = input(f"The definition for card #{i+1}: \n> ")
            
            self.terms.append(term)
            self.definitions.append(definition)
        
        self.review_flashcards()   
        # self.view_flashcards()
        
    def view_flashcards(self):
        for term, definition in zip(self.terms, self.definitions):
            print("Card:")
            print(self.terms)
            print("Definition:")
            print(self.definitions)
            
    def review_flashcards(self):
        for term, definition in zip(self.terms, self.definitions):
            answer = input(f'Print the definition of "{term}": \n> ')
            evaluation = "Correct!" if answer == definition \
            else f'Wrong! The right answer is "{definition}".'
            
            print(evaluation)


if __name__ == "__main__":
    flashcards = Flashcards()
    flashcards.main()
