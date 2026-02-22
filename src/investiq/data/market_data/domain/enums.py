from enum import Enum, auto


class AssetType(Enum):
    FUTURE = auto()
    CONT_FUTURE = auto()
    STOCK = auto()
    FOREX = auto()
    OPTION = auto()


class WhatToShow(str, Enum):
    TRADES = "TRADES"
    MIDPOINT = "MIDPOINT"


class Currency(str, Enum):
    USD = "USD"


class Exchange(str, Enum):
    CME = "CME"
    NYSE = "NYSE"
    IDEALPRO = "IDEALPRO"


class BarSize(str, Enum):
    ONE_MINUTE = "1 min"
    ONE_HOUR = "1 hour"
    FOUR_HOURS = "4 hours"
    ONE_DAY = "1 day"
    ONE_WEEK = "1 week"