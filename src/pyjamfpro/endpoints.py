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

from typing import List, Dict


class ClassicMixin:
    """
    The ClassicMixin class contains public methods for the
    Jamf Classic API. More information about the Classic API
    can be found on Jamf's documentation site.
    https://developer.jamf.com/jamf-pro/docs/getting-started-2
    """

    async def classic_computer_for_id(self, device_id: int) -> Dict:
        """
        Retrieves the computer with the given ID.

        Args:
            device_id (int): ID value for desired computer

        Returns:
            A dictionary representing the retrieved computer.
        """
        computer_data = await self.fetch_data(f"JSSResource/computers/id/{device_id}")
        return computer_data.json()["computer"]

    async def classic_computers(self) -> List:
        """
        Retrieves all computers.

        Returns:
            A list of all computers currently enrolled.
        """
        computer_data = await self.fetch_data("JSSResource/computers")
        return computer_data.json()["computers"]

    async def classic_mobile_device_for_id(self, device_id: int) -> Dict:
        """
        Retrieves the mobile device with the given ID.

        Args:
            device_id (int): ID value for desired mobile device

        Returns:
            A dictionary representing the retrieved mobile device.
        """
        device_data = await self.fetch_data(f"JSSResource/mobiledevices/id/{device_id}")
        return device_data.json()["mobile_device"]

    async def classic_mobile_devices(self) -> List:
        """
        Retrieves all mobile devices.

        Returns:
            A list of all mobile devices currently enrolled.
        """
        device_data = await self.fetch_data("JSSResource/mobiledevices")
        return device_data.json()["mobile_devices"]

    async def classic_search_mobile_devices_for(self, search_term: str) -> List:
        """
        Search for mobile devices that match the provided term.

        Args:
            search_term (str): Name, mac address, etc. to filter the search by

        Returns:
            A list of the found mobile devices.
        """
        device_data = await self.fetch_data(f"JSSResource/mobiledevices/match/{search_term}")
        return device_data.json()["mobile_devices"]


class JamfProMixin:
    """
    The JamfProMixin class contains public methods for the
    Jamf Pro API. More information about the Jamf Pro API
    can be found on Jamf's documentation site.
    https://developer.jamf.com/jamf-pro/docs/jamf-pro-api-overview
    """

    async def pro_computers(self) -> List:
        """
        Retrieves all computers.

        Returns:
            A list of all computers currently enrolled.
        """
        device_data = await self.fetch_paginated_data("api/v1/computers-inventory")
        return device_data

    async def pro_mobile_device_for_id(self, device_id: int, with_details: bool = False) -> Dict:
        """
        Retrieves the mobile device with the given ID.

        Args:
            device_dcid (int): ID value for desired mobile device
            with_details (bool, optional): If true, full device details are returned

        Returns:
            A dictionary representing the retrieved mobile device.
        """
        endpoint_url = f"api/v2/mobile-devices/{device_id}"
        if with_details:
            endpoint_url = endpoint_url + "/detail"
        device_data = await self.fetch_data(endpoint_url)
        return device_data.json()

    async def pro_mobile_devices(self) -> List:
        """
        Retrieves all mobile devices.

        Returns:
            A list of all mobile devices currently enrolled.
        """
        device_data = await self.fetch_paginated_data("api/v2/mobile-devices")
        return device_data
