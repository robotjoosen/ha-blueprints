# Contributing to Home Assistant Blueprints

Thank you for your interest in contributing! This document provides guidelines for submitting blueprints to this repository.

## Getting Started

1. Fork this repository
2. Clone your fork locally
3. Create a new branch for your blueprint (`git checkout -b add-my-blueprint`)
4. Make your changes
5. Test your blueprint in Home Assistant
6. Submit a pull request

## Blueprint Requirements

All blueprints must meet the following criteria:

### 1. Valid YAML

- Use valid YAML syntax
- Pass `yamllint` validation
- Include proper indentation (2 spaces)

### 2. Required Metadata

Every blueprint must include these fields:

```yaml
blueprint:
  name: "Human Readable Name"
  description: "Clear description of what this blueprint does"
  author: "Your Name or GitHub Username"
  domain: automation|script|scene
  input:
    # Input fields here
```

### 3. Documentation

Include as comments in the YAML:

- **Purpose**: What does this blueprint do?
- **Requirements**: Entities, integrations, or hardware needed
- **Setup**: Step-by-step configuration instructions
- **Changelog**: Version history with dates

### 4. Input Fields

Use descriptive input fields with:

- Clear `name` and `description`
- Appropriate `selector` types
- Sensible `default` values where applicable

### 5. Naming Conventions

- **Filename**: Use kebab-case (e.g., `motion-activated-light.yaml`)
- **Blueprint name**: Title case (e.g., "Motion Activated Light")
- **Variables**: snake_case (e.g., `motion_sensor`)

## File Structure

Place blueprints in the appropriate directory:

- `blueprints/automations/` - For automation blueprints
- `blueprints/scripts/` - For script blueprints
- `blueprints/scenes/` - For scene blueprints
- `blueprints/helpers/` - For reusable templates and helpers

## Testing Checklist

Before submitting, verify:

- [ ] Blueprint imports successfully in Home Assistant
- [ ] All input fields work as expected
- [ ] Default values make sense
- [ ] Automation/script runs without errors
- [ ] Edge cases are handled
- [ ] YAML passes linting (`yamllint blueprints/`)

## Pull Request Process

1. Update the README.md to include your blueprint in the table
2. Ensure all CI checks pass
3. Request review from maintainers
4. Address any feedback

## Code of Conduct

- Be respectful and constructive
- Focus on the blueprint, not the person
- Accept feedback gracefully

## Questions?

Open an issue for:

- Questions about contributing
- Proposing a new blueprint idea
- Reporting bugs in existing blueprints
