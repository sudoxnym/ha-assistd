"""assistd - exposes assist-exposed entities via REST."""
from __future__ import annotations

import logging
from typing import Any

from aiohttp import web
from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "assistd"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up assistd."""
    hass.http.register_view(AssistdView(hass))
    _LOGGER.info("assistd registered at /api/assistd")
    return True


class AssistdView(HomeAssistantView):
    """View to return entities exposed to Assist."""

    url = "/api/assistd"
    name = "api:assistd"
    requires_auth = True

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the view."""
        self._hass = hass

    async def get(self, request: web.Request) -> web.Response:
        """Return list of entities exposed to Assist/conversation."""
        registry = er.async_get(self._hass)
        exposed = []

        for entity_id, entry in registry.entities.items():
            # check if exposed to conversation/assist
            options = entry.options or {}
            conversation_opts = options.get("conversation", {})

            if conversation_opts.get("should_expose"):
                # get current state
                state = self._hass.states.get(entity_id)
                state_val = state.state if state else "unknown"
                attrs = state.attributes if state else {}

                exposed.append({
                    "entity_id": entity_id,
                    "name": entry.name or entry.original_name or attrs.get("friendly_name", entity_id),
                    "aliases": list(entry.aliases) if entry.aliases else [],
                    "domain": entry.domain,
                    "platform": entry.platform,
                    "state": state_val,
                    "area_id": entry.area_id,
                })

        return self.json({
            "count": len(exposed),
            "entities": exposed
        })
