from unittest.mock import Mock
import pytest
from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient

class TestBurger:  
    def setup_method(self):
        self.burger = Burger()

    def test_set_buns(self):
        bun_mock = Mock(spec=Bun)
        self.burger.set_buns(bun_mock)
        assert self.burger.bun == bun_mock

    def test_add_ingredient(self):
        ingredient_mock = Mock(spec=Ingredient)
        self.burger.add_ingredient(ingredient_mock)
        assert len(self.burger.ingredients) == 1
        assert self.burger.ingredients[0] == ingredient_mock

    def test_remove_ingredient(self):
        ingredient_mock = Mock(spec=Ingredient)
        self.burger.add_ingredient(ingredient_mock)
        self.burger.remove_ingredient(0)
        assert len(self.burger.ingredients) == 0

    def test_move_ingredient(self):
        ingredient1 = Mock(spec=Ingredient)
        ingredient2 = Mock(spec=Ingredient)
        ingredient3 = Mock(spec=Ingredient) 
        self.burger.add_ingredient(ingredient1)
        self.burger.add_ingredient(ingredient2)
        self.burger.add_ingredient(ingredient3)
        self.burger.move_ingredient(2, 0)
        
        assert self.burger.ingredients[0] == ingredient3
        assert self.burger.ingredients[1] == ingredient1
        assert self.burger.ingredients[2] == ingredient2
    
    @pytest.mark.parametrize("bun_price, ingredients_prices, expected_price", [(100, [], 200),(100, [50], 250),(100, [50, 30, 20], 300),(200, [100, 50], 550),])
    
    def test_get_price(self, bun_price, ingredients_prices, expected_price):
        bun_mock = Mock(spec=Bun)
        bun_mock.get_price.return_value = bun_price
        self.burger.set_buns(bun_mock)
        for price in ingredients_prices:
            ingredient_mock = Mock(spec=Ingredient)
            ingredient_mock.get_price.return_value = price
            self.burger.add_ingredient(ingredient_mock)
        
        assert self.burger.get_price() == expected_price
    
    def test_get_receipt(self):
        bun_mock = Mock(spec=Bun)
        bun_mock.get_name.return_value = "Test Bun"
        bun_mock.get_price.return_value = 100
        
        self.burger.set_buns(bun_mock)
        
        ingredient1_mock = Mock(spec=Ingredient)
        ingredient1_mock.get_name.return_value = "Test Ingredient 1"
        ingredient1_mock.get_type.return_value = "SAUCE"
        ingredient1_mock.get_price.return_value = 50
        ingredient2_mock = Mock(spec=Ingredient)
        ingredient2_mock.get_name.return_value = "Test Ingredient 2"
        ingredient2_mock.get_type.return_value = "FILLING"
        ingredient2_mock.get_price.return_value = 30
        
        self.burger.add_ingredient(ingredient1_mock)
        self.burger.add_ingredient(ingredient2_mock)
        
        actual_receipt = self.burger.get_receipt()
        lines = actual_receipt.split('\n')
        
        assert lines[0] == "(==== Test Bun ====)"
        assert lines[1] == "= sauce Test Ingredient 1 ="
        assert lines[2] == "= filling Test Ingredient 2 ="
        assert lines[3] == "(==== Test Bun ====)"
        assert lines[4] == ""
        assert lines[5] == "Price: 280"
