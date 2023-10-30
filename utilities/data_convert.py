"""Data handling class."""

class DictConverter():
    """Works with dictionaries and lists and converts between them."""
    def dict_to_list(list_dict:list[dict]) -> dict[list]:
        """Converts a list of dictionaries to a dictionary of lists."""
        dict_list = {}
        for dictionary in list_dict:
            for key, value in dictionary.items():
                if key not in dict_list:
                    dict_list[key] = []
                dict_list[key].append(value)
        return dict_list  
