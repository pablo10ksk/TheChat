def get_country_code(code: str):
    print(code)
    return {"ES": "+34", "US": "+1"}[code]


def get_countries_map():
    countries = [
        ("", "Select a country"),
        ("ES", "Spain"),
        ("US", "United States"),
        ("CA", "Canada"),
        ("DE", "Germany"),
        ("FR", "France"),
        ("UK", "United Kingdom"),
        ("CN", "China"),
        ("JP", "Japan"),
        ("IN", "India"),
    ]
    # Create a dictionary for easy lookup
    map_data = {code: name for code, name in countries}
    return map_data
