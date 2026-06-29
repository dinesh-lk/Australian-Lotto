import secrets

class SecureOzLottoGenerator:
    """Cryptographically secure Oz Lotto number generator"""

    @staticmethod
    def generate_ozlotto():
        """Generate secure Oz Lotto numbers (7 from 47)"""

        available = list(range(1, 48))  # Numbers 1-47
        numbers = []

        for _ in range(7):
            num = secrets.choice(available)
            numbers.append(num)
            available.remove(num)

        numbers.sort()
        return numbers

    @staticmethod
    def generate_tickets(num_tickets=1):
        """Generate multiple Oz Lotto tickets"""
        return [
            SecureOzLottoGenerator.generate_ozlotto()
            for _ in range(num_tickets)
        ]

    @staticmethod
    def display_ticket(numbers, ticket_num=None):
        """Display one ticket"""

        if ticket_num:
            print(f"Ticket {ticket_num:2d}: ", end="")

        print(" ".join(f"{n:2d}" for n in numbers))


# Main execution
if __name__ == "__main__":

    print("=" * 60)
    print("SECURE OZ LOTTO NUMBER GENERATOR")
    print("=" * 60)

    num_tickets = int(input("\nHow many tickets to generate? "))

    tickets = SecureOzLottoGenerator.generate_tickets(num_tickets)

    print("\nYour Oz Lotto Tickets")
    print("-" * 60)

    for i, ticket in enumerate(tickets, 1):
        SecureOzLottoGenerator.display_ticket(ticket, i)

    