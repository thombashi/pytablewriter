def bool_to_str(value) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"

    return value
