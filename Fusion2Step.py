# Assuming you have not changed the general structure of the template no modification is needed in this file.
# Learn More about using this template here:
# https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-DF32F126-366B-45C0-88B0-CEB46F5A9BE8

from . import commands
from .lib import fusion360utils as futil


def run(context):
    try:
        # This will run the start function in each of your commands as defined in commands/__init__.py
        commands.start()

    except:
        futil.handle_error('run')


def stop(context):
    try:
        # Remove all the event handlers your app has created
        futil.clear_handlers()

        # This will run the start function in each of your commands as defined in commands/__init__.py
        commands.stop()

    except:
        futil.handle_error('stop')
