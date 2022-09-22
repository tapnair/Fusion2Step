# Here you define the commands that will be added to your add-in.

# If you want to add a command, duplicate one of the existing directories and import it here.
# You need to use aliases (import "entry" as "my_module") assuming you have the default module named "entry".
from .designCommand1 import entry as design_command_1
from .mfgCommand2 import entry as mfg_command_2


# TODO add your imported modules to this list.
# Fusion will automatically call the start() and stop() functions.
commands = [
    design_command_1,
    mfg_command_2,
]


# Assumes you defined a "start" function in each of your modules.
# The start function will be run when the add-in is started.
def start():
    for command in commands:
        command.start()


# Assumes you defined a "stop" function in each of your modules.
# The stop function will be run when the add-in is stopped.
def stop():
    for command in commands:
        command.stop()
