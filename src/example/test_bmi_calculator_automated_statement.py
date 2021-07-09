import bmi_calculator
import pytest

def test_0():
	cut = bmi_calculator.BMICalc(120,860,13)
	cut.classifyBMI_teensAndChildren()

def test_1():
	cut = bmi_calculator.BMICalc(151,769,97)
	cut.age = 8
	cut.classifyBMI_teensAndChildren()

def test_2():
	cut = bmi_calculator.BMICalc(43,243,59)
	cut.classifyBMI_adults()
	cut.height = 526
	cut.classifyBMI_adults()
	cut.classifyBMI_adults()

def test_3():
	cut = bmi_calculator.BMICalc(118,379,4)
	cut.height = 668
	cut.classifyBMI_teensAndChildren()
	cut.weight = 953
	cut.classifyBMI_teensAndChildren()

def test_4():
	cut = bmi_calculator.BMICalc(598,403,146)
	cut.age = 7
	cut.classifyBMI_teensAndChildren()

def test_5():
	cut = bmi_calculator.BMICalc(374,343,17)
	cut.age = 123
	cut.classifyBMI_adults()
	cut.age = 18
	cut.classifyBMI_teensAndChildren()
	cut.weight = 396
	cut.classifyBMI_teensAndChildren()

def test_6():
	cut = bmi_calculator.BMICalc(476,779,46)
	cut.age = 6
	cut.classifyBMI_teensAndChildren()

def test_7():
	cut = bmi_calculator.BMICalc(609,-1,94)

def test_8():
	cut = bmi_calculator.BMICalc(982,35,62)
	cut.age = 9
	cut.classifyBMI_teensAndChildren()

def test_9():
	cut = bmi_calculator.BMICalc(550,193,18)
	cut.classifyBMI_teensAndChildren()

def test_10():
	cut = bmi_calculator.BMICalc(443,74,-1)

def test_11():
	cut = bmi_calculator.BMICalc(491,712,20)
	cut.classifyBMI_adults()

def test_12():
	cut = bmi_calculator.BMICalc(559,667,13)
	cut.classifyBMI_teensAndChildren()

def test_13():
	cut = bmi_calculator.BMICalc(813,233,30)
	cut.height = 482
	cut.weight = 885
	cut.classifyBMI_adults()

def test_14():
	cut = bmi_calculator.BMICalc(407,326,1)

def test_15():
	cut = bmi_calculator.BMICalc(584,861,15)
	cut.classifyBMI_teensAndChildren()
	cut.height = -1

def test_16():
	cut = bmi_calculator.BMICalc(896,536,11)
	cut.classifyBMI_teensAndChildren()

def test_17():
	cut = bmi_calculator.BMICalc(608,717,6)
	cut.classifyBMI_teensAndChildren()
	cut.age = 91
	cut.classifyBMI_teensAndChildren()
	cut.classifyBMI_teensAndChildren()

def test_18():
	cut = bmi_calculator.BMICalc(172,345,15)
	cut.classifyBMI_teensAndChildren()
	cut.height = 705
	cut.classifyBMI_teensAndChildren()
	cut.classifyBMI_teensAndChildren()

def test_19():
	cut = bmi_calculator.BMICalc(288,515,18)
	cut.classifyBMI_teensAndChildren()

def test_20():
	cut = bmi_calculator.BMICalc(512,574,9)
	cut.classifyBMI_teensAndChildren()
	cut.classifyBMI_adults()

def test_21():
	cut = bmi_calculator.BMICalc(488,141,62)
	cut.weight = 563
	cut.age = 14
	cut.classifyBMI_teensAndChildren()
