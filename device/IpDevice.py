import sqlite3
import subprocess
from core.device.model.Device import Device
from core.device.model.DeviceException import RequiresGuiSettings
from core.device.model.DeviceType import DeviceType
from core.dialog.model.DialogSession import DialogSession
from flask import jsonify


class IpDevice(DeviceType):
	DEV_SETTINGS = {
		'name': '',
		'ip'  : '',
		'href': ''
	}


	def __init__(self, data: sqlite3.Row):
		super().__init__(data, devSettings=self.DEV_SETTINGS, heartbeatRate=0, allowLocationLinks=False)


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
				return 'IpDevice_connected.png'
			else:
				return 'IpDevice_disconnected.png'
		except:
			pass
		return 'IpDevice.png'


	def toggle(self, device: Device):
		if not 'href' in device.devSettings or not device.devSettings['href']:
			raise RequiresGuiSettings()
		return jsonify(href=device.devSettings['href'])
