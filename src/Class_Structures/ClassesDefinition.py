from dataclasses import dataclass


@dataclass
class Trip:
    departure: str
    destination: str
    merchandise: dict[str, int] #JUST FOR TYPE HINTING!! PYTHON IS DINAMICALLY TYPED. DONT MESS WITH TYPES PLS :) TODO: change from int to float


@dataclass
class StandardRoute:
    """
    this class is used to represent the standard routes

    Attributes
    ----------
    id : str
        the id of the route
    route : list[Trip]
        the list of trips that compose the route
    """
    id: str
    route: list[Trip]

@dataclass
class ActualRoute:
    """
    this class is used to represent the actual routes implemented by the drivers

    Attributes
    ----------
    id : str
        the id of the route
    driver : str
        the id of the driver
    sroute : str
        the id of the standard route
    route : list[Trip]
        the list of trips that compose the route
    """
    id: str
    driver: str
    sroute: str
    route: list[Trip]

@dataclass
class HiddenRoute:
    """
    this class is used to represent the hidden routes

    Attributes
    ----------
    dr_id : str
        the id of the driver
    length : int
        the length of the route
    route : list[Trip]
        the list of trips that compose the route
    """
    dr_id: str
    length: int
    route: list[Trip]

@dataclass
class Driver:
    id: str
    hidden_route: HiddenRoute