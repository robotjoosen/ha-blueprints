#!/usr/bin/env python3
"""Check blueprint metadata requirements."""

import sys
from pathlib import Path
import yaml


def check_metadata(file_path: Path) -> list[str]:
    """Check metadata for a single blueprint file."""
    errors = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = yaml.safe_load(f)
    except yaml.YAMLError:
        return []

    if not isinstance(content, dict):
        return []

    if "blueprint" not in content:
        return []

    blueprint = content.get("blueprint", {})

    # Check for author
    if "author" not in blueprint:
        errors.append("Missing 'author' field in blueprint metadata")

    # Check for source_url (optional but recommended)
    if "source_url" not in blueprint:
        errors.append("WARNING: Consider adding 'source_url' for easier imports")

    # Check name length
    name = blueprint.get("name", "")
    if len(name) > 60:
        errors.append(f"Blueprint name is too long ({len(name)} chars). Consider shortening to 60 chars or less")

    # Check description
    description = blueprint.get("description", "")
    if len(description) < 20:
        errors.append("Description is too short. Add more details about what this blueprint does")

    return errors


def main():
    """Main entry point."""
    blueprint_dir = Path("blueprints")
    if not blueprint_dir.exists():
        print("ERROR: blueprints/ directory not found")
        sys.exit(1)

    yaml_files = list(blueprint_dir.rglob("*.yaml"))
    if not yaml_files:
        print("No YAML files found in blueprints/")
        sys.exit(0)

    exit_code = 0
    for yaml_file in yaml_files:
        # Skip template file
        if yaml_file.name == "blueprint-template.yaml":
            continue

        print(f"\nChecking metadata: {yaml_file}")
        errors = check_metadata(yaml_file)

        if errors:
            for error in errors:
                if error.startswith("WARNING"):
                    print(f"  {error}")
                else:
                    exit_code = 1
                    print(f"  ERROR: {error}")
        else:
            print(f"  OK")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
