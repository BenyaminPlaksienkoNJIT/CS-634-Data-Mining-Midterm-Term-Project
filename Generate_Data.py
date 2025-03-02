import random
import csv

stores = {
    "Amazon": [
        "A Beginner’s Guide", "Java: The Complete Reference", "Java For Dummies",
        "Android Programming: The Big Nerd Ranch", "Head First Java 2nd Edition",
        "Beginning Programming with Java", "Java 8 Pocket Guide",
        "C++ Programming in Easy Steps", "Effective Java (2nd Edition)",
        "HTML and CSS: Design and Build Websites"
    ],
    "Best_Buy": [
        "Digital Camera", "Lab Top", "Desk Top", "Printer", "Flash Drive",
        "Microsoft Office", "Speakers", "Lab Top Case", "Anti-Virus", "External Hard-Drive"
    ],
    "K-Mart": [
        "Quilts", "Bedspreads", "Decorative Pillows", "Bed Skirts", "Sheets",
        "Shams", "Bedding Collections", "Kids Bedding", "Embroidered Bedspread", "Towels"
    ],
    "Nike": [
        "Running Shoe", "Soccer Shoe", "Socks", "Swimming Shirt", "Dry Fit V-Nick",
        "Rash Guard", "Sweatshirts", "Hoodies", "Tech Pants", "Modern Pants"
    ],
    "Generic": ["A", "B", "C", "D", "E", "F"]
}

store_seeds = {
    "Amazon": 69,
    "Best_Buy": 420,
    "K-Mart": 690,
    "Nike": 4200,
    "Generic": 6900
}



def generate_transactions(item_list, seed_value, num_transactions=20, min_items=1, max_items=10):
    random.seed(seed_value)
    transactions = []
    for i in range(1, num_transactions + 1):
        max_possible_items = min(max_items, len(item_list)) 
        num_items = random.randint(min_items, max_possible_items) 
        selected_items = random.sample(item_list, num_items)
        transactions.append((f"Trans{i}", ", ".join(selected_items)))
    return transactions


for store, items in stores.items():
    seed_value = store_seeds[store]
    transactions = generate_transactions(items, seed_value)

    
    with open(f"{store}_transactions.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Transaction ID", "Transaction"])
        writer.writerows(transactions)

    print(f"Generated transactions for {store} (Seed: {seed_value})")