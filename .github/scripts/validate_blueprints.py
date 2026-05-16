#!/usr/bin/env python3
"""Validate Home Assistant blueprint YAML schema."""

import sys
from pathlib import Path
import yaml

REQUIRED_FIELDS = {
    "name": str,
    "description": str,
    "domain": str,
}

VALID_DOMAINS = {"automation", "script"}


def validate_blueprint(file_path: Path) -> list[str]:
    """Validate a single blueprint file."""
    errors = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [f"YAML syntax error: {e}"]

    if not isinstance(content, dict):
        return ["Root must be a dictionary"]

    if "blueprint" not in content:
        return ["Missing 'blueprint' root key"]

    blueprint = content["blueprint"]
    if not isinstance(blueprint, dict):
        return ["'blueprint' must be a dictionary"]

    # Check required fields
    for field, field_type in REQUIRED_FIELDS.items():
        if field not in blueprint:
            errors.append(f"Missing required field: blueprint.{field}")
        elif not isinstance(blueprint[field], field_type):
            errors.append(f"Field '{field}' must be of type {field_type.__name__}")

    # Validate domain
    if "domain" in blueprint:
        domain = blueprint["domain"]
        if domain not in VALID_DOMAINS:
            errors.append(f"Invalid domain '{domain}'. Must be one of: {VALID_DOMAINS}")

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

        print(f"\nChecking: {yaml_file}")
        errors = validate_blueprint(yaml_file)

        if errors:
            exit_code = 1
            for error in errors:
                print(f"  ERROR: {error}")
        else:
            print(f"  OK")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
