from importlib.metadata import distribution
import streamlit as st
import numpy as np
import pandas as pd


def norm_dist(dist):
    total = sum(dist)
    return[x / total for x in dist] if total != 0 else dist

## streamlit UI
st.title("Paw Kiddos Dashboard")


st.header("Enter Projected Distributions")

st.subheader(" Dog Sizes: Petite, Small, Medium, Large")
petite_size = st.number_input("Petite Size (%)", min_value = 0.0, max_value = 100.0, value = 25.0)
small_size = st.number_input("Small Size (%)", min_value = 0.0, max_value = 100.0, value = 25.0)
medium_size = st.number_input("Medium Size (%)", min_value = 0.0, max_value = 100.0, value = 25.0)
large_size = st.number_input("Large Size (%)", min_value = 0.0, max_value = 100.0, value = 25.0)


dog_size_dist = [petite_size, small_size, medium_size, large_size]
total_percentage = sum(dog_size_dist)
st.write(f"Total Percentage: {total_percentage}%")

if total_percentage !=100.0:
    st.warning("distribution does not sum to 100%, please adjust")
else:
    dog_size_dist = norm_dist(dog_size_dist)

price_packages = [45,50,55,60]

weighted_avg_price = sum(np.array(dog_size_dist) * np.array(price_packages))
st.write(f"Weighted Avg Price Per Visit: ${weighted_avg_price:.2f}")
with st.expander("See explanation"):
    st.write(''' 
    Take the given probability distribution of dogs of various sizes and multiply by the 10 session price for each size.
    Assumes 10 session price for simplicity - $45, $50, $55 and $60
            ''')



# Visit Frequencies (percentages)
st.subheader("Client Visit Frequencies")

normal_freq = st.number_input("Normal (%)", min_value=0.0, max_value=100.0, value=25.0, help = " Visits once every 2 weeks or twice a month ")
regular_freq = st.number_input("Regular (%)", min_value=0.0, max_value=100.0, value=25.0, help = " Visits once a week or 4x a month ")
pawesome_freq = st.number_input("Pawesome (%)", min_value=0.0, max_value=100.0, value=25.0, help = " Visits twice a week or 8x a month ")
super_pawsome_freq = st.number_input("Super Pawsome (%)", min_value=0.0, max_value=100.0, value=25.0, help = "Visits thrice a month or 12 times a month")

visit_freq_dist = [normal_freq, regular_freq, pawesome_freq, super_pawsome_freq]
total_visit_percentage = sum(visit_freq_dist)
st.write(f"Total Visit Percentage: {total_visit_percentage}")
if total_visit_percentage != 100.0:
    st.warning("visit frequency distribution does not sum to 100% , please adjust")
else:
    visit_freq_dist = norm_dist(visit_freq_dist)

monthly_visit_freq = [2,4,8,12]
weighted_avg_visits = sum(np.array(visit_freq_dist)* np.array(monthly_visit_freq))
st.write(f"Weighted Average Visits per Month per Client: {weighted_avg_visits:.2f}")
with st.expander("See explanation"):
    st.write(''' 
    Take the given probability distribution of visit frequency for different clients. Assume frequency and dog size has no correlation
            ''')


st.header("Transport Revenue")
transport_usage_rate = st.number_input("Transport Usage  (% of client base)", min_value = 0.0, max_value = 1.0, value = 0.85)
transport_fee = st.number_input("Transport Fee per round trip:", min_value = 0, value = 25)
apply_discount = st.number_input("Apply Discount(%)", min_value = 0.0, max_value = 1.0, value = 0.0)
effective_transport_charge = transport_fee * (1 - apply_discount)

transport_revenue_per_client_per_month = transport_usage_rate * effective_transport_charge * weighted_avg_visits
st.write(f"Transport Revenue per Client per Month: ${transport_revenue_per_client_per_month:.2f}")
with st.expander("See explanation"):
    st.write(''' 
        Product of assumed transport usage rate, transport revenue per client after discount and weighted average visits per month per client
            ''')

revenue_per_month_per_client = (weighted_avg_price * weighted_avg_visits) 
total_revenue_per_month_per_client = revenue_per_month_per_client + transport_revenue_per_client_per_month
st.write(f"Monthly Revenue Per Client: ${revenue_per_month_per_client:.2f}")
st.write(f"Monthly Revenue Per Client incl Transport: ${total_revenue_per_month_per_client:.2f}")
with st.expander("See explanation"):
    st.write(''' 
                weighted average revenue per visit (including transport)* weighted average number of visits per month per client
            ''')

st.header("Enter Operating Expenses")
shop_rental = st.number_input("Shop Rental ($)", min_value = 0.0, value = 5300.0)
shop_quantity = st.number_input("Number of Shops rented", min_value = 1, value = 1)

van_rental = st.number_input("Van Rental($)", min_value = 0.0, value = 2000.0)
van_quantity = st.number_input("Number of Vans", min_value = 1, value = 1)

employee_salary = st.number_input("Employee Salary($)", min_value = 0.00, value = 2700.0)
employee_quantity =st.number_input("Number of Employees", min_value = 0, value = 3 )

other_expenses = st.number_input("Other Operating Supplies & Expenses ($)", min_value=0.0, value=1000.0)
with st.expander("See explanation"):
    st.write(''' 
                Includes parking, fuel, utilities, dog supplies and treats, etc
            ''')

cost_buffer = st.number_input("Buffer(%)", min_value = 0.0, max_value = 100.0, value = 10.0 )
with st.expander("See explanation"):
    st.write(''' 
            Apply a flat buffer of 10%
            ''')

# Calculate total monthly expenses
total_expenses = (shop_rental * shop_quantity) + (van_rental * van_quantity) + (employee_salary * employee_quantity) + other_expenses
buffer_amount = total_expenses * (cost_buffer / 100)
total_expenses_with_buffer = total_expenses + buffer_amount

# Display results
st.write(f"Total Monthly Operating Expenses (excluding buffer): ${total_expenses:.2f}")
# st.write(f"Buffer Amount: {buffer_amount:.2f}")
st.write(f"Total Monthly Operating Expenses (including buffer): ${total_expenses_with_buffer:.2f}")


no_of_clients_needed = total_expenses/total_revenue_per_month_per_client
st.write(f"No. of clients needed: {round(no_of_clients_needed)}")
with st.expander("See explanation"):
    st.write(''' 
        Obtained by taking the total operating expenses divided by the total revenue per client including transport
            ''')