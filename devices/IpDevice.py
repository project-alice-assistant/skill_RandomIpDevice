import sqlite3
import subprocess
from core.device.model.Device import Device
from core.device.model.DeviceException import RequiresGuiSettings
from core.device.model.DeviceType import DeviceType
from core.dialog.model.DialogSession import DialogSession
from core.device.model.DeviceAbility import DeviceAbility
from flask import jsonify


class IpDevice(Device):

	@classmethod
	def getDeviceTypeDefinition(cls) -> dict:
		return {
			'deviceTypeName'        : 'RandomIpDevice',
			'perLocationLimit'      : 0,
			'totalDeviceLimit'      : 0,
			'allowLocationLinks'    : False,
			'allowHeartbeatOverride': False,
			'heartbeatRate'         : 0,
			'deviceSettings'        : { 'ip'  : '',
			                            'href': '' },
			'abilities'             : [DeviceAbility.PLAY_SOUND, DeviceAbility.CAPTURE_SOUND]
		}


	def discover(self, device: Device, uid: str, replyOnSiteId: str = "", session: DialogSession = None) -> bool:
		if not 'ip' in device.devSettings or not device.devSettings['ip']:
			raise RequiresGuiSettings()
		pong = subprocess.call(['ping', '-c', '1', device.devSettings['ip']]) == 0
		if pong:
			device.pairingDone(uid=uid)


	def getDeviceIcon(self, device: Device) -> str:
		# ping now and decide on icon
		# enhancement: ping periodically and update
		# easy: onFiveMinutes
		# hard: custom setting
		try:
			if subprocess.call(['ping', '-c', '1', device.devSettings['ip']]) == 0:
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
		if not 'href' in device.devSettings or not device.devSettings['href']:
			raise RequiresGuiSettings()

		return OnDeviceClickReaction(action=DeviceClickReactionAction.NAVIGATE.value, data=device.devSettings['href']).toDict()