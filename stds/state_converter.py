"""
A module for converting state names to abbreviations.

TODO: Make function to convert state abbreviations to the full state name.
"""

def state_to_abbrev(state_name):
    """
    Return the abbreviation for the given state name.

    Does minor error handling:
         Lowercase, strip, and replace single spaces from input string.

    TODO: Improve error handling

    Parameters
    ----------
    state_name: str
        The name of the state to convert to an abbreviaton.

    Returns
    -------
    str
        The two letter abbreviation for the given state name.
    """
    state_name = state_name.lower().strip().replace(" ", "")
    if state_name == "alabama":
        return "AL"
    elif state_name == "alaska":
        return "AK"
    elif state_name == "arkansas":
        return "AR"
    elif state_name == "arizona":
        return "AZ"
    elif state_name == "california":
        return "CA"
    elif state_name == "colorado":
        return "CO"
    elif state_name == "connecticut":
        return "CT"
    elif state_name == "d.c.":
        return "DC"
    elif state_name == "delaware":
        return "DE"
    elif state_name == "florida":
        return "FL"
    elif state_name == "georgia":
        return "GA"
    elif state_name == "hawaii":
        return "HI"
    elif state_name == "iowa":
        return "IA"
    elif state_name == "idaho":
        return "ID"
    elif state_name == "illinois":
        return "IL"
    elif state_name == "indiana":
        return "IN"
    elif state_name == "kansas":
        return "KS"
    elif state_name == "kentucky":
        return "KY"
    elif state_name == "louisiana":
        return "LA"
    elif state_name == "massachusetts":
        return "MA"
    elif state_name == "maryland":
        return "MD"
    elif state_name == "maine":
        return "ME"
    elif state_name == "michigan":
        return "MI"
    elif state_name == "minnesota":
        return "MN"
    elif state_name == "missouri":
        return "MO"
    elif state_name == "mississippi":
        return"MS"
    elif state_name == "montana":
        return "MT"
    elif state_name == "northcarolina":
        return "NC"
    elif state_name == "northdakota":
        return "ND"
    elif state_name == "nebraska":
        return "NE"
    elif state_name == "newhampshire":
        return "NH"
    elif state_name == "newjersey":
        return "NJ"
    elif state_name == "newmexico":
        return "NM"
    elif state_name == "nevada":
        return "NV"
    elif state_name == "newyork":
        return "NY"
    elif state_name == "oklahoma":
        return "OK"
    elif state_name == "ohio":
        return "OH"
    elif state_name == "oregon":
        return "OR"
    elif state_name == "pennsylvania":
        return "PA"
    elif state_name == "rhodeisland":
        return "RI"
    elif state_name == "southcarolina":
        return "SC"
    elif state_name == "southdakota":
        return "SD"
    elif state_name == "tennessee":
        return "TN"
    elif state_name == "texas":
        return "TX"
    elif state_name == "utah":
        return "UT"
    elif state_name == "virginia":
        return "VA"
    elif state_name == "vermont":
        return "VT"
    elif state_name == "washington":
        return "WA"
    elif state_name == "wisconsin":
        return "WI"
    elif state_name == "westvirginia":
        return "WV"
    else:
        return "WY"
