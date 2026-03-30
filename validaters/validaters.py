import re

from jsonschema.exceptions import ValidationError


def validate_phone(value):
    pattern = r'^\+?[\d\s\-\(\)]{10,20}$'
    if not re.match(pattern, value):
        raise ValidationError('Неверный формат телефона')