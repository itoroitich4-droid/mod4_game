import pytest
from game_logic.auth import AccountManager

@pytest.fixture
def manager():
    return AccountManager()

def test_register_user_success(manager):
    result = manager.register_user("alice", 25)
    assert result is True
    assert manager.is_active("alice") is True


def test_register_duplicate_user_returns_false(manager):
    manager.register_user("bob", 30)
    result = manager.register_user("bob", 30)  # Try registering again
    assert result is False


@pytest.mark.parametrize("invalid_username", ["", None, 123])
def test_register_invalid_username_raises_error(manager, invalid_username):
    with pytest.raises(ValueError, match="Invalid username"):
        manager.register_user(invalid_username, 25)


def test_register_underage_user_raises_error(manager):
    with pytest.raises(ValueError, match="User must be at least 18 years old"):
        manager.register_user("charlie", 17)


def test_is_active_for_non_existent_user(manager):
    assert manager.is_active("ghost_user") is False