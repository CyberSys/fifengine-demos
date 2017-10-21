Fifengine Demos ![Python 2.7 Compatiblity](https://img.shields.io/badge/Python%202.7-OK-brightgreen.svg)
---------------

### CEGUI

The CEGUI demo shows, how to work with CrazyEddie's GUI. The demo requires [PyCEGUI](http://cegui.org.uk/wiki/PyCEGUI).

### PyChan

Last but not least there is an example client residing in `<FIFE>/demos/pychan_demo` that shows how the pychan GUI library works. Start the GUI demo application by running `pychan_demo.py`.

### Rio De Hola

Rio de hola is a technology demo showing off many of the FIFE features. It is located in the `<FIFE>/demos/rio_de_hola` directory and can be launched by running `run.py`. It was at one time meant to be an example game but we have moved away from that idea and it is now more of a technology demo and a playground for developers to test their code. It does serve as a good starting point for people wishing to play around with FIFE or base your game off of.

### Rocket

A demo using librocket.

### RPG

A basic RPG example.

### Shooter

The Shooter demo was an attempt to show the versatility and flexibility of FIFE. It is a simple side scrolling shooter that has a main menu, one level and an end boss. Try your luck and see if you can defeat the boss!

### Configuring the Editor and Demos

The engine utilizes special settings files for configuring FIFE. This file is called `settings.xml` and resides in the `~/.fife directory` (in `<User>\Application Data\fife` for Windows users). The Shooter Demo and the PyChan demo are exceptions. They both store their `settings.xml` file in their root directories.

NOTE that the `settings.xml` file is auto generated and wont be there until you run the demos for the first time. FIFE automatically fills the settings file with default values. For more information on FIFE settings please see the manual: https://fifengine.github.io/fifengine-docs/developer-manual/en/#_engine_settings
