import json
from time import sleep

import pandas as pd
import requests
from requests import Response
import urllib.parse

from biotools_utils import extract_terms


def _download_full_tool_list() -> list[dict]:
    """
    Download the entire tool list from bio.tools.

    :return: The tool list.
    """
    tool_list: list[dict] = []
    next_page: str = ""
    base_url = f"https://bio.tools/api/t/?format=json"
    # Get the first page
    resp: Response = requests.get(base_url)
    resp.raise_for_status()
    resp_json = resp.json()
    next_page = resp_json["next"]
    tool_list.extend(resp_json["list"])
    sleep(1)

    # Get the next pages
    while next_page is not None:
        resp: Response = requests.get(f"{base_url}&{next_page[1:]}")
        print(resp.url)
        resp.raise_for_status()
        resp_json = resp.json()
        next_page = resp_json["next"]
        tool_list.extend(resp_json["list"])
        sleep(1)

    with open("TestFiles/all_tools.json", "w") as f:
        f.write(json.dumps(tool_list))

    return tool_list


def _download_tool_list(collection_id: str) -> list[dict]:
    """
    Download tool list for a given collection ID.

    :param collection_id: The collection ID.
    :return: The list of tools.
    """
    tool_list: list[dict] = []
    next_page: str = ""
    # Create base URL
    escaped_collection_id: str = urllib.parse.quote(collection_id.encode('utf8'))
    base_url = f"https://bio.tools/api/t/?collectionID=%22{escaped_collection_id}%22&format=json"

    # Get the first page
    resp: Response = requests.get(base_url)
    resp.raise_for_status()
    resp_json = resp.json()
    next_page = resp_json["next"]
    tool_list.extend(resp_json["list"])
    sleep(1)

    # Get the next pages
    while next_page is not None:
        resp: Response = requests.get(f"{base_url}&{next_page[1:]}")
        print(resp.url)
        resp.raise_for_status()
        resp_json = resp.json()
        next_page = resp_json["next"]
        tool_list.extend(resp_json["list"])
        sleep(1)

    with open(f"TestFiles/{collection_id}_tools.json", "w") as f:
        f.write(json.dumps(tool_list))

    return tool_list


def _extract_collection_tools(tool_list: list[dict], collection_id: str) -> list[dict]:
    """
    Extract tools with  a given collection ID.

    :param tool_list: The list of tools.
    :param collection_id: The collection ID.
    :return: The list of tools.
    """
    return [tool for tool in tool_list if collection_id in tool["collectionID"]]


def _create_collection_tool_list(tool_list: list[dict]):
    """
    Create the tool list.

    :param tool_list: The list of tools.
    """
    parsed_tool_list: dict = {}
    with open("Resources/topic_index.json", "r") as f:
        topic_index = json.load(f)["data"]
    with open("Resources/operation_index.json", "r") as f:
        operation_index = json.load(f)["data"]
    for tool in tool_list:
        tool_idx: str = f"{tool['name']}\n(https://bio.tools/{tool['biotoolsID']})"
        # Extract the terms
        topics_raw: list = list(extract_terms(tools=[tool], term_type="Topic").values())[0]
        operations_raw: list = list(extract_terms(tools=[tool], term_type="Operation").values())
        if len(operations_raw) > 0:
            operations_raw = operations_raw[0]

        # Get the term names
        topics_list: list = list(set([term["uri"].replace("http://edamontology.org/", "")
                                      for term in topics_raw]))
        operations_list: list = list(
            set([term["uri"].replace("http://edamontology.org/", "") for term in operations_raw]))

        topics: str = "\n".join([f"{topic_index[term]['name']} ({term})"
                                 for term in topics_list if term in topic_index])
        operations: str = "\n".join([f"{operation_index[term]['name']} ({term})"
                                     for term in operations_list if term in operation_index])

        # Add the term to the dictionary
        parsed_tool_list[tool_idx] = [tool["description"], topics, operations]

    tools_df: pd.DataFrame = pd.DataFrame.from_dict(parsed_tool_list, orient="index", columns=["Description", "Topics",
                                                                                               "Operations"])
    tools_df.index.name = "ID"
    tools_df.to_excel("TestFiles/biotools_proteomics.xlsx")


def main():
    collection_id: str = "Proteomics"
    # full_tools: list[dict] = _download_full_tool_list()
    with open("Resources/all_tools.json", "r") as f:
        full_tools = json.load(f)

    tools: list[dict] = _extract_collection_tools(tool_list=full_tools, collection_id=collection_id)
    _create_collection_tool_list(tool_list=tools)


if __name__ == "__main__":
    main()
