#  Copyright 2022 by Autodesk, Inc.
#  Permission to use, copy, modify, and distribute this software in object code form
#  for any purpose and without fee is hereby granted, provided that the above copyright
#  notice appears in all copies and that both that copyright notice and the limited
#  warranty and restricted rights notice below appear in all supporting documentation.
#  AUTODESK PROVIDES THIS PROGRAM "AS IS" AND WITH ALL FAULTS. AUTODESK SPECIFICALLY
#  DISCLAIMS ANY IMPLIED WARRANTY OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR USE.
#  AUTODESK, INC. DOES NOT WARRANT THAT THE OPERATION OF THE PROGRAM WILL BE
#  UNINTERRUPTED OR ERROR FREE.
import adsk.core
import adsk.cam

import os
from time import sleep

from ...lib import fusion360utils as futil

app = adsk.core.Application.get()
ui = app.userInterface

CMD_ID = 'two_step_command_2'
CMD_NAME = '2 Step Command Sample - MFG '
CMD_Description = 'Second command for MFG related functionality (Should be hidden)'

# This is done by specifying the workspace, the tab, and the panel, and the
# command it will be inserted beside. Not providing the command to position it
# will insert it at the end.
WORKSPACE_ID = 'FusionSolidEnvironment'
PANEL_ID = 'SolidScriptsAddinsPanel'
COMMAND_BESIDE_ID = 'ScriptsManagerCommand'

# Resource location for command icons, here we assume a sub folder in this directory named "resources".
ICON_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', '')

# Local list of event handlers used to maintain a reference
# So they are not released and garbage collected.
local_handlers = []

# Time to sleep while waiting for tool path regeneration to complete (in seconds)
POST_PROCESS_INTERVAL = 1


# Executed when add-in is run.
def start():
    # Create a command Definition.
    cmd_def = ui.commandDefinitions.addButtonDefinition(CMD_ID, CMD_NAME, CMD_Description, ICON_FOLDER)

    # Define an event handler for the command created event. It will be called when the button is clicked.
    futil.add_handler(cmd_def.commandCreated, command_created)

    # ******** Add a button into the UI so the user can run the command. ********
    # Get the target workspace the button will be created in.
    workspace = ui.workspaces.itemById(WORKSPACE_ID)

    # Get the panel the button will be created in.
    panel = workspace.toolbarPanels.itemById(PANEL_ID)

    # Create the button command control in the UI after the specified existing command.
    control = panel.controls.addCommand(cmd_def, COMMAND_BESIDE_ID, False)

    # Hide the control in the UI since it is auto-executed.
    control.isVisible = False


# Executed when add-in is stopped.
def stop():
    # Get the various UI elements for this command
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    panel = workspace.toolbarPanels.itemById(PANEL_ID)
    command_control = panel.controls.itemById(CMD_ID)
    command_definition = ui.commandDefinitions.itemById(CMD_ID)

    # Delete the button command control
    if command_control:
        command_control.deleteMe()

    # Delete the command definition
    if command_definition:
        command_definition.deleteMe()


# The command created event in this case simply attaches our handlers and then sets the command to auto-execute
def command_created(args: adsk.core.CommandCreatedEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME} Command Created Event')

    # Important!!
    # Enables auto-execute of the command instead of relying on user to click OK in a dialog.
    args.command.isAutoExecute = True

    # Attach our event handlers for execution and destroy
    futil.add_handler(args.command.execute, command_execute, local_handlers=local_handlers)
    futil.add_handler(args.command.destroy, command_destroy, local_handlers=local_handlers)


# Here we execute the switch to the MFG workspace and do any other MFG processing (such as update tool paths)
def command_execute(args: adsk.core.CommandEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME} Command Execute Event')

    # Here we activate the CAM workspace now that the geometry edits have been committed
    ui.workspaces.itemById('CAMEnvironment').activate()

    # Get the CAM Product for the current document
    doc = app.activeDocument
    products = doc.products
    product = products.itemByProductType('CAMProductType')
    cam = adsk.cam.CAM.cast(product)
    if not cam:
        return

    # TODO ******************************** Update MFG here ********************************

    # Regenerate the tool paths
    future = cam.generateAllToolpaths(False)

    # Wait for tool path generation to complete
    while not future.isGenerationCompleted:
        app.log('Waiting for CAM to finish')
        adsk.doEvents()
        sleep(POST_PROCESS_INTERVAL)

    # TODO Add POST Process functions here


# This event handler is called when the command terminates.
def command_destroy(args: adsk.core.CommandEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME} Command Destroy Event')

    global local_handlers
    local_handlers = []
