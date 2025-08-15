import os
import json
from flask import Flask, request, jsonify
from datetime import datetime
from graphviz import Digraph

# configuration flask apllication
app = Flask(__name__)

class automata:
    def __init__(self, data): #store data from JSON in the class
        #Check for required fields
        required_fields = ['id', 'initial_state', 'acceptance_states', 'alphabet', 'states', 'transitions']
        for key in required_fields:
            if key not in required_fields:
                raise ValueError(f"Missing required key: {key}") 
        self.id = data.get('id', '')
        self.name = data.get('name', '')
        self.initialState = data.get('initial_state', '')
        self.acceptState = data.get('acceptance_states', [])
        self.alphabet = data.get('alphabet', [])
        self.states = data.get('states', [])
        self.testWords = data.get('test_strings', [])
        self.transitions = {}

        #Easy use of transitions
        for trans in data.get('transitions', []):
            if 'from_state' in trans and 'symbol' in trans and 'to_state' in trans:
                if trans['from_state'] not in self.transitions:
                    self.transitions[trans['from_state']] = {}
                self.transitions [trans['from_state']][trans['symbol']] = trans['to_state']

    def checkAll(self):
        #Check specific errors
        if not self.id: #if not found id show error
            raise ValueError("It need an Id")
        if not self.initialState:
            raise ValueError("There is no initial state")
        if not self.states:
            raise ValueError("There is no states")
        if not self.acceptState:
            raise ValueError("It need acceptance states")
        if not self.alphabet:
            raise ValueError("It need an alphabet")
        
        #All arrays
        if not isinstance(self.states, list): #if states is not a list show error
            raise ValueError("States must be on array")
        if not isinstance(self.acceptState, list):
            raise ValueError("Acceptance states must be on array")
        if not isinstance(self.alphabet, list):
            raise ValueError("Alphabet must be on array")
        
        #Check if the initial state is in the states
        if self.initialState not in self.states:
            raise ValueError(f" The initial state {self.initialState} is not in the states array")
        
        #Check acceptance states
        for s in self.acceptState:
            if s not in self.states:
                raise ValueError(f"The acceptance state {s} is not in the states")
        
        #Check transitions
        for s in self.states:
            if s not in self.transitions:
                raise ValueError(f"The state {s} hasn't transitions")
            for letter in self.alphabet:
                if letter not in self.transitions[s]:
                    raise ValueError(f"The state {s} hasn't transition for the letter {letter}")
                #Check if the destination state is valid
                if self.transitions[s][letter] not in self.states:
                    raise ValueError(f"The transition from {s} with letter {letter} to {self.transitions[s][letter]} is not valid")
        
        #Check if the letters of the transitions are in the alphabet
        for s in self.transitions:
            for letter in self.transitions[s]:
                if letter not in self.alphabet:
                    raise ValueError(f"The letter {letter} isn't in the alphabet")
    
    #Fuction for chak words step by step
    def checkWord(self, word):
        def advance(actualState, rest):
            if not rest:  # If no more letters to process
                return actualState in self.acceptState  
            letter = rest[0]  # Get the first letter
            if letter not in self.alphabet:
                raise ValueError(f"Letter {letter} is not permited")
            nextState = self.transitions.get(actualState, {}).get(letter)
            if not nextState:
                return False # Can't advance 
            return advance(nextState, rest[1:]) 
        if not word: # void word
            return self.initialState in self.acceptState
        return advance(self.initialState, word)
    
    #Function to prove all words
    def proveWords(self):
        results = []
        for word in self.testWords:
            try:
                accepted = self.checkWord(word)
                results.append({'input': word, 'result': accepted})
            except ValueError as e:
                results.append({'input': word, 'result': False, 'error': str(e)})
        return results

    def drawGraph(self):

        os.makedirs('imagesAutomata', exist_ok=True)  
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nameFile = f"imagesAutomata/{self.id}_{date}.png"

        #create the graph
        drawing = Digraph(format='png')
        drawing.attr(rankdir='LR')

        #initial arrow
        drawing.node('inicial', shape='none', label='')
        drawing.edge('inicial', self.initialState, label='inicial', color='purple')

        #draw states
        for state in self.states:
            if state in self.acceptState:
                drawing.node(state, shape='doublecircle', color='purple') #acceptence state
            else:
                drawing.node(state, shape='circle', color='purple') #normal state
        
        #draw transitions
        for state in self.transitions:
            for letter, next_state in self.transitions[state].items():
                drawing.edge(state, next_state, label=letter, color='purple')
        
        try:
            drawing.render(nameFile, view=False)
            print(f"Graph is ready: {nameFile}.png")
            return f"{nameFile}.png"
        except:
            raise RuntimeError("Error creating the graph image")

@app.route('/process-automata', methods=['POST'])
def processAutomata():
    try:
        data = request.json
        if not isinstance(data, list):
            return jsonify({"error": "Invalid input format, must be a array"}), 400
        
        results = []
        for item in data:
            try:
                automataInsta = automata(item)
                automataInsta.checkAll()
                routeGraph = automataInsta.drawGraph()
                resultWords = automataInsta.proveWords()
                results.append({
                    "id": automataInsta.id,
                    "success": True,
                    "inputs_validation": resultWords,
                    "graph": routeGraph
                })
            except Exception as e:
                results.append({
                    "id": item.get('id', 'no id'),
                    "success": False,
                    "error_description": str(e)
                })
        return jsonify(results)
    except:
        return jsonify({"error": "An error processing automata graph"}), 500

if __name__ == '__main__':
    app.run(debug=True) #Run application 





