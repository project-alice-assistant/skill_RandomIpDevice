import sqlite3
from core.device.model.Device import Device
from core.device.model.DeviceAbility import DeviceAbility
from core.device.model.DeviceException import RequiresGuiSettings
from core.device.model.DeviceType import DeviceType
from core.dialog.model.DialogSession import DialogSession
from core.util.model.TelemetryType import TelemetryType
from core.webui.model.DeviceClickReactionAction import DeviceClickReactionAction
from core.webui.model.OnDeviceClickReaction import OnDeviceClickReaction
from flask import jsonify
from icmplib import ping
from pathlib import Path
from typing import Dict, Union


class IpDevice(Device):


	def __init__(self, data: Union[sqlite3.Row, Dict]):
		super().__init__(data)
		if self.getConfig('ip'):
			self.pingMe()


	@classmethod
	def getDeviceTypeDefinition(cls) -> dict:
		return {
			'deviceTypeName'        : 'IpDevice',
			'perLocationLimit'      : 0,
			'totalDeviceLimit'      : 0,
			'allowLocationLinks'    : False,
			'allowHeartbeatOverride': False,
			'heartbeatRate'         : 80,
			'abilities'             : []
		}

	def getDeviceIcon(self) -> Path:
		# ping now and decide on icon
		# enhancement: ping periodically and update
		# easy: onFiveMinutes
		# hard: custom setting
		if self.getConfig('ip'):
			try:
				if self.pingMe():
					return Path(f'{self.Commons.rootDir()}/skills/{self.skillName}/devices/img/IpDevice_connected.png')
				else:
					return Path(f'{self.Commons.rootDir()}/skills/{self.skillName}/devices/img/IpDevice_disconnected.png')
			except:
				pass
		return Path(f'{self.Commons.rootDir()}/skills/{self.skillName}/devices/img/IpDevice.png')


	def onUIClick(self) -> dict:
		"""
		Called whenever a device's icon is clicked on the UI
		:return:
		"""
		if self.getConfig('ip') and not self.paired:
			if self.pingMe():
				self.pairingDone(uid=self.newSecret())

		if not self.getConfig('href'):
			raise RequiresGuiSettings()

		return OnDeviceClickReaction(action=DeviceClickReactionAction.NAVIGATE.value, data=self.getConfig('href')).toDict()


	def pingMe(self):
		before = self.connected
		request = ping(self.getConfig('ip'), privileged=False)
		self.connected = self.getConfig('ip') and request.is_alive
		if before != self.connected:
			self.broadcastUpdated()
		if self.getConfig('storeTelemetry'):
			self.TelemetryManager.storeData(deviceId=self.id, locationId=self.parentLocation, ttype=TelemetryType.LATENCY, value=request.avg_rtt, service=self._skillName)
			self.TelemetryManager.storeData(deviceId=self.id, locationId=self.parentLocation, ttype=TelemetryType.PACKET_LOSS, value=request.packet_loss, service=self._skillName)
		return self.connected
