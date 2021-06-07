import simpleBMI
import pytest


#Creation tests that are expected to FAIL.
@pytest.mark.xfail(strict=True)
def test_BMICalcFail():
    assert simpleBMI.BMICalc(180, 90, 20, 1) #invalid gender (numeric)
    assert simpleBMI.BMICalc(-180, 90, 20, 'f') #invalid height (negative)
    assert simpleBMI.BMICalc(180, -90, 20, 'F') #invalid weight (negative)
    assert simpleBMI.BMICalc(180, 90, -20, 'm') #invalid age (negative)
    assert simpleBMI.BMICalc(180, 90, 1, 'M') #invalid age (under two)
    

#Creation tests that are expected to PASS.
def test_BMICalc():
    #low values & valid gender
    assert simpleBMI.BMICalc(1, 1, 2, 'f') 
    assert simpleBMI.BMICalc(1, 1, 2, 'F') 
    assert simpleBMI.BMICalc(1, 1, 2, 'M') 
    assert simpleBMI.BMICalc(1, 1, 2, 'm') 
    #high values & valid gender
    assert simpleBMI.BMICalc(999, 999, 999, 'f') 
    assert simpleBMI.BMICalc(999, 999, 999, 'F') 
    assert simpleBMI.BMICalc(999, 999, 999, 'M') 
    assert simpleBMI.BMICalc(999, 999, 999, 'm')

#Calculation tests that are expected to FAIL.
@pytest.mark.xfail(strict=True)    
def test_classifyBMIFail():
    #children/teen fail at the lower age border
    p1 = simpleBMI.BMICalc(1, 1, 2, 'f') #female & low height & low weight
    assert p1.classifyBMI_adults()
    p1 = simpleBMI.BMICalc(1, 1, 2, 'm') #male & low height & low weight
    assert p1.classifyBMI_adults()
    p1 = simpleBMI.BMICalc(999, 999, 2, 'f') #female & high height & high weight
    assert p1.classifyBMI_adults()
    p1 = simpleBMI.BMICalc(999, 999, 2, 'm') #male & high height & high weight
    assert p1.classifyBMI_adults()
    
    #children/teen fail at the higher age border
    p1 = simpleBMI.BMICalc(1, 1, 19, 'f') #female & low height & low weight
    assert p1.classifyBMI_adults()
    p1 = simpleBMI.BMICalc(1, 1, 19, 'm') #male & low height & low weight
    assert p1.classifyBMI_adults()
    p1 = simpleBMI.BMICalc(999, 999, 19, 'f') #female & high height & high weight
    assert p1.classifyBMI_adults()
    p1 = simpleBMI.BMICalc(999, 999, 19, 'm') #male & high height & high weight
    assert p1.classifyBMI_adults()
    
    #adult fail at the lower age border
    p2 = simpleBMI.BMICalc(1, 1, 20, 'f') #female & low height & low weight
    assert p1.classifyBMI_teensAndChildren()
    p2 = simpleBMI.BMICalc(1, 1, 20, 'm') #male & low height & low weight
    assert p1.classifyBMI_teensAndChildren()
    p2 = simpleBMI.BMICalc(999, 999, 20, 'f') #female & high height & high weight
    assert p1.classifyBMI_teensAndChildren()
    p2 = simpleBMI.BMICalc(999, 999, 20, 'm') #male & high height & high weight
    assert p1.classifyBMI_teensAndChildren()
    
    #adult fail at the higher age border
    p2 = simpleBMI.BMICalc(1, 1, 999, 'f') #female & low height & low weight
    assert p1.classifyBMI_teensAndChildren()
    p2 = simpleBMI.BMICalc(1, 1, 999, 'm') #male & low height & low weight
    assert p1.classifyBMI_teensAndChildren()
    p2 = simpleBMI.BMICalc(999, 999, 999, 'f') #female & high height & high weight
    assert p1.classifyBMI_teensAndChildren()
    p2 = simpleBMI.BMICalc(999, 999, 999, 'm') #male & high height & high weight
    assert p1.classifyBMI_teensAndChildren()
    
    
#Calculation tests that are expected to PASS.
def test_classifyBMIPass():
    #children/teen at the lower age border
    p1 = simpleBMI.BMICalc(1, 1, 2, 'f') #female & low height & low weight
    assert p1.classifyBMI_teensAndChildren()
    p1 = simpleBMI.BMICalc(1, 1, 2, 'm') #male & low height & low weight
    assert p1.classifyBMI_teensAndChildren()
    p1 = simpleBMI.BMICalc(999, 999, 2, 'f') #female & high height & high weight
    assert p1.classifyBMI_teensAndChildren()
    p1 = simpleBMI.BMICalc(999, 999, 2, 'm') #male & high height & high weight
    assert p1.classifyBMI_teensAndChildren()
    
    #children/teen at the higher age border
    p1 = simpleBMI.BMICalc(1, 1, 19, 'f') #female & low height & low weight
    assert p1.classifyBMI_teensAndChildren()
    p1 = simpleBMI.BMICalc(1, 1, 19, 'm') #male & low height & low weight
    assert p1.classifyBMI_teensAndChildren()
    p1 = simpleBMI.BMICalc(999, 999, 19, 'f') #female & high height & high weight
    assert p1.classifyBMI_teensAndChildren()
    p1 = simpleBMI.BMICalc(999, 999, 19, 'm') #male & high height & high weight
    assert p1.classifyBMI_teensAndChildren()
    
    #adult at the lower age border
    p2 = simpleBMI.BMICalc(1, 1, 20, 'f') #female & low height & low weight
    assert p2.classifyBMI_adults()
    p2 = simpleBMI.BMICalc(1, 1, 20, 'm') #male & low height & low weight
    assert p2.classifyBMI_adults()
    p2 = simpleBMI.BMICalc(999, 999, 20, 'f') #female & high height & high weight
    assert p2.classifyBMI_adults()
    p2 = simpleBMI.BMICalc(999, 999, 20, 'm') #male & high height & high weight
    assert p2.classifyBMI_adults()
    
    #adult at the higher age border
    p2 = simpleBMI.BMICalc(1, 1, 999, 'f') #female & low height & low weight
    assert p2.classifyBMI_adults()
    p2 = simpleBMI.BMICalc(1, 1, 999, 'm') #male & low height & low weight
    assert p2.classifyBMI_adults()
    p2 = simpleBMI.BMICalc(999, 999, 999, 'f') #female & high height & high weight
    assert p2.classifyBMI_adults()
    p2 = simpleBMI.BMICalc(999, 999, 999, 'm') #male & high height & high weight
    assert p2.classifyBMI_adults()
    