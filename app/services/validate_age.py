from datetime import datetime


def validate_age(birthdate):
    birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
    age = (datetime.now() - birthdate).days // 365
    if age >= 18 :
        pass
    else:
        raise ValueError("You must be at least 18 years old to register")
    return birthdate