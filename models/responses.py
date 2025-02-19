from db.tables import CountryCodes, Granularity, Commodity
from pydantic import BaseModel
from datetime import datetime


class GeneratePricesResponse(BaseModel):
    """
    Response model for the model_prices endpoint.
    """

    commodity: Commodity
    date: datetime
    country_code: CountryCodes
    granularity: Granularity
    prices: list[float]
