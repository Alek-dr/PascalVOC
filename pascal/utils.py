def _is_primitive(obj):
    """
    https://stackoverflow.com/questions/6391694/how-to-check-if-a-variables-type-is-primitive
    """
    return not hasattr(obj, '__dict__')