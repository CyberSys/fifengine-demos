# -*- coding: utf-8 -*-

# ####################################################################
#  Copyright (C) 2005-2017 by the FIFE team
#  http://www.fifengine.net
#  This file is part of FIFE.
#
#  FIFE is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the
#  Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
# ####################################################################

from fife import fife

class JoystickListener(fife.IJoystickListener):
	def __init__(self, world):
		self.world = world
		self.eventmanager = world._engine.getEventManager()
		fife.IJoystickListener.__init__(self)
		self.eventmanager.addJoystickListener(self)

	def axisMotion(self, evt):
                axisX = 0
                axisY = 1
                if evt.isController:
                        axisX = fife.Joystick.CONTOLLER_AXIS_LEFTX
                        axisY = fife.Joystick.CONTOLLER_AXIS_LEFTY
		if evt.getAxis() == axisX:
			if evt.getAxisValue() < 0:
				self.world._keystate['LEFT'] = True
			elif evt.getAxisValue() > 0:
				self.world._keystate['RIGHT'] = True
			else:
				self.world._keystate['LEFT'] = False
				self.world._keystate['RIGHT'] = False
		elif evt.getAxis() == axisY:
			if evt.getAxisValue() < 0:
				self.world._keystate['UP'] = True
			elif evt.getAxisValue() > 0:
				self.world._keystate['DOWN'] = True
			else:
				self.world._keystate['UP'] = False
				self.world._keystate['DOWN'] = False

	def hatMotion(self, evt):
		pass

	def buttonPressed(self, evt):
                button = 0
		if evt.isController(): button = fife.Joystick.CONTOLLER_BUTTON_A
		if evt.getButton() == button:
			self.world._keystate['SPACE'] = True

	def buttonReleased(self, evt):
                button = 0
		if evt.isController(): button = fife.Joystick.CONTOLLER_BUTTON_A
		if evt.getButton() == button:
			self.world._keystate['SPACE'] = False

	def deviceAdded(self, evt):
		pass

	def deviceRemoved(self, evt):
		pass
