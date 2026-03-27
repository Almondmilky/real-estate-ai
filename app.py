import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.set_page_config(page_title="Tìm Nhà Cùng Rắn Xanh", layout="wide")

# =========================
# IMAGE
# =========================
LIGHT = {
    "onboarding":"https://images.unsplash.com/photo-1580041065738-e72023775cdc",
    "home":"https://images.unsplash.com/photo-1493606371202-6275828f90f3",
    "predict":"https://images.unsplash.com/photo-1580041065738-e72023775cdc",
    "recommend":"https://images.unsplash.com/photo-1493606371202-6275828f90f3",
    "about":"https://images.unsplash.com/photo-1580041065738-e72023775cdc"
}
DARK = {
    "onboarding":"https://images.unsplash.com/photo-1557723128-f8691255db09",
    "home":"https://images.unsplash.com/photo-1758295124283-d9eb271dd1ce",
    "predict":"https://images.unsplash.com/photo-1557723128-f8691255db09",
    "recommend":"https://images.unsplash.com/photo-1758295124283-d9eb271dd1ce",
    "about":"https://images.unsplash.com/photo-1557723128-f8691255db09"
}

# =========================
# SESSION
# =========================
if "predicted" not in st.session_state:
    st.session_state.predicted = False
if "page" not in st.session_state:
    st.session_state.page="onboarding"
if "theme" not in st.session_state:
    st.session_state.theme="light"
if "pro" not in st.session_state:
    st.session_state.pro="standard"
if "user" not in st.session_state:
    st.session_state.user={}

# =========================
# CSS
# =========================
def css():
    if st.session_state.theme == "dark":
        st.markdown("""
        <style>

        /* ===== ROOT ===== */
        .stApp {
            background-color: #0E1117;
            color: #EAECEE;
        }

        /* ===== SIDEBAR ===== */
        section[data-testid="stSidebar"] {
            background-color: #161A23;
            border-right: 1px solid rgba(255,255,255,0.05);
        }

        /* ===== TEXT GLOBAL ===== */
        html, body, [class*="css"] {
            color: #EAECEE;
        }

        /* ===== HEADINGS ===== */
        h1, h2, h3 {
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        /* ===== INPUT FIELDS ===== */
        input, textarea {
            background-color: #1E222B !important;
            color: #FFFFFF !important;
            border: 1px solid #2C313C !important;
            border-radius: 8px;
        }

        /* ===== SELECTBOX ===== */
        div[data-baseweb="select"] > div {
            background-color: #1E222B !important;
            border-radius: 8px;
        }

        /* ===== NUMBER INPUT ===== */
        div[data-baseweb="input"] input {
            background-color: #1E222B !important;
            color: white !important;
        }

        /* ===== SLIDER ===== */
        .stSlider label {
            color: #D5D8DC !important;
        }

        /* ===== BUTTON ===== */
        .stButton>button {
            background: linear-gradient(90deg,#2E86C1,#5DADE2);
            color: white;
            border-radius: 12px;
            height: 45px;
            border: none;
            font-weight: 600;
            transition: 0.2s;
        }

        .stButton>button:hover {
            transform: scale(1.03);
            opacity: 0.9;
        }

        /* ===== METRIC ===== */
        [data-testid="stMetric"] {
            background: #1E222B;
            padding: 15px;
            border-radius: 12px;
        }

        [data-testid="stMetricValue"] {
            color: #58D68D;
            font-size: 24px;
            font-weight: bold;
        }

        /* ===== CHART ===== */
        canvas {
            filter: brightness(0.9);
        }

        /* ===== DATAFRAME ===== */
        .stDataFrame {
            background-color: #1E222B;
            border-radius: 10px;
        }

        /* ===== ALERT BOX ===== */
        .stAlert {
            border-radius: 12px;
        }

        /* ===== CARD ===== */
        .card {
            background: linear-gradient(145deg,#1E222B,#23272F);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }

        </style>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <style>

        .stApp {
            background-color: #F4F6F7;
            color: #2C3E50;
        }

        section[data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid rgba(0,0,0,0.05);
        }

        /* ===== INPUT ===== */
        input, textarea {
            border-radius: 8px;
        }

        /* ===== BUTTON ===== */
        .stButton>button {
            background: linear-gradient(90deg,#3498DB,#85C1E9);
            color: white;
            border-radius: 12px;
            height: 45px;
            border: none;
            font-weight: 600;
        }

        /* ===== CARD ===== */
        .card {
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }

        </style>
        """, unsafe_allow_html=True)

def banner(p):
    img = LIGHT[p] if st.session_state.theme=="light" else DARK[p]
    st.image(img, use_container_width=True)

# =========================
# LOAD
# =========================
@st.cache_resource
def load_model():
    return pickle.load(open("model.pkl","rb"))

@st.cache_data
def load_data():
    df = pd.read_csv("VN-real-estate-Apr-Sept-2025.csv")
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df["Area"] = pd.to_numeric(df["Area"], errors="coerce")
    return df.dropna(subset=["Price","Area","Location"])

data = load_model()
df = load_data()

model = data["model"]
le_location = data["le_location"]
le_property = data["le_property"]
le_slug = data["le_slug"]
le_province = data["le_province"]

# =========================
# SIDEBAR
# =========================
def sidebar():
    with st.sidebar:
        st.title("🏠 Rắn Xanh")

        if st.button("Trang chủ"): st.session_state.page="home"; st.rerun()
        if st.button("Dự đoán"): st.session_state.page="predict"; st.rerun()
        if st.button("Vị trí"): st.session_state.page="recommend"; st.rerun()
        if st.button("Về chúng tôi"): st.session_state.page="about"; st.rerun()

        st.divider()
        st.session_state.theme = st.selectbox("Theme",["light","dark"])
        st.session_state.pro = st.selectbox("Account",["standard","pro"])

        st.divider()
        u = st.session_state.user
        st.write(f"👤 {u.get('name','')}")
        st.write(f"📞 {u.get('phone','')}")

# =========================
# ONBOARD
# =========================
def onboarding():
    css(); banner("onboarding")

    st.title("🚀 PropTech AI")

    name = st.text_input("Tên")
    phone = st.text_input("SĐT")
    age = st.number_input("Tuổi",18,100,22)

    if st.button("Bắt đầu"):
        st.session_state.user={"name":name,"phone":phone,"age":age}
        st.session_state.page="home"
        st.rerun()

# =========================
# HOME
# =========================
def home():
    sidebar(); css(); banner("home")

    st.title(f"Xin chào {st.session_state.user.get('name')} 👋")

    c1,c2,c3 = st.columns(3)
    c1.metric("Listings", len(df))
    c2.metric("Giá TB", f"{df['Price'].mean()/1e9:.2f} tỷ")
    c3.metric("Giá/m² TB", f"{(df['Price']/df['Area']).mean():,.0f}")

    df2 = df.copy()
    df2["date"] = pd.to_datetime(df2["Last Updated Date"], errors="coerce")
    trend = df2.groupby(df2["date"].dt.to_period("M"))["Price"].mean().tail(6)
    st.line_chart(trend)

    st.divider()

    col1,col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">📊 Dự đoán giá</div>', unsafe_allow_html=True)
        if st.button("Go Predict"):
            st.session_state.page="predict"; st.rerun()

    with col2:
        st.markdown('<div class="card">📍 Tìm vị trí</div>', unsafe_allow_html=True)
        if st.button("Go Recommend"):
            st.session_state.page="recommend"; st.rerun()

# =========================
# PREDICT
# =========================
def predict():
    sidebar(); css(); banner("predict")

    st.title("📊 Dự đoán giá")

    # ===== PROVINCE → LOCATION =====
    provinces = sorted(df["Province"].dropna().unique())
    province = st.selectbox("Tỉnh/Thành", provinces)

    df_prov = df[df["Province"] == province]
    location = st.selectbox("Khu vực", sorted(df_prov["Location"].unique()))

    property_type = st.selectbox("Loại nhà", df["Property Type"].unique())
    slug = st.selectbox("Phân loại", df["Property Type Slug"].unique())

    area = st.number_input("Diện tích",10,500,50)
    bedroom = st.number_input("Phòng ngủ",0,10,2)
    bathroom = st.number_input("Phòng tắm",0,10,1)

    month = st.slider("Tháng",1,12,6)
    year = st.slider("Năm",2024,2030,2025)

    if st.button("Dự đoán"):
        st.session_state.predicted = True

    if st.session_state.predicted:
        if st.button("🔄 Dự đoán lại"):
            st.session_state.predicted = False
            st.rerun()
        # encode
        try:
            loc_code = le_location.transform([location])[0]
            prop_code = le_property.transform([property_type])[0]
            slug_code = le_slug.transform([slug])[0]
            prov_code = le_province.transform([province])[0]
        except:
            st.error("Dữ liệu không hợp lệ")
            return

        X = np.array([[area,np.log1p(area),bedroom,bathroom,
                       bedroom/area,bathroom/area,
                       month,year,
                       loc_code,prop_code,slug_code,prov_code,1]])

        price = np.expm1(model.predict(X)[0])*1e6

        st.success(f"{price/1e9:.2f} tỷ")
        st.info(f"{price/area:,.0f} VND/m²")

        # ===== PRO =====
        if st.session_state.pro == "pro":

            st.subheader("📊 So sánh thị trường")

            avg_price = df["Price"].mean()
            avg_m2 = (df["Price"]/df["Area"]).mean()

            col1,col2 = st.columns(2)
            col1.metric("Giá TB thị trường", f"{avg_price/1e9:.2f} tỷ")
            col2.metric("Giá TB/m²", f"{avg_m2:,.0f}")

            diff = (price - avg_price)/avg_price*100

            if diff > 0:
                st.warning(f"⚠️ Cao hơn thị trường {diff:.1f}%")
            else:
                st.success(f"✅ Thấp hơn thị trường {abs(diff):.1f}%")

            # ===== ROI =====
            st.subheader("📈 ROI & IRR")

            roi = (avg_price - price)/price*100
            st.metric("ROI tiềm năng", f"{roi:.1f}%")

            # IRR
            try:
                import numpy_financial as npf
                cf = [-price,0,0,0,0,avg_price]
                irr = npf.irr(cf)*100
                st.metric("IRR (5 năm)", f"{irr:.2f}%")
            except:
                st.warning("Không tính được IRR")

            # ===== TREND =====
            st.subheader("📈 Xu hướng thị trường")

            df2 = df.copy()
            df2["date"] = pd.to_datetime(df2["Last Updated Date"], errors="coerce")
            trend = df2.groupby(df2["date"].dt.to_period("M"))["Price"].mean().tail(6)

            st.line_chart(trend)

            # ===== SAVING =====
            st.subheader("💰 Kế hoạch tiết kiệm")

            income = st.number_input("Thu nhập",15000000, key="income_pro")
            save = st.slider("% tiết kiệm",0,100,30)

            monthly = income*save/100
            months = price/monthly if monthly>0 else 0

            st.metric("Thời gian",f"{months/12:.1f} năm")

            savings = np.cumsum([monthly]*int(min(months,240)))
            st.line_chart(savings)

            # =========================
            # 🏦 LOAN SIMULATION (PRO+)
            # =========================
            st.subheader("🏦 Mô phỏng vay ngân hàng")

            col1, col2 = st.columns(2)

            with col1:
                down_payment_pct = st.slider("Trả trước (%)", 0, 100, 30)
                interest_rate = st.slider("Lãi suất (%/năm)", 1.0, 15.0, 8.0)

            with col2:
                loan_years = st.slider("Thời hạn vay (năm)", 5, 30, 20)
                income = st.number_input("Thu nhập/tháng", value=15000000)

            income_growth = st.slider("Tăng trưởng thu nhập (%/năm)", 0, 20, 5)
            living_cost_pct = st.slider("Chi phí sinh hoạt (%)", 10, 90, 50)

            # ===== LOAN CALC =====
            loan_amount = price * (1 - down_payment_pct/100)

            monthly_rate = interest_rate / 100 / 12
            n_months = loan_years * 12

            if monthly_rate > 0:
                monthly_payment = loan_amount * (monthly_rate * (1+monthly_rate)**n_months) / ((1+monthly_rate)**n_months - 1)
            else:
                monthly_payment = loan_amount / n_months

            st.metric("💸 Trả hàng tháng", f"{monthly_payment:,.0f} VND")

            # =========================
            # 📈 INCOME SIMULATION
            # =========================
            st.subheader("📈 Khả năng chi trả theo thời gian")

            months = min(n_months, 240)

            current_income = income
            income_list = []
            payment_list = []
            free_cashflow = []

            for m in range(months):
                if m % 12 == 0 and m != 0:
                    current_income *= (1 + income_growth/100)

                living_cost = current_income * (living_cost_pct/100)
                net_income = current_income - living_cost

                income_list.append(net_income)
                payment_list.append(monthly_payment)
                free_cashflow.append(net_income - monthly_payment)

            df_sim = pd.DataFrame({
                "Net Income": income_list,
                "Loan Payment": payment_list,
                "Free Cashflow": free_cashflow
            })

            st.line_chart(df_sim)

            # =========================
            # ⚠️ RISK CHECK (REAL)
            # =========================
            st.subheader("⚠️ Đánh giá rủi ro")

            avg_income = sum(income_list[:12]) / 12  # năm đầu
            afford_ratio = monthly_payment / avg_income * 100

            if afford_ratio > 50:
                st.error(f"🔴 Rủi ro cao ({afford_ratio:.1f}% thu nhập khả dụng)")
            elif afford_ratio > 30:
                st.warning(f"🟡 Khá căng ({afford_ratio:.1f}%)")
            else:
                st.success(f"🟢 An toàn ({afford_ratio:.1f}%)")

            # =========================
            # 💣 STRESS TEST
            # =========================
            st.subheader("💣 Stress Test")

            stress_rate = interest_rate + 3
            stress_monthly_rate = stress_rate / 100 / 12

            stress_payment = loan_amount * (stress_monthly_rate * (1+stress_monthly_rate)**n_months) / ((1+stress_monthly_rate)**n_months - 1)

            st.write(f"👉 Nếu lãi suất tăng lên {stress_rate:.1f}%:")
            st.write(f"➡️ Trả hàng tháng: {stress_payment:,.0f} VND")

            # =========================
            # 💡 SUMMARY
            # =========================
            st.subheader("💡 Kết luận tài chính")

            if afford_ratio > 50:
                st.write("❌ Không nên vay — áp lực tài chính quá lớn")
            elif min(free_cashflow) < 0:
                st.write("⚠️ Có giai đoạn âm tiền — cần cân nhắc")
            elif roi > 0:
                st.write("✅ Có thể đầu tư nếu kiểm soát tốt tài chính")
            else:
                st.write("⚠️ Giá chưa hấp dẫn so với thị trường")

        else:
            st.warning("🔒 PRO để xem phân tích")

    if st.button("⬅️ Quay lại"):
        st.session_state.page="home"; st.rerun()
        
# =========================
# RECOMMEND
# =========================
def recommend():
    sidebar(); css(); banner("recommend")

    st.title("📍 Gợi ý vị trí")

    budget = st.number_input("Ngân sách",2000000000)

    area = st.number_input("Diện tích",10,500,50)
    bedroom = st.number_input("Phòng ngủ",0,10,2)
    bathroom = st.number_input("Phòng tắm",0,10,1)

    property_type = st.selectbox("Loại nhà", df["Property Type"].unique())
    slug = st.selectbox("Phân loại", df["Property Type Slug"].unique())

    if st.button("Tìm vị trí"):

        sample = df.sample(300)

        rows = []
        for _, row in sample.iterrows():

            if row["Location"] not in le_location.classes_:
                continue

            X = np.array([[area,np.log1p(area),bedroom,bathroom,
                           bedroom/area,bathroom/area,
                           6,2025,
                           le_location.transform([row["Location"]])[0],
                           le_property.transform([property_type])[0],
                           le_slug.transform([slug])[0],
                           0,1]])

            pred = np.expm1(model.predict(X)[0])*1e6

            if pred <= budget:
                rows.append({
                    "Location": row["Location"],
                    "price": pred
                })

        result = pd.DataFrame(rows)

        if not result.empty:

            result["price/m2"] = result["price"]/area

            if st.session_state.pro == "pro":

                loc_avg = df.groupby("Location")["Price"].mean()

                result["market_avg"] = result["Location"].map(loc_avg)
                result["ROI"] = (result["market_avg"] - result["price"]) / result["price"] * 100

                # IRR
                def calc_irr(r):
                    try:
                        import numpy_financial as npf
                        return npf.irr([-r["price"],0,0,0,0,r["market_avg"]])*100
                    except:
                        return 0

                result["IRR"] = result.apply(calc_irr, axis=1)

                result = result.sort_values("ROI", ascending=False)

                st.subheader("🏆 Best Deals")
                st.dataframe(result.head(15))

                st.bar_chart(result["ROI"].head(20))

            else:
                st.dataframe(result[["Location","price","price/m2"]])
                st.warning("🔒 PRO để xem phân tích")

        else:
            st.warning("Không tìm thấy vị trí phù hợp")

    if st.button("⬅️ Quay lại"):
            st.session_state.page="home"; st.rerun()

# =========================
# 📘 ABOUT
# =========================
def about():
    sidebar(); css(); banner("about")
    st.title("📘 Về chúng tôi")

    st.markdown("""
    ## 🏢 Tập đoàn cung cấp giải pháp Rắn Xanh

    Công ty Rắn Xanh là một tập đoàn đa quốc gia hoạt động trong lĩnh vực công nghệ và phân tích dữ liệu. Cùng với các chuyên gia đầu ngành đến từ mọi lĩnh vực, tập đoàn chúng tôi tập trung phát triển các giải pháp hỗ trợ ra quyết định trong thị trường bất động sản, hướng đến mục tiêu mang lại cho người dùng những thông tin có giá trị, tối ưu hóa quyết định tài chính và đầu tư theo đuổi tiêu chuẩn phát triển sản phẩm ở mức cao, hướng tới việc tạo ra các giải pháp có khả năng mở rộng và ứng dụng trong nhiều bối cảnh khác nhau.
    Trong tương lai, Rắn Xanh đặt mục tiêu tiếp tục hoàn thiện hệ thống, mở rộng phạm vi dữ liệu và phát triển thêm các tính năng phân tích chuyên sâu, tiến tới trở thành một công cụ đáng tin cậy trong lĩnh vực bất động sản và tài chính cá nhân.
    
    Tìm Nhà Cùng Rắn Xanh là Nền tảng AI hỗ trợ:
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
# ROUTER
# =========================
if st.session_state.page=="onboarding": onboarding()
elif st.session_state.page=="home": home()
elif st.session_state.page=="predict": predict()
elif st.session_state.page=="recommend": recommend()
elif st.session_state.page=="about": about()

