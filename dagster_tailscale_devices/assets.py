import dagster as dg

from dagster_tailscale_devices import resources


@dg.asset
def tailscale_devices(
    context: dg.AssetExecutionContext, tailscale: resources.TailscaleResource
) -> dict:
    """
    Download a list of tailnet devices from Tailscale.
    https://tailscale.com/api#tag/devices/GET/tailnet/{tailnet}/devices
    """
    devices = tailscale.get(path=f"tailnet/{tailscale.tailnet}/devices")
    context.log.info(f"Downloaded {len(devices['devices'])} devices from Tailscale")
    context.add_output_metadata({"devices_preview": devices["devices"][:2]})
    return devices
