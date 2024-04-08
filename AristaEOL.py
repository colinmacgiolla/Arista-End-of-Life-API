#!/usr/bin/python
# Copyright (c) 2024 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,  this list of conditions and the following disclaimer in the documentation 
#   and/or other materials provided with the distribution.
# * Neither the name of the Arista nor the names of its contributors may be used to endorse or promote products derived from this software without 
#   specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.

import base64
import sys
from urllib.error import HTTPError
import logging
import json
import requests

log = logging.getLogger(__name__)


class AristaEOL():
    """A class to interact with Arista End-of-Life (EOL) API.

    This class provides methods to authenticate with the Arista EOL API and
    check hardware or software End-of-Life status.
    """
    def __init__(self, token) -> None:
        self.user_token = token
        self._encode_token()
        self._authenticate()

    def _encode_token(self) -> None:
        """
        Encodes the user token using base64.

        Sets the encoded_token attribute with the base64 encoded version
        of the user token.
        """
        self.encoded_token = base64.encodebytes(self.user_token.encode('ascii'))
        log.debug("Encoded token: %s", self.encoded_token)  # Use debug for token details

    def _authenticate(self):
        """
        Authenticates with the Arista EOL API.

        Establishes a session with the Arista EOL API using the provided token.
        Raises an exception on authentication failure.

        Sets the cookie attribute with the session code obtained from the response.
        """
        url = 'https://www.arista.com/api/sessionCode/'
        headers = {}
        headers['content-type'] = 'application/json'
        data = {}
        data['accessToken'] = self.encoded_token.decode("utf-8")
        try:
            r = requests.post(url, json=data, headers=headers)
            r.raise_for_status()
        except HTTPError as http_err:
            log.error("HTTP Error occurred: %s", http_err)
            sys.exit(1)
        except Exception as err:
            log.error("Error getting session token: %s", err)
            sys.exit(1)

        log.info("Successfully authenticated")
        raw_resp = r.text
        resp = json.loads(raw_resp)
        self.cookie = resp['data']['session_code']

    def hardware_check(self, sku: str) -> dict:
        """
        Checks the End-of-Life status of a hardware SKU.

        Queries the Arista EOL API for the End-of-Life details of the provided hardware SKU.
        This needs to be the full SKU e.g. DCS-7150S-52-CL-R

        Args:
            sku (str): The hardware SKU to check.

        Returns:
            dict: A dictionary containing the hardware EOL information.
        """
        url = 'https://www.arista.com/api/eox/hwLifecycle/'
        headers = {}
        headers['content-type'] = 'application/json'
        data = {}
        data['sessionCode'] = self.cookie
        data['mainSku'] = sku

        try:
            r = requests.post(url, json=data, headers=headers)
            r.raise_for_status()
        except HTTPError as http_err:
            log.error("HTTP Error occurred: %s", http_err)
            sys.exit(1)
        except Exception as err:
            log.error("Error downloading Alertbase: %s", err)
            sys.exit(1)

        raw_resp = r.text
        resp = json.loads(raw_resp)

        return resp['data']

    def software_check(self, releaseTrain: str) -> None:
        """
        Checks the End-of-Life status of a software release train.

        Args:
            releaseTrain (str): The software release train to check e.g. 4.28

        Returns:
            dict: A dictionary containing the software EOL information.
        """
        url = 'https://www.arista.com/api/eox/swLifecycle/'
        headers = {}
        headers['content-type'] = 'application/json'
        data = {}
        data['sessionCode'] = self.cookie
        data['releaseTrain'] = releaseTrain

        try:
            r = requests.post(url, json=data, headers=headers)
            r.raise_for_status()
        except HTTPError as http_err:
            log.error("HTTP Error occurred: %s", http_err)
            sys.exit(1)
        except Exception as err:
            log.error("Error downloading Alertbase: %s", err)
            sys.exit(1)

        raw_resp = r.text
        resp = json.loads(raw_resp)

        return resp['data']
