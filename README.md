# Association Rule Mining 

## Overview
This program implements association rule mining using two approaches:
1. **Brute-Force Approach**: A method that systematically generates and evaluates all possible itemsets.
2. **Apriori Principle Approach**: A more efficient method using the `mlxtend` library to discover frequent itemsets and generate association rules.

## Prerequisites
Ensure you have the following software and libraries installed:

### Required Versions
- **Python Version**: 3.8.20
- **Conda Version**: 24.11.3

### Required Libraries
Install the necessary Python libraries using pip:
```sh
pip install mlxtend pandas numpy matplotlib random csv time
```

## How It Works
The program follows these steps:
1. **User Input**:
   - Choose a store from a predefined list (Amazon, Best Buy, K-Mart, Nike, Generic).
   - Specify minimum support and confidence thresholds.
2. **Transaction Data Extraction**:
   - Reads transactional data from a CSV file corresponding to the selected store.
   - Extracts transactions and unique items.
3. **Mining Association Rules**:
   - **Brute-Force Approach**: Generates itemsets, calculates support, and derives rules using confidence thresholds.
   - **Apriori Principle Approach**: Uses `mlxtend` to perform efficient rule mining.
4. **Results Comparison**:
   - Prints and compares the frequent itemsets and rules derived from both methods.
   - Displays runtime performance for each approach.

## Running the Program
### Running on Command Line
Execute the script using:
```sh
python script_name.py
```
Follow the on-screen prompts to select a store and enter threshold values.

### Running on Jupyter Notebook
If running in a Jupyter Notebook, use the following command to prevent output-related errors:
```sh
jupyter notebook --ServerApp.iopub_data_rate_limit=10000000
```
**Reason**: This increases the data rate limit for the notebook server, preventing issues with large output data, such as frequent itemsets and association rules exceeding the default data transmission limit.

## Output
The program displays:
- Frequent itemsets with their support values.
- Association rules with confidence and support values.
- A runtime comparison between the brute-force and Apriori approaches.
- Validation of matching itemsets and rules between both methods.


## Author
Benyamin Plaksienko
