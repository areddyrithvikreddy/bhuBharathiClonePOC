from dataclasses import dataclass
from src.enums.land_classification import LandClassification
from src.enums.land_nature import LandNature
from src.enums.land_dropdowns import District, Mandal, Village, SurveyNumber, KhataNumber

@dataclass(frozen=True, slots=True)
class LandDataKey:
    district: District
    mandal: Mandal
    village: Village
    survey_number: SurveyNumber
    khata_number: KhataNumber