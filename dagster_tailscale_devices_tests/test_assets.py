import dagster as dg
import pytest

from dagster_tailscale_devices import assets, resources


@pytest.fixture
def devices() -> dict:
    return {
        "devices": [
            {
                "addresses": ["100.100.1.1"],
                "authorized": True,
                "blocksIncomingConnections": False,
                "clientVersion": "1.76.6-t1edcf9d46-gd0a6cd8b2",
                "created": "2024-10-15T13:58:11Z",
                "expires": "2025-04-13T13:58:11Z",
                "hostname": "ip-172-31-45-72",
                "id": "1111",
                "isExternal": False,
                "keyExpiryDisabled": False,
                "lastSeen": "2024-12-13T16:18:48Z",
                "machineKey": "mkey:key",
                "name": "name.tailnet.ts.net",
                "nodeId": "nodeid",
                "nodeKey": "nodekey:key",
                "os": "linux",
                "tags": ["tag:server"],
                "tailnetLockError": "",
                "tailnetLockKey": "nlpub:key",
                "updateAvailable": True,
                "user": "myuser@github",
            }
        ]
    }


def test_tailscale_devices(requests_mock, devices):
    """Test the tailscale_devices asset."""
    context = dg.build_asset_context()
    tailscale = resources.TailscaleResource(api_key="key", tailnet="tailnet")
    requests_mock.get(
        f"https://api.tailscale.com/api/v2/tailnet/{tailscale.tailnet}/devices",
        json=devices,
    )
    result = assets.tailscale_devices(context=context, tailscale=tailscale)
    assert result == devices


def test_tailscale_device_table(mocker, devices):
    """Test the tailscale_device_table asset."""
    context = dg.build_asset_context()
    mocker.patch.object(resources.PostgresResource, "engine")
    db = resources.PostgresResource(database_url="postgresql://localhost/test")
    mocker.patch("pandas.DataFrame.to_sql")
    df = assets.tailscale_device_table(
        context=context, db=db, tailscale_devices=devices
    )
    df.to_sql.assert_called_once()
    assert len(df.index) == 1
    assert df.columns.tolist() == [
        "addresses",
        "authorized",
        "blocks_incoming_connections",
        "client_version",
        "created",
        "expires",
        "hostname",
        "id",
        "is_external",
        "key_expiry_disabled",
        "last_seen",
        "machine_key",
        "name",
        "node_id",
        "node_key",
        "os",
        "tags",
        "tailnet_lock_error",
        "tailnet_lock_key",
        "update_available",
        "user",
        "synced_at",
    ]
