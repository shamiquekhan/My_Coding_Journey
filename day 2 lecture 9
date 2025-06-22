"""oops part 2 """
"""del keywords"""
# class Student:
#     def __init__(self,name,marks):
#         self.name = name
#         self.marks = marks
#     def get_avg(self):
#         sum =0
#         for i in self.marks:
#             sum+=i
#         print("hi", self.name,"your avg marks is ",sum/3)
# s1=Student("shamique Khan",[99,98,97])
# print(s1.name,s1.marks)
# s1.get_avg()
# del s1.marks
# print(s1.name,s1.marks) #error message
#----------------------------------------------------------------
"""private attribute & methods"""
# private attribute & methods can be assesed by interal fuction in a class but not outside the class
# class Account:
#     def __init__(self,bal,acc): #now private, cant be accesd outside the class
#         self.__bal = bal
#         self.acc =acc
# acc1=Account("shamique", 12334)
# print(acc1.__bal)
#----------------------------------------------------------------
"""inheritance"""
#when one class(child/derived) derives the properties & methods of other class (parent)
class Car:
    color="black"
    modal="SUV"
    @staticmethod
    def start ():
        print("car started")
    @staticmethod
    def stop():
        print("car stopped")
class ToyotaCar(Car): #single inheritance
    def __init__(self,name):
        self.name = name
car1=ToyotaCar("fortuner")
car2=ToyotaCar("Prius")
print(car1.name)
print(car1.modal)
print(car2.stop())
#---------------------------------------------------------------------------------------------------
"""types : single , multilevel and multiple inhertence"""
class Fortuner(ToyotaCar) : #multilevel and multiple inhertence
    def __init__(self,name):
        self.name=name
car5=Fortuner("x12")
print(car5.color)
class Prius(Car,Fortuner): #multiple inhertence
    def __init__(self,name):
        self.name=name
cr=Prius("fortuner112")
print(cr.color)
#---------------------------------------------------------------------------------------------------
"""super method"""
#used to access methods of parent class
#just add super().fuction (eg ; stop(), start()
#) in child to access attributes of the parent class
#---------------------------------------------------------------------------------------------------
"""class method"""
#bound to a class and recieve the class as an implici first argument
""" @classmethod """ #used at starting of the class
#used to give the value to whole class
#=======================================================================================
# """property decorator method"""

