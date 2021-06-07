import simpleBMI
import pytest

def test_0():
	gender = 'm' 
	height = 918.0 
	weight = 428.0 
	age = 111 
	a = simpleBMI.BMICalc(height, weight, age, gender)
	a.classifyBMI_teensAndChildren()
	a.weight = 491.0 
	a.height = 241.0 
	a.height = 913.0 
	a.classifyBMI_adults()
	a.height = 299.0 
	a.calculateBMI(a.height, a.weight)
	a.gender = 'm' 
	a.gender = 'm' 
	a.age = 363 
	a.classifyBMI_adults()
	a.classifyBMI_adults()
def test_1():
	gender = 'f' 
	height = -2.0 
	weight = 451.0 
	age = 738 
	a = simpleBMI.BMICalc(height, weight, age, gender)
	a.classifyBMI_adults()
	a.weight = 371.0 
	a.classifyBMI_teensAndChildren()
	a.gender = 'm' 
	a.height = 859.0 
	a.calculateBMI(a.height, a.weight)
	a.calculateBMI(a.height, a.weight)
	a.calculateBMI(a.height, a.weight)
	a.classifyBMI_teensAndChildren()
def test_2():
	gender = 'm' 
	height = 731.0 
	weight = -56.0 
	age = 888 
	a = simpleBMI.BMICalc(height, weight, age, gender)
	a.calculateBMI(a.height, a.weight)
	a.height = 183.0 
	a.weight = 452.0 
	a.calculateBMI(a.height, a.weight)
	a.calculateBMI(a.height, a.weight)
def test_3():
	gender = 'm' 
	height = 235.0 
	weight = 390.0 
	age = 239 
	a = simpleBMI.BMICalc(height, weight, age, gender)
	a.height = 215.0 
	a.age = 319 
	a.gender = 'R' 
	a.weight = 706.0 
	a.calculateBMI(a.height, a.weight)
def test_4():
	gender = 'f' 
	height = 903.0 
	weight = 251.0 
	age = 322 
	a = simpleBMI.BMICalc(height, weight, age, gender)
	a.calculateBMI(a.height, a.weight)
	a.height = 752.0 
	a.classifyBMI_teensAndChildren()
	a.height = 656.0 
	a.weight = 606.0 
	a.gender = 'M' 
	a.calculateBMI(a.height, a.weight)
	a.age = 525 
def test_5():
	gender = 'R' 
	height = 481.0 
	weight = 61.0 
	age = -28 
	a = simpleBMI.BMICalc(height, weight, age, gender)
	a.gender = 'f' 
	a.weight = 158.0 
	a.weight = 753.0 
	a.weight = 526.0 
	a.classifyBMI_teensAndChildren()
	a.classifyBMI_adults()
def test_6():
	gender = 'F' 
	height = 713.0 
	weight = 160.0 
	age = 279 
	a = simpleBMI.BMICalc(height, weight, age, gender)
	a.classifyBMI_teensAndChildren()
	a.classifyBMI_teensAndChildren()
	a.height = 271.0 
	a.classifyBMI_teensAndChildren()
def test_7():
	gender = 'R' 
	height = 685.0 
	weight = 528.0 
	age = 713 
	a = simpleBMI.BMICalc(height, weight, age, gender)
	a.classifyBMI_teensAndChildren()
def test_8():
	gender = 'm' 
	height = 611.0 
	weight = 13.0 
	age = -18 
	a = simpleBMI.BMICalc(height, weight, age, gender)
	a.calculateBMI(a.height, a.weight)
	a.height = -93.0 
	a.classifyBMI_adults()
	a.weight = 126.0 
	a.age = 173 
	a.age = 449 
	a.gender = 'R' 
	a.weight = 370.0 
	a.classifyBMI_adults()
	a.calculateBMI(a.height, a.weight)
	a.age = 371 
	a.height = 829.0 
	a.weight = 318.0 
	a.classifyBMI_teensAndChildren()
	a.age = 569 
	a.weight = 563.0 
	a.age = 963 
	a.gender = 'm' 
def test_9():
	gender = 'F' 
	height = 861.0 
	weight = 1.0 
	age = 615 
	a = simpleBMI.BMICalc(height, weight, age, gender)
	a.calculateBMI(a.height, a.weight)
	a.calculateBMI(a.height, a.weight)
	a.classifyBMI_teensAndChildren()
	a.gender = 'R' 
	a.weight = 854.0 
	a.gender = 'M' 
	a.weight = 244.0 
	a.age = 461 
	a.age = -26 
	a.gender = 'F' 
	a.age = 390 
	a.calculateBMI(a.height, a.weight)
	a.gender = 'f' 
	a.classifyBMI_adults()
	a.classifyBMI_adults()
def test_10():
	gender = 'F' 
	height = 77.0 
	weight = 112.0 
	age = 771 
	a = simpleBMI.BMICalc(height, weight, age, gender)
	a.classifyBMI_teensAndChildren()
	a.age = 143 
	a.weight = 78.0 
	a.weight = 630.0 
	a.height = 629.0 
	a.age = 315 
	a.age = 446 
	a.classifyBMI_adults()
	a.age = 297 
	a.calculateBMI(a.height, a.weight)
	a.classifyBMI_adults()
	a.classifyBMI_teensAndChildren()
	a.weight = 535.0 
	a.gender = 'F' 
def test_11():
	gender = 'f' 
	height = 615.0 
	weight = 325.0 
	age = 57 
	a = simpleBMI.BMICalc(height, weight, age, gender)
	a.age = 57 
	a.classifyBMI_adults()
	a.calculateBMI(a.height, a.weight)
	a.weight = 649.0 
	a.weight = 210.0 
	a.weight = 1.0 
	a.calculateBMI(a.height, a.weight)
def test_12():
	gender = 'R' 
	height = 276.0 
	weight = 589.0 
	age = 296 
	a = simpleBMI.BMICalc(height, weight, age, gender)
	a.gender = 'R' 
	a.calculateBMI(a.height, a.weight)
	a.weight = 576.0 
	a.calculateBMI(a.height, a.weight)
	a.height = 222.0 
	a.age = 292 
	a.height = 535.0 
def test_13():
	gender = 'R' 
	height = -8.0 
	weight = 56.0 
	age = 285 
	a = simpleBMI.BMICalc(height, weight, age, gender)
	a.calculateBMI(a.height, a.weight)
	a.age = 223 
	a.classifyBMI_teensAndChildren()
	a.classifyBMI_teensAndChildren()
	a.height = 20.0 
	a.classifyBMI_adults()
	a.gender = 'f' 
	a.age = 465 
	a.height = -48.0 
	a.height = 955.0 
	a.calculateBMI(a.height, a.weight)
	a.age = 806 
	a.calculateBMI(a.height, a.weight)
	a.classifyBMI_adults()
	a.weight = 388.0 
	a.calculateBMI(a.height, a.weight)
	a.height = 739.0 
	a.classifyBMI_teensAndChildren()
def test_14():
	gender = 'F' 
	height = 21.0 
	weight = 588.0 
	age = 131 
	a = simpleBMI.BMICalc(height, weight, age, gender)
	a.gender = 'f' 
	a.age = 512 
	a.age = 46 
	a.calculateBMI(a.height, a.weight)
	a.calculateBMI(a.height, a.weight)
	a.gender = 'f' 
	a.calculateBMI(a.height, a.weight)
	a.classifyBMI_teensAndChildren()
	a.age = 441 
	a.height = 123.0 
	a.height = 774.0 
	a.gender = 'R' 
	a.weight = 603.0 
	a.classifyBMI_teensAndChildren()
	a.weight = 929.0 
	a.classifyBMI_teensAndChildren()
	a.gender = 'f' 
	a.calculateBMI(a.height, a.weight)
def test_15():
	gender = 'R' 
	height = 544.0 
	weight = 403.0 
	age = 406 
	a = simpleBMI.BMICalc(height, weight, age, gender)
	a.height = 332.0 
	a.calculateBMI(a.height, a.weight)
	a.weight = 152.0 
	a.classifyBMI_teensAndChildren()
	a.height = 101.0 
	a.classifyBMI_adults()
	a.classifyBMI_teensAndChildren()
	a.age = 130 
	a.gender = 'R' 
	a.gender = 'F' 
	a.gender = 'f' 
	a.height = 853.0 
def test_16():
	gender = 'f' 
	height = 492.0 
	weight = 726.0 
	age = -18 
	a = simpleBMI.BMICalc(height, weight, age, gender)
	a.classifyBMI_adults()
	a.age = 805 
	a.height = 224.0 
	a.calculateBMI(a.height, a.weight)
def test_17():
	gender = 'M' 
	height = -80.0 
	weight = -20.0 
	age = 60 
	a = simpleBMI.BMICalc(height, weight, age, gender)
	a.age = 953 
	a.calculateBMI(a.height, a.weight)
	a.classifyBMI_adults()
	a.gender = 'F' 
	a.height = 368.0 
	a.gender = 'f' 
	a.classifyBMI_teensAndChildren()
	a.weight = 393.0 
def test_18():
	gender = 'm' 
	height = 470.0 
	weight = -61.0 
	age = 360 
	a = simpleBMI.BMICalc(height, weight, age, gender)
	a.classifyBMI_teensAndChildren()
	a.gender = 'M' 
	a.gender = 'M' 
	a.gender = 'F' 
	a.calculateBMI(a.height, a.weight)
def test_19():
	gender = 'F' 
	height = 616.0 
	weight = 799.0 
	age = 411 
	a = simpleBMI.BMICalc(height, weight, age, gender)
	a.calculateBMI(a.height, a.weight)
	a.calculateBMI(a.height, a.weight)
