"""Keyboard builders.

Keep keyboard creation in a separate module so handlers stay small and readable.
This also makes it easier to reuse the same keyboards across multiple handlers.
"""
 
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
 
 
def test_button_kb() -> types.InlineKeyboardMarkup:
    """Create a one-button inline keyboard.

    The `callback_data` value must match the filter used in the callback handler
    (see `handlers/buttons.py`).
    """
 
    # InlineKeyboardBuilder helps you add buttons and then convert to markup.
    kb = InlineKeyboardBuilder()
 
    # Add a single inline button.
    kb.add(
        types.InlineKeyboardButton(
            text="Test",
            callback_data="test_button",
        )
    )
 
    # Convert builder to markup object expected by `reply_markup=test_button_kb()`.
    return kb.as_markup()


def ask_user_kb() -> types.InlineKeyboardMarkup:
    """Create a simple keyboard for FSM testing."""

    # Create a keyboard builder.
    kb = InlineKeyboardBuilder()
    # Add a button to the builder.
    kb.add(
        types.InlineKeyboardButton(
            text="Test FSM",
            callback_data="ask_user",
        )
    )

    # Convert the builder to markup.
    return kb.as_markup()
