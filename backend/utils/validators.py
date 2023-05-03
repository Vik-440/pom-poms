

def validate_field(field, field_type, data):
    if field not in data:
        return {field: f'miss in data'}
    if not any(isinstance(data[field], t) for t in (field_type if isinstance(field_type, tuple) else (field_type,))):
        return {field: f'is not {", ".join(t.__name__ for t in (field_type if isinstance(field_type, tuple) else (field_type,)))} type'}
    return