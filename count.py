from collections import Counter
import re

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

# Use the function
main_counts, pb_counts = count_powerball_numbers("powerball_2018_2026.txt")

# Display main numbers 1-45 in descending order of frequency
print("MAIN NUMBERS FREQUENCY (Highest to Lowest)")
print("=" * 40)
sorted_main = sorted(main_counts.items(), key=lambda x: x[1], reverse=True)
print("Number | Frequency | %")
print("-" * 30)
total_main = sum(main_counts.values())
for num, count in sorted_main:
    percentage = (count / total_main) * 100
    print(f"{num:6} | {count:9} | {percentage:5.2f}%")

# Display jackpot numbers 1-45 in descending order of frequency
print("\nJACKPOT NUMBERS FREQUENCY (Highest to Lowest)")
print("=" * 45)
sorted_pb = sorted(pb_counts.items(), key=lambda x: x[1], reverse=True)
print("PB Number | Frequency | %")
print("-" * 30)
total_pb = sum(pb_counts.values())
for num, count in sorted_pb:
    percentage = (count / total_pb) * 100
    print(f"{num:9} | {count:9} | {percentage:5.2f}%")
