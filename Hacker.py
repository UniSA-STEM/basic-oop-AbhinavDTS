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

#Inventory helpers
    def add_to_inventory(self, asset: Asset):
        self.inventory.append(asset)
        print(f"[{self.name}] Added {asset.name} to inventory.")

    def remove_from_inventory(self, asset_name: str) -> Asset | None:
        for i, a in enumerate(self.inventory):
            if a.name == asset_name:
                return self.inventory.pop(i)
        return None

    def has_asset(self, asset_name: str) -> bool:
        return any(a.name == asset_name for a in self.inventory)

    def scan_inventory(self, name: str) -> Asset | None:
        for i, a in enumerate(self.inventory):
            if a.name == name:
                return self.inventory.pop(i)  # per spec: "returning and removing it if found"
        return None