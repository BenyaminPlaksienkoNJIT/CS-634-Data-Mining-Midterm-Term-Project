#Note: this program requires the following prereqs

#Python Version: 3.8.20
#Conda Version: 24.11.3
#Python Libraries:
#pip install mlxtend
#-----------------------
#for Generating Datasets and Data extraction
import random
import csv
#-----------------------
#for Apriori Principle Approach
#pip install mlxtend
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import pandas as pd
#----------------------------------
#for testing
import time
import matplotlib.pyplot as plt
import numpy as np

def pick_store_and_support():
    store_names = ["Amazon", "Best_Buy", "K-Mart", "Nike", "Generic"]
    print("\nAvailable Stores:")
    for index, store in enumerate(store_names, start=1):
        print(f"{index}. {store}")

    store = get_valid_store_choice(store_names)
    min_support = get_valid_threshold("Enter the minimum support threshold (0.01 - 1.0): ")
    min_confidence = get_valid_threshold("Enter the minimum confidence threshold (0.01 - 1.0): ")
    print("\nYou selected:")
    print(f"Store: {store}")
    print(f"Minimum Support: {min_support}")
    print(f"Minimum Confidence: {min_confidence}")
    csv_file = f"{store}_transactions.csv"
    return csv_file, min_support, min_confidence


def get_valid_store_choice(store_names):
    while True:
        try:
            store_index = int(input("\nPlease select a store by number: ").strip())
            if 1 <= store_index <= len(store_names):
                return store_names[store_index - 1]
            else:
                print(f"Invalid selection. Please enter a number between 1 and {len(store_names)}.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def get_valid_threshold(prompt):
    while True:
        try:
            value = float(input(f"\n{prompt}").strip())
            if 0.01 <= value <= 1.0:
                return value
            print("Value must be between 0.01 and 1.0.")
        except ValueError:
            print("Invalid input. Please enter a numeric value between 0.01 and 1.0.")

#--------------------------------------------------------------------------------------
def extract_transactions_and_items(csv_file):
    transactions = []
    item_set = set()
    with open(csv_file, newline='', encoding='utf-8', errors='replace') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            items = set(item.strip() for item in row[1].strip().split(','))
            transactions.append(items)
            item_set.update(items)
    return transactions, list(item_set)
#--------------------------------------------------------------------------------------
def generate_itemsets(items, k):
    itemsets = []
    if k <= 0 or k > len(items):
        return itemsets
    generate_combinations(items, 0, [], k, itemsets)
    return itemsets

def generate_combinations(items, start, current_combination, k, itemsets):
    if len(current_combination) == k:
        itemsets.append(set(current_combination))
        return
    for i in range(start, len(items)):
        generate_combinations(items, i + 1, current_combination + [items[i]], k, itemsets)

def calculate_support(transactions, itemset):
    itemset = set(itemset)
    count = sum(1 for transaction in transactions if itemset.issubset(transaction))
    return count / len(transactions) if len(transactions) > 0 else 0

def generate_association_rules(frequent_itemsets, transactions, min_confidence):
    rules = []   
    for itemset in frequent_itemsets.keys():
        if len(itemset) < 2:  
            continue  
        subsets = generate_all_subsets(itemset)
        for antecedent in subsets:
            consequent = itemset - antecedent  
            
            if not consequent:  
                continue
            

            support_antecedent_union_consequent = frequent_itemsets[itemset]
            support_antecedent = frequent_itemsets.get(frozenset(antecedent), calculate_support(transactions, antecedent))
            confidence = support_antecedent_union_consequent / support_antecedent if support_antecedent > 0 else 0
            if confidence >= min_confidence:
                rules.append({
                    'antecedent': antecedent, 
                    'consequent': consequent, 
                    'support': support_antecedent_union_consequent, 
                    'confidence': confidence
                })
    return rules
    
def backtrack(start, current_subset, item_list, subsets):
    if current_subset:
        subsets.append(frozenset(current_subset))  
    for i in range(start, len(item_list)):
        backtrack(i + 1, current_subset + [item_list[i]], item_list, subsets)

def generate_all_subsets(itemset):
    item_list = list(itemset)
    subsets = []
    backtrack(0, [], item_list, subsets)
    return subsets

def brute_force_approach(csv_file, min_support, min_confidence):
    transactions_list, items_list = extract_transactions_and_items(csv_file) 
    all_frequent_itemsets = {}  

    for k in range(1, len(items_list) + 1):
        current_itemsets = generate_itemsets(items_list, k)
        new_frequent = {}  

        for itemset in current_itemsets:
            support = calculate_support(transactions_list, itemset)
            if support >= min_support:
                new_frequent[frozenset(itemset)] = support  

        if not new_frequent:  # If no new frequent itemsets were found, break the loop without generating (k+ 1 )-itemsets
            break

        all_frequent_itemsets.update(new_frequent)  

    association_rules = generate_association_rules(all_frequent_itemsets, transactions_list, min_confidence)
    return all_frequent_itemsets, association_rules
#-------------------------------------------------------------------------------------------------------------
def approach_print(frequent_itemsets, rules):
    print("\nFrequent Itemsets:")
    for i, (itemset, support) in enumerate(frequent_itemsets.items(), 1):
        print(f"{i}. Itemset: {set(itemset)}, Support: {support:.4f}")
    
    print("\nAssociation Rules:")
    for i, rule in enumerate(rules, 1):
        print(f"{i}. Rule: {set(rule['antecedent'])} → {set(rule['consequent'])}, "
              f"Support: {rule['support']:.4f}, Confidence: {rule['confidence']:.4f}")

#------------------------------------------------------------------------------------------------------------
def apriori_principle_approach(csv_file, min_support, min_confidence):
    transactions_list, _ = extract_transactions_and_items(csv_file)
    te = TransactionEncoder()
    te_ary = te.fit(transactions_list).transform(transactions_list)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    try:
        frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)
        if frequent_itemsets.empty:
            raise ValueError("The input DataFrame `df` containing the frequent itemsets is empty.")

        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
        frequent_itemsets_dict = {frozenset(itemset): support for itemset, support in 
                                  zip(frequent_itemsets['itemsets'], frequent_itemsets['support'])}
        rules_list = [
            {
                "antecedent": frozenset(rule['antecedents']),
                "consequent": frozenset(rule['consequents']),
                "support": rule['support'],
                "confidence": rule['confidence']
            }
            for _, rule in rules.iterrows()
        ]
        return frequent_itemsets_dict, rules_list

    except ValueError:
        #print("No frequent itemsets found. Returning empty results.")
        return {}, []




if __name__ == "__main__":
    
    csv_file, min_support, min_confidence = pick_store_and_support()
    start_time_brute_force = time.time()
    frequent_itemsets_brute_force, rules_brute_force = brute_force_approach(csv_file, min_support, min_confidence)
    end_time_brute_force = time.time()
    runtime_brute_force = end_time_brute_force - start_time_brute_force
    start_time_apriori = time.time()
    frequent_itemsets_apriori, rules_apriori = apriori_principle_approach(csv_file, min_support, min_confidence)
    end_time_apriori = time.time()
    runtime_apriori = end_time_apriori - start_time_apriori
    print('---------Brute-Force Approach for Mining Association Rules---------')
    approach_print( frequent_itemsets_brute_force, rules_brute_force)
    print('---------Apriori Principle Approach from a Python Library---------')
    approach_print( frequent_itemsets_apriori, rules_apriori)
    print('---------Testing---------')
    if frequent_itemsets_brute_force == frequent_itemsets_apriori:
        print("Frequent itemsets match!")
        
    else:
        print("Frequent itemsets do NOT match!")
        
        
    brute_rules_set = {
        (frozenset(rule['antecedent']), frozenset(rule['consequent']), rule['confidence'])
        for rule in rules_brute_force
    }
    apriori_rules_set = {
        (frozenset(rule['antecedent']), frozenset(rule['consequent']), rule['confidence'])
        for rule in rules_apriori
    }

    if brute_rules_set == apriori_rules_set:
        print("Association rules match!")
       
    else:
        print("Association rules do NOT match!")
    print('---------Runtime Comparison---------')
    print(f"Brute Force Approach Runtime: {runtime_brute_force:.4f} seconds")
    print(f"Apriori Principle Approach Runtime: {runtime_apriori:.4f} seconds")
    
        
    

