import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="رمضان بصحة", page_icon="🌙", layout="wide")

# 2. كود الـ CSS (دمجت فيه نفس تنسيق الـ HTML اللي أرسلتيه وطورته)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    * { font-family: 'Cairo', sans-serif !important; direction: rtl; }
    
    /* إخفاء الهيدر والفوتر الخاص بـ ستريمليت */
    header, footer, .stDeployButton { visibility: hidden; }
    .block-container { padding-top: 0rem !important; }

    /* Navbar */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 50px;
        background: white;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .logo { font-weight: bold; font-size: 24px; color: #1b4332; }

    /* Hero Section */
    .hero {
        background: linear-gradient(135deg, #eaf5ee 0%, #f8fbf9 100%);
        padding: 60px 10% ;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-radius: 0 0 50px 50px;
    }
    .hero-text h1 { color: #1b4332; font-size: 45px; margin-bottom: 10px; }
    .hero-text p { color: #555; font-size: 20px; }

    /* Services Cards */
    .section-title { text-align: center; margin-top: 50px; color: #1b4332; font-weight: 700; }
    .cards-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        padding: 20px 10%;
        flex-wrap: wrap;
    }
    .card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        width: 200px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
    }
    .card h4 { margin-top: 15px; color: #1b4332; }

    /* Tips Section */
    .tips-section {
        display: flex;
        gap: 30px;
        padding: 40px 10%;
    }
    .tip-main {
        background: #1b4332;
        color: white;
        padding: 35px;
        border-radius: 25px;
        width: 35%;
    }
    .tip-list { width: 65%; }
    .tip-item {
        background: white;
        padding: 18px;
        border-radius: 15px;
        margin-bottom: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        border-right: 5px solid #1b4332;
    }

    /* تنسيق زر "ابدأ المحادثة" ليتوافق مع التصميم */
    div.stButton > button {
        background-color: #1b4332 !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 12px 35px !important;
        border: none !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        box-shadow: 0 5px 15px rgba(27, 67, 50, 0.2) !important;
    }
    
    .footer-custom {
        background: #1b4332;
        color: white;
        text-align: center;
        padding: 20px;
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة التنقل والحالة
if "page" not in st.session_state:
    st.session_state.page = "welcome"

# --- الصفحة الأولى: الواجهة المطورة (HTML + Logic) ---
if st.session_state.page == "welcome":
    # Navbar
    st.markdown("""<div class="navbar"><div class="logo">رمضان بصحة 🌙</div>
    <div style="color: #666; font-size: 14px;">خدماتنا | نصائح | حول السكري</div></div>""", unsafe_allow_html=True)

    # Hero
    st.markdown("""<div class="hero">
        <div class="hero-text">
            <h1>مرحباً بكِ</h1>
            <p>مساعدكِ الطبي الذكي للتوعية بمرض السكري خلال شهر رمضان المبارك</p>
        </div>
        <div style="font-size: 100px;">🌙</div>
    </div>""", unsafe_allow_html=True)

    # بدلاً من زر HTML، نستخدم زر Streamlit ليعمل الكود
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("ابدأ المحادثة الآن ✨"):
            st.session_state.page = "chat"
            st.rerun()

    # Services
    st.markdown('<h2 class="section-title">كيف أساعدكِ؟</h2>', unsafe_allow_html=True)
    st.markdown("""<div class="cards-container">
        <div class="card">🩺<h4>نصائح مخصصة</h4><p style="font-size:13px; color:#777;">حسب حالتكِ الصحية</p></div>
        <div class="card">🥗<h4>إرشادات غذائية</h4><p style="font-size:13px; color:#777;">اختيارات صحية ذكية</p></div>
        <div class="card">📊<h4>إدارة السكر</h4><p style="font-size:13px; color:#777;">متابعة آمنة للصيام</p></div>
        <div class="card">🏃<h4>نمط حياة</h4><p style="font-size:13px; color:#777;">نشاط ونوم مثالي</p></div>
    </div>""", unsafe_allow_html=True)

    # Tips
    st.markdown('<h2 class="section-title">نصائح صحية في رمضان</h2>', unsafe_allow_html=True)
    st.markdown("""<div class="tips-section">
        <div class="tip-main">
            <h3>صيامكِ أمانة</h3>
            <p>اتبعي التوجيهات الطبية واستمتعي بشهر الفضيل بصحة ونشاط دائم.</p>
        </div>
        <div class="tip-list">
            <div class="tip-item">📌 استشارة الطبيب ضرورة قبل بدء الصيام</div>
            <div class="tip-item">🥗 اختيار الكربوهيدرات المعقدة في السحور</div>
            <div class="tip-item">💧 شرب لترين من الماء بين الإفطار والسحور</div>
            <div class="tip-item">📉 فحص مستوى السكر بانتظام خلال ساعات النهار</div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Footer
    st.markdown('<div class="footer-custom">رمضان بصحة © 2024 - جميع الحقوق محفوظة</div>', unsafe_allow_html=True)

# --- الصفحة الثانية: المحادثة الطبية ---
elif st.session_state.page == "chat":
    st.markdown("""<div class="navbar"><div class="logo">مركز الاستشارات 🩺</div></div>""", unsafe_allow_html=True)
    
    if st.button("⬅️ العودة للرئيسية"):
        st.session_state.page = "welcome"
        st.rerun()

    # هنا نضع كود OpenAI الخاص بكِ (تأكدي من وضع الـ API Key في الـ Secrets)
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض الرسائل بتنسيق فقاعات
    for m in st.session_state.messages:
        role_class = "user-bubble" if m["role"] == "user" else "bot-bubble"
        st.markdown(f'<div class="{role_class}">{m["content"]}</div>', unsafe_allow_html=True)

    # (ملاحظة: يمكنكِ إضافة تنسيق فقاعات الشات هنا أيضاً لزيادة الاحترافية)

    if prompt := st.chat_input("اسأليني عن السكري في رمضان..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # استجابة الـ AI مع الـ Strict Mode
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد طبي حصري لمرضى السكري في رمضان. لا تجب على أي سؤال خارج هذا النطاق."},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            ]
        )
        answer = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()