import dagster as dg

from dagster_tailscale_devices import assets  # noqa: TID252

all_assets = dg.load_assets_from_modules([assets])


defs = dg.Definitions(assets=all_assets)
