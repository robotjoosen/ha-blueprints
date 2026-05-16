# Home Assistant Blueprints - Claude Context

## Project Overview

This repository contains Home Assistant blueprints - reusable templates for automations, scripts, and scenes. Blueprints allow users to quickly set up complex automations without starting from scratch.

## Repository Structure

```
.
├── blueprints/
│   ├── automations/     # Automation blueprints
│   ├── scripts/         # Script blueprints
│   ├── scenes/          # Scene blueprints
│   └── helpers/         # Helper templates and utilities
├── .github/
│   ├── workflows/       # GitHub Actions CI/CD
│   └── scripts/         # Validation scripts
├── blueprint-template.yaml    # Template for new blueprints
├── CONTRIBUTING.md        # Contribution guidelines
├── README.md             # Project documentation
├── .yamllint.yaml        # YAML linting configuration
├── .pre-commit-config.yaml  # Pre-commit hooks
└── requirements.txt      # Python dependencies
```

## Common Tasks

### Adding a New Blueprint

1. Copy `blueprint-template.yaml` to the appropriate subdirectory
2. Fill in the blueprint metadata and logic
3. Test in Home Assistant
4. Run validation: `yamllint blueprints/`
5. Update README.md with the new blueprint

### Running Validation Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Lint all YAML files
yamllint -c .yamllint.yaml blueprints/

# Validate blueprint schema
python .github/scripts/validate_blueprints.py

# Check metadata
python .github/scripts/check_metadata.py
```

### Setting Up Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

## Blueprint Schema

Required fields in the `blueprint` section:

- `name`: Human-readable name (string, max 60 chars)
- `description`: Detailed description of functionality
- `domain`: Type of blueprint - `automation` or `script`
- `input`: User-configurable input fields

Optional but recommended:

- `author`: Your name or GitHub username
- `source_url`: Direct URL to the blueprint file

## Validation Rules

- YAML must pass `yamllint` checks
- Required blueprint fields must be present
- Domain must be valid (`automation` or `script`)
- Name should be 60 characters or less
- Description should be meaningful (20+ chars)
