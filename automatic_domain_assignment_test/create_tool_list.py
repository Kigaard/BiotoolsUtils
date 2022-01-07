import json
from time import sleep

import pandas as pd
import requests
from requests import Response
import urllib.parse


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

    with open("tools.json", "w") as f:
        f.write(json.dumps(tool_list))

    return tool_list


def _create_tool_list(tool_list: list[dict]):
    """
    Create the tool list.

    :param tool_list: The list of tools.
    """
    parsed_tool_list: dict = {}

    for tool in tool_list:
        tool_idx: str = f"{tool['name']}\n(https://bio.tools/{tool['biotoolsID']})"
        topics: str = "\n".join([topic["term"] for topic in tool["topic"]])
        operations: str = "\n".join(list(set([op["term"] for op in
                                              [function["operation"][0] for function in tool["function"]]])))
        parsed_tool_list[tool_idx] = [tool["description"], topics, operations]

    tools_df: pd.DataFrame = pd.DataFrame.from_dict(parsed_tool_list, orient="index", columns=["Description", "Topics",
                                                                                               "Operations"])
    tools_df.to_excel("tool_list.xlsx")


def main():
    tools: list[dict] = _download_tool_list(collection_id="")
    _create_tool_list(tool_list=tools)


if __name__ == "__main__":
    main()
