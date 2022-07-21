from string import ascii_uppercase
import sys

class GamertagManager:
    def __init__(self, deep: int=1) -> None:
        self.deep = deep
        self.names = []

    def alphabet_loop(self) -> list[str]:
        for letter1 in ascii_uppercase:
            self.names.append(letter1)
            for letter2 in ascii_uppercase:
                self.names.append(letter1 + letter2)
                for letter3 in ascii_uppercase:
                    self.names.append(letter1 + letter2 + letter3)
                    for letter4 in ascii_uppercase:
                        self.names.append(letter1 + letter2 + letter3 + letter4)

gamertag_manager = GamertagManager()
gamertag_manager.alphabet_loop()
gamertag_manager.names.sort()
with open('name-list.txt', 'w') as outfile:
    outfile.write(','.join(gamertag_manager.names))

