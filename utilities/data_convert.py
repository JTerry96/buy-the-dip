"""Data handling class."""
from flask import request
import pandas as pd
import io


class DictConverter():
    """Works with dictionaries and lists and converts between them."""
    def dict_to_list(list_dict: list[dict]) -> dict[list]:
        """Converts a list of dictionaries to a dictionary of lists."""
        dict_list = {}
        for dictionary in list_dict:
            for key, value in dictionary.items():
                if key not in dict_list:
                    dict_list[key] = []
                dict_list[key].append(value)
        return dict_list


class YfCsvReader():
    """Takes a Yahoo Finance portfolio CSV file and manipulates the data."""

    def extract_symbols(csv_file) -> list[str]:
        """Extracts the symbols from the Yfinance portfolio CSV file."""

        try:
            csv_file = request.files['csv_file']
            symbols = []

            if csv_file.filename != '':
                with io.TextIOWrapper(csv_file.stream) as csvfile:
                    df = pd.read_csv(csvfile)
                    symbols = df['Symbol'].tolist()

        except Exception:
            symbols = []

        return symbols
