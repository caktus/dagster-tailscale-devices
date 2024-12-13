from urllib.parse import urljoin

import dagster as dg
import requests
import sqlalchemy


class TailscaleResource(dg.ConfigurableResource):
    """A Dagster resource for interacting with the Tailscale API."""

    api_key: str
    base_url: str = "https://api.tailscale.com/api/v2/"
    tailnet: str

    def client(self) -> requests.Session:
        """Return a requests session configured with the Tailscale API key."""
        session = requests.Session()
        session.headers["Authorization"] = f"Bearer {self.api_key}"
        return session

    def url(self, path: str) -> str:
        """Return a full URL for the Tailscale API."""
        return urljoin(self.base_url, path.lstrip("/"))

    def get(self, path: str, *args, **kwargs) -> requests.Response:
        """Make a GET request to the Tailscale API."""
        response = self.client().get(url=self.url(path), *args, **kwargs)
        response.raise_for_status()
        return response.json()


class PostgresResource(dg.ConfigurableResource):
    """A resource that configures a SQLAlchemy engine."""

    database_url: str

    def engine(self) -> sqlalchemy.Engine:
        """Return a SQLAlchemy engine connected to the configured PostgreSQL database."""
        return sqlalchemy.create_engine(url=self.database_url)
