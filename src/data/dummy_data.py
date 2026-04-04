from src.models.land_details import LandDetails
from src.enums.land_nature import LandNature
from src.enums.land_classification import LandClassification
from src.models.land_data_key import LandDataKey
from src.enums.land_dropdowns import District, Mandal, Village, SurveyNumber, KhataNumber

land_data = {
    LandDataKey(District.PEDDAPALLI, Mandal.MANTHANI, Village.MANTHANI, SurveyNumber.S101, KhataNumber.KH001): LandDetails(
        pattadar_name="Ramesh",
        father_name="Suresh",
        land_size="2 Acres",
        nature=LandNature.PATTA_LAND,
        classification=LandClassification.DRY,
        market_value=2000000.0
    ),
    LandDataKey(District.PEDDAPALLI, Mandal.RAMAGUNDAM, Village.GODAVARIKHANI, SurveyNumber.S231B, KhataNumber.Z01SHS1): LandDetails(
        pattadar_name="Mahesh",
        father_name="Naresh",
        land_size="1.5 Acres",
        nature=LandNature.LOANI_PATTA,
        classification=LandClassification.WET,
        market_value=3500000.0
    ),
    LandDataKey(District.SIDDIPET, Mandal.SIDDIPET_URBAN, Village.SIDDIPET, SurveyNumber.S1B32, KhataNumber.ZZPP01): LandDetails(
        pattadar_name="Srinivas",
        father_name="Rajesh",
        land_size="3 Acres",
        nature=LandNature.INAM_LAND,
        classification=LandClassification.DRY,
        market_value=25000000.0
    ),
}