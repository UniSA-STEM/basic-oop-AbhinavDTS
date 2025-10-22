"""
File: Rig.py
Description: <A brief description of this Python module.>
Author: <Abhinav Sharma>
ID: <110376072>
Username: <shaay186>
This is my own work as defined by the University's Academic Misconduct Policy.
"""
#Defines the Rig class.
from __future__ import annotations
from typing import List
import random
from asset import Asset, DataSpike, RemovableDrive, SecurityChip, CryptoToken, HardwarePatch


class Rig:
    def __init__(self, name: str):
        self.name = name
        self.damage = 0
        self.broken = False
        self.upgrade_level = 0
        # start with 2 data spikes and 1 removable drive
        self.storage: List[Asset] = [DataSpike(), DataSpike(), RemovableDrive()]

    def base_storage_capacity(self) -> int:

        return 5 + (3 * self.upgrade_level)
