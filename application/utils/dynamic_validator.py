def validate_config(fields, config):
    for field in fields:
        key = field.key
        if field.is_required and key not in config:
            raise ValueError(f"{field.name} is required")

        if key in config:
            value = config[key]

            if field.type == "int" and not isinstance(value, int):
                raise ValueError(f"{field.name} must be int")

            if field.type == "string" and not isinstance(value, str):
                raise ValueError(f"{field.name} must be string")