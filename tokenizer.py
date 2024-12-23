import streamlit as st
import pandas as pd
from datetime import datetime, date

st.set_page_config(page_title="DCP Addons Tokenizer", layout="centered")

def get_current_and_previous_month():
    now = datetime.now()
    current_month = now.strftime("%B")
    current_year = now.year
    if now.month == 1:
        previous_month = "Desember"
        previous_year = now.year - 1
    else:
        previous_month = datetime(now.year, now.month - 1, 1).strftime("%B")
        previous_year = now.year
    return current_month, previous_month, current_year, previous_year

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('https://raw.github.com/prtmaars/DCP-Addons-Tokenizer/3eb11d488462d100745e9cbfaa91e129b588fe81/tokenizer.csv', 
                         sep=',',  
                         dtype=str, 
                         na_filter=False)
        return df
    except Exception as e:
        st.error(f"Unable to load data. Check CSV file: {e}")
        return pd.DataFrame()

def search_user(df, user_id, dob_str):
    # Cari user berdasarkan USER_ID
    user_matches = df[df['USER_ID'] == str(user_id)]
    
    # Jika user ID ditemukan, cek tanggal lahir
    if not user_matches.empty:
        result = user_matches[user_matches['DOB_STR'] == str(dob_str)]
        return result, len(user_matches) > 0
    
    return pd.DataFrame(), False

def format_date(date):
    return date.strftime("%d%m%Y")

current_month, previous_month, current_year, previous_year = get_current_and_previous_month()

st.title('DCP Addons Tokenizer')
df = load_data()
if df.empty:
    st.error("Unable to load data. Please check the CSV file.")
else:
    with st.container():
        user_id = st.text_input('Nomor User / *User ID*', 
                                placeholder="1807101",
                                help="Nomor User bisa dilihat di email pengiriman addons / *User ID can be seen in the addons delivery email*")
        dob = st.date_input('Tanggal Lahir / *Date of Birth*', 
                            min_value=date(1950, 1, 1),
                            max_value=date(2020, 12, 31),
                            value=date(2000, 1, 1))
        search_button = st.button('Cari')

    if search_button:
        if not user_id or not dob:
            st.warning('Harap isi semua data / *Please fill in all data*')
        else:
            try:
                dob_str = format_date(dob)
                result, user_id_exists = search_user(df, user_id, dob_str)
                
                if not user_id_exists:
                    st.error("User ID tidak ditemukan / *User ID not found*")
                elif result.empty:
                    st.error("Tanggal lahir tidak sesuai / *Date of Birth does not match*")
                else:
                    st.snow()
                    st.subheader('Detail User / *User Detail*')
                    col1, col2 = st.columns(2)
                    status = result['STATUS'].values[0]
                    
                    with col1:
                        st.write("Nomor User / *User ID*")
                        st.write("Status User / *User Status*")
                        st.write("Token " + current_month + " " + str(current_year))
                        if status.lower() not in ['blacklist', 'nonactive']:
                            st.markdown(f"<div style='opacity:0.5'>{"Token "}{previous_month} {str(previous_year)}</div>", unsafe_allow_html=True)
                        else:
                            st.write("Informasi / *Information* ")

                    with col2:
                        st.write(result['USER_ID'].values[0])
                        st.write(status)
                        if status.lower() in ['nonactive']:
                            st.write("-")
                            st.write("Mohon lakukan registrasi ulang terlebih dahulu, hubungi admin / *Please re-register first, contact admin*")
                        elif status.lower() in ['blacklist']:
                            st.write("-")
                            st.write("User telah diblacklist, token tidak tersedia / *User has been blacklisted, token is not available*")
                        else:
                            st.write(result['TOKEN'].values[0])
                            st.markdown(f"<div style='opacity:0.5'>{result['TOKEN_PREV'].values[0]}</div>", unsafe_allow_html=True)
            
            except Exception as e:
                st.error(f"An error occurred: {e}")

st.markdown("---")
st.markdown("© 2025 DCP Addons Tokenizer")