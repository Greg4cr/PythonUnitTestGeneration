class BMICalc:

    def __init__(self, height, weight, age, gender):

        try:
            assert height > 0
        except AssertionError :
            raise ValueError("Height can not be zero or a negative number.")        
        try:
            assert weight > 0
        except AssertionError :
            raise ValueError("Weight can not be zero or a negative number.")        
        try:
            assert age >= 0
        except AssertionError :
            raise ValueError("Age can not be a negative number.")         
        try:
            assert age >= 2
        except AssertionError :
            raise ValueError("This calculator is not valid for children under 2 years old.")  
        try:
            assert (gender == 'f' or gender == 'F' or gender == 'm' or gender == 'M')
        except AssertionError :
            raise ValueError("Gender must be 'f' or 'F' for 'female', and 'm' or 'M' for male.")
        
        self.height = height
        self.weight = weight
        self.age = age
        self.gender = gender
    
    def calculateBMI(self, height, weight):
        BMI = weight / (height/100)**2
        #print(f"You BMI is {BMI}")
        return BMI

    
    def classifyBMI_teensAndChildren(self):

        try:
            assert (self.age >= 2 and self.age <= 19)
        except:
            print("The method classifyBMI_teensAndChildren only works for persons between the ages of 2 and 19. Try classifyBMI_adults instead.")

        BMI = self.calculateBMI(self.height, self.weight)
        if (self.gender == 'f' or self.gender == 'F'): #values are an approximation of values from this table: https://www.obesityaction.org/get-educated/understanding-childhood-obesity/what-is-childhood-obesity/girls-bmi-for-age-percentile-chart/
            if self.age <=4:
                if BMI <= 14:
                    return ("You are underweight.")
                elif BMI <= 17.5:
                    return ("You are healthy.")
                elif BMI <= 18.5:
                    return ("You are over weight.")
                else:
                    return ("You are obese.")

            elif self.age <=7:
                if BMI <= 13.5:
                    return ("You are underweight.")
                elif BMI <= 14:
                    return ("You are healthy.")
                elif BMI <= 20:
                    return ("You are over weight.")
                else:
                    return ("You are obese.")

            elif self.age <=10:
                if BMI <= 14:
                    return ("You are underweight.")
                elif BMI <= 20:
                    return ("You are healthy.")
                elif BMI <= 22:
                    return ("You are over weight.")
                else:
                    return ("You are obese.")

            elif self.age <=13:
                if BMI <= 15:
                    return ("You are underweight.")
                elif BMI <= 22:
                    return ("You are healthy.")
                elif BMI <= 26.5:
                    return ("You are over weight.")
                else:
                    return ("You are obese.")

            elif self.age <=16:
                if BMI <= 16.5:
                    return ("You are underweight.")
                elif BMI <= 24.5:
                    return ("You are healthy.")
                elif BMI <= 29:
                    return ("You are over weight.")
                else:
                    return ("You are obese.")

            elif self.age <=19:
                if BMI <= 17.5:
                    return ("You are underweight.")
                elif BMI <= 26.5:
                    return ("You are healthy.")
                elif BMI <= 31:
                    return ("You are over weight.")
                else:
                    return ("You are obese.")

        if (self.gender == 'm' or self.gender == 'M'): #values are an approximation of values from this table: https://www.obesityaction.org/get-educated/understanding-childhood-obesity/what-is-childhood-obesity/boys-bmi-chart/
            if self.age <=4:
                if BMI <= 14.5:
                    return ("You are underweight.")
                elif BMI <= 17.5:
                    return ("You are healthy.")
                elif BMI <= 18.5:
                    return ("You are over weight.")
                else:
                    return ("You are obese.")

            elif self.age <=7:
                if BMI <= 14:
                    return ("You are underweight.")
                elif BMI <= 17.5:
                    return ("You are healthy.")
                elif BMI <= 19.5:
                    return ("You are over weight.")
                else:
                    return ("You are obese.")

            elif self.age <=10:
                if BMI <= 14.5:
                    return ("You are underweight.")
                elif BMI <= 19:
                    return ("You are healthy.")
                elif BMI <= 22:
                    return ("You are over weight.")
                else:
                    return ("You are obese.")

            elif self.age <=13:
                if BMI <= 15.5:
                    return ("You are underweight.")
                elif BMI <= 21.5:
                    return ("You are healthy.")
                elif BMI <= 25:
                    return ("You are over weight.")
                else:
                    return ("You are obese.")

            elif self.age <=16:
                if BMI <= 17:
                    return ("You are underweight.")
                elif BMI <= 23.5:
                    return ("You are healthy.")
                elif BMI <= 27.5:
                    return ("You are over weight.")
                else:
                    return ("You are obese.")

            elif self.age <=19:
                if BMI <= 18.5:
                    return ("You are underweight.")
                elif BMI <= 26:
                    return ("You are healthy.")
                elif BMI <= 29.5:
                    return ("You are over weight.")
                else:
                    return ("You are obese.")



    
    def classifyBMI_adults(self):
        
        
        try:
            assert self.age > 19
        except:
            print("The method classifyBMI_adults only works for persons older than 19 years old. Try classifyBMI_teensAndChildren instead.")


        BMI = self.calculateBMI(self.height, self.weight)
        if self.age > 19:
            if BMI <= 18.4:
                return ("You are underweight.")
            elif BMI <= 24.9:
                return ("You are healthy.")
            elif BMI <= 29.9:
                return ("You are over weight.")
            elif BMI <= 34.9:
                return ("You are severely over weight.")
            elif BMI <= 39.9:
                return ("You are obese.")
            else:
                return ("You are severely obese.")



if __name__ == "__main__":                        
    height=180 #in cm
    weight=90 #in kg
    age=33 #years
    gender=2 #expects ['m','M','f','F']
    
    person1 = BMICalc(height, weight, age, gender)
    
    print(person1.classifyBMI_adults())
    
    height=92 #in cm
    weight=13 #in kg
    age=3 #years
    gender='f' #expects ['m','M','f','F']
    
    person2 = BMICalc(height, weight, age, gender)
    
    print(person2.classifyBMI_teensAndChildren())
    