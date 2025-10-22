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

    def store_asset(self, asset: Asset) -> bool:
        if len(self.storage) >= self.base_storage_capacity():
            print(f"[Rig:{self.name}] Storage full. Cannot store {asset.name}.")
            return False
        self.storage.append(asset)
        print(f"[Rig:{self.name}] Stored {asset.name}.")
        return True

    def release_asset(self, asset_name: str) -> Asset | None:
        for i, a in enumerate(self.storage):
            if a.name == asset_name:
                if a.encrypted:
                    print(f"[Rig:{self.name}] Cannot release encrypted asset: {a.name}.")
                    return None
                return self.storage.pop(i)
        print(f"[Rig:{self.name}] Asset {asset_name} not found in storage.")
        return None

    def take_hit(self):
        if self.broken:
            print(f"[Rig:{self.name}] Already broken; further attacks irrelevant.")
            return
        # increase damage by 1 per hit
        self.damage += 1
        print(f"[Rig:{self.name}] Took hit. Damage is now {self.damage}.")
        if self.damage >= self.break_threshold():
            self.broken = True
            print(f"[Rig:{self.name}] Rig is now broken!")
