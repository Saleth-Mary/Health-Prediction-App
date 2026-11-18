
import re
from datetime import datetime, date
import math

# 1. Validate full name
def validate_name(name):

    if not name or not name.strip():
        return False, "Full name cannot be empty."

    return True, ""


# 2. Validate email
def validate_email(email):

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not re.match(pattern, email):
        return False, "Please enter a valid email address."

    return True, ""


# 3. Validate date of birth
def validate_dob(dob):

    try:
        dob = dob.replace(".", "/")
        birth_date = datetime.strptime(
            dob, "%d/%m/%Y"
        ).date()

        if birth_date > date.today():
            return False, "Date of birth cannot be in the future."

        return True, birth_date.strftime("%d/%m/%Y")

    except ValueError:
        return False, "Invalid date. Please use dd/mm/yyyy format."


def validate_blood_value(value, field_name):

    try:
        number = float(value)

        if not math.isfinite(number):
            return False, f"{field_name} must be a valid finite number."

        if number <= 0:
            return False, f"{field_name} must be greater than zero."

        return True, number

    except (ValueError, TypeError):
        return False, f"{field_name} must be numeric."


# 5. Validate all patient information
def validate_patient(data):

    errors = []

    valid, message = validate_name(data["full_name"])
    if not valid:
        errors.append(message)

    valid, message = validate_email(data["email"])
    if not valid:
        errors.append(message)

    valid, result = validate_dob(data["dob"])
    if not valid:
        errors.append(result)
    else:
        data["dob"] = result

    for field in ["glucose", "haemoglobin", "cholesterol"]:

        valid, result = validate_blood_value(
            data[field], field.capitalize()
        )

        if not valid:
            errors.append(result)
        else:
            data[field] = result

    return errors
