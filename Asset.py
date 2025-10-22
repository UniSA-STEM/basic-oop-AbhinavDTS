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

    def encrypt(self):
        if self.encrypted:
            print(f"[Asset] {self.name} is already encrypted.")
            return False
        self.encrypted = True
        return True

    def decrypt(self):
        if not self.encrypted:
            print(f"[Asset] {self.name} is not encrypted.")
            return False
        self.encrypted = False
        return True

    def __str__(self) -> str:
        s = f"{self.name}: {self.description}"
        if self.encrypted:
            s += " [Encrypted]"
        return s

    #The code for the Convenience factory functions for core assets
    def CryptoToken() -> Asset:
        return Asset("CryptoToken", "Used to acquire or repair rigs.")

    def DataSpike() -> Asset:
        return Asset("DataSpike", "Used in battles to damage rigs.")

    def RemovableDrive() -> Asset:
        return Asset("RemovableDrive", "Used to extract unsecured assets from broken rigs.")

    def SecurityChip() -> Asset:
        return Asset("SecurityChip", "Enables encryption and decryption operations.")

    def HardwarePatch() -> Asset:
        return Asset("HardwarePatch", "Used to upgrade rigs.")
