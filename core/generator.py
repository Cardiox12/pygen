# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    generator.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: tony <tony@student.42.fr>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/10/01 15:58:58 by bbellavi          #+#    #+#              #
#    Updated: 2019/10/01 22:45:58 by tony             ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from enum import Enum
from functools import reduce
from random import randint
from pprint import pprint
from operator import itemgetter
from itertools import repeat

class Delim(Enum):
    SPACE = " "

class Generator(object):
    SPACE = " "
    def __init__(self, sourcecode):
        self.sourcecode = sourcecode
        self.tokens = {}
        self.probabilities = {}

    def tokenize(self):
        tokens = {}
        splitted_tokens = [token.strip() for token in self.sourcecode.split(Delim.SPACE.value) if token != ""]

        for token in splitted_tokens:
            positions = self.localize(token)
            token_dict = {}
            occurrences = []
            
            for position in positions:
                try:
                    next_token = splitted_tokens[position + 1]
                    occurrences.append(next_token)
                except IndexError:
                    pass
            
            for occurrence in occurrences:
                token_dict[occurrence] = occurrences.count(occurrence)

            tokens[token] = token_dict
            tmp_dict = {}
        self.tokens = tokens
        return self.tokens

    def localize(self, token):
        """[Search tokens into a string and returns its index]
        
        Arguments:
            token {[string]} -- [token to search]
        """
        return [index for index, tok in enumerate(self.sourcecode.split(Delim.SPACE.value)) if tok == token]

    def get_probabilties_dict(self):
        tokens_probs = {}
        probs = {}

        for key, value in self.tokens.items():
            if value != {}:
                total = reduce(lambda x, y: x + y, value.values())
            else:
                total = 0

            for k, v in value.items():
                probs[k] = v / total
            tokens_probs[key] = probs
            probs = {}
        
        self.probabilities = tokens_probs
        return tokens_probs


    def train(self):
        self.tokenize()
        self.get_probabilties_dict()
    
    def get_next_word(self):
        tokens = list(self.tokens.keys())
        first_token = [word for word in tokens if word[0].isupper()]

        if len(first_token) == 0:
            first_token = tokens[randint(0, len(tokens) - 1)]
        if len(first_token) > 1:
            first_token = first_token[randint(0, len(first_token) - 1)]
        else:
            first_token = first_token[0]

        next_token = first_token
        while True:
            yield next_token

            next_token = sorted(self.probabilities[next_token].items(), key=lambda x: x[1])
            if len(next_token) > 3:
                next_token = next_token[randint(0, len(next_token) - 1)][0]
            else:
                next_token = next_token[0][0]

if __name__ == "__main__":
    with open("file_test/obama.txt") as f:
        data = f.read()
        gen = Generator(data)
        gen.train()
        
        for i in range(10):
            generator = gen.get_next_word()
            sentence = []

            for _ in range(20):
                sentence.append(generator.__next__())

            print(f"========================================== PHRASE {i} ==========================================")
            print() 
            print(" ".join(sentence))
            print() 