from animal import Bird, Mammal, Reptile, animal_sound
from staff import ZooKeeper, Veterinarian
from zoo import Zoo

def main():
    # Create Zoo
    my_zoo = Zoo()

    # Create Animals
    parrot = Bird("Polly", 2)
    lion = Mammal("Simba", 5)
    snake = Reptile("Kaa", 3)

    # Create Staff
    keeper = ZooKeeper("Alice")
    vet = Veterinarian("Bob")

    # Add to Zoo
    print("--- Adding inhabitants ---")
    my_zoo.add_animal(parrot)
    my_zoo.add_animal(lion)
    my_zoo.add_animal(snake)
    my_zoo.add_staff(keeper)
    my_zoo.add_staff(vet)

    # Demonstrate Polymorphism
    print("\n--- Animal Sounds ---")
    animal_sound(my_zoo.animals)

    # Demonstrate Staff Actions
    print("\n--- Staff Actions ---")
    keeper.feed_animal(lion)
    vet.heal_animal(snake)

    # Save State
    print("\n--- Saving State ---")
    my_zoo.save_to_file("zoo_state.txt")

    # Load State into new object
    print("\n--- Loading State into new Zoo ---")
    new_zoo = Zoo()
    new_zoo.load_from_file("zoo_state.txt")

    print("\n--- Verifying Loaded Zoo ---")
    print(f"Animals in new zoo: {len(new_zoo.animals)}")
    print(f"Staff in new zoo: {len(new_zoo.staff)}")
    for animal in new_zoo.animals:
        print(f"Restored Animal: {animal.name}, Age: {animal.age}")
    
    print("\n--- Testing Restored Polymorphism ---")
    animal_sound(new_zoo.animals)

if __name__ == "__main__":
    main()
