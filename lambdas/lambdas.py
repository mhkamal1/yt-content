from functools import reduce

myfunc = lambda x, y: x*y
myfunc(10, 10)

# Lambda as a key
students = [
    {'name': 'Alice', 'grade': 85},
    {'name': 'Bob', 'grade': 70},
    {'name': 'Charlie', 'grade': 95}
]
students.sort(key=lambda student: student['name'])
print(students)

# Filtering with lambda and filter()
numbers = [-1, 5, -6, -2, 3, 5, 9, 0, 10]
pos_numbers = list(filter(lambda x: x > 0, numbers))
print(pos_numbers)

# Mapping with lambda and map()
numbers = [1, 2, 3, 4, 5]
squared_numbers = list(map(lambda x: x**2, numbers))
print(squared_numbers)

numbers = [1, 2, 3, 4, 5]
nums = [1,2,3]
squared_numbers = list(map(lambda x, y: x*y, numbers, nums))
print(squared_numbers)

# Reducing with lambda and reduce()
numbers = [1, 2, 3, 4, 5]
product = reduce(lambda x, y: x * y, numbers)
print(product)
######
from functools import reduce

from functools import reduce

shopping_cart = [
    {'item': 'Shirt', 'price': 20},
    {'item': 'Jeans', 'price': 50},
    {'item': 'Shoes', 'price': 80}
]

discount_rate = 0.2

total_price = reduce(
    lambda acc, item: acc + (item['price'] * (1 - discount_rate)),
    shopping_cart,
    0
)

print(f'Total price with discount: {total_price}')
