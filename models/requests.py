from db.tables import CountryCodes, Granularity, Commodity
from pydantic import BaseModel
from datetime import datetime


class GeneratePricesRequest(BaseModel):
    """
    Request model for the model_prices endpoint.
    """

    for_date: datetime
    country_code: CountryCodes
    granularity: Granularity
    commodity: Commodity
