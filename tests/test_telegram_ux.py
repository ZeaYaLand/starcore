from handlers.menu import MENU_BUTTONS, main_menu_keyboard


def test_stage54_menu_has_expected_navigation_buttons():
    buttons = [text for row in MENU_BUTTONS for text, _ in row]
    assert buttons == [
        "🧬 Профиль",
        "🎮 Играть",
        "📊 Статистика",
        "🔔 Уведомления",
        "ℹ️ Помощь",
        "❌ Скрыть меню",
    ]
    assert len(buttons) == len(set(buttons))


def test_stage54_inline_keyboard_has_navigation_callbacks():
    keyboard = main_menu_keyboard()
    assert [[button.text for button in row] for row in keyboard.inline_keyboard] == [
        ["🧬 Профиль", "🎮 Играть"],
        ["📊 Статистика", "🔔 Уведомления"],
        ["ℹ️ Помощь", "❌ Скрыть меню"],
    ]
    assert [[button.callback_data for button in row] for row in keyboard.inline_keyboard] == [
        ["menu:profile", "menu:play"],
        ["menu:stats", "menu:notifications"],
        ["menu:help", "menu:hide"],
    ]


# Stage 54 CI verification: exercise the real inline menu builder and its callbacks.
