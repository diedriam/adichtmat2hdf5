from dataclasses import dataclass


@dataclass
class Paths:
    log: str
    data: str

@dataclass
class Files:
    file: str

@dataclass
class Params:
    tokens: dict
