from animal import Bird, Mammal, Reptile
from staff import ZooKeeper, Veterinarian

class Zoo:
    def __init__(self):
        self.animals = []
        self.staff = []

    def add_animal(self, animal):
        self.animals.append(animal)
        print(f"Added {animal.name} to the zoo.")

    def add_staff(self, staff_member):
        self.staff.append(staff_member)
        print(f"Added {staff_member.name} to the staff.")

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            for animal in self.animals:
                # Format: AnimalClass,Name,Age
                f.write(f"{animal.__class__.__name__},{animal.name},{animal.age}\n")
            
            f.write("---\n") # Separator between animals and staff
            
            for member in self.staff:
                # Format: StaffClass,Name
                f.write(f"{member.__class__.__name__},{member.name}\n")
        
        print(f"Zoo state saved to {filename}")

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                content = f.read()
            
            # Clear current state
            self.animals = []
            self.staff = []

            # Split content by separator
            parts = content.split("---")
            animal_lines = parts[0].strip().split('\n')
            staff_lines = parts[1].strip().split('\n') if len(parts) > 1 else []

            for line in animal_lines:
                if not line: continue
                parts = line.split(',')
                if len(parts) == 3:
                    type_str, name, age = parts
                    age = int(age)
                    if type_str == "Bird":
                        self.animals.append(Bird(name, age))
                    elif type_str == "Mammal":
                        self.animals.append(Mammal(name, age))
                    elif type_str == "Reptile":
                        self.animals.append(Reptile(name, age))

            for line in staff_lines:
                if not line: continue
                parts = line.split(',')
                if len(parts) == 2:
                    type_str, name = parts
                    if type_str == "ZooKeeper":
                        self.staff.append(ZooKeeper(name))
                    elif type_str == "Veterinarian":
                        self.staff.append(Veterinarian(name))
            
            print(f"Zoo state loaded from {filename}")
        except FileNotFoundError:
            print(f"File {filename} not found.")
