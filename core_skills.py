import random

rand_list = random.sample(range(1, 21), 10)

list_comprehension_below_10 = [n for n in rand_list if n < 10]
print(f"Data with list comprehension : {list_comprehension_below_10}")

list_comprehension_below_10 = list(filter(lambda x: x < 10, rand_list))
print(f"Data with list filter : {list_comprehension_below_10}")
