from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

import logging
from datetime import datetime  # ← Добавляем импорт!

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
        self._attr_unique_id = f"{coordinator.entry.entry_id}_state"
        self._attr_name = f"{coordinator.entry.title} State"
        self._attr_icon = "mdi:alarm"
        self._attr_should_poll = False

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return "off"
        return self.coordinator.data.get("state", "off")

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        state = self.native_value
        if state == "off":
            return "mdi:alarm-off"
        elif state == "on":
            return "mdi:alarm-check"
        return "mdi:alarm"

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.data is not None


class NextAlarmSensor(CoordinatorEntity, SensorEntity):
    """Representation of the next alarm sensor."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_next"
        self._attr_name = f"{coordinator.entry.title} Next Alarm"
        self._attr_device_class = "timestamp"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_should_poll = False

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        if not self.coordinator.is_enabled:
            return None
        
        next_alarm = self.coordinator.data.get("next")
        # Если next_alarm уже datetime объект - возвращаем его
        if isinstance(next_alarm, datetime):
            return next_alarm
        # Если это строка - парсим
        if isinstance(next_alarm, str):
            try:
                return dt_util.parse_datetime(next_alarm)
            except (ValueError, TypeError):
                return None
        return None

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if self.coordinator.data is None:
            return None
        if not self.coordinator.is_enabled:
            return None
        minutes = self.coordinator.data.get("minutes")
        if minutes is not None:
            return {"minutes": minutes}
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.data is not None