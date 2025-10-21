"""
Provides a function to substitute placeholders in a template.
"""


def substitute(template: str, substitutions: dict[str, str]) -> str:
    """
    Substitutes placeholders in a template string.

    Parameters
    ----------
    template : str
        the template string
    substitutions : dict[str, str]
        the placeholders with their value

    Returns
    -------
    str
        the template after replacements
    """
    conv_template = template
    for name, value in substitutions.items():
        conv_template = conv_template.replace(f'[[{name}]]', value)
    return conv_template
