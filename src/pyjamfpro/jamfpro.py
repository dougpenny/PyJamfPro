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

import base64
import datetime
import logging

from enum import Enum
from typing import Dict, List, Union
from urllib.parse import urljoin

import requests

from dateutil import tz
from dateutil.parser import isoparse
from pyjamfpro.endpoints import ClassicMixin, JamfProMixin


HTTPMethod = Enum(
    "HTTPMethod", ["GET", "POST", "PUT", "DELETE"]
)


class Client(ClassicMixin, JamfProMixin):
    """
    The Client object handles requests to a Jamf Pro server.
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
        headers = {
            "Accept": "application/json",
            "Authorization": self._access_token(),
            "User-Agent": "PyJamfPro/0.1.9"
        }
        self.session = requests.Session()
        self.session.headers = headers

    def _access_token(self) -> Union[str, None]:
        """
        Fetches a valid access token.

        Retrieves a valid access token which is used in all future requests.

        Returns:
            A string to be used as the value of the HTTP Authorization header.
        """
        if hasattr(self, "access_token_response"):
            if self.access_token_response["expiration_datetime"] > datetime.datetime.now(tz.UTC):
                return f"Bearer {self.access_token_response['token']}"
        token_url = self.base_url + "/api/v1/auth/token"
        credentials = base64.b64encode(self.username + b":" + self.password)
        auth_string = f"Basic {str(credentials, encoding='utf8')}"
        headers = {
            "Accept": "application/json",
            "Authorization": auth_string,
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        }
        try:
            response = requests.post(token_url, headers=headers)
            response.raise_for_status()
            json_response = response.json()
            json_response["expiration_datetime"] = isoparse(json_response["expires"])
        except requests.RequestException as e:
            logging.error(f"An error occured making the request: {e}")
            return None
        except Exception as e:
            logging.error(f"An unknown error occured: {e}")
            return None
        self.access_token_response = json_response
        return f"Bearer {json_response['token']}"

    def _access_token_expired(self) -> bool:
        """
        Checks access token expiration.

        Checks to see if an access token exists and, if so, if it has expired.

        Returns:
            True if the token has expired or does not exist.
            False if the token exists and is valid.
        """
        if hasattr(self, "access_token_response"):
            if self.access_token_response["expiration_datetime"] > datetime.datetime.now(tz.UTC):
                return False
            else:
                return True
        else:
            return True

    def make_api_request(self, endpoint: str, method: HTTPMethod = HTTPMethod.GET, data: Union[bytes, str] = b"", classic: bool = False) -> Union[requests.Response, None]:
        """
        Makes an API request to the Jamf Pro server.

        Args:
            endpoint (str):
                Endpoint URL for the requested resource
            method (HTTPMethod, optional):
                HTTP method to use for request
            data (bytes or string, optional):
                Data for body of POST or PUT methods
            classic (bool, optional):
                Boolean for using the Jamf Classic API

        Returns:
            Response object, which contains the Jamf server response
        """
        endpoint_url = urljoin(self.base_url, endpoint)
        if self._access_token_expired():
            self.session.headers["Authorization"] = self._access_token()

        if classic:
            self.session.headers["Content-Type"] = "application/xml"
        else:
            self.session.headers["Content-Type"] = "application/json"

        try:
            if method == HTTPMethod.POST:
                response = self.session.post(endpoint_url, data=data)
                response.raise_for_status()
                return response
            if method == HTTPMethod.PUT:
                response = self.session.put(endpoint_url, data=data)
                response.raise_for_status()
                return response
            if method == HTTPMethod.DELETE:
                response = self.session.delete(endpoint_url)
                response.raise_for_status()
                return response

            response = self.session.get(endpoint_url)
            response.raise_for_status()
            if response.json().get("totalCount"):
                total: int = response.json()["totalCount"]
                data: List = response.json()["results"]
                params: Dict = {}
                params["page"] = 1
                while len(data) < total:
                    next_page = self.session.get(endpoint_url, params=params)
                    data.extend(next_page.json()["results"])
                    params["page"] = params["page"] + 1
                return data
            else:
                return response
        except requests.RequestException as e:
            logging.error(f"An error occured making the request: {e}")
        except Exception as e:
            logging.error(f"An unknown error occured: {e}")
        return None
