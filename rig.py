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

    def break_threshold(self) -> int:
        # Level 0: break at damage 2 (per spec)
        # higher levels tolerate more damage
        return 2 + self.upgrade_level

    def repair(self, hacker_inventory: List[Asset]) -> bool:
        # requires a CryptoToken in hacker inventory
        token_index = next((i for i, a in enumerate(hacker_inventory) if a.name == "CryptoToken"), None)
        if token_index is None:
            print(f"[Rig:{self.name}] Repair failed: no CryptoToken available.")
            return False
        # consume token
        consumed = hacker_inventory.pop(token_index)
        print(f"[Rig:{self.name}] Consumed {consumed.name} to repair rig.")
        if self.damage == 0 and not self.broken:
            print(f"[Rig:{self.name}] No repair needed.")
            return True
        self.damage = 0
        self.broken = False
        print(f"[Rig:{self.name}] Repaired successfully.")
        return True

    def upgrade(self, hacker_inventory: List[Asset]) -> bool:
        # requires a HardwarePatch in hacker inventory
        patch_index = next((i for i, a in enumerate(hacker_inventory) if a.name == "HardwarePatch"), None)
        if patch_index is None:
            print(f"[Rig:{self.name}] Upgrade failed: no HardwarePatch available.")
            return False
        hacker_inventory.pop(patch_index)
        self.upgrade_level += 1
        print(f"[Rig:{self.name}] Upgraded to level {self.upgrade_level}.")
        return True


    def generate_asset(self) -> Asset:
        # generate a random asset (one per call)
        choice = random.choice(["CryptoToken", "DataSpike", "SecurityChip", "HardwarePatch"])
        if choice == "CryptoToken":
            asset = CryptoToken()
        elif choice == "DataSpike":
            asset = DataSpike()
        elif choice == "SecurityChip":
            asset = SecurityChip()
        else:
            asset = HardwarePatch()
            # store generated asset if capacity allows; otherwise return it (caller can decide)
        stored = self.store_asset(asset)
        if not stored:
            print(f"[Rig:{self.name}] Generated {asset.name} but storage is full; returning asset.")
        else:
            print(f"[Rig:{self.name}] Generated and stored {asset.name}.")
        return asset

    def scan_storage(self, name: str) -> Asset | None:
        for a in self.storage:
            if a.name == name:
                return a
        return None

    def extract_unencrypted_assets(self) -> List[Asset]:
        # returns and removes all unencrypted assets from storage
        extracted = [a for a in self.storage if not a.encrypted and a.name != "RemovableDrive"]
        # remove extracted assets
        self.storage = [a for a in self.storage if a.encrypted or a.name == "RemovableDrive"]
        if extracted:
            print(f"[Rig:{self.name}] Extracted {len(extracted)} unencrypted assets.")
        else:
            print(f"[Rig:{self.name}] No unencrypted assets to extract.")
        return extracted

    def condition(self) -> str:
        if self.broken:
            return f"Broken (Level {self.upgrade_level})"
        # some status mapping based on damage
        if self.damage == 0:
            status = "Pristine"
        elif self.damage == 1:
            status = "Wounded"
        else:
            status = "Damaged"
            return f"{status} (Level {self.upgrade_level})"

    def __str__(self) -> str:
            storage_list = ", ".join([a.name + ("[E]" if a.encrypted else "") for a in self.storage]) or "Empty"
            return f"{self.name} - Condition: {self.condition()} | Stored ({len(self.storage)}/{self.base_storage_capacity()}): [{storage_list}]"


