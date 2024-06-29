# discord-py-template

Language in: [[English](README.md)] [[日本語](README_ja.md)]

## Overview

A highly extensible Discord Bot template with rich logging and features. It comes with a built-in database (SQLite + Prisma) by default, allowing for easy data persistence.

## Features

- Rich log output
- Built-in database
- Cog-based extensibility

## Table of Contents

- [discord-py-template](#discord-py-template)
  - [Overview](#overview)
  - [Features](#features)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [Requirements](#requirements)
    - [Clone \& Install](#clone--install)
    - [Bot Configuration](#bot-configuration)
  - [How to Use Prisma](#how-to-use-prisma)
  - [Adding Cogs](#adding-cogs)
    - [Adding a Cog as a .py file](#adding-a-cog-as-a-py-file)
    - [Adding a Cog as a folder](#adding-a-cog-as-a-folder)
  - [To Do](#to-do)
  - [License](#license)
  - [Contributing](#contributing)

## Installation

### Requirements

- Python 3.8 or later
- Discord account
- Git

### Clone & Install

```bash
git clone https://github.com/caru-ini/discord-py-template.git
cd discord-py-template
python -m venv .venv
# use python3 -m venv .venv on Linux
.venv\Scripts\activate
# source .venv/bin/activate on Linux
pip install -r requirements.txt
```

### Bot Configuration

Copy `.env.example` to create `.env`. Set each value accordingly.

```bash
cp .env.example .env
```

- `DATABASE_URL`: Database URL
  This can generally be left as is. If you change the database type, you'll need to modify the Prisma configuration.
- `TOKEN`: Discord Bot token
  If you don't have one, create a new Bot from the [Discord Developer Portal](https://discord.com/developers/applications).
  Make sure to enable all Intents in the Bot settings.

`config.json` contains the settings for `Cogs`. No initial setup is required.

Now your Bot is ready. You can start the Bot with the following command:

```bash
python main.py
```

## How to Use Prisma

Prisma is an ORM that simplifies database operations. For details, refer to the [official Prisma documentation](https://www.prisma.io/docs/).

Tips: To check the database in a GUI, run the following command:

```bash
prisma studio
```

access `http://localhost:5555` in your browser.

## Adding Cogs

### Adding a Cog as a .py file

Create a new `.py` file in the `cogs` directory. You can add a Cog in the following format:

For information on how to use Cogs, [this article](https://zenn.dev/nano_sudo/articles/a00db1a55d6c4c) (in Japanese) is helpful.

### Adding a Cog as a folder

When setting up as a folder, in addition to the normal procedure, create an `__init__.py`:

`cogs/<Cog_name>/__init__.py`:

```python
try:
    from . import main
    setup = main.setup
except ImportError:
    raise ImportError("Function 'setup' must be implemented in the main module of the cog")
```

Create a Cog in `cogs/<Cog_name>/main.py` following the same procedure as for .py files.

## To Do

- [ ] Add Cog Examples
- [ ] Add UI & Embed Presets
- [ ] Add more logging options
- [ ] Add usage of prisma
- [ ] i18n support

## License

MIT License

## Contributing

Issues and Pull Requests are very welcome. Feel free to submit them.
There's no specific template, but for PRs, please follow these rules:

- Code changes should comply with PEP8
- Include type annotations
- Use double quotes for strings
- Use f-strings for template literals
