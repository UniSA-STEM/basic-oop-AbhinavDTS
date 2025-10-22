"""
File: main.py
Description: <A brief description of this Python module.>
Author: <Abhinav Sharma>>
ID: <110376072>
Username: <shaay186>
This is my own work as defined by the University's Academic Misconduct Policy.
"""
# main.py Contains tests and example scenarios for the Into the Grid assignment.

from asset import CryptoToken, DataSpike, RemovableDrive, SecurityChip, HardwarePatch
from hacker import Hacker
from rig import Rig
import random
import sys

random.seed(1)  # deterministic randomness for repeatable tests


def separator(title: str = ""):
    print("\n" + "=" * 70)
    if title:
        print(f"= {title}")
        print("=" * 70)


def scenario_basic_acquire_and_upgrade():
    separator("Scenario: Acquire rig, upgrade, and inspect")
    alice = Hacker("Alice")
    print(alice)
    # give her a HardwarePatch so she can upgrade later
    alice.add_to_inventory(HardwarePatch())
    # Acquire rig (consumes CryptoToken)
    alice.acquire_rig(Rig("BlackICE"))
    print(alice.rig)
    # Try upgrade (consumes HardwarePatch)
    alice.upgrade_rig()
    print(alice.rig)
    # Generate an asset in the rig
    alice.rig.generate_asset()
    print(alice.rig)
    print(alice)


def scenario_battle_and_extraction():
    separator("Scenario: Battle and Extraction")
    attacker = Hacker("Neo")
    defender = Hacker("Trinity")
    # Both acquire rigs
    attacker.acquire_rig(Rig("AttackerDeck"))
    defender.acquire_rig(Rig("DefenderDeck"))
    # Add a DataSpike to attacker's rig (they start with 2, but show adding too)
    attacker.rig.store_asset(DataSpike())
    # Put some assets in defender rig (some encrypted, some not)
    defender.rig.store_asset(CryptoToken())
    defender.rig.store_asset(SecurityChip())
    defender.rig.store_asset(HardwarePatch())
    # Encrypt one asset in defender rig (simulate defender protecting something)
    defender.encrypt_asset_in_rig("HardwarePatch")
    print(defender.rig)
    # Attacker launches two data spikes to break the rig
    attacker.launch_data_spike(defender.rig)
    attacker.launch_data_spike(defender.rig)
    # After hits, rig should be broken (level 0 -> break threshold 2)
    print(defender.rig)
    # Attacker needs a removable drive to extract
    # Put a RemovableDrive in attacker's inventory
    attacker.add_to_inventory(RemovableDrive())
    # Extract from broken rig (should pull only unencrypted assets)
    attacker.extract_from_broken_rig(defender.rig)
    print(attacker)
    print(defender.rig)


def scenario_encryption_decryption_and_trace():
    separator("Scenario: Encryption/Decryption and Trace Management")
    y = Hacker("Yoko")
    y.acquire_rig(Rig("DeckY"))
    # Give security chip and an asset to encrypt
    y.add_to_inventory(SecurityChip())
    y.add_to_inventory(CryptoToken())
    # Scan (remove) CryptoToken from inventory
    token = y.scan_inventory("CryptoToken")
    if token:
        print(f"[Test] scan_inventory returned and removed: {token}")
    print(y)
    # Try encrypting an asset that is not present
    y.encrypt_asset_in_inventory("CryptoToken")  # no token anymore
    # Add a generic asset to inventory and encrypt it
    y.add_to_inventory(HardwarePatch())
    y.encrypt_asset_in_inventory("HardwarePatch")
    print(y)
    # Decrypt it
    y.decrypt_asset_in_inventory("HardwarePatch")
    # Cause trace to exceed threshold
    for _ in range(7):
        y.increase_trace(1)
    # Attempt a risky action (launch attack) when trace too high
    # give DataSpike to rig to attempt attack
    y.rig.store_asset(DataSpike())
    dummy_target = Rig("Dummy")
    y.launch_data_spike(dummy_target)  # should be blocked because trace > threshold
    # Use CryptoToken to reduce trace (add one to inventory first)
    y.add_to_inventory(CryptoToken())
    y.reduce_trace_with_token()
    # Now attempt attack again (should be allowed if trace <= threshold)
    y.launch_data_spike(dummy_target)
    print(y)
    print(dummy_target)


def scenario_edge_cases():
    separator("Scenario: Edge Cases")
    bob = Hacker("Bob")
    # Try upgrading without rig
    bob.upgrade_rig()
    # Try encrypting without SecurityChip
    bob.add_to_inventory(HardwarePatch())
    bob.encrypt_asset_in_inventory("HardwarePatch")
    # Try repairing rig when none exists
    bob.repair_my_rig()
    # Acquire rig without CryptoToken (consume it first)
    bob.scan_inventory("CryptoToken")  # remove initial CryptoToken
    bob.acquire_rig(Rig("NoTokenRig"))  # should fail
    # Create rig and try repair without token
    rig = Rig("BrokenOne")
    rig.damage = 1
    rig.broken = True
    bob.rig = rig
    bob.repair_my_rig()  # should fail (no CryptoToken)
    # Add CryptoToken and repair
    bob.add_to_inventory(CryptoToken())
    bob.repair_my_rig()
    print(bob.rig)


def run_all():
    scenario_basic_acquire_and_upgrade()
    scenario_battle_and_extraction()
    scenario_encryption_decryption_and_trace()
    scenario_edge_cases()


if __name__ == "__main__":
    run_all()

