import dagster as dg

from dagster_tailscale_devices import assets, resources  # noqa: TID252

all_assets = dg.load_assets_from_modules([assets])


defs = dg.Definitions(
    assets=all_assets,
    resources={
        "db": resources.PostgresResource(database_url=dg.EnvVar("DATABASE_URL")),
        "tailscale": resources.TailscaleResource(
            api_key=dg.EnvVar("TAILSCALE_API_KEY"),
            tailnet=dg.EnvVar("TAILSCALE_TAILNET"),
        ),
    },
)
