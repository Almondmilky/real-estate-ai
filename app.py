import streamlit as st
import pickle
import numpy as np
import pandas as pd

st.set_page_config(page_title="PropTech AI Advisor", layout="wide")

# =========================
# 🖼️ IMAGE MAPPING
# =========================
LIGHT_IMAGES = {
    "onboarding": "https://images.unsplash.com/photo-1580041065738-e72023775cdc",
    "home": "https://images.unsplash.com/photo-1493606371202-6275828f90f3",
    "predict": "https://images.unsplash.com/photo-1580041065738-e72023775cdc",
    "recommend": "https://images.unsplash.com/photo-1493606371202-6275828f90f3",
    "about": "https://images.unsplash.com/photo-1580041065738-e72023775cdc"
}

DARK_IMAGES = {
    "onboarding": "https://images.unsplash.com/photo-1557723128-f8691255db09",
    "home": "https://images.unsplash.com/photo-1758295124283-d9eb271dd1ce",
    "predict": "https://images.unsplash.com/photo-1557723128-f8691255db09",
    "recommend": "https://images.unsplash.com/photo-1758295124283-d9eb271dd1ce",
    "about": "https://images.unsplash.com/photo-1557723128-f8691255db09"
}

# =========================
# 🎨 CSS THEME
# =========================
def load_css(theme):
    if theme == "dark":
        css = """
        <style>
        .stApp { background-color: #0E1117; color: white; }

        section[data-testid="stSidebar"] {
            background-color: #1C1F26;
        }

        h1,h2,h3,h4,h5,p,label { color: white !important; }

        .stButton>button {
            background: linear-gradient(90deg,#2E86C1,#5DADE2);
            color:white;
            border-radius:12px;
            height:50px;
            font-weight:bold;
        }
        </style>
        """
    else:
        css = """
        <style>
        .stApp { background-color: #F4F6F7; color: black; }

        section[data-testid="stSidebar"] {
            background-color: #FFFFFF;
        }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

# =========================
# 🖼️ SHOW BANNER
# =========================
def show_banner(page):
    if st.session_state.theme == "light":
        img = LIGHT_IMAGES.get(page)
    else:
        img = DARK_IMAGES.get(page)
    st.image(img, use_column_width=True)

# =========================
# 🧠 SESSION STATE
# =========================
if "page" not in st.session_state:
    st.session_state.page = "onboarding"
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "pro" not in st.session_state:
    st.session_state.pro = "standard"
if "user" not in st.session_state:
    st.session_state.user = {"name":"","phone":"","age":18}

# =========================
# 📦 LOAD MODEL + DATA
# =========================
@st.cache_resource
def load_model():
    return pickle.load(open("model.pkl","rb"))

@st.cache_data
def load_data():
    return pd.read_csv("VN-real-estate-Apr-Sept-2025.csv")

data = load_model()
df = load_data()

model = data["model"]
le_location = data["le_location"]
le_property = data["le_property"]
le_slug = data["le_slug"]
le_province = data["le_province"]

# =========================
# ⚙️ SIDEBAR
# =========================
def sidebar():
    with st.sidebar:
        st.header("⚙️ Tùy chỉnh")
        st.session_state.theme = st.radio("Theme", ["light","dark"])
        st.session_state.pro = st.radio("Tài khoản", ["standard","pro"])
        st.divider()
        st.write("👤 Người dùng")
        st.write(st.session_state.user)

# =========================
# 🧾 ONBOARDING
# =========================
def onboarding():
    load_css(st.session_state.theme)
    show_banner("onboarding")

    st.title("🚀 PropTech AI Advisor")
    st.subheader("Nhập thông tin cá nhân")

    name = st.text_input("Tên")
    phone = st.text_input("SĐT")
    age = st.number_input("Tuổi",10,100,18)

    if st.button("Bắt đầu"):
        st.session_state.user = {"name":name,"phone":phone,"age":age}
        st.session_state.page="home"
        st.rerun()

# =========================
# 🏠 HOME
# =========================
def home():
    sidebar()
    load_css(st.session_state.theme)
    show_banner("home")

    st.title("🏠 Trang chủ")
    st.subheader(f"Xin chào {st.session_state.user['name']} 👋")

    col1,col2 = st.columns(2)

    with col1:
        st.markdown("### 🔍 Dự đoán giá nhà")
        if st.button("Truy cập dự đoán"):
            st.session_state.page="predict"; st.rerun()

    with col2:
        st.markdown("### 📍 Gợi ý vị trí")
        if st.button("Truy cập vị trí"):
            st.session_state.page="recommend"; st.rerun()

    st.divider()

    if st.button("📘 Về chúng tôi"):
        st.session_state.page="about"; st.rerun()

# =========================
# 📘 ABOUT
# =========================
def about():
    sidebar()
    load_css(st.session_state.theme)
    show_banner("about")

    st.title("📘 Về chúng tôi")

    st.markdown("""
    ## 🏢 Tập đoàn cung cấp giải pháp Rắn Xanh

    Nền tảng AI hỗ trợ:
    - Dự đoán giá bất động sản  
    - Gợi ý vị trí phù hợp  
    - Tối ưu quyết định tài chính  

    ## 👨‍💼 CEO
    Đỗ Trí Dũng – Đại học Ngoại Thương  

    ## 👩‍💼 Chủ tịch HĐQT
    Nguyễn Quỳnh Anh – Đại học Ngoại Thương  

    ## 💎 Bản Pro
    - Dự báo tài chính  
    - ROI  
    - Insight đầu tư  
    """)

    if st.button("⬅️ Quay lại"):
        st.session_state.page="home"; st.rerun()

# =========================
# 📊 PREDICT + FINANCE PRO
# =========================
def predict():
    sidebar()
    load_css(st.session_state.theme)
    show_banner("predict")

    st.title("📊 Dự đoán giá")

    province = st.selectbox("Tỉnh", df['Province'].unique())
    location = st.selectbox("Khu vực", df[df['Province']==province]['Location'].unique())

    property_type = st.selectbox("Loại nhà", df['Property Type'].unique())
    slug = st.selectbox("Phân loại", df['Property Type Slug'].unique())

    area = st.number_input("Diện tích",10,500,50)
    bedroom = st.number_input("Phòng ngủ",0,10,2)
    bathroom = st.number_input("Phòng tắm",0,10,1)
    month = st.slider("Tháng",1,12,6)
    year = st.slider("Năm",2024,2030,2025)

    if st.session_state.pro == "pro":
        st.subheader("💰 Kế hoạch tài chính")
        income = st.number_input("Thu nhập/tháng", value=15000000)
        save_rate = st.slider("% tiết kiệm", 0, 100, 30)
        growth = st.slider("% tăng trưởng thu nhập/năm", 0, 20, 5)

    if st.button("🔍 Dự đoán"):

        X = np.array([[
            area, np.log1p(area), bedroom, bathroom,
            bedroom/area if area>0 else 0,
            bathroom/area if area>0 else 0,
            month, year,
            le_location.transform([location])[0],
            le_property.transform([property_type])[0],
            le_slug.transform([slug])[0],
            le_province.transform([province])[0],
            1 if month in [3,4,5,9,10] else 0
        ]])

        price = np.expm1(model.predict(X)[0]) * 1_000_000
        st.success(f"💰 {price/1e9:.2f} tỷ VND")

        # ===== PRO FINANCE =====
        if st.session_state.pro == "pro":

            total = 0
            months = 0
            current_income = income

            while total < price:
                monthly_saving = current_income * save_rate / 100
                total += monthly_saving
                months += 1

                if months % 12 == 0:
                    current_income *= (1 + growth/100)

                if months > 600:
                    break

            years = months / 12

            st.info(f"📅 Thời gian tiết kiệm: {years:.1f} năm")
            st.info(f"💵 Tiết kiệm/tháng: {monthly_saving:,.0f} VND")

            if years > 30:
                st.warning("⚠️ Quá lâu → nên tăng thu nhập hoặc giảm mục tiêu")

    if st.button("⬅️ Quay lại"):
        st.session_state.page="home"; st.rerun()

# =========================
# 📍 RECOMMEND FAST
# =========================
def recommend():
    sidebar()
    load_css(st.session_state.theme)
    show_banner("recommend")

    st.title("📍 Gợi ý vị trí ")

    province = st.selectbox("Tỉnh", df['Province'].unique())
    budget = st.number_input("Ngân sách", value=2_000_000_000)

    area = st.number_input("Diện tích",10,500,50)
    bedroom = st.number_input("Phòng ngủ",0,10,2)
    bathroom = st.number_input("Phòng tắm",0,10,1)

    if st.button("📍 Tìm kiếm"):

        df_prov = df[df['Province'] == province].copy()

        df_prov["loc_code"] = df_prov["Location"].map(
            lambda x: le_location.transform([x])[0] if x in le_location.classes_ else -1
        )
        df_prov = df_prov[df_prov["loc_code"] != -1]

        property_code = le_property.transform([df_prov['Property Type'].iloc[0]])[0]
        slug_code = le_slug.transform([df_prov['Property Type Slug'].iloc[0]])[0]
        province_code = le_province.transform([province])[0]

        X = np.column_stack([
            np.full(len(df_prov), area),
            np.full(len(df_prov), np.log1p(area)),
            np.full(len(df_prov), bedroom),
            np.full(len(df_prov), bathroom),
            np.full(len(df_prov), bedroom/area if area>0 else 0),
            np.full(len(df_prov), bathroom/area if area>0 else 0),
            np.full(len(df_prov), 6),
            np.full(len(df_prov), 2025),
            df_prov["loc_code"],
            np.full(len(df_prov), property_code),
            np.full(len(df_prov), slug_code),
            np.full(len(df_prov), province_code),
            np.full(len(df_prov), 1)
        ])

        preds = np.expm1(model.predict(X)) * 1_000_000
        df_prov["pred_price"] = preds

        result = df_prov[df_prov["pred_price"] <= budget]

        if not result.empty:
            result["Giá (tỷ)"] = result["pred_price"]/1e9
            st.dataframe(result[["Location","Giá (tỷ)"]].drop_duplicates())
        else:
            st.warning("Không tìm thấy khu vực phù hợp")

    if st.button("⬅️ Quay lại"):
        st.session_state.page="home"; st.rerun()

# =========================
# 🚀 ROUTER
# =========================
if st.session_state.page=="onboarding":
    onboarding()
elif st.session_state.page=="home":
    home()
elif st.session_state.page=="about":
    about()
elif st.session_state.page=="predict":
    predict()
elif st.session_state.page=="recommend":
    recommend()