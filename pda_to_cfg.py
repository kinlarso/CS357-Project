###########################################
# CS357                                   #
# Project - Convert PDA to equivalent CFG #
# Kincaid Larson                          #
###########################################

import json
import sys

def convertPDA(data):
    # dummied up
    # might not do this function
    
    # alter json data to match the requirements necessary for
    # conversion from PDA to CFG
    print("in convertPDA")
    return data

def locatePairs(data):
    # dummied up
    print("in locatePairs")
    
    # return a list of pairs
    return [(1,3), (2,4)]
    
def generateRules(data, pairs):
    # dummied up
    print("in generateRules")
    
    # generate the rules for the grammar (make the json)
    grammar = {}
    
    # return a json
    return grammar
    
def makeCFG(data):
    print("in makeCFG")
    
    # make new json file for grammar
    with open('new_grammar.json', 'w') as f:
        json.dump(data, f)
        
    print(data)
    
def main():
    if len(sys.argv) < 2:
        print("Error: Please input a json file as an argument")
        sys.exit(1)
        
    file = sys.argv[1]
    
    try:
        with open(file) as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("Error: file is in incorrect JSON format")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: File not found")
        sys.exit(1)
    
    # Convert PDA to proper format
    data = convertPDA(data)
    
    # locate all push/pop and pop/push pairs 
    pairs = locatePairs(data)
    
    # use information from locatePairs to generate rules for the grammar
    grammar = generateRules(data, pairs)
    
    # create a JSON and output it as a new file
    makeCFG(grammar)

if __name__ == "__main__":
    main()