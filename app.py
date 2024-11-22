import streamlit as st
import pandas as pd
import json
from yahooquery import Ticker
import numpy as np


def check_individual_position(value_of_portfolio=1000000.00, total_mrkt_value_of_position=10000.00):
    max_asset_weight = 0.05
    if round(total_mrkt_value_of_position/value_of_portfolio, 1) <= max_asset_weight:
        st.subheader(f"Portfolio is compliant in terms of individual position sizing. ✅")
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
    total_portfolio_value = df.loc[0][5]
    current_cash_balance = df.loc[0][1]
    long_position_markt_value = df.loc[0][3]
    short_position_markt_value = df.loc[2][3]
    
    total_portfolio_value = total_portfolio_value.replace("$", "").replace(",", "")
    total_portfolio_value = float(total_portfolio_value)
    
    
    
    current_cash_balance = current_cash_balance.replace("$", "").replace(",", "")
    current_cash_balance = float(current_cash_balance)
    
    
    long_position_markt_value = long_position_markt_value.replace("$", "").replace(",", "")
    long_position_markt_value = float(long_position_markt_value)
    
    
    short_position_markt_value = short_position_markt_value.replace("$", "").replace(",", "")
    short_position_markt_value = float(short_position_markt_value)
    st.write(f"Portfolio Current Value: $ {total_portfolio_value}")
    st.write(f"Current Cash Balance: $ {current_cash_balance}")
    st.write(f"Long position market value: $ {long_position_markt_value}")
    st.write(f"Short position market value: $ {short_position_markt_value}")
    
    if 0.9 <= round(long_position_markt_value/short_position_markt_value, 1) <= 1.1:
        st.subheader("Portfolio is Dollar Neutral ✅")
    else:
        st.subheader("Portfolio is NOT Dollar Neutral. Please adjust your positions.")
        
    if round(current_cash_balance / total_portfolio_value, 1) <= 0.05:
        st.subheader("Portfolio Cash Level is Compliant ✅")
    else:
        st.subheader("Your Cash level is NOT compliant. ❌")

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
    cash_dollar_neutrality, individual_position_value, upload_current_position_excel, filter_long_positions, filter_short_positions = st.tabs(["Cash and Dollar Neutrality", "Individual Position Value", "Current Position Filter (Long)", "Current Position Filter (Short)","Upload Position Spreadsheet"])
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
        st.title("Position sizing")
        st.subheader("Enter the total portfolio value and the market value of the largest Position held.")
        total_portfolio_value = st.number_input("Enter Portfolio Value Including Decimals 👇🏾", placeholder="Total Portfolio Value", key="total_portfolio_value", step=1., format="%.2f")
        max_individual_asset_value = st.number_input("Enter the max asset value Including Decimals 👇🏾", placeholder="Max Asset Market Value", key="max_individual_asset_value", step=1., format="%.2f")
        if st.button('Check Individual Position'):
            check_individual_position(total_portfolio_value, max_individual_asset_value)
    with upload_current_position_excel:
        uploaded_file = st.file_uploader("Upload an Excel file", type=["csv"], key="uploaded_file_position_compliance")
        if uploaded_file:
            portfolio_data = uploaded_file
            read_excel(portfolio_data)
    with filter_long_positions:
        uploaded_file_containing_open_positions = st.file_uploader("Upload the CSV of Open Positions", type=["csv"], key="uploaded_file_current_open_positions_long")
        uploaded_file_containing_long_model_positions = st.file_uploader("Upload the long positions from the model", type=["xlsx"], key="uploaded_file_recommended_open_positions_long")
        if uploaded_file_containing_open_positions and uploaded_file_containing_long_model_positions:
            recommended_long_positions_df = pd.read_excel(uploaded_file_containing_long_model_positions)
            opened_long_positions_df = pd.read_csv(uploaded_file_containing_open_positions)
            opened_long_positions_df = opened_long_positions_df[opened_long_positions_df['Quantity'] > 0]
            current_opened_positions_not_from_model = opened_long_positions_df[~opened_long_positions_df['Symbol'].isin(recommended_long_positions_df['ticker_symbol'])]
            current_not_opened_long_positions_from_model = recommended_long_positions_df[~recommended_long_positions_df['ticker_symbol'].isin(opened_long_positions_df['Symbol'])]
            st.title("Long Position Filtering")
            st.subheader("These are the long positions you are currently holding that are not from the model")
            st.write("You may want to consider closing these positions.")
            for position in current_opened_positions_not_from_model['Symbol']:
                st.write(position)
            st.subheader("These are the long positions from the model that are not currently in your portfolio.")
            st.write("You may want to consider opening these positions.")
            for position in current_not_opened_long_positions_from_model['ticker_symbol']:
                st.write(position)
    with filter_short_positions:
        uploaded_file_containing_open_positions = st.file_uploader("Upload the CSV of Open Positions", type=["csv"], key="uploaded_file_current_open_positions_short")
        uploaded_file_containing_short_model_positions = st.file_uploader("Upload the short positions from the model", type=["xlsx"], key="uploaded_file_recommended_open_positions_short")
        if uploaded_file_containing_open_positions and uploaded_file_containing_short_model_positions:
            recommended_short_positions_df = pd.read_excel(uploaded_file_containing_short_model_positions)
            opened_short_positions_df = pd.read_csv(uploaded_file_containing_open_positions)
            opened_short_positions_df = opened_short_positions_df[opened_short_positions_df['Quantity'] < 0]
            current_opened_short_positions_not_from_model = opened_short_positions_df[~opened_short_positions_df['Symbol'].isin(recommended_short_positions_df['ticker_symbol'])]
            current_not_opened_short_positions_from_model = recommended_short_positions_df[~recommended_short_positions_df['ticker_symbol'].isin(opened_short_positions_df['Symbol'])]
            st.title("Short Position Filtering")
            st.subheader("These are the short positions you are currently holding that are not from the model")
            st.write("You may want to consider closing these positions.")
            for position in current_opened_short_positions_not_from_model['Symbol']:
                st.write(position)
            st.subheader("These are the short positions from the model that are not currently in your portfolio.")
            st.write("You may want to consider opening these positions.")
            for position in current_not_opened_short_positions_from_model['ticker_symbol']:
                st.write(position)
            
        
if __name__ == "__main__":
    main()
