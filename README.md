# Home Assistant Blueprints

A curated collection of Home Assistant blueprints for automations, scripts, and scenes.

## Overview

This repository contains reusable blueprints for Home Assistant that help you quickly set up common automation patterns, scripts, and scenes without starting from scratch.

## What are Blueprints?

Blueprints are pre-made automation configurations that allow you to create complex automations with minimal configuration. They use YAML and can accept user input through the UI, making them accessible to users of all skill levels.

## Repository Structure

```
blueprints/
├── automations/    # Automation blueprints
├── scripts/        # Script blueprints
├── scenes/         # Scene blueprints
└── helpers/        # Helper blueprints and utility templates
```

## Installation

### Method 1: Import via URL

1. Go to **Settings** > **Automations & Scenes** > **Blueprints**
2. Click the **Import Blueprint** button
3. Paste the URL of the blueprint file (e.g., `https://github.com/robotjoosen/homeassistant/blob/main/blueprints/automations/motion-light.yaml`)

### Method 2: Manual Installation

1. Copy the blueprint YAML file content
2. Go to **Settings** > **Automations & Scenes** > **Blueprints**
3. Click the menu (⋮) in the top right and select **Edit in YAML**
4. Paste the content and save

### Method 3: Using Home Assistant Community Store (HACS)

If you have HACS installed, you can add this repository as a custom repository:

1. Open HACS
2. Click on **Automations**
3. Click the menu (⋮) and select **Custom repositories**
4. Add this repository URL and select category **Automation**

## Available Blueprints

### Automations

| Blueprint | Description |
|-----------|-------------|
| [Motion-Activated Light](blueprints/automations/motion-light.yaml) | Turn on lights when motion is detected, with configurable timeout |

### Scripts

| Blueprint | Description |
|-----------|-------------|
| [Toggle Entity](blueprints/scripts/toggle-entity.yaml) | Simple script to toggle any entity with optional conditions |

### Scenes

| Blueprint | Description |
|-----------|-------------|
| [Evening Scene](blueprints/scenes/evening.yaml) | Dim the lights for a cozy evening atmosphere |

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to submit blueprints.

## Support

- [Home Assistant Blueprint Documentation](https://www.home-assistant.io/docs/blueprint/)
- [Home Assistant Community Forum](https://community.home-assistant.io/c/blueprints/53)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
