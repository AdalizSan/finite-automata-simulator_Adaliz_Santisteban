import os
import json
from flask import Flask, request, jsonify
from graphviz import Digraph

# configuration flask apllication
app = Flask(__name__)

class automata:
    def __init__(self, data): #store data from JSON in the class
        self.id = data.get('id', '')
        self.name = data.get('name', '')
        self.statr = data.get('start', '')
        