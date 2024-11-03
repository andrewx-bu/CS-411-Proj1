import pytest

from meal_max.models.battle_model import BattleModel
from meal_max.models.kitchen_model import Meal

#assert for errors and for equality 
@pytest.fixture()
def battle_model():
    """Fixture to provide a new instance of BattleModel """
    return BattleModel()

@pytest.fixture()
def mock_update_play_count(mocker):
    """Mock the get_battle_score for testing purposes"""
    return mocker.patch("meal_max.models.battle_model.battle_model.get_battle_score")

"""Fixtures providing sample combatants for the test"""
@pytest.fixture()
def sample_combatants1():
    return BattleModel([Meal (id=1, meal='Pasta', cuisine= 'Italian', price=12.00,difficulty='High'),
                        Meal(id=2, meal='Dumplings',cuisine= 'Chinese', price=10.00, dfficulty= 'Medium')])

def sample_combatants1():
    return BattleModel([Meal (id=1, meal='Pasta', cuisine= 'Italian', price=12.00,difficulty='High'),
                        Meal(id=2, meal='Dumplings',cuisine= 'Chinese', price=10.00, dfficulty= 'Medium')])

def sample_combatant2():
     return BattleModel([Meal (id=1, meal='Pizza', cuisine= 'Italian', price=11.00,difficulty='Medium'),
                        Meal(id=2, meal='Sushi',cuisine= 'Japanese', price=13.00, dfficulty= 'High')])

def sample_meal1():
    return Meal(id=1, meal='Pizza', cuisine= 'Italian', price=11.00,difficulty='Medium')


def test_clear_combatants(battle_model, sample_combatants1):
    """Test clearing the entire playlist."""
    battle_model.get_combatants(sample_combatants1)

    battle_model.clear_combatants()
    assert len(battle_model.battle) == 0, "combatant list should be empty after clearing"

def test_get_battle_score(combatant = sample_meal1()):
    assert BattleModel.get_battle_score(combatant= sample_meal1()) == 75

def test_get_combatants(battle_model, sample_combatants1):
    """Test successfully retrieving all songs from the playlist."""
    battle_model.battle.extend(sample_combatants)

    all_combatants = battle_model.get_combatants()
    assert len(combatants) == 2
    assert combatants[0].id == 1
    assert combatants[1].id == 2


def test_prep_combatant(battle_model, combatant_data)
    battle_model.prep_combatant(combatant_data)
    assert len(battle_model.combatants) == 1
    assert battle_model.combatants[0] == combatant_data













