"""Callback query handlers (inline button clicks).

Inline keyboard buttons send a CallbackQuery update. You typically filter by
`callback_data` (see `keyboards.py`).
"""
 
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import ask_user_kb
 
 
# Router instance exported and included in `main.py`.
router = Router()
 

# Create an FSM object where data from user input will be stored.
class AskUser(StatesGroup):
    age = State()




# Callback data handler for the `Test` button.
@router.callback_query(F.data == "test_button")
async def on_test_button_callback(
    callback: types.CallbackQuery
) -> None:
    """Handle presses of the "Test" inline button."""
 
    # Always acknowledge callback updates. Here we answer with a message.
    # (Optionally you can call `await callback.answer()` to stop the loading
    # animation without sending a message.)
    user_id = callback.message.from_user.id
 
    await callback.message.answer(
        f"This is your id: {user_id}",
        reply_markup=ask_user_kb()  # Shows a keyboard button for FSM testing.
    )




# Callback data handler for the `FSM test` button.
@router.callback_query(F.data == "ask_user")
async def ask_user_button(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    """Handle presses of the "Test FSM" inline button.

    `state` is injected by aiogram and is useful for multi-step dialogs.
    Use it here, and keep it in the signature as a template.
    """

    # Always clear the state before starting another one.
    await state.clear()
    # Set the state to get data from the user.
    await state.set_state(AskUser.age)
    # Ask the user to enter some input (age, in our case).
    await callback.message.answer('How old are you?')




# Message handler for user input while the FSM is in the `AskUser.age` state.
@router.message(AskUser.age)
# Use `types.Message` here since we don't process any callback data.
async def proceed_user_answer(message: types.Message, state: FSMContext) -> None:
    # Save user input into the state.
    # Here `user_age` will be used later to get this data from the state.
    await state.update_data(user_age=message.text)
    # We can use this data immediately, or use it later in other bot messages.
    state_data = await state.get_data()
    # Put this data into a variable so we can use it here or later.
    user_age_from_state = int(state_data['user_age'])
    # Reply to the user based on their age.
    check_age = lambda x: 'Hi granny!' if x > 25 else 'Hi kid!'
    await message.answer(f"{check_age(user_age_from_state)}")