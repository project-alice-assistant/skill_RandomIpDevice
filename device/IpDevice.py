from flask import jsonify
import subprocess
from core.device.model.Device import Device
from core.device.model.DeviceType import DeviceType
from core.device.model.DeviceException import RequiresGuiSettings
from core.dialog.model.DialogSession import DialogSession
import sqlite3

class IpDevice(DeviceType):

	DEV_SETTINGS = { 'ip': '',
					 'name': '',
	                 'href': '' }

	def __init__(self, data: sqlite3.Row):
		super().__init__(data, devSettings=self.DEV_SETTINGS, heartbeatRate=0)


	def discover(self, device: Device, uid: str, replyOnSiteId: str = "", session:DialogSession = None) -> bool:
		if not 'ip' in device.devSettings or not device.devSettings['ip']:
			raise RequiresGuiSettings()
		pong = subprocess.call(['ping', '-c', '1', device.devSettings['ip']]) == 0
		if pong:
			device.pairingDone(uid=uid)


	def getDeviceIcon(self, device: Device) -> str:
		try:
			if subprocess.call(['ping', '-c', '1', device.devSettings['ip']]) == 0:
				return 'IpDevice_connected.png'
			else:
				return 'IpDevice_disconnected.png'
		except:
			pass
		# ping now and decide on icon
		return 'IpDevice.png'


	def toggle(self, device: Device):
		if not 'href' in device.devSettings or not device.devSettings['href']:
			raise RequiresGuiSettings()
		return jsonify(href=device.devSettings['href'])
