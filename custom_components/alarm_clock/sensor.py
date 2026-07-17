from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

import logging

from .constants import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        StateSensor(coordinator),
        NextAlarmSensor(coordinator)
    ])
    return True


class StateSensor(CoordinatorEntity, SensorEntity):
    """Representation of the alarm state sensor."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.data['id']}_state"
        self._attr_name = f"{coordinator.data['name']} State"
        self._attr_device_class = None
        self._attr_icon = "mdi:alarm"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data["state"]

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        state = self.coordinator.data["state"]
        if state == "off":
            return "mdi:alarm-off"
        elif state == "on":
            return "mdi:alarm-check"
        return "mdi:alarm"


class NextAlarmSensor(CoordinatorEntity, SensorEntity):
    """Representation of the next alarm sensor."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.data['id']}_next"
        self._attr_name = f"{coordinator.data['name']} Next Alarm"
        self._attr_device_class = "timestamp"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.is_enabled:
            return self.coordinator.data["next"]
        return None

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if self.coordinator.is_enabled:
            return {"minutes": self.coordinator.data["minutes"]}
        return None
