# AristaEOL Python Class

This Python class provides a way to interact with the Arista End-of-Life (EOL) API. It allows you to:
* Authenticate with the Arista EOL API using your access token.
* Check the End-of-Life (EOL) status of Arista hardware by SKU.
* Check the End-of-Life (EOL) status of Arista software release trains.

## Installation

You can install the required libraries using the pip command:
```bash
pip install -r requirements.txt
```

## Usage

Here's a basic example of how to use the AristaEOL class:
```python

from AristaEOL import AristaEOL

# Replace with your Arista API access token
access_token = "YOUR_ACCESS_TOKEN"

# Create an AristaEOL object
clnt = AristaEOL(access_token)

# Check hardware EOL status for a specific SKU
sku = "DCS-7150S-52-CL-F"
hardware_eol_info = clnt.hardware_check(sku)
print(hardware_eol_info)

# Check software EOL status for a release train
release_train = "4.23"
software_eol_info = clnt.software_check(release_train)
print(software_eol_info)
```

Note: Replace YOUR_ACCESS_TOKEN with your actual Arista API access token.

## API Documentation

Here's a detailed explanation of the class methods:

    __init__(self, token: str) -> None
        Initializes the AristaEOL object.
        Takes the Arista API access token as a string argument.
        Internally calls _encode_token and _authenticate methods.

    _encode_token(self) -> None
        Encodes the user token using base64.
        Sets the encoded_token attribute with the base64 encoded version of the user token.

    _authenticate(self) -> None
        Authenticates with the Arista EOL API.
        Establishes a session with the API using the provided token.
        Raises an exception on authentication failure.
        Sets the cookie attribute with the session code obtained from the response.

    hardware_check(self, sku: str) -> dict
        Checks the End-of-Life status of a hardware SKU.
        Takes the hardware SKU as a string argument.
        Returns a dictionary containing the hardware EOL information.

    software_check(self, releaseTrain: str) -> dict
        Checks the End-of-Life status of a software release train.
        Takes the software release train as a string argument.
        Returns a dictionary containing the software EOL information.
