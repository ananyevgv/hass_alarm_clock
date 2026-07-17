from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

import logging

from .constants import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the switch platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ActiveSwitch(coordinator)])
    return True


class ActiveSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of the alarm active switch."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.data['id']}_active"
        self._attr_name = f"{coordinator.data['name']} Active"
        self._attr_entity_category = EntityCategory.CONFIG
        self._attr_icon = "mdi:alarm"

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self.coordinator.is_enabled

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:alarm" if self.is_on else "mdi:alarm-off"

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        await self.coordinator.set_enabled(True)

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        await self.coordinator.set_enabled(False)
