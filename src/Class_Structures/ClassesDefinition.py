from dataclasses import dataclass


@dataclass
class Trip:
    departure: str
    destination: str
    merchandise: dict[str, int] #JUST FOR TYPE HINTING!! PYTHON IS DINAMICALLY TYPED. DONT MESS WITH TYPES PLS :) TODO: change from int to float

    def __init__(self, departure, destination, merchandise):
        self.departure = departure
        self.destination = destination
        try:
            self.merchandise = {item: int(merchandise[item]) for item in merchandise}
        except ValueError:
            print("Error: merchandise quantities must be integers"
                  f"({merchandise} is not a valid merchandise dictionary)")
            exit(1)

    def __str__(self):
        return f"Trip({self.departure}, {self.destination}, {self.merchandise})"

    def __getstate__(self):
        return [self.departure, self.destination, self.merchandise]


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

    def __init__(self, id, route):
        self.id = id
        self.route = route

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
    driver : str
        the id of the driver
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