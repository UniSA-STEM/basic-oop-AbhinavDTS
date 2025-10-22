"""
File: Asset.py
Description: <A brief description of this Python module.>
Author: <Abhinav Sharma>
ID: <110376072>
Username: <shaay186>
This is my own work as defined by the University's Academic Misconduct Policy.
"""

# Defines the Asset base class and several concrete asset factories for convenience.
from __future__ import annotations
from dataclasses import dataclass

class Asset:
    name: str
    description: str
    encrypted: bool = False