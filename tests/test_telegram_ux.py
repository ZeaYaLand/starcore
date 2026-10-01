from handlers.menu import MENU_BUTTONS, main_menu_keyboard


def test_stage54_menu_has_expected_navigation_buttons():
    buttons = [button for row in MENU_BUTTONS for button in row]
    assert buttons == [
        "🧬 Профиль",
        "🎮 Играть",
        "📊 Статистика",
        "🔔 Уведомления",
        "ℹ️ Помощь",
        "❌ Скрыть меню",
    ]
    assert len(buttons) == len(set(buttons))


def test_stage54_keyboard_is_resizable_and_persistent():
    keyboard = main_menu_keyboard()
    assert keyboard.resize_keyboard is True
    assert keyboard.is_persistent is True
    assert keyboard.input_field_placeholder == "Выберите раздел STARCORE"
    assert [[button.text for button in row] for row in keyboard.keyboard] == [
        ["🧬 Профиль", "🎮 Играть"],
        ["📊 Статистика", "🔔 Уведомления"],
        ["ℹ️ Помощь", "❌ Скрыть меню"],
    ]


# Stage 54 CI verification: these tests intentionally exercise the real menu builder.
