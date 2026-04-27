import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة
st.set_page_config(page_title="رمضان بصحة", page_icon="🌙", layout="wide")

# 2. كود الـ CSS (للتصميم الكامل: المربعات، المستطيلات، الألوان، وفقاعات الشات)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    * { font-family: 'Cairo', sans-serif !important; direction: rtl; text-align: right; }
    header, footer, .stDeployButton { visibility: hidden; }
    .block-container { padding-top: 1rem !important; }

    /* تنسيق الواجهة الرئيسية */
    .hero {
        background: linear-gradient(135deg, #eaf5ee 0%, #f8fbf9 100%);
        padding: 50px 8%;
        border-radius: 30px;
        margin-bottom: 30px;
    }
    
    /* المربعات الواضحة */
    .card-container { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-top: 30px; }
    .card {
        background: white; padding: 25px; border-radius: 20px; width: 200px;
        text-align: center !important; box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: 2px solid #1b4332;
    }
    
    /* مستطيلات النصائح الواضحة */
    .tip-item {
        background: white; padding: 18px; border-radius: 15px; margin-bottom: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08); border-right: 8px solid #1b4332;
    }

    /* ألوان فقاعات المحادثة (عشان ترجع ملونة زي ما تحبين) */
    [data-testid="stChatMessage"]:nth-child(even) { background-color: #f0f2f6 !important; border-radius: 15px; }
    [data-testid="stChatMessage"]:nth-child(odd) { background-color: #eaf5ee !important; border-radius: 15px; }

    /* العنوان العلوي في صفحة الشات */
    .chat-header {
        background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%);
        padding: 25px; border-radius: 20px; margin-bottom: 25px; text-align: center;
    }
    .chat-header h2, .chat-header p { color: white !important; text-align: center !important; margin: 0; }

    /* تنسيق الأزرار */
    .stButton > button {
        background-color: #1b4332 !important; color: white !important;
        border-radius: 25px !important; padding: 10px 30px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة التنقل
if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- الصفحة الأولى: الواجهة الرئيسية ---
if st.session_state.page == "welcome":
    st.markdown("""
        <div class="hero">
            <h1 style="color: #1b4332;">مرحباً بكِ في رمضان بصحة 🌙</h1>
            <p style="font-size: 20px;">مساعدكِ الطبي المتخصص في التوعية بمرض السكري خلال شهر رمضان.</p>
        </div>
    """, unsafe_allow_html=True)

    # الزر العلوي يمين
    col_r, _ = st.columns([1, 3])
    with col_r:
        if st.button("ابدأ المحادثة الآن ✨", key="top_btn"):
            st.session_state.page = "chat"
            st.rerun()

    st.markdown("<h2 style='text-align: center; color: #1b4332; margin-top: 40px;'>كيف أساعدكِ؟</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div class="card-container">
            <div class="card"><div style="font-size:40px;">🩺</div><h4>نصائح مخصصة</h4><p>حسب حالتكِ الصحية</p></div>
            <div class="card"><div style="font-size:40px;">🥗</div><h4>إرشادات غذائية</h4><p>خيارات سحور وإفطار</p></div>
            <div class="card"><div style="font-size:40px;">📊</div><h4>إدارة السكر</h4><p>متابعة آمنة للصيام</p></div>
            <div class="card"><div style="font-size:40px;">🏃</div><h4>نمط حياة</h4><p>نشاط ونوم مثالي</p></div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: #1b4332; margin-top: 40px;'>نصائح صحية في رمضان</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div style="padding: 0 10%;">
            <div class="tip-item">📌 استشارة الطبيب ضرورة قبل بدء الصيام لتعديل جرعات الأدوية.</div>
            <div class="tip-item">🥗 التركيز على الكربوهيدرات المعقدة والبقوليات في وجبة السحور.</div>
            <div class="tip-item">💧 شرب لترين إلى ثلاثة من الماء في الفترة بين الإفطار والسحور.</div>
            <div class="tip-item">📉 فحص مستوى السكر بانتظام، خاصةً عند الظهر وقبل المغرب.</div>
        </div>
    """, unsafe_allow_html=True)

    # الزر السفلي وسط
    _, col_m, _ = st.columns([1, 1, 1])
    with col_m:
        if st.button("تحدثي مع المساعد الآن ✨", key="bottom_btn"):
            st.session_state.page = "chat"
            st.rerun()

# --- الصفحة الثانية: المحادثة ---
elif st.session_state.page == "chat":
    st.markdown("""
        <div class="chat-header">
            <h2>💬 مركز الاستشارات الطبية الذكي</h2>
            <p>نحن هنا للإجابة على استفساراتكِ حول السكري في رمضان</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("⬅️ العودة للرئيسية", key="back_btn"):
        st.session_state.page = "welcome"
        st.rerun()

    st.markdown("---")

    # عرض الرسائل (ستظهر ملونة بفضل CSS في الأعلى)
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # إدخال المحادثة (مع Key فريد لمنع الأخطاء)
    if prompt := st.chat_input("اسأليني عن السكري في رمضان...", key="chat_input_final_v3"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "أنت مساعد طبي حصري لمرضى السكري في رمضان. لا تجب على أي سؤال خارج هذا النطاق."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ]
            )
            answer = response.choices[0].message.content
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()
        except Exception as e:
            st.error("تأكدي من إعداد مفتاح OpenAI (API Key) بشكل صحيح في Secrets.")