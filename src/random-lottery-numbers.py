import random

def generate_powerball_numbers():
    """Generate 7 main numbers (1-35) and 1 Powerball (1-20)"""
    main_numbers = sorted(random.sample(range(1, 36), 7))
    powerball = random.randint(1, 20)
    return main_numbers, powerball

# Generate and display 1 ticket
main_numbers, powerball = generate_powerball_numbers()
print(f"Main Numbers: {' '.join(map(str, main_numbers))}")
print(f"Powerball: {powerball}")

# Generate and display 5 tickets
print("\n5 Random Tickets:")
for i in range(5):
    main_numbers, powerball = generate_powerball_numbers()
    print(f"Ticket {i+1}: {' '.join(map(str, main_numbers))} | PB {powerball}")