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
        df = pd.read_csv('https://raw.github.com/prtmaars/DCP-Addons-Tokenizer/637ccff5e16e4d0eb55706029594ddccb4097c8c/tokenizer.csv', 
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
        search_button = st.button('Search')

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

                    # Tentukan warna dan status
                    status = result['STATUS'].values[0].lower()
                    status_colors = {
                        'active': '#9DC183',
                        'blacklist': '#FF6666',
                        'admin': '#87CEEB',
                        'associate': '#D1D1F6',
                        'non-active': '#D8D8D8'
                    }
                    color = status_colors.get(status, '#D8D8D8')  # Default warna abu-abu jika tidak ditemukan

                    # Token berdasarkan status
                    token_current = result['TOKEN'].values[0] if status not in ['non-active', 'blacklist'] else '-'
                    token_previous = result['TOKEN_PREV'].values[0] if status not in ['non-active', 'blacklist'] else '-'

                    # Pesan informasi tambahan
                    information = ""
                    if status == 'non-active':
                        information = information + "<div style='font-weight:normal;'>Informasi / <i>Information</i></div>"  
                        information = information + "<div style='background-color:#FF6666;color:black;padding:10px;border-radius:5px;text-align:center;margin-top:5px;margin-bottom:12px;'>Mohon lakukan registrasi ulang terlebih dahulu, hubungi admin.</div>"
                        information = information + "<div style='background-color:#FF6666;color:black;padding:10px;border-radius:5px;text-align:center;margin-top:5px;margin-bottom:12px;'><i>Please re-register first, contact admin</i></div>"
                    elif status == 'blacklist':
                        information = information + "<div style='font-weight:normal;'>Informasi / <i>Information</i></div>"  
                        information = information + "<div style='background-color:#FF6666;color:black;padding:10px;border-radius:5px;text-align:center;margin-top:5px;margin-bottom:12px;'>User telah diblacklist, token tidak tersedia.</div>"
                        information = information + "<div style='background-color:#FF6666;color:black;padding:10px;border-radius:5px;text-align:center;margin-top:5px;margin-bottom:12px;'><i>User has been blacklisted, token is not available.</i></div>"

                    # Tampilkan detail pengguna
                    st.markdown("---")
                    st.markdown(f"""
                    ### Detail User / *User Detail*
                    <div style='font-weight:normal;'>Nomor User / <i>User ID</i></div>  
                    <div style='background-color:{'#D8D8D8'};color:black;padding:5px;border-radius:5px;text-align:center;margin-top:5px;margin-bottom:12px;'>{result['USER_ID'].values[0]}</div>
                    <div style='font-weight:normal;'>Status User / <i>User Status</i></div>  
                    <div style='background-color:{color};color:black;padding:5px;border-radius:5px;text-align:center;margin-top:5px;margin-bottom:12px;'>{status.upper()}</div>
                    <div style='font-weight:normal;'>Token {current_month} {current_year}</div>  
                    <div style='background-color:{'#D8D8D8'};color:black;padding:5px;border-radius:5px;text-align:center;margin-top:5px;margin-bottom:12px;'>{token_current}</div>
                    <div style='font-weight:normal;opacity: 0.5;'>Token {previous_month} {previous_year}</div>                      
                    <div style='background-color:rgba(191, 191, 191, 0.5);color:rgba(0, 0, 0, 0.5);padding:5px;border-radius:5px;text-align:center;margin-top:5px;margin-bottom:12px;opacity:0.5;'>{token_previous}</div>
                    {information}
                    """, unsafe_allow_html=True)
            
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e} / *An error occurred: {e}*")

st.markdown("---")
st.markdown("© 2025 DCP Addons Tokenizer")