import dataclasses
import json
from dataclasses import dataclass
from typing import List


# overriding of the standard encoder in order to make it accept dataclasses
class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


@dataclass
class Trip:
    departure: str
    destination: str
    merchandise: dict[str, int]  # JUST FOR TYPE HINTING!! PYTHON IS DINAMICALLY TYPED. DONT MESS WITH TYPES PLS :) TODO: change from int to float


@dataclass
class Route:
    id: str
    route: list[Trip]


@dataclass
class StandardRoute(Route):
    """
    this class is used to represent the standard routes

    Attributes
    ----------
    id : str
        the id of the route
    route : list[Trip]
        the list of trips that compose the route
    """



@dataclass
class ActualRoute(Route):
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
    driver: str
    sroute: str



@dataclass
class HiddenRoute(Route):
    """
    this class is used to represent the hidden routes

    Attributes
    ----------
    dr_id : str
        the id of the driver
    length : int
        the g length of the route
    route : list[Trip]
        the list of trips that compose the route
    """
    driver_id: str
    length: int


@dataclass
class Driver:
    id: str
    standards: List[StandardRoute]
    actuals: List[ActualRoute]
    hidden_route: HiddenRoute
