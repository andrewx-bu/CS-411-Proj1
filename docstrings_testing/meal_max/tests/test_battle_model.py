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





