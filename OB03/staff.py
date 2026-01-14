class Staff:
    def __init__(self, name):
        self.name = name

class ZooKeeper(Staff):
    def feed_animal(self, animal):
        print(f"{self.name} is feeding {animal.name}.")

class Veterinarian(Staff):
    def heal_animal(self, animal):
        print(f"{self.name} is healing {animal.name}.")
