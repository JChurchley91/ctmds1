from enum import Enum

import polars


class CountryCodes(str, Enum):
    """
    Enum class for the different country codes available.
    """

    GB = "GB"
    FR = "FR"
    NL = "NL"
    DE = "DE"

    @classmethod
    def get_price(cls, country_code: str) -> int:
        """
        Return the base price for the specified country code.

        :param country_code: the country code to get the base price for
        :return: base price for specified country code
        """
        price_mapping = {
            "GB": 61,
            "FR": 58,
            "NL": 52,
            "DE": 57,
        }

        return price_mapping[country_code]

    @classmethod
    def return_as_df(cls) -> polars.DataFrame:
        """
        Return a Polars DataFrame containing the available country codes.

        :return: Polars DataFrame
        """
        data = {
            "country_code": [country_code.value for country_code in cls],
            "country_base_price": [
                cls.get_price(country_code.value) for country_code in cls
            ],
        }
        df = polars.DataFrame(data)
        return df


class Granularity(str, Enum):
    h = "h"
    hh = "hh"

    @classmethod
    def return_as_df(cls) -> polars.DataFrame:
        """
        Return a Polars DataFrame containing the available granularities.

        :return: Polars DataFrame
        """
        data = {"granularity": [granularity.value for granularity in cls]}
        return polars.DataFrame(data)


class Commodity(str, Enum):
    wind = "wind"
    natural_gas = "natural_gas"
    nuclear = "nuclear"
    solar = "solar"
    hydro = "hydro"
    biofuel = "biofuel"

    @classmethod
    def return_as_df(cls) -> polars.DataFrame:
        """
        Return a Polars DataFrame containing the available commodities.

        :return: Polars DataFrame
        """
        data = {"commodity": [commodity.value for commodity in cls]}
        df = polars.DataFrame(data)
        return df


class CountryEnergyMix(str, Enum):
    GB = "GB"
    FR = "FR"
    NL = "NL"
    DE = "DE"

    @classmethod
    def get_energy_mix(cls, country_code: str, commodity: str) -> float:
        energy_mix_mapping = {
            "GB": {
                "wind": 20,
                "natural_gas": 30,
                "nuclear": 15,
                "solar": 15,
                "hydro": 15,
                "biofuel": 5,
            },
            "FR": {
                "wind": 15,
                "natural_gas": 10,
                "nuclear": 50,
                "solar": 10,
                "hydro": 10,
                "biofuel": 5,
            },
            "NL": {
                "wind": 25,
                "natural_gas": 40,
                "nuclear": 5,
                "solar": 15,
                "hydro": 5,
                "biofuel": 10,
            },
            "DE": {
                "wind": 30,
                "natural_gas": 20,
                "nuclear": 10,
                "solar": 20,
                "hydro": 10,
                "biofuel": 10,
            },
        }
        return energy_mix_mapping[country_code][commodity]

    @classmethod
    def return_as_df(cls) -> polars.DataFrame:
        """
        Return a Polars DataFrame containing the energy mix for every country.

        :return: Polars DataFrame
        """
        data = {
            "country_code": [country_code.value for country_code in cls],
            "wind": [
                cls.get_energy_mix(country_code.value, "wind") for country_code in cls
            ],
            "natural_gas": [
                cls.get_energy_mix(country_code.value, "natural_gas")
                for country_code in cls
            ],
            "nuclear": [
                cls.get_energy_mix(country_code.value, "nuclear")
                for country_code in cls
            ],
            "solar": [
                cls.get_energy_mix(country_code.value, "solar") for country_code in cls
            ],
            "hydro": [
                cls.get_energy_mix(country_code.value, "hydro") for country_code in cls
            ],
            "biofuel": [
                cls.get_energy_mix(country_code.value, "biofuel")
                for country_code in cls
            ],
        }
        df = polars.DataFrame(data)
        return df
