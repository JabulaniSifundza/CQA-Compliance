import streamlit as st
import pandas as pd
import json
from yahooquery import Ticker
import numpy as np


def check_individual_position(value_of_portfolio=1000000.00, total_mrkt_value_of_position=10000.00):
    max_asset_weight = 0.05
    if round(total_mrkt_value_of_position/value_of_portfolio, 1) <= max_asset_weight:
        st.subheader(f"Portfolio is compliant ✅")
    else:
        st.subheader(f"Portfolio is not compliant. Please adjust your position ❌")
    return None

def read_excel(file):
    # Load the Excel file
    df = pd.read_csv(file, skiprows=5)
    df = df.reset_index()
    # print(df)
    st.write(df)
    # row_1 = df.loc[1]
    # st.write(row_1)
    st.write(df.index)
    # st.write()
    current_cash_balance = df.loc[0][1]
    st.write(df.loc[2][0])
    

def portfolio_compliance_assistance(current_portfolio_value=1000000.00, current_cash_amount=1.00, long_postions_value=1000000.00, short_position_value=1000000.00):
        # Max Portfolio weight
        max_asset_weight = 0.05
        
        # cash in hand
        cash_in_hand_amount = 0.025 * current_portfolio_value
        cash_to_spend = current_portfolio_value - cash_in_hand_amount
        # st.write(f"Your current disposable cash level is: $ {round(cash_to_spend)}.")
        
        # Max single asset value
        max_single_asset_value = current_portfolio_value * max_asset_weight
        
        # Number of shares
        # share_count_to_buy = max_single_asset_value/asset_price
        # st.write(f"You should buy: {round(share_count_to_buy)} shares.")
        
        # Cash ratio
        portfolio_cash_status = None
        portfolio_cash_status_string = ''
        current_cash_ratio = current_cash_amount / current_portfolio_value
        if round(current_cash_ratio, 1) <= 0.05:
            portfolio_cash_status = True
            portfolio_cash_status_string += "Your Cash level is compliant"
            st.subheader(f"{portfolio_cash_status_string} ✅")
        else:
            portfolio_cash_status = False
            portfolio_cash_status_string += "Your Cash level is NOT compliant. Please adjust your portfolio"
            st.subheader(f"{portfolio_cash_status_string} ❌")
        # Dollar Neutrality
        dollar_neutrality = None
        dollar_neutrality_string = ''
        dollar_neutrality_coefficient = long_postions_value/short_position_value
        if 0.9 <= round(dollar_neutrality_coefficient, 1) <= 1.1:
            dollar_neutrality = True
            dollar_neutrality_string +='The portfolio is dollar neutral'
            print("Portfolio is Dollar Neutral")
            st.subheader("Portfolio is Dollar Neutral ✅")
        else:
            print("Portfolio is NOT Dollar Neutral. Please adjust your positions")
            dollar_neutrality = False
            dollar_neutrality_string += f'Portfolio is NOT Dollar Neutral. Please adjust your positions. The ratio is currently {round(dollar_neutrality_coefficient, 1)}'
            st.subheader(f"Portfolio is NOT Dollar Neutral. Please adjust your positions. The ratio is currently {round(dollar_neutrality_coefficient, 1)}")        
        return cash_in_hand_amount, cash_to_spend, dollar_neutrality, dollar_neutrality_string, portfolio_cash_status, portfolio_cash_status_string

def main():
    st.title("CQA Compliance Tool")
    cash_dollar_neutrality, individual_position_value, upload_current_position_excel = st.tabs(["Cash and Dollar Neutrality", "Individual Position Value", "Upload Position Spreadsheet"])
    with cash_dollar_neutrality:
        st.title("Cash and Dollar Neutrality")
        current_portfolio_value = st.number_input("Enter Portfolio Value Including Decimals 👇🏾", placeholder="Current Portfolio Value", key="current_portfolio_value", step=1., format="%.2f")
        # current_asset_price = st.number_input("Enter Asset Price Including Decimals 👇🏾", placeholder="Current Asset/Security Price", key="current_asset_price", step=1., format="%.2f")
        current_cash_amount = st.number_input("Enter Current Cash Amount Including Decimals 👇🏾", placeholder="Current Cash Level", key="current_cash_amount", step=1., format="%.2f")
        long_postions_value = st.number_input("Enter Long Position Value Including Decimals 👇🏾", placeholder="Long Position Value", key="long_postions_value", step=1., format="%.2f")
        short_position_value = st.number_input("Enter Short Position Value Including Decimals 👇🏾", placeholder="Short Position Value", key="short_position_value", step=1., format="%.2f")
        if st.button('Check Cash and Dollar Compliance'):
            portfolio_compliance_assistance(current_portfolio_value, current_cash_amount, long_postions_value, short_position_value)
    with individual_position_value:
        total_portfolio_value = st.number_input("Enter Portfolio Value Including Decimals 👇🏾", placeholder="Total Portfolio Value", key="total_portfolio_value", step=1., format="%.2f")
        max_individual_asset_value = st.number_input("Enter the max asset value Including Decimals 👇🏾", placeholder="Max Asset Market Value", key="max_individual_asset_value", step=1., format="%.2f")
        if st.button('Check Individual Position'):
            check_individual_position(total_portfolio_value, max_individual_asset_value)
    with upload_current_position_excel:
        uploaded_file = st.file_uploader("Upload an Excel file", type=["csv"])
        if uploaded_file:
            portfolio_data = uploaded_file
            read_excel(portfolio_data)
if __name__ == "__main__":
    main()
