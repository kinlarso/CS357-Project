#######################################################
# CS357                                               #
# Project - Convert PDA to equivalent CFG             #
# Kincaid Larson                                      #
#                                                     #
# to run - (python command) pda_to_cfg.py (test file) #
#######################################################

import json
import sys

#################
# checkPDARec -    #
#################
def checkPDARec(data, dest):
    for _states in data['states']:
        # find destination state
        if dest == _states['state'] :
            # get each transition in destination state
            for _transitions in _states['transitions']:
                # check if transition has been visited before
                if _transitions['painted'] == "F":
                    # "paint" the transition (to prevent infinite loops)
                    _transitions['painted'] = "T"
                    
                    # check if current transition dest goes to accept state (there is a path from start_state to accept_state)
                    if _transitions['dest'] == data['accept_state']:
                        return 1
                    
                    # recursive call the destination of each transition
                    return checkPDARec(data, _transitions['dest'])
             
    # base case - no transitions or all transitions painted
    # i know its kind of a bad way to do this base case but hey it works       
    return 0

#################
# checkPDA -    #
#################
def checkPDA(data):
    # print("in convertPDA")
    
    # check if json has correct format
    # (check for typos in states, state, transitions, read, pop, push, dest)
    # loop through states
    #    check state name
    #    loop through transitions
    #        check read, pop, push, dest
    
    # IMPORTANT: '~' is used to represent empty
    
    if "states" not in data:
        print("Error: states key is missing")
        sys.exit(1)
    elif "start_state" not in data:
        print("Error: start_state key is missing")
        sys.exit(1)
    elif "accept_state" not in data:
        print("Error: accept_states key is missing")
        sys.exit(1)
        
    for _states in data['states']:
        if "state" not in _states:
            print("Error: state key missing")
            sys.exit(1)
        elif "transitions" not in _states:
            print("Error: transitions key missing in state " + _states['state'])
            sys.exit(1)
            
        for _transitions in _states['transitions']:
            if "read" not in _transitions:
                print("Error: read key missing in transition from state " + _states['state'])
                sys.exit(1)
            elif "pop" not in _transitions:
                print("Error: pop key missing in transition from state " + _states['state'])
                sys.exit(1)
            elif "push" not in _transitions:
                print("Error: push key missing in transition from state " + _states['state'])
                sys.exit(1)
            elif "dest" not in _transitions:
                print("Error: dest key missing in transition from state " + _states['state'])
                sys.exit(1)
        
    # check if start state and accept state correspond to an existing state
    _startCheck = 0
    _acceptCheck = 0
    for _states in data['states']:
        if data['start_state'] == _states['state']:
            _startCheck = 1
        if data['accept_state'] == _states['state']:
            _acceptCheck = 1
            
    if _startCheck != 1:
        print("Error: start state does not correspond to a state defined by the json")
        sys.exit(1)
    if _acceptCheck != 1:
        print("Error: accept state does not correspond to a state defined by the json")
        sys.exit(1)
    
    # check that pda can go from start to accept state
    valid = 0
    
    for _states in data['states']:
        if _states['state'] == data['start_state']:
            # check every starting transition
            for _transitions in _states['transitions']:
                if valid == 1:
                    break
                
                # initialize/reset painted transitions
                for _i in data['states']:
                    for _j in _i['transitions']:
                        _j['painted'] = "F"
                
                valid = checkPDARec(data, _transitions['dest'])
                
    if valid == 0:
        print("Error: couldn't reach accept state from start state")
        sys.exit(1)
    
    # check if pda meets reqs to convert into a cfg
    #    1. has only one accept state
    #    2. empties stack before accepting
    #    3. Each transition pops or pushes a symbol
    
    # req 1 - count accept states, send an error if less than/greater than 1
    # already handled by json format
        
    # req 2 - check if initial symbol push matches end symbol pop
    for _s1 in data['states']:
        if _s1['state'] == data['start_state']:
            # check every starting transition
            for _t1 in _s1['transitions']:
                # compare against every transition that goes to accept state
                for _s2 in data['states']:
                    for _t2 in _s2['transitions']:
                        if _t2['dest'] == data['accept_state'] and _t1['push'] != _t2['pop']:
                            print("Error: stack is not emptied before accepting")
                            sys.exit(1)
    
    # req 3 - check if both states pop/push a symbol or doesn't pop/push a symbol
    for _states in data['states']:
        for _transitions in _states['transitions']:
            if _transitions['pop'] == '~' and _transitions['push'] == '~':
                print("Error: " + _states['state'] + " to " + _transitions['dest'] + " requires adjustment")
                sys.exit(1)
            elif _transitions['pop'] != '~' and _transitions['push'] != '~':
                print("Error: " + _states['state'] + " to " + _transitions['dest'] + " requires adjustment")
                sys.exit(1)
    
    return data

#################
# locatePairsRec -  #
#################
def locatePairsRec(data, dest, origDest, origSymbol, origInitial, origRead, rulesList, switch):
    # recursive case
    for _states in data['states']:
        # find destination state
        if dest == _states['state'] :
            # get each transition in destination state
            for _transitions in _states['transitions']:
                # check if transition has been visited before
                if _transitions['painted'] == "F":
                    # "paint" the transition (to prevent infinite loops)
                    _transitions['painted'] = "T"
                    
                    # check if pushed symbol matches current transition's pop symbol
                    if origSymbol == _transitions['pop'] and switch == 0:
                        # push/pop pair found
                        print(origSymbol + ": " + origInitial + " -> " + origDest + ", " + _states['state'] + " -> " + _transitions['dest'])
                        #print("A" + origInitial + _transitions['dest'] + " -> " + origRead + "A" + origDest + _states['state'] + _transitions['read'])
                        
                        _variable = "(A_" + origInitial + "_" + _transitions['dest'] + ")"
                        _rule = origRead + "(A_" + origDest + "_" + _states['state'] + ")" + _transitions['read']
                        
                        # create rule
                        _r = {
                            "variable": _variable,
                            "rule": _rule
                        }
                        
                        # add rule to list
                        rulesList['rules'].append(_r)
                    elif origSymbol == _transitions['push'] and switch == 1:
                        # pop/push pair found
                        print(origSymbol + ": " + origInitial + " -> " + origDest + ", " + _states['state'] + " -> " + _transitions['dest'])
                        #print("A" + origInitial + _transitions['dest'] + " -> " + origRead + "A" + origDest + _states['state'] + _transitions['read'])
                        
                        _variable = "A_" + origInitial + "_" + _transitions['dest']
                        _rule = origRead + "A_" + origDest + "_" + _states['state'] + _transitions['read']
                        
                        # create rule
                        _r = {
                            "variable": _variable,
                            "rule": _rule
                        }
                        
                        # add rule to list
                        rulesList['rules'].append(_r)
                    
                    # recursive call the destination of each transition
                    locatePairsRec(data, _transitions['dest'], origDest, origSymbol, origInitial, origRead, rulesList, switch)        
    
    # base case - no transitions or all transitions painted
    # i know its kind of a bad way to do this base case but hey it works (part 2!)
    return 

#################
# locatePairs -  #
#################
def locatePairs(data):
    #print("in locatePairs")
    
    # initialize pairs list
    rulesList = {
        "rules": []
    }
    
    # these will be done with insane amounts of nested loops. oops!
    # push/pop pairs
    print("")
    print("push/pop pairs:")
    for _states in data['states']:
        for _transitions in _states['transitions']:
            # reset painted transitions before running the recursive call
            for _i in data['states']:
                for _j in _i['transitions']:
                    _j['painted'] = "F"
            
            # save symbol, dest, initial state, and read
            origSymbol = _transitions['push']
            origDest = _transitions['dest']
            origInitial = _states['state']
            origRead = _transitions['read']
            
            # call traversal function on dest
            # make sure to not generate pairs for empty
            if origSymbol != '~':
                locatePairsRec(data, _transitions['dest'], origDest, origSymbol, origInitial, origRead, rulesList, 0)
          
    # pop/push pairs
    print("")
    print("pop/push pairs:")
    for _states in data['states']:
        for _transitions in _states['transitions']:
            # reset painted transitions before running the recursive call
            for _i in data['states']:
                for _j in _i['transitions']:
                    _j['painted'] = "F"
            
            # save symbol and initial state
            origSymbol = _transitions['pop']
            origDest = _transitions['dest']
            origInitial = _states['state']
            origRead = _transitions['read']
            
            # call traversal function on dest
            # make sure to not generate pairs for empty
            if origSymbol != '~':
                locatePairsRec(data, _transitions['dest'], origDest, origSymbol, origInitial, origRead, rulesList, 1)
            
    # print(rulesList)
    
    # return a list of rules
    return rulesList

#################
# makeCFG -  #
#################
def makeCFG(data, rulesList):
    # print("in generateRules")
    
    # initialize grammar json
    cfg = {
        "variables": []
    }
    
    # add rules generated by locatePairs
    for _rules in rulesList['rules']:
        _setContinue = 0
        
        # check if variable already exists and append rule to it directly
        for _variables in cfg['variables']:
            if _variables['variable'] == _rules['variable']:
                _variables['rules'].append({"rule": _rules['rule']})
                _setContinue = 1           

        if _setContinue == 1:
            continue
        
        # append new variable with its rule
        cfg['variables'].append(
            {
                "variable": _rules['variable'],
                "rules": [{"rule": _rules['rule']}]
            }
        )
        
    # add rules (A_p_p) -> ~ for all p
    for _states in data['states']:
        _setContinue = 0
        
        # variable to add
        _var = "(A_" + _states['state'] + "_" + _states['state'] + ")"
        
        # check if variable already exists and append rule to it directly
        for _variables in cfg['variables']:
            if _variables['variable'] == _var:
                _variables['rules'].append({"rule": "~"})     
                _setContinue = 1
                
        if _setContinue == 1:
            continue
        
        # append new variable with its rule
        cfg['variables'].append(
            {
                "variable": _var,
                "rules": [{"rule": "~"}]
            }
        )
    
    # add rules (A_i_k) -> (A_i_j)(A_j_k) for all i,j,k 
    for _s1 in data['states']:
        for _s2 in data['states']:
            for _s3 in data['states']:
                _setContinue = 0
                
                # variable and rule to add
                _var = "(A_" + _s1['state'] + "_" + _s3['state'] + ")"
                _rule = "(A_" + _s1['state'] + "_" + _s2['state'] + ")(A_" + _s2['state'] + "_" + _s3['state'] + ")"
                
                # check if variable already exists and append rule to it directly
                for _variables in cfg['variables']:
                    if _variables['variable'] == _var:
                        _variables['rules'].append({"rule": _rule})     
                        _setContinue = 1
                
                if _setContinue == 1:
                    continue
                
                # append new variable with its rule
                cfg['variables'].append(
                    {
                        "variable": _var,
                        "rules": [{"rule": _rule}]
                    }
                )
    
    # print(cfg)
    
    # return a json
    return cfg
    
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
    
    # Check if PDA is in proper format
    data = checkPDA(data)
    
    # locate all push/pop and pop/push pairs 
    rulesList = locatePairs(data)
    
    # use information from locatePairs to generate the grammar (as a json)
    grammar = makeCFG(data, rulesList)
    
    # create a JSON and output it as a new file
    with open('output_grammar.json', 'w') as f:
        json.dump(grammar, f, indent=4)

if __name__ == "__main__":
    main()