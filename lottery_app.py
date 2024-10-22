import streamlit as st
import pandas as pd

# Core functions
def factorial(n):
    final_product = 1
    for i in range(n, 0, -1):
        final_product *= i
    return final_product

def combinations(n, k):
    numerator = factorial(n)
    denominator = factorial(k) * factorial(n - k)
    return numerator / denominator

# Streamlit app
st.title("Lottery Probability Calculator")

# Load the CSV file
file_path = "649.csv"
lottery_canada = pd.read_csv(file_path)

def extract_numbers(row):
    row = row[4:10]
    row = set(row.values)
    return row

winning_numbers = lottery_canada.apply(extract_numbers, axis=1)

# Core functions continued...
def one_ticket_probability(user_numbers):
    n_combinations = combinations(49, 6)
    probability_one_ticket = 1 / n_combinations
    percentage_form = probability_one_ticket * 100

    return '''Your chances to win the big prize with the numbers {} are {:.7f}%.
In other words, you have a 1 in {:,} chances to win.'''.format(user_numbers, percentage_form, int(n_combinations))

def check_historical_occurrence(user_numbers, historical_numbers):
    user_numbers_set = set(user_numbers)
    check_occurrence = historical_numbers == user_numbers_set
    n_occurrences = check_occurrence.sum()

    if n_occurrences == 0:
        return '''The combination {} has never occurred.
This doesn't mean it's more likely to occur now. Your chances to win the big prize in the next drawing using the combination {} are 0.0000072%.
In other words, you have a 1 in 13,983,816 chances to win.'''.format(user_numbers, user_numbers)
    else:
        return '''The number of times combination {} has occurred in the past is {}.
Your chances to win the big prize in the next drawing using the combination {} are 0.0000072%.
In other words, you have a 1 in 13,983,816 chances to win.'''.format(user_numbers, n_occurrences, user_numbers)

def multi_ticket_probability(n_tickets):
    n_combinations = combinations(49, 6)
    probability = n_tickets / n_combinations
    percentage_form = probability * 100

    if n_tickets == 1:
        return '''Your chances to win the big prize with one ticket are {:.6f}%.
In other words, you have a 1 in {:,} chances to win.'''.format(percentage_form, int(n_combinations))
    else:
        combinations_simplified = round(n_combinations / n_tickets)
        return '''Your chances to win the big prize with {:,} different tickets are {:.6f}%.
In other words, you have a 1 in {:,} chances to win.'''.format(n_tickets, percentage_form, combinations_simplified)

def probability_less_6(n_winning_numbers):
    n_combinations_ticket = combinations(6, n_winning_numbers)
    n_combinations_remaining = combinations(43, 6 - n_winning_numbers)
    successful_outcomes = n_combinations_ticket * n_combinations_remaining
    n_combinations_total = combinations(49, 6)
    probability = successful_outcomes / n_combinations_total
    probability_percentage = probability * 100
    combinations_simplified = round(n_combinations_total / successful_outcomes)

    return '''Your chances of having {} winning numbers with this ticket are {:.6f}%.
In other words, you have a 1 in {:,} chances to win.'''.format(n_winning_numbers, probability_percentage, int(combinations_simplified))

# User Inputs
st.header("1. Single Ticket Probability")
user_numbers = st.text_input("Enter six unique numbers (separated by commas):", "1, 2, 3, 4, 5, 6")
user_numbers = [int(num.strip()) for num in user_numbers.split(",")]

if st.button("Calculate Probability for Single Ticket"):
    result = one_ticket_probability(user_numbers)
    st.write(result)

st.header("2. Check Historical Occurrence")
if st.button("Check Historical Occurrence"):
    result = check_historical_occurrence(user_numbers, winning_numbers)
    st.write(result)

st.header("3. Multi-Ticket Probability")
n_tickets = st.number_input("Enter the number of tickets you want to play:", min_value=1, max_value=13983816, value=1, step=1)

if st.button("Calculate Multi-Ticket Probability"):
    result = multi_ticket_probability(n_tickets)
    st.write(result)

st.header("4. Probability for Less Than Six Winning Numbers")
n_winning_numbers = st.slider("Select the number of winning numbers expected (between 2 and 5):", 2, 5)

if st.button("Calculate Probability for Less Than 6 Winning Numbers"):
    result = probability_less_6(n_winning_numbers)
    st.write(result)
