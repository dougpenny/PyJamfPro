#
# endpoints.py
#
# Copyright (c) 2022 Doug Penny
# Licensed under MIT
#
# See LICENSE.md for license information
#
# SPDX-License-Identifier: MIT
#

import xml.etree.ElementTree as ET

from typing import Dict, List, Union

import pyjamfpro.jamfpro as jamf

from pyjamfpro.utils.dict_to_xml import class_dict_to_xml
from requests import Response


class ClassicMixin:
    """
    The ClassicMixin class contains public methods for the
    Jamf Classic API. More information about the Classic API
    can be found on Jamf's documentation site.
    https://developer.jamf.com/jamf-pro/docs/getting-started-2
    """

    def classic_class_with_id(self, id: int) -> Dict:
        """
        Retrieves the class with the given ID.

        Args:
            id (int):
                ID of the class to retrieve

        Returns:
            A dictionary representing the retrieved class.
        """
        class_data = self.make_api_request(f"JSSResource/classes/id/{id}")
        return class_data.json()["class"]

    def classic_class_with_name(self, name: str) -> Dict:
        """
        Retrieves the class with the given name.

        Args:
            name (str):
                Name of the class to retrieve

        Returns:
            A dictionary representing the retrieved class.
        """
        class_data = self.make_api_request(f"JSSResource/classes/name/{name}")
        return class_data.json()["class"]

    def classic_classes(self) -> List:
        """
        Retrieves all classes.

        Returns:
            A list of all classes currently in Jamf.
        """
        class_data = self.make_api_request("JSSResource/classes")
        return class_data.json()["classes"]

    def classic_delete_class_with_id(self, id: int) -> bool:
        """
        Deletes the class with the given ID.

        Args:
            id (int):
                ID value for the class to delete

        Returns:
            A boolean representing success or failure in deleting the class.
        """
        delete_response = self.make_api_request(f"JSSResource/classes/id/{id}", method=jamf.HTTPMethod.DELETE)
        if delete_response.status_code == 200:
            return True
        else:
            return False

    def classic_delete_class_with_name(self, name: str) -> bool:
        """
        Deletes the class with the given name.

        Args:
            name (str):
                Name of the class to delete

        Returns:
            A boolean representing success or failure in deleting the class.
        """
        delete_response = self.make_api_request(f"JSSResource/classes/name/{name}", method=jamf.HTTPMethod.DELETE)
        if delete_response.status_code == 200:
            return True
        else:
            return False

    def classic_new_class(self, new_class: Dict) -> Union[None, str]:
        """
        Create a new class in Jamf Pro.

        Args:
            new_class (Dict):
                Dictionary representation of the class information

        Returns:
            If creation is successful, the ID of the new class,
            otherwise, None.
        """
        data = class_dict_to_xml(new_class)
        class_response: Response = self.make_api_request("JSSResource/classes/id/-1", data=data, method=jamf.HTTPMethod.POST, classic=True)
        if class_response.status_code == 201:
            xml_data = ET.fromstring(class_response.text)
            return xml_data.findtext('id')
        else:
            return None

    def classic_update_class_with_id(self, id: int, existing_class: Dict) -> Union[None, str]:
        """
        Updates the class with the given id.

        Args:
            id (int):
                ID of the class to update
            existing_class (Dict):
                Dictionary representation of the class information

        Returns:
            If update is successful, the ID of the updated class,
            otherwise, None.
        """
        data = class_dict_to_xml(existing_class)
        class_response: Response = self.make_api_request(f"JSSResource/classes/id/{id}", data=data, method=jamf.HTTPMethod.PUT, classic=True)
        if class_response.status_code == 201:
            xml_data = ET.fromstring(class_response.text)
            return xml_data.findtext('id')
        else:
            return None

    def classic_update_class_with_name(self, name: str, existing_class: Dict) -> Union[None, str]:
        """
        Updates the class with the given name.

        Args:
            name (str):
                Name of the class to update
            existing_class (Dict):
                Dictionary representation of the class information

        Returns:
            If update is successful, the ID of the updated class,
            otherwise, None.
        """
        data = class_dict_to_xml(existing_class)
        class_response: Response = self.make_api_request(f"JSSResource/classes/name/{name}", data=data, method=jamf.HTTPMethod.PUT, classic=True)
        if class_response.status_code == 201:
            xml_data = ET.fromstring(class_response.text)
            return xml_data.findtext('id')
        else:
            return None

    def classic_computer_for_id(self, id: int) -> Dict:
        """
        Retrieves the computer with the given ID.

        Args:
            id (int):
                ID of the computer to retrieve

        Returns:
            A dictionary representing the retrieved computer.
        """
        computer_data = self.make_api_request(f"JSSResource/computers/id/{id}")
        return computer_data.json()["computer"]

    def classic_computers(self) -> List:
        """
        Retrieves all computers.

        Returns:
            A list of all computers currently enrolled.
        """
        computer_data = self.make_api_request("JSSResource/computers")
        return computer_data.json()["computers"]

    def classic_mobile_device_for_id(self, id: int) -> Dict:
        """
        Retrieves the mobile device with the given ID.

        Args:
            id (int):
                ID of the mobile device to retrieve

        Returns:
            A dictionary representing the retrieved mobile device.
        """
        device_data = self.make_api_request(f"JSSResource/mobiledevices/id/{id}")
        return device_data.json()["mobile_device"]

    def classic_mobile_devices(self) -> List:
        """
        Retrieves all mobile devices.

        Returns:
            A list of all mobile devices currently enrolled.
        """
        device_data = self.make_api_request("JSSResource/mobiledevices")
        return device_data.json()["mobile_devices"]

    def classic_search_mobile_devices_for(self, search_term: str) -> List:
        """
        Search for mobile devices that match the provided term.

        Args:
            search_term (str):
                Name, mac address, etc. to filter the search by

        Returns:
            A list of the found mobile devices.
        """
        device_data = self.make_api_request(f"JSSResource/mobiledevices/match/{search_term}")
        return device_data.json()["mobile_devices"]


class JamfProMixin:
    """
    The JamfProMixin class contains public methods for the
    Jamf Pro API. More information about the Jamf Pro API
    can be found on Jamf's documentation site.
    https://developer.jamf.com/jamf-pro/docs/jamf-pro-api-overview
    """

    def pro_computers(self) -> List:
        """
        Retrieves all computers.

        Returns:
            A list of all computers currently enrolled.
        """
        device_data = self.make_api_request("api/v1/computers-inventory")
        return device_data

    def pro_mobile_device_for_id(self, id: int, with_details: bool = False) -> Dict:
        """
        Retrieves the mobile device with the given ID.

        Args:
            id (int):
                ID of the mobile device to retrieve
            with_details (bool, optional):
                If true, full device details are returned

        Returns:
            A dictionary representing the retrieved mobile device.
        """
        endpoint_url = f"api/v2/mobile-devices/{id}"
        if with_details:
            endpoint_url = endpoint_url + "/detail"
        device_data = self.make_api_request(endpoint_url)
        return device_data.json()

    def pro_mobile_devices(self) -> List:
        """
        Retrieves all mobile devices.

        Returns:
            A list of all mobile devices currently enrolled.
        """
        device_data = self.make_api_request("api/v2/mobile-devices")
        return device_data
