import streamlit as st
import pandas as pd
import calendar
from datetime import datetime

st.set_page_config(page_title="DCP Addons Tokenizer", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('user_data.csv')
    df['DOB'] = pd.to_datetime(df['DOB'], format='%d%m%Y')
    return df

def get_token_columns():
    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month
    
    current_column = f"{current_year}_{current_month:02d}"
    
    if current_month == 1:
        prev_month = 12
        prev_year = current_year - 1
    else:
        prev_month = current_month - 1
        prev_year = current_year
    
    prev_column = f"{prev_year}_{prev_month:02d}"
    
    return current_column, prev_column

def display_user_info(user):
    current_date = datetime.now()
    current_month = calendar.month_name[current_date.month]
    current_year = current_date.year
    
    current_token_col = f"{current_year}_{current_date.month:02d}"
    
    if current_date.month == 1:
        prev_token_col = f"{current_year-1}_12"
    else:
        prev_token_col = f"{current_year}_{current_date.month-1:02d}"
    
    st.write("### User Information")
    st.write(f"**Name:** {user['Name'].iloc[0]}")
    st.write(f"**Email:** {user['E-Mail'].iloc[0]}")
    st.write(f"**Status:** {user['STATUS'].iloc[0]}")
    
    status = user['STATUS'].iloc[0]
    if status not in ['BLACKLIST', 'NON-ACTIVE']:
        st.write(f"**Current Token ({current_month}):** {user[current_token_col].iloc[0]:,}")
        st.write(f"**Previous Month Token:** {user[prev_token_col].iloc[0]:,}")
    else:
        st.warning("Token information is not available for BLACKLIST or NON-ACTIVE users.")

def main():
    st.title("User Token Search")
    
    col1, col2 = st.columns(2)
    
    with col1:
        user_id = st.text_input("User ID")
    
    with col2:
        dob = st.date_input("Date of Birth")
    
    search = st.button("Search")
    
    if search:
        if user_id and dob:
            df = load_data()
            
            dob_formatted = pd.to_datetime(dob)
            
            user = df[(df['User ID'] == user_id) & (df['DOB'] == dob_formatted)]
            
            if not user.empty:
                st.success("User found!")
                display_user_info(user)
            else:
                st.error("User not found. Please check User ID and Date of Birth.")
        else:
            st.warning("Please enter both User ID and Date of Birth.")

if __name__ == "__main__":
    main()