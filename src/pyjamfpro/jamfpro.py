#
# jamfpro.py
#
# Copyright (c) 2022 Doug Penny
# Licensed under MIT
#
# See LICENSE.md for license information
#
# SPDX-License-Identifier: MIT
#

from dateutil.parser import isoparse
from typing import Dict, List, Union
from urllib.parse import urljoin
from xml.etree import ElementTree
import base64
import datetime
import json
import sys

from dict2xml import dict2xml
import httpx

from pyjamfpro.endpoints import ClassicMixin, JamfProMixin


class Client(ClassicMixin, JamfProMixin):
    """
    The Client object handles GET and POST requests to a Jamf Pro server.
    Requests are made asynchronously when possible.

    Public Methods:
        fetch_data(self, endpoint: str, params: Dict[str, str] = {}) -> Dict
        post_data(self, endpoint: str, post_data: Dict) -> Union[None, int]
    """

    def __init__(self, url: str, username: str, password: str) -> None:
        """
        Initializes a new Client object.

        Args:
            base_url:
                The base URL of the Jamf Pro server
            username:
                Username of the Jamf Pro user to connect as
            password:
                Password of the Jamf Pro user to connect as
        """
        self.base_url = url
        self.username = username.encode("UTF-8")
        self.password = password.encode("UTF-8")
        try:
            self.headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": self._access_token(),
            }
        except httpx.RequestError as e:
            sys.stderr.write(f"An error occured making the request: {e}\n")
        except httpx.HTTPStatusError as e:
            sys.stderr.write(f"Error response {e.response.status_code}\n")
            sys.stderr.write(f"A connection error occured: {e}\n")
        except Exception as e:
            sys.stderr.write(f"An unknown error occured: {e}\n")

    def _access_token(self) -> str:
        """
        Fetches a valid access token.

        Retrieves a valid access token which is used in all future requests.

        Returns:
            A string to be used as the value of the HTTP Authorization header.
        """
        if hasattr(self, "access_token_response"):
            if self.access_token_response["expiration_datetime"] > datetime.datetime.utcnow():
                return f"Bearer {self.access_token_response['token']}"
        token_url = self.base_url + "/api/v1/auth/token"
        credentials = base64.b64encode(self.username + b":" + self.password)
        auth_string = f"Basic {str(credentials, encoding='utf8')}"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Authorization": auth_string,
        }
        r = httpx.post(token_url, headers=headers)
        response = r.json()
        response["expiration_datetime"] = isoparse(response["expires"])
        self.access_token_response = response
        return "Bearer " + response["token"]

    def _access_token_expired(self) -> bool:
        """
        Checkes access token expiration.

        Checkes to see if an access token exists and, if so, if it has expired.

        Returns:
            True if the token has expired or does not exist.
            False if the token exists and is valid.
        """
        if hasattr(self, "access_token_response"):
            if self.access_token_response["expiration_datetime"] > datetime.datetime.utcnow():
                return False
            else:
                return True
        else:
            return True

    async def fetch_data(self, endpoint: str, params: Dict[str, str] = {}) -> Dict:
        """
        Fetches data from the Jamf Pro server.

        Args:
            endpoint (str):
                Endpoint URL for the requested resource
            params (Dict[str, str], optional):
                URL parameters to be included in the request

        Returns:
            A dictionary representing the record retrieved.
        """
        endpoint_url = urljoin(self.base_url, endpoint)
        if self._access_token_expired():
            self.headers["Authorization"] = self._access_token()
        async with httpx.AsyncClient() as async_client:
            return await async_client.get(endpoint_url, headers=self.headers, params=params)

    async def fetch_paginated_data(self, endpoint: str, params: Dict[str, str] = {}) -> List:
        """
        Fetches paginated data from the Jamf Pro server.

        When fetching paginated data we need to do so
        synchronously so we can build up the enitre
        data set.

        Args:
            endpoint (str):
                Endpoint URL for the requested resource
            params (Dict[str, str], optional):
                URL parameters to be included in the request

        Returns:
            A list representing the records retrieved.
        """
        endpoint_url = urljoin(self.base_url, endpoint)
        if self._access_token_expired():
            self.headers["Authorization"] = self._access_token()
        with httpx.Client() as http_client:
            response = http_client.get(endpoint_url, headers=self.headers, params=params)
        if response.json().get("totalCount"):
            total: int = response.json()["totalCount"]
            data: List = response.json()["results"]
            page: int = 1
            while len(data) < total:
                params["page"] = page
                with httpx.Client() as http_client:
                    next_page = http_client.get(endpoint_url, headers=self.headers, params=params)
                data.extend(next_page.json()["results"])
                page = page + 1
            return data
        else:
            return response

    async def post_data(self, endpoint: str, post_data: Dict,
                        classic: bool = False) -> Union[None, int]:
        """
        Creates a new entry for the given endpoint using the
        Classic of Jamf Pro API. The Classic API requires that
        an XML body be passed with the request, while the
        Jamf Pro API requires that a JSON body be passed with
        the request.

        Args:
            endpoint (str):
                Endpoint URL for the new entry
            post_data (dict):
                Dictionay of values used for creating the new entry
            classic (bool, optional):
                Designates if this is a Classic API endpoint

        Returns:
            If creation is successful, the ID of the new entry,
            otherwise, None.
        """
        if self._access_token_expired():
            self.headers["Authorization"] = self._access_token()
        post_url = urljoin(self.base_url, endpoint)
        if classic:
            data = dict2xml(post_data, newlines=False)
        else:
            data = json.dumps(post_data)
        try:
            async with httpx.AsyncClient() as async_client:
                response = await async_client.post(post_url, data=data, headers=self.headers)
            response.raise_for_status()
            if classic:
                created_resource = ElementTree.fromstring(response.text)
                return created_resource.find('id').text
            else:
                return response.json()['id']
        except Exception as e:
            sys.stderr.write(f"An error occured attempting to post data: {e}\n")
            return None
