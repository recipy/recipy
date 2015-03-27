def recursive_getattr(obj, attr):
    prev_part = obj

    for part in attr.split("."):
        prev_part = getattr(prev_part, part)

    return prev_part

def recursive_setattr(obj, attr, value):
    prev_part = obj

    for part in attr.split(".")[:-1]:
        prev_part = getattr(prev_part, part)

    setattr(prev_part, attr.split(".")[-1], value)
