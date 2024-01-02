#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import math
import wpilib
import wpimath.controller
import wpimath.estimator
import wpimath.units
import wpimath.trajectory
import wpimath.system
import wpimath.system.plant

kMotorPort = 0
kEncoderAChannel = 0
kEncoderBChannel = 1
kJoystickPort = 0
kHighGoalPosition = wpimath.units.feetToMeters(3)
kLowGoalPosition = wpimath.units.feetToMeters(0)

kCarriageMass = 4.5
# kilograms

# A 1.5in diameter drum has a radius of 0.75in, or 0.019in.
kDrumRadius = 1.5 / 2.0 * 25.4 / 1000.0

# Reduction between motors and encoder, as output over input. If the elevator spins slower than
# the motors, this number should be greater than one.
kElevatorGearing = 6.0


class MyRobot(wpilib.TimedRobot):
    """This is a sample program to demonstrate how to use a state-space controller to control an
    elevator.
    """

    def robotInit(self) -> None:
        self.profile = wpimath.trajectory.TrapezoidProfile(
            wpimath.trajectory.TrapezoidProfile.Constraints(
                wpimath.units.feetToMeters(3.0),
                wpimath.units.feetToMeters(6.0),  # Max elevator speed and acceleration.
            )
        )

        self.lastProfiledReference = wpimath.trajectory.TrapezoidProfile.State()

        # The plant holds a state-space model of our elevator. This system has the following properties:

        # States: [position, velocity], in meters and meters per second.
        # Inputs (what we can "put in"): [voltage], in volts.
        # Outputs (what we can measure): [position], in meters.

        # This elevator is driven by two NEO motors.
        self.elevatorPlant = wpimath.system.plant.LinearSystemId.elevatorSystem(
            wpimath.system.plant.DCMotor.NEO(2),
            kCarriageMass,
            kDrumRadius,
            kElevatorGearing,
        )

        # The observer fuses our encoder data and voltage inputs to reject noise.
        self.observer = wpimath.estimator.KalmanFilter_2_1_1(
            self.elevatorPlant,
            [
                wpimath.units.inchesToMeters(2),
                wpimath.units.inchesToMeters(40),
            ],  # How accurate we think our model is, in meters and meters/second.
            [
                0.001
            ],  # How accurate we think our encoder position data is. In this case we very highly trust our encoder position reading.
            0.020,
        )

        # A LQR uses feedback to create voltage commands.
        self.controller = wpimath.controller.LinearQuadraticRegulator_2_1(
            self.elevatorPlant,
            [
                wpimath.units.inchesToMeters(1.0),
                wpimath.units.inchesToMeters(10.0),
            ],  # qelms. Position
            # and velocity error tolerances, in meters and meters per second. Decrease this to more
            # heavily penalize state excursion, or make the controller behave more aggressively. In
            # this example we weight position much more highly than velocity, but this can be
            # tuned to balance the two.
            [12.0],  # relms. Control effort (voltage) tolerance. Decrease this to more
            # heavily penalize control effort, or make the controller less aggressive. 12 is a good
            # starting point because that is the (approximate) maximum voltage of a battery.
            0.020,  # Nominal time between loops. 0.020 for TimedRobot, but can be
            # lower if using notifiers.
        )

        # The state-space loop combines a controller, observer, feedforward and plant for easy control.
        self.loop = wpimath.system.LinearSystemLoop_2_1_1(
            self.elevatorPlant, self.controller, self.observer, 12.0, 0.020
        )

        # An encoder set up to measure flywheel velocity in radians per second.
        self.encoder = wpilib.Encoder(kEncoderAChannel, kEncoderBChannel)

        self.motor = wpilib.PWMSparkMax(kMotorPort)

        # A joystick to read the trigger from.
        self.joystick = wpilib.Joystick(kJoystickPort)

        # Circumference = pi * d, so distance per click = pi * d / counts
        self.encoder.setDistancePerPulse(math.tau * kDrumRadius / 4096)


def teleopInit(self) -> None:
    # Reset our loop to make sure it's in a known state.
    self.loop.reset([self.encoder.getDistance(), self.encoder.getRate()])

    # Reset our last reference to the current state.
    self.lastProfiledReference = wpimath.trajectory.TrapezoidProfile.State(
        self.encoder.getDistance(), self.encoder.getRate()
    )

    def teleopPeriodic(self) -> None:
        # Sets the target position of our arm. This is similar to setting the setpoint of a
        # PID controller.

        goal = wpimath.trajectory.TrapezoidProfile.State()

        if self.joystick.getTrigger():
            # the trigger is pressed, so we go to the high goal.
            goal = wpimath.trajectory.TrapezoidProfile.State(kHighGoalPosition, 0.0)

        else:
            # Otherwise, we go to the low goal
            goal = wpimath.trajectory.TrapezoidProfile.State(kLowGoalPosition, 0.0)

        # Step our TrapezoidalProfile forward 20ms and set it as our next reference
        self.lastProfiledReference = self.profile.calculate(
            0.020, self.lastProfiledReference, goal
        )
        self.loop.setNextR(
            self.lastProfiledReference.position, self.lastProfiledReference.velocity
        )

        # Correct our Kalman filter's state vector estimate with encoder data.
        self.loop.correct([self.encoder.getDistance()])

        # Update our LQR to generate new voltage commands and use the voltages to predict the next
        # state with out Kalman filter.
        self.loop.predict(0.020)

        # Send the new calculated voltage to the motors.
        # voltage = duty cycle * battery voltage, so
        # duty cycle = voltage / battery voltage
        nextVoltage = self.loop.U(0)
        self.motor.setVoltage(nextVoltage)


if __name__ == "__main__":
    wpilib.run(MyRobot)
