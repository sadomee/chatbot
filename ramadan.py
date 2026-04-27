import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="رمضان بصحة", page_icon="🌙", layout="wide")

# 2. كود الـ CSS المطور لوضوح العناصر والمحاذاة لليمين
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    * { 
        font-family: 'Cairo', sans-serif !important; 
        direction: rtl; 
        text-align: right; 
    }

    header, footer, .stDeployButton { visibility: hidden; }
    
    .block-container { 
        padding-top: 1rem !important; 
        padding-bottom: 0rem !important;
    }

    .stApp { background-color: #ffffff; }

    .hero {
        background: linear-gradient(135deg, #eaf5ee 0%, #f8fbf9 100%);
        padding: 60px 10%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-radius: 30px;
        margin: 20px 0;
    }
    .hero-text h1 { color: #1b4332; font-size: 45px; margin-bottom: 10px; }
    .hero-text p { color: #555; font-size: 20px; margin-bottom: 20px; }

    div.stButton {
        display: flex;
        justify-content: flex-start;
        width: 100%;
        margin-bottom: 20px;
    }
    
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

    .section-title { text-align: center !important; margin-top: 50px; color: #1b4332; font-weight: 700; margin-bottom: 30px; }
    
    .cards-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        padding: 20px 5%;
        flex-wrap: wrap;
    }
    
    .card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        width: 210px;
        text-align: center !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1) !important;
        border: 2px solid #1b4332;
    }
    .card .icon-placeholder { font-size: 50px; margin-bottom: 15px; display: block; }
    .card h4 { margin-top: 5px; color: #1b4332; font-weight: 600; text-align: center !important; }
    .card p { font-size: 14px; color: #777; text-align: center !important; }

    .tips-section {
        display: flex;
        gap: 30px;
        padding: 40px 10%;
        margin-top: 40px;
    }
    
    .tip-main {
        background: #1b4332;
        color: white;
        padding: 35px;
        border-radius: 25px;
        width: 35%;
        box-shadow: 0 10px 20px rgba(27, 67, 50, 0.2);
    }
    .tip-main h3, .tip-main p { color: white !important; text-align: right !important; }
    
    .tip-list { width: 65%; }
    
    .tip-item {
        background: white;
        padding: 18px;
        border-radius: 15px;
        margin-bottom: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08) !important;
        border-right: 8px solid #1b4332;
        border: 1px solid #f0f0f0;
    }

    .bottom-btn-container {
        display: flex;
        justify-content: center;
        width: 100%;
        margin-top: 50px;
        margin-bottom: 50px;
    }
    
    .bottom-btn-container div.stButton { justify-content: center; }

    .footer-custom {
        background: #1b4332;
        color: white;
        text-align: center !important;
        padding: 20px;
        width: 100%;
        border-radius: 20px 20px 0 0;
    }
    .footer-custom p { text-align: center !important; color: white !important; font-size: 14px; margin: 0; }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة الحالة (State Management)
if "page" not in st.session_state:
    st.session_state.page = "welcome"

if "messages" not in st.session_state:
    st.session_state.messages = []

# دالة لتغيير الصفحة
def start_chat():
    st.session_state.page = "chat"
    st.rerun()

# --- الصفحة الأولى: الواجهة الرئيسية ---
if st.session_state.page == "welcome":
    col_text, col_icon = st.columns([2, 1])
    with col_text:
        st.markdown('<div class="hero-text"><h1>مرحباً بكِ</h1><p>مساعدكِ الطبي الذكي للتوعية بمرض السكري خلال شهر رمضان المبارك</p></div>', unsafe_allow_html=True)
        if st.button("ابدأ المحادثة الآن ✨", key="top_btn"):
            start_chat()
    with col_icon:
        st.markdown('<div style="font-size: 120px; text-align: center;">🌙</div>', unsafe_allow_html=True)

    st.markdown('<h2 class="section-title">كيف أساعدكِ؟</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="cards-container">
        <div class="card"><span class="icon-placeholder">🩺</span><h4>نصائح مخصصة</h4><p>خطط توافق حالتكِ وأدويتكِ</p></div>
        <div class="card"><span class="icon-placeholder">🥗</span><h4>إرشادات غذائية</h4><p>خيارات صحية للسحور والإفطار</p></div>
        <div class="card"><span class="icon-placeholder">📊</span><h4>إدارة السكر</h4><p>نصائح لمراقبة المستويات بأمان</p></div>
        <div class="card"><span class="icon-placeholder">🏃</span><h4>نمط حياة</h4><p>توجيهات للنشاط والنوم الصحي</p></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<h2 class="section-title">نصائح صحية في رمضان</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="tips-section">
        <div class="tip-main"><h3>صيامكِ أمانة</h3><p>اتبعي التوجيهات الطبية واستمتعي بشهر الفضيل بصحة ونشاط دائم.</p></div>
        <div class="tip-list">
            <div class="tip-item">📌 استشارة الطبيب ضرورة قبل بدء الصيام لتعديل جرعات الأدوية</div>
            <div class="tip-item">🥗 التركيز على الكربوهيدرات المعقدة والبقوليات في وجبة السحور</div>
            <div class="tip-item">💧 شرب لترين إلى ثلاثة من الماء في الفترة بين الإفطار والسحور</div>
            <div class="tip-item">📉 فحص مستوى السكر بانتظام، خاصةً عند الظهر وقبل المغرب</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="bottom-btn-container">', unsafe_allow_html=True)
    if st.button("تحدثي مع مساعدك الطبي الآن ✨", key="bottom_btn"):
        start_chat()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="footer-custom"><p>رمضان بصحة ©️ 2024 - جميع الحقوق محفوظة</p></div>', unsafe_allow_html=True)

# --- الصفحة الثانية: المحادثة الطبية ---
elif st.session_state.page == "chat":
    st.markdown("""
        <div style="background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%); 
                    padding: 30px; border-radius: 20px; margin-bottom: 20px; text-align: center;">
            <h2 style="color: white !important; margin: 0; text-align: center !important;">💬 مركز الاستشارات الطبية الذكي</h2>
            <p style="color: #eaf5ee; margin-top: 10px; text-align: center !important; font-size: 0.9em;">نحن هنا للإجابة على استفساراتكِ حول السكري في رمضان</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("⬅️ العودة للرئيسية", key="back_to_home"):
        st.session_state.page = "welcome"
        st.rerun()

    st.markdown("---")

    # عرض الرسائل السابقة
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # معالجة المدخلات والربط مع OpenAI
    if prompt := st.chat_input("اسأليني عن السكري في رمضان...", key="chat_input_final"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "أنت مساعد طبي حصري لمرضى السكري في رمضان. لا تجب على أي سؤال خارج هذا النطاق بأسلوب ودود وواضح."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ]
            )
            answer = response.choices[0].message.content
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error("عذراً، حدث خطأ في الاتصال. تأكدي من إعداد المفتاح (API Key) بشكل صحيح.")