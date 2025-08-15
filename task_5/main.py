#!/usr/bin/env python3

def analyze_numbers(nums):
    unique_count = len(set(nums))
    if len(set(nums)) < 2:
        second_max = None
    else:
        second_max = sorted(set(nums), reverse=True)[1]
    divisible_by_3 = [x for x in nums if x % 3 == 0]
    return unique_count, second_max, divisible_by_3

if __name__ == "__main__":
    input_list = [10, 20, 30, 40, 50, 30, 20]
    u, s2, div3 = analyze_numbers(input_list)
    print("Уникальные числа:", u)
    print("Второе по величине число:", s2)
    print("Числа, делящиеся на 3:", div3)
