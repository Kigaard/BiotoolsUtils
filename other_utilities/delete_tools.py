"""
Utility script for bulk deletion of tools
Copyright (C) 2022  Mads Kierkegaard

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from argparse import ArgumentParser, FileType, Namespace
import json
import sys
import time

import requests
from requests import HTTPError


class CustomArgumentParser(ArgumentParser):
    def error(self, message: str):
        sys.stdout.write(LICENSE_STR)
        sys.stdout.write("\n")
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        exit(2)


BASE_API_URL: str = "https://bio.tools/api"
LICENSE_STR: str = """
delete_tools.py  Copyright (C) 2022  Mads Kierkegaard

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


def delete_tools(account_credentials: dict, tool_id_list_file: str):
    """
    Delete tools from bio.tools.

    :param account_credentials: The dictionary with the the username and password of the account responsible
        for the deletion.
    :param tool_id_list_file: The text file with the user.
    """
    # Parse tool ids
    tool_ids: list = [tool.rstrip("\n") for tool in open(tool_id_list_file, 'r').readlines()]

    token: str = ""
    # Get the token
    try:
        resp_auth = requests.post(f"{BASE_API_URL}/rest-auth/login/", json=account_credentials,
                                  headers={"Content-Type": "application/json"})
        resp_auth.raise_for_status()
        token = resp_auth.json()['key']
        print("Got the token")
    except HTTPError as e:
        if e.response.status_code == 400:
            sys.stderr.write("ERROR: Please verify the login credentials.")
            exit(5)
        else:
            sys.stderr.write(f"ERROR: {e.response.status_code} {e.response.reason}")
            exit(5)

    # Loop through the tools and delete them
    number_of_tools: int = len(tool_ids)
    for idx, tool_id in enumerate(tool_ids):
        time.sleep(1)
        try:
            resp_delete = requests.delete(f"{BASE_API_URL}/tool/{tool_id}/",
                                          headers={'Authorization': f"Token {token}"})
            resp_delete.raise_for_status()
            print(f"Deleted tool {idx + 1}/{number_of_tools}: 'biotools:{tool_id}'")
        except HTTPError as e:
            if e.response.status_code == 404:
                print(f"Tool {idx + 1}/{number_of_tools}: 'biotools:{tool_id}' has already been deleted or "
                      f"does not exist.")
                continue
            sys.stderr.write(f"ERROR: {e.response.status_code} {e.response.reason}")
            continue


if __name__ == '__main__':
    # Create the argument parser, add the arguments and parse the arguments
    parser: CustomArgumentParser = CustomArgumentParser(prog="delete_tools.py",
                                                        description="Script for bulk deletion of tools", add_help=True)
    parser.add_argument("--credentials", '-c', help="The JSON-file containing the dictionary with the keys: 'username'"
                                                    "and 'password' for the account responsible for the deletion.",
                        type=FileType('r'), required=True)
    parser.add_argument("--ids", "-i", help="The file containing the ids of the bio.tools to be deleted. "
                                            "One ID per line.",
                        type=FileType('r'), required=True)
    args: Namespace = parser.parse_args()

    print(LICENSE_STR)

    # Read the credentials and check that it contains the required fields
    with open(args.credentials.name, 'r') as f:
        credentials = json.load(f)
    if 'username' not in credentials or str.isspace(credentials['username']):
        sys.stderr.write("No 'username' found in credentials.")
        exit(2)
    if 'password' not in credentials or str.isspace(credentials['username']):
        sys.stderr.write("No 'password' found in credentials.")
        exit(2)

    # Call the script
    delete_tools(account_credentials=credentials, tool_id_list_file=args.file.name)
