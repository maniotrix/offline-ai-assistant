# robot/__init__.py
"""
By robot we mean an agent which can automate actions and events on os level
This module contains the classes and functions for the robot.

This package is used by backend to execute the robotic actions on the current running system.
from opening the apps on os to autoamting mouse/key events on the system to performing actions on the system.

"""

from robot import Robot, Point, Region
from windows_robot import WindowsRobot
from chrome_robot import ChromeRobot

__all__ = ['Robot', 'WindowsRobot', 'ChromeRobot', 'Point', 'Region']
