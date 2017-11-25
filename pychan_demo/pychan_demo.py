#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ####################################################################
#  Copyright (C) 2005-2013 by the FIFE team
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

# This is the pychan demo client for FIFE.

from __future__ import print_function
from builtins import str
from builtins import object
import sys, os, re

fife_path = os.path.join('..','..','engine','python')
if os.path.isdir(fife_path) and fife_path not in sys.path:
	sys.path.insert(0,fife_path)

from fife import fife
print("Using the FIFE python module found here: ", os.path.dirname(fife.__file__))

from fife.extensions import fifelog
from fife.extensions import pychan
from fife.extensions.pychan import pychanbasicapplication
from fife.extensions.pychan.dialogs import trace

class PyChanExample(object):
	"""
	Example class.
	"""
	def __init__(self, xmlFile, application=None):
		self.application = application
		self.xmlFile = xmlFile
		self.widget = None

	def start(self):
		"""
		The Example Protocoll: start
		"""
		# For simplicity the most basic examples should define
		# a okButton and/or a closeButton. Those are mapped
		# to the stop handler.
		self.widget = pychan.loadXML(self.xmlFile)
		eventMap = {
			'closeButton':self.stop,
			'okButton'   :self.stop
		}
		# Since the basic example are not required to
		# supply close and ok button, we 'ignoreMissing'
		self.widget.mapEvents(eventMap, ignoreMissing = True)
		self.widget.show()

		#from pprint import pprint
		#pprint(self.widget.getNamedChildren())

	def stop(self):
		"""
		The Example Protocoll: stop
		"""
		if self.widget:
			self.widget.hide()
		self.widget = None
		if self.application:
			self.application.demoList.requestFocus()

class TextSetter(object):
	def __init__(self,text):
		self.text = text
	def __call__(self,widget):
		widget.text = self.text

class KeyFilter(fife.IKeyFilter):
	"""
	This is the implementation of the fife.IKeyFilter class.
	
	Prevents any filtered keys from being consumed by fifechan.
	"""
	def __init__(self, keys):
		fife.IKeyFilter.__init__(self)
		self._keys = keys

	def isFiltered(self, event):
		return event.getKey().getValue() in self._keys

class ApplicationListener(fife.IKeyListener, fife.ICommandListener):
	"""
	Listens for window commands.
	"""
	def __init__(self, engine):
		"""
		Initializes listener and registers itself with the eventmanager.
		"""
		self._engine = engine
		self._eventmanager = self._engine.getEventManager()
		
		fife.IKeyListener.__init__(self)
		self._eventmanager.addKeyListener(self)
		
		fife.ICommandListener.__init__(self)
		self._eventmanager.addCommandListener(self)
		
		keyfilter = KeyFilter([fife.Key.ESCAPE])
		keyfilter.__disown__()		
		
		self._eventmanager.setKeyFilter(keyfilter)		
		
		self.quit = False

	def keyPressed(self, event):
		"""
		Processes any non game related keyboard input.
		"""
		if event.isConsumed():
			return

		keyval = event.getKey().getValue()
		keystr = event.getKey().getAsString().lower()
		
		if keyval == fife.Key.ESCAPE:
			self.quit = True
			event.consume()

	def keyReleased(self, event):
		pass

	def onCommand(self, command):
		if command.getCommandType() == fife.CMD_QUIT_GAME:
			self.quit = True
			command.consume()

class DemoApplication(pychanbasicapplication.PychanApplicationBase):
	def __init__(self):
		# Let the ApplicationBase initialise FIFE
		super(DemoApplication,self).__init__()

		# Init Pychan
		pychan.loadFonts("fonts/freefont.xml")
		pychan.manager.setDefaultFont("FreeSans")
		pychan.setupModalExecution(self.mainLoop,self.breakFromMainLoop)

		# Build the main GUI
		self.gui = pychan.loadXML('gui/demoapp.xml')
		self.gui.min_size = self.engine.getRenderBackend().getScreenWidth(),self.engine.getRenderBackend().getScreenHeight()

		eventMap = {
			'creditsLink'  : self.showCredits,
			'closeButton'  : self.quit,
			'demoList' : self.selectExample,
			'xmlButton' : self.loadRuntimeXML,
		}
		self.gui.mapEvents(eventMap)

		# A simple hover-effect for the credits label
		credits = self.gui.findChild(name="creditsLink")
		# Note that we can't simply write:
		# credits.capture(credits._setText(u"Credits"), event_name="mouseExited")
		# that's because that would call credits._setText _NOW_ and we want to call
		# it later.
		credits.capture(lambda : credits._setText(u"CREDITS"), event_name="mouseEntered")
		credits.capture(lambda : credits._setText(u"Credits"), event_name="mouseExited")

		# import example modules
		from dynamic import DynamicExample
		from styling import StylingExample
		from sliders import SliderExample
		from colortester import ColorExample
		from poc_gui_animation import PocAnimations
		from stretching import StretchingExample
		from tabbedarea import TabbedAreaExample
		from dynamicgraph import DynamicGraphExample
		from iconprogressbar import IconProgressBarExample
		from imageprogressbar import ImageProgressBarExample
		from modalfocus import ModalFocusExample
		from showhide import ShowHideExample

		# Our list of examples
		# We keep a dictionary of these and fill
		# the ListBox on the left with its names.
		self.examples = {
			'Absolute Positioning' : PyChanExample('gui/absolute.xml', self),
			'Adjusting Container' : PyChanExample('gui/adjustingcontainer.xml'),
			'All Widgets' : PyChanExample('gui/all_widgets.xml'),
			'Basic Styling' : StylingExample(),
			'Circular Box' : PyChanExample('gui/circularcontainer.xml'),
			'Dynamic Widgets' : DynamicExample(),
			'Sliders' : SliderExample(),
			'ScrollArea' : PyChanExample('gui/scrollarea.xml'),
			'Colortester': ColorExample(),
			'GuiAnimations' : PocAnimations(),
			'Tabbed Area' : TabbedAreaExample(),
			'Image Stretching' : StretchingExample(),
			'Resizable Window' : PyChanExample('gui/resizable.xml'),
			'Dock Area' : PyChanExample('gui/dockarea.xml'),
			'Graph Widgets' : PyChanExample('gui/graphwidgets.xml'),
			'Dynamic Graph' : DynamicGraphExample(),
			'Icon Progress Bar' : IconProgressBarExample(),
			'Image Progress Bar' : ImageProgressBarExample(),
			'Flow Container' : PyChanExample('gui/flowcontainer.xml'),
			'Animation Icon' : PyChanExample('gui/animationicon.xml'),
			'Modal Focus' : ModalFocusExample(),
			'Show and Hide' : ShowHideExample(),
		}
		self.demoList = self.gui.findChild(name='demoList')
		self.demoList.items = sorted(self.examples.keys())

		# Finally show the main GUI
		self.gui.show()
		
		self.currentExample = None
		self.creditsWidget = None

	# We use the trace decorator which can help debugging the examples.
	# mostly it's for show though :-)
	@trace
	def selectExample(self):
		"""
		Callback handler for clicking on the example list.
		"""
		if self.demoList.selected_item is None:
			return
		#print "selected",self.demoList.selected_item
		if self.currentExample:
			self.currentExample.stop()
		self.currentExample = self.examples[self.demoList.selected_item]
		self.gui.findChild(name="xmlSource").text = open(self.currentExample.xmlFile).read()
		self.currentExample.start()

	def loadRuntimeXML(self):
		"""
		Callback handler for clicking on the XML button.
		"""
		if self.demoList.selected_item is None:
			return
		
		if self.currentExample:
			self.currentExample.stop()

		# save source to file
		tmp = open("gui/tmp.xml", "w")
		tmp.write(self.gui.findChild(name="xmlSource").text.encode("utf-8"))
		tmp.close()
		# change the xml path, load it and reset the path
		xml_orig = self.currentExample.xmlFile
		self.currentExample.xmlFile = "gui/tmp.xml"
		self.currentExample.start()
		self.currentExample.xmlFile = xml_orig

	def showCredits(self):
		"""
		Callback handler from the credits link/label.
		"""
		# We use PyChan's synchronous execution feature here.
		if self.creditsWidget is None:
			self.creditsWidget = pychan.loadXML('gui/credits.xml')
		self.creditsWidget.execute({ 'okButton' : "Yay!" })
		
	def createListener(self):
		"""
		@note: This function had to be overloaded otherwise the default
		listener would have been created.
		"""
		self._listener = ApplicationListener(self.engine)
		return self._listener
		
	def _pump(self):
		"""
		Overloaded this function to check for quit message.  Quit if message
		is received.
		"""
		if self._listener.quit:
			self.quit()
		
class TestXMLApplication(pychanbasicapplication.PychanApplicationBase):
	"""
	Test Application. Run the pychan_test.py file
	with the XML file you want to load as argument.
	"""
	def __init__(self,xmlfile):
		super(TestXMLApplication,self).__init__()
		pychan.init(self.engine,debug=True)
		self.start()
	@trace
	def start(self):
		self.widget = pychan.loadXML(xmlfile)
		self.widget.show()

if __name__ == '__main__':
	import sys
	if len(sys.argv) == 2:
		app = TestXMLApplication(sys.argv[1])
	else:
		app = DemoApplication()
	app.run()
