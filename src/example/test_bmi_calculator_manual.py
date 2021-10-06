import bmi_calculator
import pytest


def test_bmi_constructor():
    bmi_calc = bmi_calculator.BMICalc(170, 65, 28)
    assert bmi_calc.height == 170
    assert bmi_calc.weight == 65
    assert bmi_calc.age == 28


def test_bmi_value_valid():
    bmi_calc = bmi_calculator.BMICalc(150, 41, 18)
    bmi_value = bmi_calc.bmi_value()
    assert pytest.approx(bmi_value, abs=0.1) == 18.2

    bmi_calc.height = 180
    bmi_calc.weight = 77
    bmi_value = bmi_calc.bmi_value()
    assert pytest.approx(bmi_value, abs=0.1) == 23.7

    bmi_calc.height = 195
    bmi_calc.weight = 95
    bmi_value = bmi_calc.bmi_value()
    assert pytest.approx(bmi_value, abs=0.1) == 24.9

    bmi_calc.height = 165
    bmi_calc.weight = 104
    bmi_value = bmi_calc.bmi_value()
    assert pytest.approx(bmi_value, abs=0.1) == 38.2


# Cases expected to throw exception
def test_invalid_height():
    # Testing Constructors
    with pytest.raises(ValueError) as context:
        bmi_calc = bmi_calculator.BMICalc(-150, 41, 18)

    with pytest.raises(ValueError) as context:
        bmi_calc = bmi_calculator.BMICalc(0, 41, 18)

    # Testing setters
    bmi_calc = bmi_calculator.BMICalc(150, 41, 18)
    with pytest.raises(ValueError) as context:
        bmi_calc.height = -5

    with pytest.raises(ValueError) as context:
        bmi_calc.height = 0


def test_invalid_weight():
    # Testing Constructors
    with pytest.raises(ValueError) as context:
        bmi_calc = bmi_calculator.BMICalc(150, -41, 18)

    with pytest.raises(ValueError) as context:
        bmi_calc = bmi_calculator.BMICalc(150, 0, 18)

    # Testing Setters
    bmi_calc = bmi_calculator.BMICalc(180, 41, 18)
    with pytest.raises(ValueError) as context:
        bmi_calc.weight = 0

    with pytest.raises(ValueError) as context:
        bmi_calc.weight = -5


def test_invalid_age():
    # Testing Constructors
    with pytest.raises(ValueError) as context:
        bmi_calc = bmi_calculator.BMICalc(150, 41, 0)

    with pytest.raises(ValueError) as context:
        bmi_calc = bmi_calculator.BMICalc(150, 41, 1)

    with pytest.raises(ValueError) as context:
        bmi_calc = bmi_calculator.BMICalc(150, 41, -1)

    # Testing Setters
    bmi_calc = bmi_calculator.BMICalc(150, 41, 18)
    with pytest.raises(ValueError) as context:
        bmi_calc.age = 0

    with pytest.raises(ValueError) as context:
        bmi_calc.age = -1


def test_bmi_adult():
    adult_age = 21
    bmi_calc = bmi_calculator.BMICalc(160, 65, 21)
    bmi_class = bmi_calc.classify_bmi_adults()
    assert bmi_class == "Overweight"

    bmi_calc.height = 170
    bmi_calc.weight = 99
    bmi_class = bmi_calc.classify_bmi_adults()
    assert bmi_class == "Obese"

    bmi_calc.height = 182
    bmi_calc.weight = 60
    bmi_class = bmi_calc.classify_bmi_adults()
    assert bmi_class == "Underweight"

    bmi_calc.height = 190
    bmi_calc.weight = 70
    bmi_class = bmi_calc.classify_bmi_adults()
    assert bmi_class == "Normal weight"


def test_bmi_children_7y():
    bmi_calc = bmi_calculator.BMICalc(115, 19, 6)
    bmi_class = bmi_calc.classify_bmi_teens_and_children()
    assert bmi_class == "Overweight"

    bmi_calc.weight = 28
    bmi_class = bmi_calc.classify_bmi_teens_and_children()
    assert bmi_class == "Obese"

    bmi_calc.weight = 17
    bmi_class = bmi_calc.classify_bmi_teens_and_children()
    assert bmi_class == "Underweight"

    bmi_calc.weight = 18
    bmi_class = bmi_calc.classify_bmi_teens_and_children()
    assert bmi_class == "Normal weight"


def test_bmi_children_4y():
    bmi_calc = bmi_calculator.BMICalc(100, 15, 4)
    bmi_class = bmi_calc.classify_bmi_teens_and_children()
    assert bmi_class == "Normal weight"

    bmi_calc.weight = 13
    bmi_class = bmi_calc.classify_bmi_teens_and_children()
    assert bmi_class == "Underweight"

    bmi_calc.weight = 18
    bmi_class = bmi_calc.classify_bmi_teens_and_children()
    assert bmi_class == "Overweight"

    bmi_calc.weight = 22
    bmi_class = bmi_calc.classify_bmi_teens_and_children()
    assert bmi_class == "Obese"


def test_bmi_children_10y():
    bmi_calc = bmi_calculator.BMICalc(140, 31, 10)
    bmi_class = bmi_calc.classify_bmi_teens_and_children()
    assert bmi_class == "Normal weight"

    bmi_calc.weight = 26
    bmi_class = bmi_calc.classify_bmi_teens_and_children()
    assert bmi_class == "Underweight"

    bmi_calc.weight = 42
    bmi_class = bmi_calc.classify_bmi_teens_and_children()
    assert bmi_class == "Overweight"

    bmi_calc.weight = 50
    bmi_class = bmi_calc.classify_bmi_teens_and_children()
    assert bmi_class == "Obese"


def test_bmi_children_13y():
    bmi_calc = bmi_calculator.BMICalc(155, 46, 13)
    bmi_class = bmi_calc.classify_bmi_teens_and_children()
    assert bmi_class == "Normal weight"

    bmi_calc.weight = 35
    bmi_class = bmi_calc.classify_bmi_teens_and_children()
    assert bmi_class == "Underweight"

    bmi_calc.weight = 58
    bmi_class = bmi_calc.classify_bmi_teens_and_children()
    assert bmi_class == "Overweight"

    bmi_calc.weight = 65
    bmi_class = bmi_calc.classify_bmi_teens_and_children()
    assert bmi_class == "Obese"


def test_bmi_children_16y():
    bmi_calc = bmi_calculator.BMICalc(162, 63, 16)
    bmi_class = bmi_calc.classify_bmi_teens_and_children()
    assert bmi_class == "Normal weight"

    bmi_calc.weight = 42
    bmi_class = bmi_calc.classify_bmi_teens_and_children()
    assert bmi_class == "Underweight"

    bmi_calc.weight = 73
    bmi_class = bmi_calc.classify_bmi_teens_and_children()
    assert bmi_class == "Overweight"

    bmi_calc.weight = 80
    bmi_class = bmi_calc.classify_bmi_teens_and_children()
    assert bmi_class == "Obese"


def test_bmi_children_19y():
    bmi_calc = bmi_calculator.BMICalc(163, 57, 19)
    bmi_class = bmi_calc.classify_bmi_teens_and_children()
    assert bmi_class == "Normal weight"

    bmi_calc.weight = 45
    bmi_class = bmi_calc.classify_bmi_teens_and_children()
    assert bmi_class == "Underweight"

    bmi_calc.weight = 75
    bmi_class = bmi_calc.classify_bmi_teens_and_children()
    assert bmi_class == "Overweight"

    bmi_calc.weight = 90
    bmi_class = bmi_calc.classify_bmi_teens_and_children()
    assert bmi_class == "Obese"


def test_bmi_children_invalid():
    bmi_calc = bmi_calculator.BMICalc(163, 57, 25)
    with pytest.raises(ValueError) as context:
        bmi_class = bmi_calc.classify_bmi_teens_and_children()


def test_bmi_adult_invalid():
    bmi_calc = bmi_calculator.BMICalc(170, 65, 15)
    with pytest.raises(ValueError) as context:
        bmi_class = bmi_calc.classify_bmi_adults()
