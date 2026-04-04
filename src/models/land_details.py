from dataclasses import dataclass
from src.enums.land_classification import LandClassification
from src.enums.land_nature import LandNature


@dataclass(frozen=True, slots=True)
class LandDetails:
    pattadar_name: str
    father_name: str
    land_size: str
    nature: LandNature
    classification: LandClassification
    market_value: float