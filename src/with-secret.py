import secrets
import os
import random
import time

class SecureLotteryGenerator:
    """Cryptographically secure lottery number generator"""
    
    @staticmethod
    def generate_powerball():
        """Generate secure Powerball numbers"""
        # Method 1: Using secrets (simplest and recommended)
        main_numbers = []
        available = list(range(1, 36))
        
        for _ in range(7):
            num = secrets.choice(available)
            main_numbers.append(num)
            available.remove(num)
        
        main_numbers.sort()
        powerball = secrets.choice(range(1, 21))
        
        return main_numbers, powerball
    
    @staticmethod
    def generate_tickets(num_tickets=1):
        """Generate multiple tickets"""
        return [SecureLotteryGenerator.generate_powerball() 
                for _ in range(num_tickets)]
    
    @staticmethod
    def display_ticket(main_numbers, powerball, ticket_num=None):
        """Display a ticket nicely"""
        # if ticket_num:
        #     print(f"\nTicket #{ticket_num}")
        print(f"  Main: {' '.join(f'{n:2d}' for n in main_numbers)}       PB:{powerball:2d}")
        # print(f"  PB:   {powerball:2d}")


# Main execution
if __name__ == "__main__":
    print("=" * 60)
    print("SECURE POWERBALL NUMBER GENERATOR")
    print("=" * 60)
    
    # Generate secure tickets
    num_tickets = int(input("\nHow many secure tickets to generate? "))
    tickets = SecureLotteryGenerator.generate_tickets(num_tickets)
    
    print("\nYour Secure Tickets:")
    print("-" * 40)
    for i, (main, pb) in enumerate(tickets, 1):
        SecureLotteryGenerator.display_ticket(main, pb, i)
    
