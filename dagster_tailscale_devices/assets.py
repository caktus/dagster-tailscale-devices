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
    context.add_output_metadata({"devices_preview": devices["devices"][:5]})
    return devices
