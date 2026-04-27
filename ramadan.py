import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة
st.set_page_config(page_title="رمضان بصحة", page_icon="🌙", layout="wide")

# 2. كود الـ CSS (كل التنسيقات في مكان واحد لضمان الشكل الاحترافي)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    * { font-family: 'Cairo', sans-serif !important; direction: rtl; text-align: right; }
    header, footer, .stDeployButton { visibility: hidden; }
    .block-container { padding-top: 1rem !important; }

    /* الهيدر العلوي (Hero) */
    .hero-section {
        background: linear-gradient(135deg, #eaf5ee 0%, #f8fbf9 100%);
        padding: 50px 10%;
        border-radius: 30px;
        margin-bottom: 30px;
    }
    .hero-section h1 { color: #1b4332; font-size: 40px; margin: 0; }
    .hero-section p { color: #555; font-size: 18px; }

    /* المربعات (Cards) - جعلناها واضحة ببرواز وظل */
    .card-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
        margin: 40px 0;
    }
    .card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        width: 200px;
        text-align: center !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: 2px solid #1b4332;
    }
    .card h4 { color: #1b4332; margin-top: 10px; text-align: center !important; }
    .card p { font-size: 13px; color: #777; text-align: center !important; }

    /* مستطيلات النصائح */
    .tip-item {
        background: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        border-right: 10px solid #1b4332;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        border-top: 1px solid #eee;
        border-left: 1px solid #eee;
        border-bottom: 1px solid #eee;
    }

    /* تنسيق الأزرار لتكون يمين (للعلوي) ووسط (للسفلي) */
    .stButton > button {
        background-color: #1b4332 !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 10px 30px !important;
        font-size: 18px !important;
    }
    
    /* تنسيق العنوان العلوي في صفحة الشات - خلفية خضراء داكنة ونص أبيض */
    .chat-header {
        background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%);
        color: white;
        padding: 20px 30px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 5px 15px rgba(27, 67, 50, 0.2);
    }
    .chat-header h1 { color: white !important; margin: 0; text-align: center !important; font-weight: 700 !important; }
    .chat-header p { color: #d1e7dd; margin-top: 8px; text-align: center !important; }

    /* تنسيق فقاعات الشات كما في الصورة الثانية */
    .chat-container { padding: 10px; }
    .chat-message {
        display: flex;
        flex-direction: column;
        max-width: 80%;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.1);
        position: relative;
    }
    
    /* فقاعة المستخدم (من جهة اليسار) */
    .chat-message.user {
        background-color: #eaf5ee;
        align-self: flex-start;
        border-right: 4px solid #1b4332;
        margin-left: 0;
        margin-right: auto;
    }
    
    /* فقاعة المساعد (من جهة اليمين) */
    .chat-message.assistant {
        background-color: #f0f2f6;
        align-self: flex-end;
        border-left: 4px solid #1b4332;
        margin-left: auto;
        margin-right: 0;
    }

    .chat-message-text { font-size: 15px; }

    /* تنسيق صندوق الإدخال في الشات */
    .chat-input { margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة التنقل والحالة
if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- الصفحة الأولى: الواجهة الرئيسية ---
if st.session_state.page == "welcome":
    # منطقة الهيرو (الترحيب)
    st.markdown("""
        <div class="hero-section">
            <h1>مرحباً بكِ في رمضان بصحة 🌙</h1>
            <p>مساعدكِ الطبي الذكي للتوعية بمرض السكري خلال شهر رمضان المبارك</p>
        </div>
    """, unsafe_allow_html=True)

    # الزر العلوي
    if st.button("ابدأ المحادثة الآن ✨", key="top_btn"):
        st.session_state.page = "chat"
        st.rerun()

    # قسم المربعات
    st.markdown("<h2 style='text-align: center; color: #1b4332;'>كيف أساعدكِ؟</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div class="card-container">
            <div class="card"><div style="font-size:40px;">🩺</div><h4>نصائح مخصصة</h4><p>حسب حالتكِ الصحية</p></div>
            <div class="card"><div style="font-size:40px;">🥗</div><h4>إرشادات غذائية</h4><p>اختيارات صحية ذكية</p></div>
            <div class="card"><div style="font-size:40px;">📊</div><h4>إدارة السكر</h4><p>متابعة آمنة للصيام</p></div>
            <div class="card"><div style="font-size:40px;">🏃</div><h4>نمط حياة</h4><p>نشاط ونوم مثالي</p></div>
        </div>
    """, unsafe_allow_html=True)

    # قسم مستطيلات النصائح
    st.markdown("<h2 style='text-align: center; color: #1b4332;'>نصائح صحية في رمضان</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div style="padding: 20px 10%;">
            <div class="tip-item">📌 استشارة الطبيب ضرورة قبل بدء الصيام لتعديل الجرعات.</div>
            <div class="tip-item">🥗 التركيز على الألياف والكربوهيدرات المعقدة في السحور.</div>
            <div class="tip-item">💧 شرب كميات كافية من الماء بين الإفطار والسحور.</div>
            <div class="tip-item">📉 فحص مستوى السكر بانتظام خلال ساعات النهار.</div>
        </div>
    """, unsafe_allow_html=True)

    # الزر السفلي
    _, col_btn2, _ = st.columns([1, 1, 1])
    with col_btn2:
        if st.button("تحدثي مع مساعدك الطبي الآن ✨", key="bottom_btn"):
            st.session_state.page = "chat"
            st.rerun()

# --- الصفحة الثانية: المحادثة الطبية ---
elif st.session_state.page == "chat":
    # عنوان الشات المطور - خلفية خضراء داكنة ونص أبيض (استجابة لطلبك)
    st.markdown("""
        <div class="chat-header">
            <h1>💬 مركز الاستشارات الطبية الذكي</h1>
            <p>اسألي عن كل ما يخص السكري في رمضان</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("⬅️ العودة للرئيسية", key="back_btn"):
        st.session_state.page = "welcome"
        st.rerun()

    st.markdown("---")

    # عرض سجل المحادثة بفقاعات ملونة (استجابة لطلبك)
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for m in st.session_state.messages:
        message_class = "user" if m["role"] == "user" else "assistant"
        st.markdown(f"""
            <div class="chat-message {message_class}">
                <div class="chat-message-text">{m["content"]}</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # عنصر الإدخال
    if prompt := st.chat_input("اسأليني عن السكري في رمضان..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # ملاحظة: هنا تربطين مع OpenAI لاحقاً
        # response = client.chat.completions.create(...)
        
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
            st.rerun() # تحديث الصفحة لعرض الرسالة الجديدة فوراً
        except Exception as e:
            st.error("تأكدي من إعداد مفتاح (API Key) بشكل صحيح في Secrets.")