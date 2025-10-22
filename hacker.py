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
    # Storage transfer
    def store_asset_to_rig(self, asset_name: str) -> bool:
        if not self.rig:
            print(f"[{self.name}] No rig to store into.")
            return False
        # find asset in inventory
        for i, a in enumerate(self.inventory):
            if a.name == asset_name:
                asset = self.inventory.pop(i)
                if asset.encrypted:
                    print(f"[{self.name}] Storing encrypted assets into rig is allowed.")
                return self.rig.store_asset(asset)
        print(f"[{self.name}] Asset {asset_name} not found in inventory.")
        return False

    def retrieve_asset_from_rig(self, asset_name: str) -> bool:
        if not self.rig:
            print(f"[{self.name}] No rig to retrieve from.")
            return False
        asset = self.rig.release_asset(asset_name)
        if asset:
            self.inventory.append(asset)
            print(f"[{self.name}] Retrieved {asset.name} from rig.")
            # retrieving sensitive assets increases trace
            self.increase_trace(1)
            return True
        return False
    # The Encryption code needed
    def encrypt_asset_in_inventory(self, asset_name: str) -> bool:
        sc = next((a for a in self.inventory if a.name == "SecurityChip"), None)
        if sc is None:
            print(f"[{self.name}] Cannot encrypt: no SecurityChip in inventory.")
            return False
        for a in self.inventory:
            if a.name == asset_name:
                if a.encrypted:
                    print(f"[{self.name}] Asset {asset_name} already encrypted.")
                    return False
                a.encrypt()
                print(f"[{self.name}] Encrypted {a.name} using SecurityChip.")
                return True
        print(f"[{self.name}] Asset {asset_name} not found in inventory.")
        return False

    def decrypt_asset_in_inventory(self, asset_name: str) -> bool:
        sc = next((a for a in self.inventory if a.name == "SecurityChip"), None)
        if sc is None:
            print(f"[{self.name}] Cannot decrypt: no SecurityChip in inventory.")
            return False
        for a in self.inventory:
            if a.name == asset_name:
                if not a.encrypted:
                    print(f"[{self.name}] Asset {asset_name} is not encrypted.")
                    return False
                a.decrypt()
                print(f"[{self.name}] Decrypted {a.name} using SecurityChip.")
                return True
            print(f"[{self.name}] Asset {asset_name} not found in inventory.")
            return False

        def encrypt_asset_in_rig(self, asset_name: str) -> bool:
            if not self.rig:
                print(f"[{self.name}] No rig to encrypt in.")
                return False
                # SecurityChip may be in inventory or rig storage
            sc = next((a for a in self.inventory if a.name == "SecurityChip"), None) or self.rig.scan_storage(
                    "SecurityChip")
            if sc is None:
                    print(f"[{self.name}] Cannot encrypt in rig: no SecurityChip available.")
                    return False
                    # find asset in rig storage
            for a in self.rig.storage:
                if a.name == asset_name:
                    if a.encrypted:
                        print(f"[{self.name}] Rig asset {asset_name} already encrypted.")
                        return False
                    a.encrypt()
                    print(f"[{self.name}] Encrypted {a.name} in rig using SecurityChip.")
                    return True
            print(f"[{self.name}] Asset {asset_name} not found in rig storage.")
            return False

        def decrypt_asset_in_rig(self, asset_name: str) -> bool:
                if not self.rig:
                    print(f"[{self.name}] No rig to decrypt in.")
                    return False
                sc = next((a for a in self.inventory if a.name == "SecurityChip"), None) or self.rig.scan_storage(
                    "SecurityChip")
                if sc is None:
                    print(f"[{self.name}] Cannot decrypt in rig: no SecurityChip available.")
                    return False
                for a in self.rig.storage:
                    if a.name == asset_name:
                        if not a.encrypted:
                            print(f"[{self.name}] Rig asset {asset_name} is not encrypted.")
                            return False
                        a.decrypt()
                        print(f"[{self.name}] Decrypted {a.name} in rig using SecurityChip.")
                        return True
                print(f"[{self.name}] Asset {asset_name} not found in rig storage.")
                return False
        # Upgrading
        def upgrade_rig(self) -> bool:
            if not self.rig:
                print(f"[{self.name}] Cannot upgrade: no rig.")
                return False
            # require HardwarePatch in inventory
            patch_index = next((i for i, a in enumerate(self.inventory) if a.name == "HardwarePatch"), None)
            if patch_index is None:
                print(f"[{self.name}] Cannot upgrade rig: no HardwarePatch in inventory.")
                return False
            # call rig.upgrade which consumes the patch
            return self.rig.upgrade(self.inventory)



