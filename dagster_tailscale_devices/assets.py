import datetime as dt

import dagster as dg
import pandas as pd

from dagster_tailscale_devices import resources


@dg.asset(description="A list of tailnet devices from Tailscale")
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


@dg.asset(description="A table of tailnet devices from Tailscale")
def tailscale_device_table(
    context: dg.AssetExecutionContext, tailscale_devices: dict
) -> pd.DataFrame:
    df = pd.DataFrame(tailscale_devices["devices"])
    df["synced_at"] = dt.datetime.now(tz=dt.UTC)
    # Convert camelCase column names from API to snake_case for PostgreSQL
    df.columns = df.columns.str.replace(
        "(?<=[a-z])(?=[A-Z])", "_", regex=True
    ).str.lower()
    context.add_output_metadata({"df": dg.MetadataValue.md(df.head().to_markdown())})
    return df
