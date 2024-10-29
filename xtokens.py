import json
from dataclasses import dataclass
from typing import List

@dataclass
class Xtoken:
    "token for intervals to cut"
    tok_id: str
    tok_longid: str
    tok_start: str
    tok_stop: str


class Xtokenset(object):
    """set of xtoken"""
    filename: str
    xtokens: List[Xtoken]

    def __init__(self, filename = "./conf/xtokens.json"):
        self.filename = filename
        self.xtokens: list

    def load(self)->None:
        self.xtokens = []
        with open(self.filename, 'r') as f:
            xtokens = json.loads(f.read())        
            self.xtokens = [Xtoken(xtok["tok_id"], xtok["tok_longid"], xtok["tok_start"], xtok["tok_stop"]) for xtok in xtokens]
       
    def print(self)->None:
        for xtok in self.xtokens:
           print(xtok)