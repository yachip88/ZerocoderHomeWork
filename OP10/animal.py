class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def make_sound(self):
        pass

    def eat(self):
        print(f"{self.name} is eating.")

class Bird(Animal):
    def make_sound(self):
        print("Chirp")

class Mammal(Animal):
    def make_sound(self):
        print("Roar")

class Reptile(Animal):
    def make_sound(self):
        print("Hiss")

def animal_sound(animals):
    for animal in animals:
        animal.make_sound()
