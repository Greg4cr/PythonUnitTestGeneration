import simpleBMI
import os
from xml.dom import minidom
import random
import string

def selectAction(x):
    if x==1:
        f.write("\ta.gender = \'%d\' \n" % random.randint(-1,2))
    if x==2:
        f.write("\ta.height = %d.0 \n" % random.randint(-99,999))
    if x==3:
        f.write("\ta.weight = %d.0 \n" % random.randint(-99,999))
    if x==4:
        f.write("\ta.age = %d \n" % random.randint(-99,999))
    if x==5:
        f.write("\ta.calculateBMI(a.height, a.weight)\n")
    if x==6:
        f.write("\ta.classifyBMI_teensAndChildren()\n")
    if x==7:
        f.write("\ta.classifyBMI_adults()\n")
        
        
#CREATE AND SAVE A TEST CASE PYTHON FILE
f= open("test_simpleBMI.py","w+") #overwrites the old file with this name

f.write("import simpleBMI\nimport pytest\n\n")

nTestsCases = random.randint(1,20)

for i in range(nTestsCases):
    
    #INSTANTIATE AN OBJECT
    f.write("def test_%d():\n" % i)
    f.write("\tgender = \'%d\' \n" % random.randint(-1,2))
    f.write("\theight = %d.0 \n" % random.randint(-99,999))
    f.write("\tweight = %d.0 \n" % random.randint(-99,999))
    f.write("\tage = %d \n" % random.randint(-99,999))
    f.write("\ta = simpleBMI.BMICalc(height, weight, age, gender)\n")
    
    nActions = random.randint(1,20)
    
    for j in range(nActions):
        action = random.randint(1,7)
        selectAction(action)
    
    
f.close() #changes are only saved after closed
os.system("pytest -v --cov=simpleBMI --cov-report term-missing --cov-report xml")
xmldoc = minidom.parse('coverage.xml')
tag = xmldoc.getElementsByTagName('coverage') 
print (tag[0].attributes['line-rate'].value)
