![PyJamfPro](Images/pyjamfpro.png)

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyjamfpro)](https://pypi.org/project/pyjamfpro/)
[![PyPI](https://img.shields.io/pypi/v/pyjamfpro?label=pypi%20package)](https://pypi.org/project/pyjamfpro/)
[![MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)


PyJamfPro is a basic Python wrapper for synchronous communication with the [Jamf Pro (and/or Classic) API](https://developer.jamf.com/jamf-pro/docs). The goal is to simplify the process of communicating with the [Jamf Pro](https://www.jamf.com/products/jamf-pro/) device management server API by handling authentication and decoding, allowing you to focus on using the data, not retrieving it.

_PyJamfPro is not endorsed, sponsored, or affilitated with Jamf in any way._

***

## Usage
Begin by installing the PyJamfPro module, using `pip`.

```shell
pip install pyjamfpro
```

In your code, simply import the PyJamfPro module and instantiate a new client object. The constructor requires three arguments:
1. base_url - the base URL of your Jamf Pro server
2. username
3. password
* _Note_: The Jamf Pro API uses the standard User Accounts and Groups functionality of Jamf Pro. You will need to ensure the account you use has the proper privilages for the actions you would like to perform with the API.

```python
from pyjamfpro import jamfpro

client = jamfpro.Client('https://example.jamfserver.com', 'username', 'password')
```

Once you have a client, you can start making synchronous calls to the API.
```python
# returns list of all mobile devices, using the Classic API
devices = client.classic_mobile_devices()

# returns a dictionary of inventory data for the mobile device with ID 1234,
# using the Classic API
device = client.classic_mobile_device_for_id(1234)

# returns a list of all computers, using the Jamf Pro API
computers = client.pro_computers()
```

Refer to the [`endpoints.py`](./src/pyjamfpro/endpoints.py) file for other built-in methods. Additionally, you can use the [`make_api_request`](./src/pyjamfpro/jamfpro.py#L121) method to access any Jamf API endpoint. Full support for GET, POST, PUT, and DELETE are included.

## Contributing
If you have a feature or idea you would like to see added to PyJamPro, please [create an issue](https://github.com/dougpenny/PyJamPro/issues/new) explaining your idea.

Likewise, if you come across a bug, please [create an issue](https://github.com/dougpenny/PyJamPro/issues/new) explaining the bug with as much detail as possible.

The Jamf Pro API provides access to a lot of information and, unfortunately, we don't have time to research and implement every endpoint. Please feel free to open a pull request with any additional endpoints you create. We would love to have as many of the core endpoints covered as possible.

## License
PyJamPro is released under an MIT license. See [LICENSE](https://opensource.org/licenses/MIT) for more information.
