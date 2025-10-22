"""
File: Hacker.py
Description: <A brief description of this Python module.>
Author: <Abhinav Sharma>
ID: <110376072>
Username: <shaay186>
This is my own work as defined by the University's Academic Misconduct Policy.
"""
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

    # Inventory helpers
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

    # Rig acquisition
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

    # Trace management
    def increase_trace(self, amount: int = 1):
        self.trace += amount
        print(f"[{self.name}] Trace increased by {amount}. Now: {self.trace}")
        if self.trace > self.TRACE_THRESHOLD:
            print(f"[{self.name}] WARNING: Trace level {self.trace} exceeds threshold {self.TRACE_THRESHOLD}. Some actions may be blocked.")

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

    # Encryption
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
        sc = next((a for a in self.inventory if a.name == "SecurityChip"), None) or self.rig.scan_storage("SecurityChip")
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
        sc = next((a for a in self.inventory if a.name == "SecurityChip"), None) or self.rig.scan_storage("SecurityChip")
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

    # Upgrade
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

    # Battles
    def launch_data_spike(self, target_rig: Rig) -> bool:
        # check trace threshold
        if self.trace > self.TRACE_THRESHOLD:
            print(f"[{self.name}] Cannot launch attack: trace {self.trace} too high.")
            return False
        # need DataSpike in current rig's storage (or inventory?)
        # per spec: consuming a Data Spike from their rig's storage
        if not self.rig:
            print(f"[{self.name}] No rig to launch attack from.")
            return False
        # find DataSpike in self.rig.storage
        ds_index = next((i for i, a in enumerate(self.rig.storage) if a.name == "DataSpike"), None)
        if ds_index is None:
            print(f"[{self.name}] No DataSpike in rig to launch.")
            return False
        # consume DataSpike
        spike = self.rig.storage.pop(ds_index)
        print(f"[{self.name}] Launched DataSpike from {self.rig.name} at {target_rig.name} (consumed {spike.name}).")
        # apply hit to target rig
        target_rig.take_hit()
        # increase trace
        self.increase_trace(1)
        # If target rig became broken, optionally extract unsecured assets (requires removable drive)
        return True

    # Extraction
    def extract_from_broken_rig(self, target_rig: Rig) -> bool:
        if not target_rig.broken:
            print(f"[{self.name}] Cannot extract: target rig {target_rig.name} is not broken.")
            return False
        # need a RemovableDrive in our rig storage or inventory
        found_drive = None
        # first check own inventory
        for i, a in enumerate(self.inventory):
            if a.name == "RemovableDrive":
                found_drive = ("inv", i)
                break
        # then check our rig storage
        if found_drive is None and self.rig:
            for i, a in enumerate(self.rig.storage):
                if a.name == "RemovableDrive":
                    found_drive = ("rig", i)
                    break
        if found_drive is None:
            print(f"[{self.name}] No RemovableDrive available to extract.")
            return False
        # consume removable drive
        if found_drive[0] == "inv":
            consumed_drive = self.inventory.pop(found_drive[1])
        else:
            consumed_drive = self.rig.storage.pop(found_drive[1])
        print(f"[{self.name}] Consumed {consumed_drive.name} to extract assets from {target_rig.name}.")
        # extract all unencrypted assets from target_rig
        extracted_assets = target_rig.extract_unencrypted_assets()
        if not extracted_assets:
            print(f"[{self.name}] No unencrypted assets available to extract.")
            return False
        # transfer to our inventory
        self.inventory.extend(extracted_assets)
        print(f"[{self.name}] Extracted {len(extracted_assets)} assets from {target_rig.name} to inventory.")
        # extraction is a risky op: increase trace by number of items extracted
        self.increase_trace(len(extracted_assets))
        return True

    # Repair
    def repair_my_rig(self) -> bool:
        if not self.rig:
            print(f"[{self.name}] No rig to repair.")
            return False
        return self.rig.repair(self.inventory)

    #String
    def __str__(self) -> str:
        rig_name = self.rig.name if self.rig else "No Rig"
        inv_summary = ", ".join([a.name + ("[E]" if a.encrypted else "") for a in self.inventory]) or "Empty"
        return f"{self.name} - Rig: {rig_name} | Trace: {self.trace} | Inventory: [{inv_summary}]"
