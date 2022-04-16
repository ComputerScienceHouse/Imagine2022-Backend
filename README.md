# Imagine2022-Backend

Imagine, nay, CONSIDER RIT

## Endpoints

`GET https://imagine-2022-backend-git-imagine2022-backend.apps.okd4.csh.rit.edu/beacons/locations` - Gets beacon locations most recently

```json
{
  "beacon id": {
    "position": [x, y], // Normalized position in meters
    "absolute_position": [lat, lon], // GPS position of beacon
    "esps": {
      "esp id": {
        "timestamp": float unix time,
        "rssi": float value rssi,
        "esp_position": [lat, lon],
        "esp_position_normal": [x, y], // Normalized position in meters
        "distance": float distance in meters
      }, ...
    }
  }, ...
}
```

`GET https://imagine-2022-backend-git-imagine2022-backend.apps.okd4.csh.rit.edu/config/zero` - Gets lat/lon of (0, 0) on campus. Returns list of `[lat, lon]`

`POST https://imagine-2022-backend-git-imagine2022-backend.apps.okd4.csh.rit.edu/esp?id=<mac_address>&lat=<latitude>&lon=<longitude>` - Adds a new sniffer with mac address `id` at `(lat, lon)`.

`POST https://imagine-2022-backend-git-imagine2022-backend.apps.okd4.csh.rit.edu/remove/esp?id=<mac_address>` - Removes sniffer with mac address `id`.
