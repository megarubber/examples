import constants
import wpilib
import commands2

class RobotContainer:
    def __init__(self) -> None:
        self.driverController = wpilib.XboxController(constants.kDriverControllerPort)
        
        self.instantCommand1 = commands2.InstantCommand()
        self.instantCommand2 = commands2.InstantCommand()
        self.waitCommand = commands2.WaitCommand()

        self.instantCommand1.setName('Instant Command 1')
        self.instantCommand2.setName('Instant Command 2')
        self.waitCommand.setName('Wait 5 Seconds Command')

        commands2.CommandScheduler.getInstance().onCommandInitialize(
            lambda Command() :  
        )
        
        self.configureButtonBindings()

    def configureButtonBindings(self) -> None:
        commands2.JoystickButton(
            self.driverController, wpilib.XboxController.Button.kA
        ).onTrue(self.instantCommand1)
        commands2.JoystickButton(
            self.driverController, wpilib.XboxController.Button.kX
        ).onTrue(self.instantCommand2)
        commands2.JoystickButton(
            self.driverController, wpilib.XboxController.Button.kY
        ).onTrue(self.instantCommand2)

    def getAutonomousCommand 
