# ha-assistd

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=sudoxnym&repository=ha-assistd&category=integration)

home assistant custom component that exposes assist-exposed entities via REST API.

## why

home assistant has no REST endpoint to get entities exposed to assist. this makes it hard to build external tools that respect your expose settings.

assistd fixes that. one endpoint. only the entities you've chosen to expose.

## installation

### manual

1. copy `custom_components/assistd` to your HA config directory
2. add to `configuration.yaml`:
   ```yaml
   assistd:
   ```
3. restart home assistant

### hacs

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=sudoxnym&repository=ha-assistd&category=integration)

or manually: HACS → Integrations → ⋮ → Custom repositories → add `https://github.com/sudoxnym/ha-assistd`

## usage

```bash
curl -s "http://YOUR_HA:8123/api/assistd" \
  -H "Authorization: Bearer YOUR_LONG_LIVED_TOKEN"
```

### response

```json
{
  "count": 4,
  "entities": [
    {
      "entity_id": "light.bedroom",
      "name": "Bedroom Light",
      "aliases": ["bedroom", "bed light"],
      "domain": "light",
      "platform": "hue",
      "state": "on",
      "area_id": "bedroom"
    },
    {
      "entity_id": "switch.fan",
      "name": "Ceiling Fan",
      "aliases": [],
      "domain": "switch",
      "platform": "zha",
      "state": "off",
      "area_id": "living_room"
    }
  ]
}
```

### fields

| field | description |
|-------|-------------|
| `entity_id` | full entity id |
| `name` | friendly name |
| `aliases` | voice aliases configured in HA |
| `domain` | entity domain (light, switch, climate, etc) |
| `platform` | integration that owns this entity |
| `state` | current state |
| `area_id` | area assignment (if any) |

## use cases

- build LLM-powered voice assistants that respect your expose settings
- create external dashboards showing only exposed entities
- sync exposed entities to external systems
- audit what's exposed to assist

## example: natural language control

pair with an LLM to build a CLI controller:

```bash
#!/bin/bash
# get exposed entities, send to LLM with user command, execute result
entities=$(curl -s "http://ha:8123/api/assistd" -H "Authorization: Bearer $TOKEN")
# ... LLM interprets "turn off the lights" → light.turn_off on light.bedroom
```

## license

MIT
