import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة
st.set_page_config(page_title="رمضان بصحة", page_icon="🌙", layout="wide")

# 2. CSS المتكامل والمفصل لضبط الواجهة، الفقاعات، وتثبيت الهيدر
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    /* الأساسيات وتصفير المساحات */
    * { font-family: 'Cairo', sans-serif !important; direction: rtl; text-align: right; scroll-behavior: smooth; }
    header, footer, .stDeployButton { visibility: hidden; }
    .block-container { padding-top: 2rem !important; }

    /* --- الصفحة الرئيسية: قسم الترحيب (Hero) --- */
    .hero-flex {
        display: flex; justify-content: space-between; align-items: center;
        background: #f8faf9; padding: 50px; border-radius: 30px; margin-bottom: 30px;
    }
    .hero-text-container { flex: 2; }
    .hero-text-container h1 { color: #1b4332; font-size: 3.5rem; margin: 0; }
    .hero-text-container p { color: #2d6a4f; font-size: 1.3rem; margin-top: 15px; }

    /* --- قسم حول السكري --- */
    .about-box { 
        background: white; padding: 35px; border-radius: 25px; 
        border: 1px solid #e5e7eb; margin-bottom: 40px; box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .about-box h3 { color: #1b4332; margin-bottom: 15px; }
    .about-box p { color: #4b5563; line-height: 1.8; font-size: 1.1rem; }

    /* --- الأيقونات الأربعة (كيف أساعدك) --- */
    .card-container {
        background: white; padding: 25px; border-radius: 25px;
        border: 1px solid #eee; text-align: center; transition: 0.3s;
        margin-bottom: 20px;
    }
    .card-icon { font-size: 2.5rem; margin-bottom: 15px; display: block; }
    .card-title { color: #1b4332; font-weight: 700; font-size: 1.1rem; }

    /* --- قسم النصائح الطبية (البطاقة الخضراء) --- */
    .tips-layout { display: flex; gap: 25px; margin-bottom: 30px; flex-wrap: wrap; }
    .green-side { 
        background: #1b4332; color: white; padding: 40px; 
        border-radius: 30px; flex: 1; min-width: 300px;
        display: flex; flex-direction: column; justify-content: center;
    }
    .tips-list { 
        flex: 2; background: white; border-radius: 25px; 
        border: 1px solid #eee; overflow: hidden; min-width: 350px;
    }
    .instruction-row { 
        padding: 20px; border-bottom: 1px solid #f5f5f5; 
        display: flex; align-items: center; font-size: 1.05rem;
    }
    .instruction-row:last-child { border-bottom: none; }
    .ins-icon { 
        font-size: 1.5rem; margin-left: 15px; background: #f0f7f4; 
        padding: 10px; border-radius: 50%; 
    }

    /* --- الفوتر الكامل --- */
    .custom-footer {
        background: #1b4332; color: white; padding: 60px 40px; 
        border-radius: 40px 40px 0 0; display: flex; justify-content: space-between; 
        margin-top: 60px; flex-wrap: wrap; gap: 30px;
    }
    .footer-col { flex: 1; min-width: 200px; }
    .footer-col h3, .footer-col h4 { margin-bottom: 20px; }
    .footer-links a { 
        color: white !important; text-decoration: none; 
        display: block; margin-bottom: 12px; font-size: 1rem; 
    }

    /* --- صفحة الشات: الهيدر الثابت والفقاعات الذكية --- */
    .sticky-header {
        position: sticky; top: 0; background: white; z-index: 1000;
        padding: 20px 0; border-bottom: 1px solid #eee; margin-bottom: 20px;
    }
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] { display: none !important; }
    [data-testid="stChatMessage"] { background-color: transparent !important; width: 100% !important; }

    /* فقاعة المستخدم (يمين) */
    div[aria-label="Chat message from user"] { flex-direction: row-reverse !important; }
    div[aria-label="Chat message from user"] .stMarkdown {
        background-color: #1b4332 !important; color: white !important;
        border-radius: 20px 20px 2px 20px !important; padding: 12px 20px !important;
        width: fit-content !important; max-width: 80% !important; margin-right: 15px;
    }

    /* فقاعة المساعد (يسار) */
    div[aria-label="Chat message from assistant"] { flex-direction: row !important; }
    div[aria-label="Chat message from assistant"] .stMarkdown {
        background-color: #f0f2f6 !important; color: #1f2937 !important;
        border-radius: 20px 20px 20px 2px !important; padding: 12px 20px !important;
        width: fit-content !important; max-width: 80% !important; margin-left: 15px;
        border: 1px solid #e5e7eb !important;
    }

    /* الأزرار الخضراء */
    div.stButton > button {
        background-color: #1b4332 !important; color: white !important;
        border-radius: 50px !important; padding: 12px 35px !important; 
        border: none !important; font-size: 1.1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# إدارة الصفحات والرسائل
if 'page' not in st.session_state: st.session_state.page = 'home'
if "messages" not in st.session_state: st.session_state.messages = []

# --- الصفحة الرئيسية (كاملة بدون اختصارات) ---
if st.session_state.page == 'home':
    st.markdown('<div id="top"></div>', unsafe_allow_html=True)

    # 1. قسم الترحيب
    st.markdown('<div class="hero-flex">', unsafe_allow_html=True)
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
        st.markdown("""
            <div class="hero-text-container">
                <h1>مرحباً بكِ 🌙</h1>
                <p>أنا مساعدكِ الطبي المتخصص في التوعية بمرض السكري خلال شهر رمضان المبارك.</p>
            </div>
        """, unsafe_allow_html=True)
    with col_t2:
        st.write("<br>", unsafe_allow_html=True)
        if st.button("ابدأ المحادثة الآن 💬", key="hero_start"):
            st.session_state.page = 'chat'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. قسم حول السكري
    st.markdown('<div id="about" class="about-box">', unsafe_allow_html=True)
    st.markdown("""
        <h3>حول السكري في رمضان 🩸</h3>
        <p>
        إدارة السكري خلال الصيام تتطلب وعياً طبياً دقيقاً؛ حيث تختلف احتياجات الجسم للطاقة والعلاج بين ساعات الصيام والإفطار. 
        يهدف هذا المساعد لتزويدك بإرشادات فورية حول كيفية التعامل مع تقلبات السكر، متى يجب كسر الصيام، وكيفية تنظيم وجباتك صحياً لضمان سلامتكِ.
        </p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. قسم كيف أساعدك (الأيقونات الأربعة)
    st.markdown('<h2 style="color:#1b4332; text-align:center; margin-bottom:30px;">كيف أساعدكِ؟</h2>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown('<div class="card-container"><span class="card-icon">🥗</span><div class="card-title">إرشادات غذائية</div></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="card-container"><span class="card-icon">🩸</span><div class="card-title">إدارة السكر</div></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="card-container"><span class="card-icon">🏃</span><div class="card-title">نمط حياة</div></div>', unsafe_allow_html=True)
    with c4: st.markdown('<div class="card-container"><span class="card-icon">🎧</span><div class="card-title">دعم فوري</div></div>', unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)

    # 4. قسم النصائح الطبية (البطاقة الخضراء)
    st.markdown('<div id="tips" class="tips-wrapper">', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#1b4332; margin-bottom:30px; text-align:center;">إرشادات طبية لصيام آمن 🍏</h2>', unsafe_allow_html=True)
    st.markdown("""
        <div class="tips-layout">
            <div class="green-side">
                <h2>صيامكِ بوعيكِ أمانكِ</h2>
                <p>اتبعي النصائح الطبية واستمتعي برمضان بصحة ونشاط دائم.</p>
            </div>
            <div class="tips-list">
                <div class="instruction-row"><span class="ins-icon">🩺</span><div><b>التعديل الدوائي:</b> لا تبدئي الصيام دون استشارة طبيبك لتعديل جرعات الأنسولين أو الحبوب.</div></div>
                <div class="instruction-row"><span class="ins-icon">🥗</span><div><b>توازن الوجبات:</b> ابدئي إفطارك بالتمر والماء، واجعلي وجبة السحور غنية بالألياف والبروتين.</div></div>
                <div class="instruction-row"><span class="ins-icon">💧</span><div><b>الحماية من الجفاف:</b> اشربي لترين من الماء على الأقل في الفترة ما بين الإفطار والسحور.</div></div>
                <div class="instruction-row"><span class="ins-icon">📊</span><div><b>الفحص الدوري:</b> قومي بقياس مستوى السكر في الدم 4 مرات يومياً على الأقل خلال الصيام.</div></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # الزر السفلي
    col_btn_center = st.columns([1, 1, 1])
    with col_btn_center[1]:
        if st.button("ابدأ المحادثة الآن 💬", key="bottom_start"):
            st.session_state.page = 'chat'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. الفوتر الكامل
    st.markdown("""
        <div class="custom-footer">
            <div class="footer-col">
                <h3>رمضان بصحة</h3>
                <p>مساعدكِ الطبي الذكي المتخصص في رفع الوعي الصحي لمرضى السكري خلال الشهر الفضيل.</p>
            </div>
            <div class="footer-col footer-links" style="text-align:center;">
                <h4>روابط سريعة</h4>
                <a href="#top">الرئيسية 🏠</a>
                <a href="#about">حول السكري 🩸</a>
                <a href="#tips">نصائح وإرشادات 📋</a>
            </div>
            <div class="footer-col" style="text-align:left;">
                <h4>تواصل معنا</h4>
                <p>📧 info@ramadanhealth.com</p>
                <p>📍 المملكة العربية السعودية</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- صفحة الشات (بالقواعد الصارمة) ---
elif st.session_state.page == 'chat':
    # الهيدر الثابت
    st.markdown('<div class="sticky-header">', unsafe_allow_html=True)
    ch1, ch2 = st.columns([1, 5])
    with ch1:
        if st.button("⬅️ عودة"):
            st.session_state.page = 'home'
            st.rerun()
    with ch2:
        st.markdown('<h2 style="color:#1b4332; margin:0;">مساعد السكري الذكي 🌙</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # عرض الرسائل بفقاعات تتناسب مع حجم النص
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # منطقة الإدخال
    if prompt := st.chat_input("اسألي عن السكري في رمضان..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            
            # القواعد الصارمة للمساعد
            rules = """أنتِ مساعدة طبية ذكية متخصصة حصرياً في مرض السكري خلال شهر رمضان.
            1. إذا قام المستخدم بالترحيب (مثل: السلام عليكم، هلا، مرحبا)، رحبي بهِ بعبارة 'مرحباً بكِ في مساعد السكري الرمضاني، كيف يمكنني مساعدتكِ اليوم؟'.
            2. لا تجيبي على أي سؤال لا يتعلق بالسكري في رمضان (مثل الطبخ العام، الأخبار، الرياضة غير المرتبطة بالسكري).
            3. إذا سُئلتِ عن شيء خارج التخصص، اعتذري بلباقة وقولي: 'عذراً، أنا متخصصة فقط في تقديم الإرشادات الطبية لمرضى السكري خلال شهر رمضان لضمان سلامتكم'."""
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": rules}] + st.session_state.messages
            )
            answer = response.choices[0].message.content
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()
        except:
            # عدم إظهار رسالة الخطأ إلا عند الضرورة القصوى
            pass