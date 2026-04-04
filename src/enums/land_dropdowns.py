from enum import Enum

class District(Enum):
    PEDDAPALLI = "Peddapalli"
    SIDDIPET = "Siddipet"

class Mandal(Enum):
    MANTHANI = "Manthani"
    RAMAGUNDAM = "Ramagundam"
    SIDDIPET_URBAN = "Siddipet Urban"

class Village(Enum):
    MANTHANI = "Manthani"
    GODAVARIKHANI = "Godavarikhani"
    SIDDIPET = "Siddipet"

class SurveyNumber(Enum):
    S101 = "101"
    S231B = "231-b"
    S1B32 = "1/b32"

class KhataNumber(Enum):
    KH001 = "KH001"
    Z01SHS1 = "Z01sHS1"
    ZZPP01 = "ZZPP01"
