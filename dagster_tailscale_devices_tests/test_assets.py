import dagster as dg

from dagster_tailscale_devices import assets, resources


def test_tailscale_devices(requests_mock):
    """Test the tailscale_devices asset."""
    context = dg.build_asset_context()
    tailscale = resources.TailscaleResource(api_key="key", tailnet="tailnet")
    devices = [
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
    requests_mock.get(
        f"https://api.tailscale.com/api/v2/tailnet/{tailscale.tailnet}/devices",
        json={"devices": devices},
    )
    result = assets.tailscale_devices(context=context, tailscale=tailscale)
    assert result == {"devices": devices}
