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
from Asset import Asset, CryptoToken, DataSpike, RemovableDrive, SecurityChip, HardwarePatch
from Rig import Rig

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

    # The rig acquisition

    def acquire_rig(self, rig: Rig | None = None) -> bool:
        if self.rig is not None:
            print(f"[{self.name}] Already has a rig: {self.rig.name}.")
            return False
        # requires 1 CryptoToken
        token_index = next((i for i, a in enumerate(self.inventory) if a.name == "CryptoToken"), None)
        if token_index is None:
            print(f"[{self.name}] Cannot acquire rig: no CryptoToken.")
            return False
        # consume token
        token = self.inventory.pop(token_index)
        if rig is None:
            rig = Rig(f"{self.name}'s Rig")
        self.rig = rig
        print(f"[{self.name}] Acquired rig '{self.rig.name}'. (Consumed {token.name})")
        return True

    # The Trace management

    def increase_trace(self, amount: int = 1):
        self.trace += amount
        print(f"[{self.name}] Trace increased by {amount}. Now: {self.trace}")
        if self.trace > self.TRACE_THRESHOLD:
            print(
                f"[{self.name}] WARNING: Trace level {self.trace} exceeds threshold {self.TRACE_THRESHOLD}. Some actions may be blocked.")

    def reduce_trace_with_token(self) -> bool:
        # consumes a CryptoToken to reduce trace by 3
        token_index = next((i for i, a in enumerate(self.inventory) if a.name == "CryptoToken"), None)
        if token_index is None:
            print(f"[{self.name}] No CryptoToken available to reduce trace.")
            return False
        self.inventory.pop(token_index)
        old = self.trace
        self.trace = max(0, self.trace - 3)
        print(f"[{self.name}] Used CryptoToken to reduce trace from {old} to {self.trace}.")
        return True
