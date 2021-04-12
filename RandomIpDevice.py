from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler


class RandomIpDevice(AliceSkill):
	"""
	Author: philipp2310
	Description: Monitor any device reachable via ip
	"""

	# possible enhancements:
	# - request status via voice (device name must be dynamically injected!)
	pass

	def onFullMinute(self):
		devices = self.DeviceManager.getDevicesBySkill(skillName=self.name)
		for device in devices:
			device.pingMe()
