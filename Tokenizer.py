import re
import sys
from collections import defaultdict
import json

# The tokenize function has a runtime complexity of O(N * (M + P)).
#    derived from O(1) * O(N) * O(M + P) = O(N * (M + P))
#    Each component is enumerated in the comments below
class Tokenize_object:
    def __init__(self):
        print("Building Tokenizer")

    def tokenize(self,json_file):
        try:  
            f = json.load(json_file) 
            for line in f:                                      # O(N) Dependent on the number of lines in a file
                for x in re.finditer(r'[0-9a-zA-Z]+', line):    # O(M) + O(P)
                                                                # O(M) is the runtime complexity of finditer
                                                                # O(P) Depends on looping through the number of tokens
                                                                #    that finditer returns
                    yield x.group(0).lower()                    # O(1) always happens
        except IOError:                                             # worst case scenario: never happens
            print('File not found: {}'.format(filPth))
            exit()
        except UnicodeDecodeError:
            print('File encoding not utf-8: {}'.format(filPth))
            exit()


# The computeWordFrequencies function has a runtime complexity of O(N)
#    derived from O(1) + O(N) * O(1) + O(1) = O(N)
#    Each component is enumerated in the comments below
    def computeWordFrequencies(self,tokListGen):
        frequencies = defaultdict(lambda: 0)    # O(1)
        for t in tokListGen:                    # O(N) Iteration through all elements of the token list generator
            frequencies[t] += 1                 # O(1)
        return frequencies                      # O(1)
    
    
# The printWordFrequencies function has a runtime complexity of O(N log N)
#    derived from O(N) + O(N log N) = O(N log N)
#    Each component is enumerated in the comments below
    def printWordFrequencies(self,freqMap):
        for t, f in sorted(freqMap.items(), key=lambda x: -x[1]):   # O(N) + O(N log N)
                                                                    # O(N) Iteration through all elements of a list
                                                                    # O(N log N) runtime complexity of sorted function
            print('{} - {}'.format(t, f))
    

if __name__ == "__main__":
    argList = sys.argv
    if (len(argList) != 2):
        print("Program needs one input txt file to run")
        exit()
    printWordFrequencies(computeWordFrequencies(tokenize(argList[1])))  # O(N * (M + P)) + O(N) + O(N log N)
                                                                        #    = O(N * (M + P))
