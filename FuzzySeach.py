from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class SearchAlgorithm:
    def __init__(self, strings):
        self.strings = strings

    def set_strings(self, strings):
        self.strings = strings

    async def top_5(self, search):
        tuples_arr = []
        for string in self.strings:
            score = fuzz.partial_ratio(string, search)
            #score = fuzz.ratio(string, search)
            tuples_arr.append((score, string))
        
        tuples_arr.sort()
        tuples_arr = tuples_arr[::-1]
        to_return = []
        for i in range(5):
            to_return.append(tuples_arr[i][1])
            
        return to_return