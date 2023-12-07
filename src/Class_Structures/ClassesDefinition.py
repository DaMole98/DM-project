from dataclasses import dataclass


@dataclass
class Trip:
    departure: str
    destination: str
    merchandise: dict[str, int] #JUST FOR TYPE HINTING!! PYTHON IS DINAMICALLY TYPED. DONT MESS WITH TYPES PLS :) TODO: change from int to float


@dataclass
class StandardRoute:
    id: str
    route: list[Trip]

@dataclass
class ActualRoute:
    id: str
    driver: str
    sroute: str
    route: list[Trip]

@dataclass
class HiddenRoute:
    dr_id: str
    length: int
    route: list[Trip]

@dataclass
class Driver:
    id: str
    hidden_route: HiddenRoute