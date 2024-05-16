# finchdemo

This repo is for demonstration of the Finch Sandbox API (https://sandbox.tryfinch.com/)

This demo utilizes Python and Flask. `requirements.txt` summarizes the required Python packages for this to run.

## Basic Overview

`main.py` is the primary Python file. The demo runs at the following address: `http://127.0.0.1:5000`

The necessary `HTML` files are stored in /templates

Download this repo and from the directory in the termainal run `FLASK_APP=main.py flask run`

The home page is a list of the included providers in the Finch sandbox. Copy and paste a provider name into the form. The Python script is hard-coded to create a new sandbox with the following products: `["company", "directory", "individual", "employment"]`

The script then redirects to display the company information. If the provider has not used any of the above products, then the script responds with the error message: _Provider has not implemented the requested products. Go back and select a different provider_

From the company page, a user can click on the link to go to the directory.

From the directory, a user can copy an employee ID to display the information from the `employment` endpoint or the `individual` endpoint
