from collections import Counter
import re
import os

def count_powerball_numbers(filename):
    main_counts = Counter()
    pb_counts = Counter()
    
    pattern = r'\d{4} \| .*? \| ([\d\s]+) \| PB (\d+)'
    
    with open(filename, 'r') as f:
        for line in f:
            if line.strip().startswith('=====') or not line.strip():
                continue
            
            match = re.search(pattern, line)
            if match:
                main_nums = [int(n) for n in match.group(1).split()]
                pb_num = int(match.group(2))
                
                main_counts.update(main_nums)
                pb_counts[pb_num] += 1
    
    return main_counts, pb_counts

def save_results_to_file(filename, main_counts, pb_counts, total_main_draws, total_pb_draws):
    # Delete file if it exists
    if os.path.exists(filename):
        os.remove(filename)
        print(f"Existing file '{filename}' deleted.")
    
    # Open file for writing
    with open(filename, 'w') as f:
        # Write header
        f.write("=" * 80 + "\n")
        f.write("AUSTRALIAN POWERBALL PROBABILITY ANALYSIS (2018-2026)\n")
        f.write("=" * 80 + "\n\n")
        
        # Write summary statistics
        f.write("SUMMARY STATISTICS\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Main Draws Analyzed: {total_main_draws}\n")
        f.write(f"Total Main Numbers Drawn: {total_main_draws * 7}\n")
        f.write(f"Total Jackpot Draws Analyzed: {total_pb_draws}\n")
        f.write(f"Total Jackpot Numbers Drawn: {total_pb_draws}\n\n")
        
        # Main numbers section - SORTED BY FREQUENCY (DESCENDING)
        f.write("=" * 80 + "\n")
        f.write("MAIN NUMBERS FREQUENCY & PROBABILITY (Numbers 1-35)\n")
        f.write("=" * 80 + "\n")
        f.write(f"{'Rank':<8} {'Number':<10} {'Frequency':<15} {'Probability':<15} {'Expected %':<15}\n")
        f.write("-" * 80 + "\n")
        
        # Sort by frequency (highest first)
        sorted_main = sorted(main_counts.items(), key=lambda x: x[1], reverse=True)
        total_main_occurrences = total_main_draws * 7
        expected_percentage = (1/35) * 100
        
        # Display all numbers 1-35 sorted by frequency
        rank = 1
        for num, count in sorted_main:
            probability = (count / total_main_occurrences) * 100
            f.write(f"{rank:<8} {num:<10} {count:<15} {probability:<14.2f}% {expected_percentage:<14.2f}%\n")
            rank += 1
        
        # Add missing numbers (count = 0) at the end
        all_numbers = set(range(1, 36))
        found_numbers = set(main_counts.keys())
        missing_numbers = all_numbers - found_numbers
        
        for num in sorted(missing_numbers):
            f.write(f"{rank:<8} {num:<10} {0:<15} {0:<14.2f}% {expected_percentage:<14.2f}%\n")
            rank += 1
        
        # Jackpot numbers section - SORTED BY FREQUENCY (DESCENDING)
        f.write("\n" + "=" * 80 + "\n")
        f.write("JACKPOT (PB) NUMBERS FREQUENCY & PROBABILITY (Numbers 1-20)\n")
        f.write("=" * 80 + "\n")
        f.write(f"{'Rank':<8} {'Number':<10} {'Frequency':<15} {'Probability':<15} {'Expected %':<15}\n")
        f.write("-" * 80 + "\n")
        
        # Sort by frequency (highest first)
        sorted_pb = sorted(pb_counts.items(), key=lambda x: x[1], reverse=True)
        total_pb_occurrences = total_pb_draws
        expected_pb_percentage = (1/20) * 100
        
        # Display all numbers 1-20 sorted by frequency
        rank = 1
        for num, count in sorted_pb:
            probability = (count / total_pb_occurrences) * 100
            f.write(f"{rank:<8} {num:<10} {count:<15} {probability:<14.2f}% {expected_pb_percentage:<14.2f}%\n")
            rank += 1
        
        # Add missing numbers (count = 0) at the end
        all_pb_numbers = set(range(1, 21))
        found_pb_numbers = set(pb_counts.keys())
        missing_pb_numbers = all_pb_numbers - found_pb_numbers
        
        for num in sorted(missing_pb_numbers):
            f.write(f"{rank:<8} {num:<10} {0:<15} {0:<14.2f}% {expected_pb_percentage:<14.2f}%\n")
            rank += 1
        
        # Additional statistics section
        f.write("\n" + "=" * 80 + "\n")
        f.write("ADDITIONAL STATISTICS\n")
        f.write("=" * 80 + "\n\n")
        
        # Most common main numbers
        f.write("TOP 10 MOST FREQUENT MAIN NUMBERS (1-35):\n")
        f.write("-" * 40 + "\n")
        for i, (num, count) in enumerate(sorted_main[:10], 1):
            probability = (count / total_main_occurrences) * 100
            f.write(f"{i:2}. Number {num:2}: {count} times ({probability:.2f}%)\n")
        
        # Least common main numbers (excluding zeros)
        f.write("\nBOTTOM 10 LEAST FREQUENT MAIN NUMBERS (1-35, excluding zeros):\n")
        f.write("-" * 40 + "\n")
        bottom_main = [item for item in sorted_main if item[1] > 0][-10:]
        for i, (num, count) in enumerate(bottom_main, 1):
            probability = (count / total_main_occurrences) * 100
            f.write(f"{i:2}. Number {num:2}: {count} times ({probability:.2f}%)\n")
        
        # Numbers never drawn in main
        if missing_numbers:
            f.write(f"\nMAIN NUMBERS NEVER DRAWN: {sorted(missing_numbers)}\n")
        else:
            f.write("\nAll main numbers (1-35) have been drawn at least once!\n")
        
        # Most common jackpot numbers
        f.write("\nTOP 10 MOST FREQUENT JACKPOT NUMBERS (1-20):\n")
        f.write("-" * 40 + "\n")
        for i, (num, count) in enumerate(sorted_pb[:10], 1):
            probability = (count / total_pb_occurrences) * 100
            f.write(f"{i:2}. Number {num:2}: {count} times ({probability:.2f}%)\n")
        
        # Least common jackpot numbers (excluding zeros)
        f.write("\nBOTTOM 10 LEAST FREQUENT JACKPOT NUMBERS (1-20, excluding zeros):\n")
        f.write("-" * 40 + "\n")
        bottom_pb = [item for item in sorted_pb if item[1] > 0][-10:]
        for i, (num, count) in enumerate(bottom_pb, 1):
            probability = (count / total_pb_occurrences) * 100
            f.write(f"{i:2}. Number {num:2}: {count} times ({probability:.2f}%)\n")
        
        # Numbers never drawn in jackpot
        if missing_pb_numbers:
            f.write(f"\nJACKPOT NUMBERS NEVER DRAWN: {sorted(missing_pb_numbers)}\n")
        else:
            f.write("\nAll jackpot numbers (1-20) have been drawn at least once!\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("END OF REPORT\n")
        f.write("=" * 80 + "\n")

# Main execution
if __name__ == "__main__":
    input_file = "powerball_2018_2026.txt"
    output_file = "probability.txt"
    
    print(f"Reading data from '{input_file}'...")
    main_counts, pb_counts = count_powerball_numbers(input_file)
    
    # Calculate total draws
    total_main_draws = sum(main_counts.values()) // 7
    total_pb_draws = sum(pb_counts.values())
    
    print(f"Found {total_main_draws} draws with {total_main_draws * 7} main numbers")
    print(f"Found {total_pb_draws} jackpot numbers")
    
    print(f"\nSaving results to '{output_file}'...")
    save_results_to_file(output_file, main_counts, pb_counts, total_main_draws, total_pb_draws)
    
    print(f"✅ Results saved to '{output_file}'")
    
    # Also display summary in console
    print("\n" + "=" * 60)
    print("QUICK SUMMARY (Sorted by Frequency - Descending)")
    print("=" * 60)
    
    # Top 10 main numbers
    print("\nTOP 10 MAIN NUMBERS (1-35):")
    sorted_main = sorted(main_counts.items(), key=lambda x: x[1], reverse=True)
    print(f"{'Rank':<6} {'Number':<10} {'Frequency':<12} {'Probability':<12}")
    print("-" * 45)
    for i, (num, count) in enumerate(sorted_main[:10], 1):
        prob = (count / (total_main_draws * 7)) * 100
        print(f"{i:<6} {num:<10} {count:<12} {prob:<11.2f}%")
    
    # Bottom 10 main numbers (with counts > 0)
    print("\nBOTTOM 10 MAIN NUMBERS (1-35, excluding zeros):")
    bottom_main = [item for item in sorted_main if item[1] > 0][-10:]
    print(f"{'Rank':<6} {'Number':<10} {'Frequency':<12} {'Probability':<12}")
    print("-" * 45)
    start_rank = len([item for item in sorted_main if item[1] > 0]) - 9
    for i, (num, count) in enumerate(bottom_main, start_rank):
        prob = (count / (total_main_draws * 7)) * 100
        print(f"{i:<6} {num:<10} {count:<12} {prob:<11.2f}%")
    
    # Top 10 jackpot numbers
    print("\nTOP 10 JACKPOT NUMBERS (1-20):")
    sorted_pb = sorted(pb_counts.items(), key=lambda x: x[1], reverse=True)
    print(f"{'Rank':<6} {'Number':<10} {'Frequency':<12} {'Probability':<12}")
    print("-" * 45)
    for i, (num, count) in enumerate(sorted_pb[:10], 1):
        prob = (count / total_pb_draws) * 100
        print(f"{i:<6} {num:<10} {count:<12} {prob:<11.2f}%")
    
    # Bottom 10 jackpot numbers (with counts > 0)
    print("\nBOTTOM 10 JACKPOT NUMBERS (1-20, excluding zeros):")
    bottom_pb = [item for item in sorted_pb if item[1] > 0][-10:]
    print(f"{'Rank':<6} {'Number':<10} {'Frequency':<12} {'Probability':<12}")
    print("-" * 45)
    start_rank = len([item for item in sorted_pb if item[1] > 0]) - 9
    for i, (num, count) in enumerate(bottom_pb, start_rank):
        prob = (count / total_pb_draws) * 100
        print(f"{i:<6} {num:<10} {count:<12} {prob:<11.2f}%")
    
    # Show missing numbers
    all_main = set(range(1, 36))
    found_main = set(main_counts.keys())
    missing_main = all_main - found_main
    if missing_main:
        print(f"\nMAIN NUMBERS NEVER DRAWN: {sorted(missing_main)}")
    else:
        print("\nAll main numbers (1-35) have been drawn at least once!")
    
    all_pb = set(range(1, 21))
    found_pb = set(pb_counts.keys())
    missing_pb = all_pb - found_pb
    if missing_pb:
        print(f"JACKPOT NUMBERS NEVER DRAWN: {sorted(missing_pb)}")
    else:
        print("All jackpot numbers (1-20) have been drawn at least once!")