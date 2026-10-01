from handlers.menu import MENU_BUTTONS, main_menu_keyboard
from handlers.sections import SECTION_LABELS, sections_keyboard


def test_main_menu_contains_all_core_sections_without_duplicate_labels_or_callbacks():
    buttons = [(text, callback) for row in MENU_BUTTONS for text, callback in row]
    labels = [text for text, _ in buttons]
    callbacks = [callback for _, callback in buttons]

    assert len(labels) == len(set(labels))
    assert len(callbacks) == len(set(callbacks))

    expected_callbacks = {
        "menu:profile",
        "menu:play",
        "menu:stats",
        "section:inventory",
        "section:missions",
        "section:achievements",
        "section:ranking",
        "section:social",
        "section:guild",
        "section:trading",
        "section:shop",
        "section:systems",
        "menu:notifications",
        "menu:help",
        "section:all",
        "menu:hide",
    }
    assert set(callbacks) == expected_callbacks


def test_main_menu_keyboard_matches_button_definition():
    keyboard = main_menu_keyboard()
    actual = [
        [(button.text, button.callback_data) for button in row]
        for row in keyboard.inline_keyboard
    ]
    expected = [list(row) for row in MENU_BUTTONS]
    assert actual == expected


def test_all_sections_keyboard_has_unique_navigation_callbacks():
    keyboard = sections_keyboard()
    callbacks = [
        button.callback_data
        for row in keyboard.inline_keyboard
        for button in row
    ]
    assert len(callbacks) == len(set(callbacks))
    assert {f"section:{key}" for key in SECTION_LABELS} <= set(callbacks)
    assert "section:menu" in callbacks
