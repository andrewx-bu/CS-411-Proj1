import pytest

from meal_max.models.battle_model import BattleModel
from meal_max.models.kitchen_model import Meal


@pytest.fixture()
def battle_model():
    """Fixture to provide a new instance of BattleModel for each test."""
    return BattleModel()

@pytest.fixture
def mock_update_meal_stats(mocker):
    """Mock the update_meal_stats function for testing purposes."""
    return mocker.patch("meal_max.models.battle_model.update_meal_stats")

"""Fixtures providing sample meals for the tests."""
@pytest.fixture
def sample_meal1():
    return Meal(id = 1, meal = "Fentanyl", price = 99.9, cuisine = "American", difficulty = "HIGH")

@pytest.fixture
def sample_meal2():
    return Meal(id = 2, meal = "Pasta", price = 7.5, cuisine = "Italian", difficulty = "LOW")

@pytest.fixture
def sample_combatants(sample_meal1, sample_meal2):
    return [sample_meal1, sample_meal2]


##################################################
# Add Meal Management Test Cases
##################################################

def test_add_meal_to_battle(battle_model, sample_meal1):
    """Test adding a meal to the battle."""
    battle_model.prep_combatant(sample_meal1)
    assert len(battle_model.combatants) == 1
    assert battle_model.combatants[0].meal == 'Fentanyl'

def test_add_more_than_two_meals_to_battle(battle_model, sample_meal1, sample_meal2):
    """Test error when adding more than two meals to the battle."""
    battle_model.prep_combatant(sample_meal1)
    battle_model.prep_combatant(sample_meal2)
    with pytest.raises(ValueError, match="Combatant list is full, cannot add more combatants."):
        battle_model.prep_combatant(sample_meal1)

##################################################
# Remove Meal Management Test Cases
##################################################

def test_clear_battle(battle_model, sample_meal1, sample_meal2, caplog):
    """Test clearing all combatants from the battle."""
    battle_model.prep_combatant(sample_meal1)
    battle_model.prep_combatant(sample_meal2)

    battle_model.clear_combatants()
    assert len(battle_model.combatants) == 0, "Combatants list should be empty after clearing"
    assert "Clearing the combatants list." in caplog.text, "Expected log not found"

##################################################
# Combatants and Battle Score Retrieval Test Cases
##################################################

def test_get_combatants(battle_model, sample_meal1, sample_meal2):
    """Test successfully retrieving combatants list."""
    battle_model.prep_combatant(sample_meal1)
    battle_model.prep_combatant(sample_meal2)

    combatants = battle_model.get_combatants()
    assert len(combatants) == 2
    assert combatants[0].id == sample_meal1.id
    assert combatants[1].id == sample_meal2.id

def test_get_battle_score(battle_model, sample_meal1, sample_meal2):
    """Test successfully retrieving the battle score for a combatant."""
    battle_model.prep_combatant(sample_meal1)
    battle_model.prep_combatant(sample_meal2)

    difficulty_modifier = {"HIGH": 1, "MED": 2, "LOW": 3}
    score1 = (sample_meal1.price * len(sample_meal1.cuisine)) - difficulty_modifier[sample_meal1.difficulty]
    score2 = (sample_meal2.price * len(sample_meal2.cuisine)) - difficulty_modifier[sample_meal2.difficulty]
    battle_score1 = battle_model.get_battle_score(sample_meal1)
    battle_score2 = battle_model.get_battle_score(sample_meal2)

    # Assertions for score calculations
    assert battle_score1 == score1, f"Expected score for meal 1 to be {score1}, but got {battle_score1}"
    assert battle_score2 == score2, f"Expected score for meal 2 to be {score2}, but got {battle_score2}"

def test_battle(battle_model, sample_meal1, sample_meal2):
    """Test successfully retrieving the battle score for a combatant."""
    battle_model.prep_combatant(sample_meal1)
    battle_model.prep_combatant(sample_meal2)

    difficulty_modifier = {"HIGH": 1, "MED": 2, "LOW": 3}
    battle_score1 = battle_model.get_battle_score(sample_meal1)
    battle_score2 = battle_model.get_battle_score(sample_meal2)

    winner = battle_model.battle()
    if battle_score1 > battle_score2:
        expected_winner = sample_meal1.meal
    else:
        expected_winner = sample_meal2.meal

    assert winner == expected_winner, f"Expected winner to be {expected_winner}, but got {winner}"

def test_battle_one_combatant(battle_model, sample_meal1):
    """ValueError should be raised when there is only one combatant."""
    battle_model.prep_combatant(sample_meal1)
    with pytest.raises(ValueError, match="Two combatants are required for a battle"):
        battle_model.battle()