import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.title('Finance Calculator for Retirement Accounts')

st.sidebar.title('Inputs')
age_current = st.sidebar.number_input('Current Age (Years):',step=1)
salary_current = st.sidebar.number_input('Current Salary ($)',step=1000)
balance_401k_current = st.sidebar.number_input('Current 401k Balance ($):',step=1000)
contribution_401k = st.sidebar.number_input('401k Contribution (Percent of Salary):',step=0.5)/100
match_employer = st.sidebar.number_input('401k Employer Match (Percent):',step=0.5)/100
age_ret = st.sidebar.number_input('Retirement Age (Years):',step=1)
salary_increase = st.sidebar.number_input('Expected Salary Increase (Percent):',step=0.5)/100
return_annual = st.sidebar.number_input('Expected Annual Return Per Year (Percent): ',step=0.1)/100
balance_ira_current = st.sidebar.number_input('Current Roth IRA Balance ($):',step=1000)
contribution_ira = st.sidebar.number_input('Annual Roth IRA Contribution ($):',step=1000)

# Temp values
# age_current = 30
# age_ret = 50
# return_annual = 0.06
# balance_ira_current = 20000
# contribution_ira = 7000
# salary_current = 75000
# balance_401k_current = 35000
# contribution_401k = 10/100
# match_employer = 5/100
# salary_increase = 3/100

# 401k Estimator
st.subheader('401k Estimator')
years_est = age_ret-age_current
balance_401k = balance_401k_current
balance_401k_contribution = balance_401k_current
gains = 0
age_401k = []
age = age_current
value_401k = []
value_401k_contribution = []
value_401k_gains = []
salary = salary_current
balance_401k_employer = 0
value_401k_employer = []

for i in range(years_est):
    balance_401k = balance_401k+(contribution_401k*salary)+(match_employer*salary)+(balance_401k+(0.5*contribution_401k*salary)+(0.5*match_employer*salary))*return_annual
    balance_401k_contribution = balance_401k_contribution + (contribution_401k*salary)
    balance_401k_employer = balance_401k_employer + match_employer*salary
    gains = balance_401k - balance_401k_contribution - balance_401k_employer
    value_401k.append(balance_401k)
    age = age + 1
    age_401k.append(age)
    value_401k_contribution.append(balance_401k_contribution)
    value_401k_gains.append(gains)
    value_401k_employer.append(balance_401k_employer)
    salary = salary*(1+salary_increase)

chart_data = pd.DataFrame({"Age": age_401k,"401k Employee Contribution": value_401k_contribution,"401k Employer Contribution": value_401k_employer,"401k Gains": value_401k_gains})
st.bar_chart(chart_data, x="Age", y=["401k Gains","401k Employee Contribution","401k Employer Contribution"])

st.text("""
401k Balance at Retirement:  ${:,.0f} """.format(balance_401k))

# Roth IRA Estimator
st.subheader('Roth IRA Estimator')
years_est = age_ret-age_current
balance_ira = balance_ira_current
balance_ira_contribution = balance_ira_current
gains = 0
age_ira = []
age = age_current
value_ira = []
value_ira_contribution = []
value_ira_gains = []

for i in range(years_est):
    balance_ira = balance_ira*(1+return_annual)+contribution_ira
    balance_ira_contribution = balance_ira_contribution + contribution_ira
    gains = balance_ira - balance_ira_contribution
    value_ira.append(balance_ira)
    age = age + 1
    age_ira.append(age)
    value_ira_contribution.append(balance_ira_contribution)
    value_ira_gains.append(gains)

chart_data = pd.DataFrame({"Age": age_ira,"Roth IRA Contribution": value_ira_contribution,"Roth IRA Gains": value_ira_gains})
st.bar_chart(chart_data, x="Age", y=["Roth IRA Gains","Roth IRA Contribution"])

st.text("""
Roth IRA Balance at Retirement:  ${:,.0f} """.format(balance_ira))

# Combined Estimator
st.subheader('Combined Estimator')

chart_data = pd.DataFrame({"Age": age_401k,"Employee Contribution": [x+y for x,y in zip(value_401k_contribution,value_ira_contribution)],"401k Employer Contribution": value_401k_employer,"Gains": [x+y for x,y in zip(value_401k_gains,value_ira_gains)]})
st.bar_chart(chart_data, x="Age", y=["Gains","Employee Contribution","401k Employer Contribution"])

st.text("""
Total Balance at Retirement:  ${:,.0f} """.format(balance_ira+balance_401k))
