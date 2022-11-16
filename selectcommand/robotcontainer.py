# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.

import enum
import commands2

class RobotContainer:
    """
    This class hosts the bulk of the robot's functions. Little robot logic needs to be
    handled here or in the robot periodic methods, as this is a command-based system.
    The structure (commands, subsystems, and button mappings) should be done here.
    """

    # The enum used as keys for selecting the command to run.
    class CommandSelector(enum.Enum) -> None:
        ONE = enum.auto()
        TWO = enum.auto()
        THREE = enum.auto()

    def __init__(self) -> None:
        """
        An example selectcommand.  Will select from the three commands based on the value returned
        by the selector method at runtime.  Note that selectcommand works on Object(), so the
        selector does not have to be an enum; it could be any desired type (string, integer,
        boolean, double...)
        """
        self.example_select_command = 
    
    def select(self) -> CommandSelector:
        """
        An example selector method for the selectcommand.  Returns the selector that will select
        which command to run.  Can base this choice on logical conditions evaluated at runtime.
        """
        return CommandSelector.ONE