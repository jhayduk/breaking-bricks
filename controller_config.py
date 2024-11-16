"""
This file contains a single dictionary, _button_mapping, which contains one entry
per known input controller and is used to map axes and buttons to certain
directions or actions that are then returned by the ControllerInput class.
The key for each entry is the GUID for the controller which should be unique
for each model and can be read with

This dictionary is considered internal to the ControllerInput class code
and is not intended to be used elsewhere.
"""
_button_mapping = {
    "default": {
        "name": "default - used if device guid is not in this table",
        "paddle": {"axis": 0, "name": "Axis 0"},
        "serve": {"button": 0, "name": "Button 0"}
    },
    "0300e6365e0400003c00000001010000": {
        "name": "Microsoft SideWinder Joystick",
        "paddle": {"axis": 0, "name": "Joystick"},
        "serve": {"button": 0, "name": "Trigger"}
    },
    "03008fe54c050000cc09000000016800": {
        "name": "PS4 Controller",
        "paddle": {"axis": 2, "name": "R-Stick"},
        "serve": {"button": 0, "name": "╳ button"}
    }
}
