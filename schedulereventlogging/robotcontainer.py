# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.

import wpilib.shuffleboard
import commands2
import commands2.button
import constants

class RobotContainer:
    """
    This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.
    """

    def __init__(self) -> None:
        """The container for the robot. Contains subsystems, OI devices, and commands."""

        # The driver's controller
        self.driver_controller = commands2.button.CommandXboxController(constants.kDriverControllerPort)
        
        # A few commands that do nothing, but will demonstrate the scheduler functionality
        self.instant_command1 = commands2.InstantCommand()
        self.instant_command2 = commands2.InstantCommand()
        self.wait_command = commands.WaitCommand(5)
        
        # Set names of commands
        self.instant_command1.setName('Instant Command 1')
        self.instant_command2.setName('Instant Command 2')
        self.wait_command.setName('Wait 5 Seconds Command')
        
        # Set the scheduler to log Shuffleboard events for command initialize, interrupt, finish
        commands2.CommandScheduler.getInstance().onCommandInitialize(
            lambda command : Shuffleboard.addEventMarker(
                "Command initialized", command.getName(), 
            )
        )
        commands2.CommandScheduler.getInstance().onCommandInitialize(
            lambda command : Shuffleboard.addEventMarker(
                "Command interrupted", command.getName(), 
            )
        )
        commands2.CommandScheduler.getInstance().onCommandInitialize(
            lambda command : Shuffleboard.addEventMarker(
                "Command finished", command.getName(), 
            )
        )
        
        # Configure the button bindings
        self.configureButtonBindings()

    def configureButtonBindings() -> None:
        """
        Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """

        # Run instant command 1 when the 'A' button is pressed
        self.driver_controller.A().onTrue(self.instant_command1)

        # Run instant command 2 when the 'X' button is pressed
        self.driver_controller.X().onTrue(self.instant_command2)

        # Run instant command 3 when the 'Y' button is held; release early to interrupt
        self.driver_controller.Y().whileTrue(self.wait_command)

    def getAutonomousCommand(self) -> commands2.Command:
        """Use this to pass the autonomous command to the main {Robot} class.

        :returns: the command to run in autonomous
        """
        return commands2.InstantCommand()
