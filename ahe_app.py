import streamlit as st
import psycopg2
import pandas as pd
from datetime import datetime
import pytz
import plotly.express as px

# --------------------------
# Page Config (Must be first)
# --------------------------
st.set_page_config(page_title="Ahe Ahe's POS System", layout="wide", page_icon="🛍️")

# --------------------------
# 🔒 Login System
# --------------------------
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.markdown("<h1 style='text-align: center; color: #ec4899;'>Welcome to Ahe Ahe's POS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 16px; margin-bottom: 0px;'>Please enter your credentials to log in.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 13px; color: #9ca3af; margin-top: 0px;'>စနစ်အတွင်းသို့ ဝင်ရောက်ရန် အမည်နှင့် စကားဝှက် ရိုက်ထည့်ပါ။</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username (အမည်)", placeholder="Enter username")
            password = st.text_input("Password (စကားဝှက်)", type="password", placeholder="Enter password")
            submit_btn = st.form_submit_button("🚪 Login (ဝင်မည်)", use_container_width=True)
            
            if submit_btn:
                if username == "aheahe" and password == "ahelove":
                    st.session_state['logged_in'] = True
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password! (အမည် သို့မဟုတ် စကားဝှက် မှားယွင်းနေပါသည်)")

else:
    # --------------------------
    # Timezone Setup
    # --------------------------
    def get_myanmar_time():
        mm_tz = pytz.timezone('Asia/Yangon')
        return datetime.now(mm_tz)

    # --------------------------
    # 🚨 Cloud Database Setup (Supabase PostgreSQL)
    # --------------------------
    # ⚠️ အရေးကြီးဆုံးနေရာ - အောက်က စာကြောင်းမှာ မင်း Copy ကူးလာတဲ့ လင့်ခ်အရှည်ကြီးကို အစားထိုးထည့်ပါ။
    # ⚠️ [YOUR-PASSWORD] ဆိုတဲ့နေရာမှာ (အစွန်းက ထောင့်ကွင်း [] တွေကိုပါ ဖျက်ပြီး) မင်းရဲ့ စကားဝှက်အစစ်ကို အစားထိုးပေးပါ။
    DB_URL = "postgresql://postgres.djkwibyhkzypwwjkarch:2026%40Japan%40Myanmar@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres"
    try:
        # PostgreSQL နှင့် ချိတ်ဆက်ခြင်း
        conn = psycopg2.connect(DB_URL)
        conn.autocommit = True  # အလိုအလျောက် Save လုပ်ပေးမည့် စနစ်
        c = conn.cursor()

        # Table များ တည်ဆောက်ခြင်း (SERIAL ကို အသုံးပြုထားသည်)
        c.execute('''CREATE TABLE IF NOT EXISTS products
                     (id SERIAL PRIMARY KEY,
                      name TEXT, price REAL, stock INTEGER)''')

        c.execute('''CREATE TABLE IF NOT EXISTS sales
                     (id SERIAL PRIMARY KEY,
                      product_name TEXT, quantity INTEGER, total REAL, date TEXT,
                      type TEXT DEFAULT 'Sale', actual_value REAL DEFAULT 0)''')

    except Exception as e:
        st.error(f"❌ Database ချိတ်ဆက်မှု မှားယွင်းနေပါသည်: {e}")
        st.stop()

    # --------------------------
    # Modern Global CSS
    # --------------------------
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');
        html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
        .modern-card { background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.01) 100%); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3); transition: transform 0.3s ease; height: 100%; }
        .modern-card:hover { transform: translateY(-5px); }
        .card-title { font-size: 13px; color: #9ca3af; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
        .card-value-blue { font-size: 28px; font-weight: 800; background: -webkit-linear-gradient(45deg, #3b82f6, #60a5fa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-top: 10px;}
        .card-value-green { font-size: 28px; font-weight: 800; background: -webkit-linear-gradient(45deg, #10b981, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-top: 10px;}
        .card-value-orange { font-size: 28px; font-weight: 800; background: -webkit-linear-gradient(45deg, #f59e0b, #fbbf24); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-top: 10px;}
        .stButton>button { background: linear-gradient(135deg, #4f46e5 0%, #ec4899 100%); color: white; border: none; border-radius: 8px; padding: 10px 24px; font-weight: 600; width: 100%; }
        .stButton>button:hover { box-shadow: 0 4px 15px rgba(236, 72, 153, 0.4); transform: scale(1.02); }
        </style>
    """, unsafe_allow_html=True)

    # --------------------------
    # Sidebar Navigation
    # --------------------------
    with st.sidebar:
        st.markdown("<h2 style='text-align: center; font-weight: 800;'>မောင့်အမျိုးသမီးအတွက် 💖</h2>", unsafe_allow_html=True)
        st.caption("<p style='text-align: center; color: #ec4899;'>🛍️ Ahe Ahe's POS</p>", unsafe_allow_html=True)
        st.markdown("---")
        menu = st.radio("MAIN MENU", ["📊 Dashboard", "🛒 Point of Sale (POS)", "📦 Inventory Management", "📈 Analytics & Reports"])
        
        st.markdown("---")
        if st.button("🚪 Logout (ထွက်မည်)"):
            st.session_state['logged_in'] = False
            st.rerun()

    # --------------------------
    # 1. Dashboard
    # --------------------------
    if menu == "📊 Dashboard":
        st.title("Business Overview")
        st.markdown("Monitor your shop's performance at a glance.")
        
        c.execute("SELECT SUM(total) FROM sales WHERE type='Sale'")
        actual_cash_in = c.fetchone()[0] or 0
        
        c.execute("SELECT SUM(actual_value) FROM sales WHERE type='Free'")
        gift_value = c.fetchone()[0] or 0
        
        total_inventory_out_value = actual_cash_in + gift_value 
        
        c.execute("SELECT COUNT(*) FROM products")
        total_prods = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM sales")
        total_orders = c.fetchone()[0]

        st.markdown("#### 💰 Financial Overview (ဘဏ္ဍာရေးအခြေအနေ)")
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='modern-card'><div class='card-title'>Total Item Value<br>(ထွက်သွားသော ကုန်တန်ဖိုး စုစုပေါင်း)</div><div class='card-value-blue'>{total_inventory_out_value:,.0f} Ks</div></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='modern-card'><div class='card-title'>Actual Cash In<br>(လက်ငင်းရငွေ အစစ်)</div><div class='card-value-green'>{actual_cash_in:,.0f} Ks</div></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='modern-card'><div class='card-title'>Free Gifts Value<br>(လက်ဆောင်ပေးမှု တန်ဖိုး)</div><div class='card-value-orange'>{gift_value:,.0f} Ks</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 📦 Store Stats (ဆိုင်အချက်အလက်)")
        c4, c5 = st.columns(2)
        with c4: st.markdown(f"<div class='modern-card'><div class='card-title'>Total Products Types<br>(ပစ္စည်းအမျိုးအစား စုစုပေါင်း)</div><div class='card-value-blue' style='color:white;'>{total_prods}</div></div>", unsafe_allow_html=True)
        with c5: st.markdown(f"<div class='modern-card'><div class='card-title'>Total Transactions<br>(အရောင်းအဝယ် ပြုလုပ်မှုအကြိမ်ရေ)</div><div class='card-value-blue' style='color:white;'>{total_orders}</div></div>", unsafe_allow_html=True)

    # --------------------------
    # 2. Point of Sale (POS)
    # --------------------------
    elif menu == "🛒 Point of Sale (POS)":
        st.title("Checkout / Point of Sale")
        c.execute("SELECT name, price, stock FROM products WHERE stock > 0")
        prods = c.fetchall()
        
        if prods:
            c1, c2 = st.columns([2, 1])
            with c1:
                names = list(set([p[0] for p in prods]))
                sel_name = st.selectbox("Search Product", names, index=None, placeholder="Select an item...")
                
                if sel_name:
                    pd_data = next(i for i in prods if i[0] == sel_name)
                    qty = st.number_input("Quantity", min_value=1, max_value=pd_data[2], value=1)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    trans_type = st.radio("Transaction Type (ရောင်းမည် / လက်ဆောင်ပေးမည်)", ["💰 ပုံမှန်ရောင်းမည် (Sale)", "🎁 အလကားပေးမည် (Free Gift)"], horizontal=True)
                    
                    is_free = (trans_type == "🎁 အလကားပေးမည် (Free Gift)")
                    actual_value = pd_data[1] * qty 
                    total_paid = 0 if is_free else actual_value 
                    db_type = "Free" if is_free else "Sale"
                    
                    with c2:
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.info(f"**Unit Price:** {pd_data[1]:,.0f} Ks")
                        st.info(f"**In Stock:** {pd_data[2]} units")
                        if is_free:
                            st.success(f"**Total Due:** 0 Ks")
                            st.warning(f"🎁 တန်ဖိုး **{actual_value:,.0f} Ks** ဖိုး လက်ဆောင်ပေးလိုက်ပါသည်။")
                        else:
                            st.success(f"**Total Due:** {total_paid:,.0f} Ks")
                        
                        if st.button("💳 CONFIRM TRANSACTION"):
                            current_mm_time = get_myanmar_time().isoformat()
                            # 🚨 Database Syntax %s လို့ ပြောင်းထားသည်
                            c.execute("UPDATE products SET stock=stock-%s WHERE name=%s", (qty, sel_name))
                            c.execute("INSERT INTO sales (product_name, quantity, total, date, type, actual_value) VALUES (%s, %s, %s, %s, %s, %s)",
                                      (sel_name, qty, total_paid, current_mm_time, db_type, actual_value))
                            st.toast("Transaction Successful! 🎉", icon="✅")
                            st.rerun()
        else:
            st.warning("No products available in stock. Please add items in Inventory.")

    # --------------------------
    # 3. Inventory Management
    # --------------------------
    elif menu == "📦 Inventory Management":
        st.title("Inventory Management")
        tab1, tab2 = st.tabs(["➕ Add New Product", "⚙️ Manage Existing Products"])
        
        with tab1:
            with st.form("add_product_form"):
                c1, c2, c3 = st.columns(3)
                name = c1.text_input("Product Name")
                price = c2.number_input("Price (Ks)", min_value=0.0, step=100.0, value=None, placeholder="0")
                stock = c3.number_input("Stock Quantity", min_value=0, step=1, value=None, placeholder="0")
                if st.form_submit_button("💾 Save Product"):
                    if name and price is not None and stock is not None:
                        c.execute("INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)", (name, price, stock))
                        st.toast(f"{name} added to inventory!", icon="📦")
                    else:
                        st.error("Please fill in all fields.")

        with tab2:
            c.execute("SELECT name, price, stock FROM products")
            prods = c.fetchall()
            if prods:
                unique_names = list(set([p[0] for p in prods]))
                edit_sel = st.selectbox("Select Product to Edit/Delete", unique_names, index=None, placeholder="Choose product...")
                if edit_sel:
                    curr_data = next(i for i in prods if i[0] == edit_sel)
                    with st.form("edit_product_form"):
                        col1, col2 = st.columns(2)
                        new_price = col1.number_input("New Price", min_value=0.0, value=float(curr_data[1]))
                        new_stock = col2.number_input("Update Stock", min_value=0, value=int(curr_data[2]))
                        if st.form_submit_button("🔄 Update Changes"):
                            c.execute("UPDATE products SET price=%s, stock=%s WHERE name=%s", (new_price, new_stock, edit_sel))
                            st.toast("Product updated successfully!", icon="✅")
                            st.rerun()
                st.markdown("---")
                with st.expander("⚠️ Danger Zone (ပစ္စည်းများဖျက်ရန်)"):
                    d1, d2 = st.columns(2)
                    with d1:
                        if edit_sel:
                            if st.button(f"❌ '{edit_sel}' ကို ဖျက်မည်", use_container_width=True):
                                c.execute("DELETE FROM products WHERE name=%s", (edit_sel,))
                                st.success(f"{edit_sel} ကို ဖျက်လိုက်ပါပြီ။")
                                st.rerun()
                        else:
                            st.button("❌ ပစ္စည်းတစ်ခုကို ဖျက်မည်", disabled=True, use_container_width=True)
                    with d2:
                        if st.button("🚨 ပစ္စည်းအားလုံးကို ဖျက်မည် (Delete All)", use_container_width=True):
                            c.execute("DELETE FROM products")
                            st.success("ပစ္စည်းအားလုံးကို ဖျက်လိုက်ပါပြီ။")
                            st.rerun()
            else:
                st.info("Inventory is empty.")

    # --------------------------
    # 4. Analytics & Reports
    # --------------------------
    elif menu == "📈 Analytics & Reports":
        st.title("Business Analytics & Reports")
        
        query = "SELECT product_name as Product, quantity as Qty, total as Paid_Ks, actual_value as Value_Ks, date as Date, type as Type FROM sales ORDER BY date DESC"
        import warnings
        warnings.filterwarnings('ignore') # pandas warning ကို ဖျောက်ထားရန်
        df_sales = pd.read_sql_query(query, conn)

        if not df_sales.empty:
            df_sales['Date_Obj'] = pd.to_datetime(df_sales['Date'])
            df_sales['Day_Label'] = df_sales['Date_Obj'].dt.strftime('%d %b')
            df_sales['Month'] = df_sales['Date_Obj'].dt.month
            df_sales['Year'] = df_sales['Date_Obj'].dt.year
            df_sales['UnitPrice_Ks'] = df_sales['Value_Ks'] / df_sales['Qty']
            
            tab_analytic, tab_history = st.tabs(["📊 Advanced Analytics (ခွဲခြမ်းစိတ်ဖြာချက်)", "📝 Transaction History (အရောင်းမှတ်တမ်းများ)"])
            
            with tab_analytic:
                st.markdown("### 📅 လအလိုက် ရောင်းအားခွဲခြမ်းစိတ်ဖြာချက်")
                available_years = sorted(df_sales['Year'].unique().tolist(), reverse=True)
                months_dict = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
                
                f1, f2 = st.columns(2)
                with f1: sel_year = st.selectbox("နှစ်ရွေးချယ်ရန် (Select Year)", available_years)
                with f2: sel_month = st.selectbox("လရွေးချယ်ရန် (Select Month)", list(months_dict.keys()), format_func=lambda x: months_dict[x], index=get_myanmar_time().month-1)
                
                prev_month = sel_month - 1 if sel_month > 1 else 12
                prev_year = sel_year if sel_month > 1 else sel_year - 1
                
                df_sale_only = df_sales[df_sales['Type'] == 'Sale']
                sel_month_sales = df_sale_only[(df_sale_only['Month'] == sel_month) & (df_sale_only['Year'] == sel_year)]['Paid_Ks'].sum()
                prev_month_sales = df_sale_only[(df_sale_only['Month'] == prev_month) & (df_sale_only['Year'] == prev_year)]['Paid_Ks'].sum()
                
                df_free_only = df_sales[(df_sales['Type'] == 'Free') & (df_sales['Month'] == sel_month) & (df_sales['Year'] == sel_year)]
                total_free_value = df_free_only['Value_Ks'].sum()
                
                m1, m2, m3 = st.columns(3)
                diff_sales = sel_month_sales - prev_month_sales
                with m1: st.metric(f"{months_dict[sel_month]} {sel_year} ရောင်းရငွေ", f"{sel_month_sales:,.0f} Ks", f"{diff_sales:,.0f} Ks (vs {months_dict[prev_month]})")
                with m2: st.metric(f"{months_dict[prev_month]} (ယခင်လ) ရောင်းရငွေ", f"{prev_month_sales:,.0f} Ks")
                with m3: st.metric(f"လက်ဆောင်ပေးမှု တန်ဖိုး (Free Gifts)", f"{total_free_value:,.0f} Ks", delta_color="off")
                
                st.markdown("---")
                st.markdown(f"### 📈 Daily Sales Trend ({months_dict[sel_month]} လအတွက် ရက်အလိုက် ရောင်းအား)")
                
                df_chart_data = df_sale_only[(df_sale_only['Month'] == sel_month) & (df_sale_only['Year'] == sel_year)]
                if not df_chart_data.empty:
                    daily_trend = df_chart_data.groupby('Day_Label')['Paid_Ks'].sum().reset_index()
                    fig = px.bar(daily_trend, x='Day_Label', y='Paid_Ks', text='Paid_Ks',
                                 labels={'Day_Label': 'ရက်စွဲ (Date)', 'Paid_Ks': 'ရောင်းရငွေ (Income Ks)'})
                    fig.update_traces(texttemplate='%{text:,.0f} Ks', textposition='outside', marker_color='#3b82f6')
                    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), margin=dict(t=20, b=20))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info(f"{months_dict[sel_month]} {sel_year} အတွက် အရောင်းအဝယ် မရှိသေးပါ။")

            with tab_history:
                st.markdown("### 🔍 Filter by Date (ရက်စွဲအလိုက် ရှာဖွေရန်)")
                col1, col2 = st.columns(2)
                min_date, max_date = df_sales['Date_Obj'].min().date(), df_sales['Date_Obj'].max().date()
                
                with col1: start_date = st.date_input("Start Date (မှ)", min_date, min_value=min_date, max_value=max_date)
                with col2: end_date = st.date_input("End Date (အထိ)", max_date, min_value=min_date, max_value=max_date)
                    
                mask = (df_sales['Date_Obj'].dt.date >= start_date) & (df_sales['Date_Obj'].dt.date <= end_date)
                filtered_df = df_sales.loc[mask].copy()
                
                st.markdown("---")
                if not filtered_df.empty:
                    f_sales = filtered_df[filtered_df['Type'] == 'Sale']['Paid_Ks'].sum()
                    f_free_val = filtered_df[filtered_df['Type'] == 'Free']['Value_Ks'].sum()
                    f_total_val = f_sales + f_free_val  
                    
                    st.success(f"🌟 **စုစုပေါင်းတန်ဖိုး (Total Value): {f_total_val:,.0f} Ks** ┃ 💰 **ရောင်းရငွေ (Income):** {f_sales:,.0f} Ks ┃ 🎁 **လက်ဆောင် (Outcome):** {f_free_val:,.0f} Ks")
                    
                    display_df = filtered_df[['Product', 'UnitPrice_Ks', 'Qty', 'Paid_Ks', 'Value_Ks', 'Type', 'Date_Obj']].copy()
                    display_df['Date'] = display_df['Date_Obj'].dt.strftime('%d %b %Y, %I:%M %p')
                    display_df = display_df.drop(columns=['Date_Obj'])
                    
                    st.dataframe(display_df.style.format({'UnitPrice_Ks': '{:,.0f}', 'Paid_Ks': '{:,.0f}', 'Value_Ks': '{:,.0f}'}), use_container_width=True, hide_index=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    with st.expander("🗑️ အရောင်းမှတ်တမ်းများ ဖျက်ရန် (Delete History)"):
                        del_opt = st.radio("မည်သည့်မှတ်တမ်းကို ဖျက်မည်နည်း?", ["ရွေးချယ်ထားသော ရက်အတွင်း မှတ်တမ်းများ ဖျက်မည်", "မှတ်တမ်းအားလုံး ဖျက်မည် (Clear All)"])
                        if st.button("🗑️ အတည်ပြု၍ ဖျက်မည်"):
                            if del_opt == "မှတ်တမ်းအားလုံး ဖျက်မည် (Clear All)": 
                                c.execute("DELETE FROM sales")
                            else: 
                                c.execute("DELETE FROM sales WHERE LEFT(date, 10) BETWEEN %s AND %s", (start_date.isoformat(), end_date.isoformat()))
                            st.success("မှတ်တမ်းများ ဖျက်ပစ်လိုက်ပါပြီ။")
                            st.rerun()
                else:
                    st.warning("⚠️ ရွေးချယ်ထားသော ရက်စွဲများအတွက် အရောင်းမှတ်တမ်း မရှိပါ။")
        else:
            st.info("No sales data available yet. (အရောင်းမှတ်တမ်း မရှိသေးပါ)")