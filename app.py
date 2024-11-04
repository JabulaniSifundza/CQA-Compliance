import streamlit as st
import pandas as pd
import json
from yahooquery import Ticker
import numpy as np





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
        if  round(current_cash_ratio, 1) <= 0.05:
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
        portfolio_compliance_assistance(current_portfolio_value, current_cash_amount, long_postions_value, short_position_value)
if __name__ == "__main__":
    main()