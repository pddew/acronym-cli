# Acronym CLI

A simple command-line tool to manage acronyms with default lookup.

## Installation

### Using pipx (recommended)

```bash
pipx install .
```

### Using pip

```bash
pip install .
```

## Usage

### Lookup an acronym (default)

```bash
acronym API
```

This will print the full name and description of the acronym.

### Add a new acronym

```bash
acronym add API
```

- You will be prompted for the full name and description.
- If the acronym already exists, you will be asked to confirm overwrite.

### Delete an acronym

```bash
acronym delete API
```

- Prompts for confirmation before deleting.

### List all acronyms

```bash
acronym list
```

- Shows all acronyms in a table.

## Data Storage

- Acronyms are stored in YAML format at:

```
~/.config/acronym/acronyms.yaml
```

- The folder and file are created automatically.

## Notes

- The CLI supports **default lookup**: if you type `acronym <ACRONYM>` without a subcommand, it will automatically look it up.
- Subcommands `add`, `delete`, `list` still work as usual.

