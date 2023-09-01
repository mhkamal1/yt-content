import cProfile, pstats
import time
import random

# Simulate fetching customer orders from a database
def fetch_orders():
    orders = []
    for _ in range(1000000):
        order = {
            "order_id": random.randint(1000, 9999),
            "customer_id": random.randint(1, 100),
            "items": [f"item_{i}" for i in range(random.randint(1, 5))],
        }
        orders.append(order)
    return orders


# Simulate processing orders and calculating total price
def process_orders(orders):
    total_revenue = 0
    for order in orders:
        order_total = sum(random.uniform(10, 100) for _ in order["items"])
        total_revenue += order_total
    return total_revenue

# Simulate generating a report for the finance department
def generate_report(revenue):
    time.sleep(2)
    report = f"Total revenue: ${revenue:.2f}"
    return report

# Main function to simulate the order processing workflow
def main():
    orders = fetch_orders()
    revenue = process_orders(orders)
    report = generate_report(revenue)
    print(report)

if __name__ == "__main__":
    
    profiler = cProfile.Profile()
    profiler.enable()

    main()

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats()
    stats.dump_stats('profile_results.prof')
