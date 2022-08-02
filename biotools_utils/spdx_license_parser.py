"""
Utilities for the parsing the license list from SPDX.
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
import json
from dataclasses import dataclass
from typing import List, Dict
import requests
from requests import Response


@dataclass
class LicensesData:
    licenses: Dict[str, str]
    licenses_list: List[str]
    osi_approved_licenses: List[str]
    fsf_approved_licenses: List[str]
    deprecated_licenses: List[str]


def parse_license_list() -> LicensesData:
    """
    Parse the licenses list from SPDXs GitHub repository
    :return: The license data.
    """
    resp: Response = requests.get("https://raw.githubusercontent.com/spdx/license-list-data/master/json/licenses.json")
    resp.raise_for_status()
    license_list = resp.json()["licenses"]

    licenses: Dict[str, str] = {}
    licenses_list: List[str] = []
    osi_licenses: List[str] = []
    fsf_licenses: List[str] = []
    deprecated_licenses: List[str] = []

    for licens in license_list:
        license_id = licens["licenseId"]

        licenses[licens["name"]] = license_id
        licenses_list.append(license_id)

        if "isOsiApproved" in licens and licens["isOsiApproved"]:
            osi_licenses.append(license_id)
        if "isFsfLibre" in licens and licens["isFsfLibre"]:
            fsf_licenses.append(license_id)
        if "isDeprecatedLicenseId" in licens and licens["isDeprecatedLicenseId"]:
            deprecated_licenses.append(license_id)

    return LicensesData(licenses=licenses, licenses_list=licenses_list,
                        osi_approved_licenses=osi_licenses, fsf_approved_licenses=fsf_licenses,
                        deprecated_licenses=deprecated_licenses)
