This is a blog post about Dagster.


Creating a new Dagster project
------------------------------

We'll start with a scaffold project by following the official `Creating a new
Dagster project`_ instructions in the Dagster documentation.

.. code-block:: shell

    pip install dagster
    dagster project scaffold --name dagster-tailscale-devices

Install the required dependencies:

.. code-block:: shell

    cd dagster-tailscale-devices
    pip install -e ".[dev]"

Start the development environment:

.. code-block:: shell

    dagster dev

You now have a new Dagster project ready to go.


Create a Tailscale API access token
-----------------------------------

To access the Tailscale API, you'll need to create an access token. You can do
this by visiting the `Tailscale admin console`_ and creating a new API key.

Export the access token and your tailnet as environment variables:

.. code-block:: shell

    export TAILSCALE_API_KEY="your-api-key"
    export TAILSCALE_TAILNET="your-tailnet"


Create the Dagster asset
-------------------------

Next we'll create a new Dagster asset that fetches the list of devices from the
Tailscale API:

.. code-block:: python

    import os
    import requests

    import dagster as dg


    @dg.asset
    def tailscale_devices(context: dg.AssetExecutionContext) -> dict:
        headers = {
            "Authorization": f"Bearer {os.getenv('TAILSCALE_API_KEY')}",
        }
        tailnet = os.getenv("TAILSCALE_TAILNET")
        url = f"https://api.tailscale.com/api/v2/tailnet/{tailnet}/devices"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        devices = response.json()
        context.log.info(f"Downloaded {len(devices['devices'])} devices from Tailscale")
        context.add_output_metadata({"devices_preview": devices["devices"][:2]})
        return devices


This asset fetches the list of devices from the Tailscale API and logs the
number of devices downloaded. It also adds a preview of the devices to the
asset metadata, which can be viewed in the Dagster asset run details.

Now visit http://localhost:3000/assets/tailscale_devices and click the Materialize
button to fetch the devices. You should see the number of devices downloaded and
a preview of the first two devices.


.. _Creating a new Dagster project: https://docs.dagster.io/getting-started/create-new-project
