"""
File: Hacker.py
Description: <A brief description of this Python module.>
Author: <Abhinav Sharma>
ID: <110376072>
Username: <shaay186>
This is my own work as defined by the University's Academic Misconduct Policy.
"""

#Defines the Hacker class with methods for acquiring rigs, attacking, encrypting, extracting, upgrades, storage, etc.
from __future__ import annotations
from typing import List
from asset import Asset, CryptoToken, DataSpike, RemovableDrive, SecurityChip, HardwarePatch
from rig import Rig

class Hacker:
    TRACE_THRESHOLD = 5

    def __init__(self, name: str):
        self.name = name
        self.trace = 0
        self.inventory: List[Asset] = [CryptoToken()]  # starts with one CryptoToken
        self.rig: Rig | None = None
