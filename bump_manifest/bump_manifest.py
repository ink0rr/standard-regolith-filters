import os
import json
from typing import List
from pathlib import Path

def create_version_file() -> None:
    """
    Creates a version file.
    """

    Path("./data/bump_manifest/").mkdir(parents=True, exist_ok=True)

    with open('./data/bump_manifest/version.json', 'a') as file:
        json.dump({'version': [1, 0, 0]}, file, indent=4)

def get_version() -> str:
    """
    Gets the current version number from the version.json file.

    Saves new version back to the file.
    """

    path = './data/bump_manifest/version.json'

    # Create version file, if it doesn't exist
    if not os.path.exists(path):
        create_version_file()

    # Read version file
    with open(path, 'r') as f:
        data = json.load(f)

    # Update version file
    data['version'][-1] = data['version'][-1] + 1
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

    return data['version']


def update_manifest(manifest: dict, version: list[int]) -> dict:
    """
    Apply a new version list to …
      - manifest["header"]["version"]
      - each module whose "type" is "resources" or "data"
      - each dependency that has a "uuid" key

    Parameters
    ----------
    manifest : dict
        Parsed JSON manifest.
    version : list[int]
        Version triple like [1, 2, 3].

    Returns
    -------
    dict
        The modified manifest (in-place edit, but also returned for chaining).
    """

    # ── header ───────────────────────────────────────────────────────────
    manifest["header"]["version"] = version

    # ── selected modules ────────────────────────────────────────────────
    allowed_types = {"resources", "data"}
    for module in manifest.get("modules", []):
        if module.get("type") in allowed_types:
            module["version"] = version

    # ── dependencies with uuid ──────────────────────────────────────────
    for dep in manifest.get("dependencies", []):
        if dep.get("uuid") is not None:
            dep["version"] = version

    return manifest

    
def main():
    """
    Program execution begins here.
    """

    # Get current version, and update the file
    version = get_version()

    print("Pack updated to version: ", str(version))

    # Write new version to resource pack
    try:
        with open('./RP/manifest.json', 'r') as manifest_file:
            manifest = json.load(manifest_file)

        with open('./RP/manifest.json', 'w') as manifest_file:
            json.dump(update_manifest(manifest, version), manifest_file, indent=4)
    except FileNotFoundError:
        pass

    # Write new version to resource pack
    try:
        with open('./BP/manifest.json', 'r') as manifest_file:
            manifest = json.load(manifest_file)

        with open('./BP/manifest.json', 'w') as manifest_file:
            json.dump(update_manifest(manifest, version), manifest_file, indent=4)

    except FileNotFoundError:
        pass

if __name__ == "__main__":
    main()