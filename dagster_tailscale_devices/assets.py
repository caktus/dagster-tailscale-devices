import datetime as dt
import io

import dagster as dg
import pandas as pd
import sqlalchemy.types as types

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


@dg.asset(description="A table of Tailscale devices over time")
def tailscale_device_table(
    context: dg.AssetExecutionContext,
    db: resources.PostgresResource,
    tailscale_devices: dict,
) -> pd.DataFrame:
    df = pd.DataFrame(tailscale_devices["devices"])
    # Convert camelCase column names from API to snake_case for PostgreSQL
    df.columns = df.columns.str.replace(
        "(?<=[a-z])(?=[A-Z])", "_", regex=True
    ).str.lower()
    # Convert columns to appropriate data types
    df["synced_at"] = dt.datetime.now(tz=dt.UTC)
    df["created"] = pd.to_datetime(df["created"], utc=True)
    df["expires"] = pd.to_datetime(df["expires"], utc=True, errors="coerce")
    df["last_seen"] = pd.to_datetime(df["last_seen"], utc=True)
    # Add DataFrame info to the context
    buffer = io.StringIO()
    df.info(buf=buffer)
    df_info = str(buffer.getvalue())
    context.add_output_metadata(
        {
            "df_info": df_info,
            "df_preview": dg.MetadataValue.md(df.head().to_markdown()),
        }
    )
    # context.pdb.set_trace()
    df.to_sql(
        name="tailscale_devices",
        con=db.engine(),
        if_exists="append",
        index=False,
        dtype={
            "addresses": types.ARRAY(types.TEXT),
            "tags": types.ARRAY(types.TEXT),
        },
    )
    return df
