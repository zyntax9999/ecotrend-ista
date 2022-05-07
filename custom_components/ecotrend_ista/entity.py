"""Entity ecotrend-ista."""
from __future__ import annotations

import logging
import datetime

from typing import Any, Dict, Mapping

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.typing import StateType

from pyecotrend_ista import pyecotrend_ista as ista

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class EcoEntity(SensorEntity, RestoreEntity):
    def __init__(
        self, controller: ista.PyEcotrendIsta, description: SensorEntityDescription, consum: Dict[str, Any], unit: str
    ) -> None:
        self._controller = controller
        self._supportCode = controller.getSupportCode()
        self.entity_description = description
        self._consum = consum
        self._name = "{}".format(self._consum.get("entity_id"))
        self._attr_unique_id = self._name
        self._attr_last_reset = datetime.datetime.now()
        self._unit = unit

    @property
    def name(self) -> str | None:
        """Return the name of the entity."""
        return self._name

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the unit of measurement of this entity, if any."""
        return self._consum.get("unit{}".format(self._unit))

    @property
    def native_value(self) -> StateType:
        """Return the value reported by the sensor."""
        return float(str(self._consum.get("value{}".format(self._unit))).replace(",", "."))

    @property
    def device_info(self) -> DeviceInfo:
        """Return a device description for device registry."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._attr_unique_id)},
            manufacturer="ista",
            name=self._name,
        )

    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        """Return entity specific state attributes.
        Implemented by platform classes. Convention for attribute names
        is lowercase snake_case.
        """
        return {
            "unit": self._consum.get("unit"),
            "value": float(str(self._consum.get("value")).replace(",", ".")),
            "unitkwh": self._consum.get("unitkwh"),
            "valuekwh": float(str(self._consum.get("valuekwh")).replace(",", ".")),
        }