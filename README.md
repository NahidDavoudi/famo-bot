# tg-bot-aiogram

A minimal, beginner-friendly **Telegram bot template** built with **[aiogram v3](https://docs.aiogram.dev/)**.

It is intended to be copied and reused as a starting point for your own bots.

## Features

- **aiogram 3** project structure with routers
- **Inline keyboards** (`keyboards.py`)
- **Callback query handlers** (`handlers/buttons.py`)
- **FSM example** (ask user for input and store it in state)
- Configuration via **environment variables** / `.env` (`config_reader.py`)
- Optional structured logging via **loguru**

## Project structure

```text
.
├─ main.py                 # Bot entrypoint (Dispatcher, routers, polling)
├─ config_reader.py        # Loads BOT_TOKEN from environment/.env
├─ keyboards.py            # Inline keyboard builders
├─ handlers/
│  ├─ commands.py          # /start (and other commands)
│  └─ buttons.py           # CallbackQuery handlers + FSM example
├─ pyproject.toml          # Poetry/PEP-621 dependencies
└─ requirements.txt        # pip dependencies (alternative)
```

## Requirements

- Python **3.10+**
- A Telegram bot token from **@BotFather**

## Configuration (.env)

Create a file named `.env` in the project root:

```env
BOT_TOKEN=123456789:ABCDEF_your_real_token_here
```

`config_reader.py` reads this value and provides it as `config.bot_token`.

## Installation & running

Choose **one** of the options below.

### Option A: Poetry (recommended)

1. Install dependencies:

```bash
poetry install
```

2. Run the bot:

```bash
poetry run python main.py
```

### Option B: pip + virtualenv

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the bot:

```bash
python main.py
```

## How to customize this template

### 1) Add new handlers

- Put **command handlers** in `handlers/commands.py`
- Put **button/callback handlers** in `handlers/buttons.py`
- If you add a new router module, include it in `main.py`:

```python
# dp.include_routers(commands.router, buttons.router, my_new_router.router)
```

### 2) Add new buttons (inline keyboard)

- Add a new keyboard builder in `keyboards.py`
- Make sure the `callback_data` matches your filter:

```python
@router.callback_query(F.data == "your_callback")
```

### 3) Use FSM (multi-step dialogs)

This template includes a simple example:

- Bot sends a message and sets a state
- Next user message is handled by `@router.message(AskUser.age)`
- Data is stored via `state.update_data(...)`

## Troubleshooting

- **Bot doesn’t start / token errors**
  - Ensure `.env` exists and contains `BOT_TOKEN=...`
  - Ensure you are running from the project root

- **Nothing happens when pressing buttons**
  - Ensure `callback_data` in `keyboards.py` matches the handler filter in `handlers/buttons.py`

## License

Use this template however you want. If you share it publicly, a small attribution is appreciated.
