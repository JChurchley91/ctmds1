import sys
import os
import datetime
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.requests import GeneratePricesRequest
from models.responses import GeneratePricesResponse

@pytest.mark.order(14)
def test_generate_prices_request_model():
    """
    Test the GeneratePricesRequest model.
    Assert that the model is created successfully.
    :return: None
    """
    request = GeneratePricesRequest(
        for_date=datetime.datetime(2025, 5, 2, 0, 0),
        country_code="GB",
        granularity="h",
        commodity="power",
    )
    assert request.for_date == datetime.datetime(2025, 5, 2, 0, 0)
    assert request.country_code == "GB"
    assert request.granularity == "h"
    assert request.commodity == "power"

@pytest.mark.order(5)
def test_generate_prices_response_model():
    """
    Test the GeneratePricesResponse model.
    Assert that the model is created successfully.
    :return: None
    """
    response = GeneratePricesResponse(
        commodity="power",
        date=datetime.datetime(2025, 5, 2, 0, 0),
        country_code="GB",
        granularity="h",
        prices=[1.0, 2.0, 3.0, 4.0],
    )
    assert response.commodity == "power"
    assert response.date == datetime.datetime(2025, 5, 2, 0, 0)
    assert response.country_code == "GB"
    assert response.granularity == "h"
    assert response.prices == [1.0, 2.0, 3.0, 4.0]
