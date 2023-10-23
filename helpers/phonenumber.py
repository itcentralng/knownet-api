class Phonenumber:
    """Phonenumber class"""
    def __init__(self, number: str) -> None:
        self.display = number

def validate_phonenumber(phonenumber, country_code="+234"):
    if phonenumber.startswith(country_code) and len(phonenumber) == 14:
        return phonenumber
    elif phonenumber.startswith(country_code[1:]) and len(phonenumber) == 13:
        return "+"+phonenumber
    elif phonenumber.startswith("0") and len(phonenumber) == 11:
        return country_code+phonenumber[1:]
    elif len(phonenumber) == 10:
        return country_code+phonenumber[1:]
    else:
        raise ValueError(Phonenumber)