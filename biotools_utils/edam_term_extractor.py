import itertools
from collections import defaultdict


def extract_terms(tools: list, term_type: str) -> dict:
    """
    Extract terms from the tools.
    :param tools: The list of tools.
    :param term_type: The term type.
    :return: The dictionary with the tool ID and the terms.
    """
    term_type = term_type.capitalize()

    if term_type == "Topic":
        return _extract_edam_topics(tools=tools)
    elif term_type == "Operation":
        return _extract_edam_operation(tools=tools)
    elif term_type == "Format":
        return _extract_edam_format(tools=tools)
    elif term_type == "Data":
        return _extract_edam_data(tools=tools)
    else:
        raise ValueError(f"The term type '{term_type}' is not valid. Must be 'Topic', 'Operation', 'Format', or"
                         f"'Data'.")


def _extract_edam_topics(tools: list) -> dict:
    """
    Get the EDAM topics for each tool.
    :param tools: The list of tools.
    :return: The dictionary with the tool id and the topics.
    """
    terms: defaultdict = defaultdict(lambda: [])

    for tool in tools:
        terms[tool["biotoolsID"]].extend([topic for topic in tool["topic"]])

    return terms


def _extract_edam_operation(tools: list) -> dict:
    """
    Get the EDAM operation for each tool.
    :param tools: The list of tools.
    :return: The dictionary with the tool id and the operations.
    """
    terms: defaultdict = defaultdict(lambda: [])

    for tool in tools:
        terms[tool["biotoolsID"]].extend(*[function["operation"] for function in tool["function"]])

    return terms


def _extract_edam_format(tools: list) -> dict:
    """
    Get the EDAM format for each tool.
    :param tools: The list of tools.
    :return: The dictionary with the tool id and the formats.
    """
    terms: defaultdict = defaultdict(lambda: [])

    for tool in tools:
        terms[tool["biotoolsID"]].extend(itertools.chain(*_get_inputs_outputs_info(tool=tool, term_type="format")))
    return terms


def _extract_edam_data(tools: list) -> dict:
    """
    Get the EDAM data for each tool.
    :param tools: The list of tools.
    :return: The dictionary with the tool id and the topics.
    """
    terms: defaultdict = defaultdict(lambda: [])
    for tool in tools:
        terms[tool["biotoolsID"]].extend(_get_inputs_outputs_info(tool=tool, term_type="data"))
    return terms


def _get_inputs_outputs_info(tool: dict, term_type: str) -> list:
    """
    Get the inputs and outputs for a tool.
    :param tool: The tool dict.
    :param term_type: The term type.
    :return: The list with the specific terms.
    """
    terms: list = []

    for function in tool["function"]:
        if "input" in function:
            for i in function["input"]:
                if term_type in i:
                    terms.append(i[term_type])
        if "output" in function:
            for o in function["output"]:
                if term_type in o:
                    terms.append(o[term_type])

    return list(terms)