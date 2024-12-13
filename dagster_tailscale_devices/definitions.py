import dagster as dg

from dagster_tailscale_devices import assets, resources  # noqa: TID252

all_assets = dg.load_assets_from_modules([assets])


tailscale_schedule = dg.ScheduleDefinition(
    name="tailscale_schedule",
    target=dg.AssetSelection.groups("tailscale_assets"),
    cron_schedule="*/15 * * * *",
    default_status=dg.DefaultScheduleStatus.RUNNING,
)


defs = dg.Definitions(
    assets=all_assets,
    resources={
        "db": resources.PostgresResource(database_url=dg.EnvVar("DATABASE_URL")),
        "tailscale": resources.TailscaleResource(
            api_key=dg.EnvVar("TAILSCALE_API_KEY"),
            tailnet=dg.EnvVar("TAILSCALE_TAILNET"),
        ),
    },
    schedules=[tailscale_schedule],
)
