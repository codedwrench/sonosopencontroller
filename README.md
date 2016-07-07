# sonosopencontroller
An open source sonos controller written in python.
Relies on PySide and the [soco](https://github.com/SoCo/SoCo) library.
Work in Progress.
I am making this application to be able to use my Sonos Play 1 on linux.
I'm trying to make this controller as complete as possible, so hopefully we will have a good controller for linux instead of having to rely on our phones and tablets to control our devices.

# Installation and Requirements
As this application relies on [soco](https://github.com/SoCo/SoCo) and [PySide](https://github.com/PySide/PySide), sonosopencontroller needs Python 2.7 or 3.3 or newer. 
Do note that officially PySide does <u>not</u> support Python 3.5.

I've had problems installing SoCo through 
`pip install soco`
So I cloned the soco repo and used
`pip install .`
whilst in the directory, this did work perfectly.

There is also an issue with UPNP classes, breaking deezer for me and some other things, to fix this copy the data_structures.py from fixed datastructures to your SoCo folder, you can check if this issue has been fixed here:
(https://github.com/SoCo/SoCo/issues/399)

# License
sonosopencontroller is released under the [MIT license](https://opensource.org/licenses/mit-license.php).
