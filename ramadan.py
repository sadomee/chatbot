import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="السكري في رمضان | Diabetes in Ramadan", page_icon="🌙", layout="wide")

# إدارة الحالة (اللغة والصفحات)
if 'lang' not in st.session_state: st.session_state.lang = 'ar'
if 'page' not in st.session_state: st.session_state.page = 'home'
if "messages" not in st.session_state: st.session_state.messages = []

# منطق تبديل اللغة
query_params = st.query_params
if "change" in query_params:
    st.session_state.lang = query_params["change"]
    st.query_params.clear()
    st.rerun()

is_ar = st.session_state.lang == 'ar'

# 2. القاموس الكامل (يحتوي على كافة النصوص الأصلية وأسئلة الدكتور)
t = {
    "title": "ريبوت دردشة لدعم مرضى السكري خلال رمضان" if is_ar else "Ramadan Diabetes Chatbot",
    "emergency_btn": "🚨 حالات الطوارئ / انخفاض أو ارتفاع السكر" if is_ar else "🚨 Emergency / Blood Sugar Fluctuations",
    "emergency_msg": """
    **إجراءات الطوارئ السريعة:**
    * افحص سكر الدم فوراً.
    * اقطع الصيام فوراً إذا كان السكر أقل من 70 أو أكثر من 300 مجم/ديسيلتر.
    * اطلب الرعاية الطبية العاجلة فوراً إذا لم تستقر الحالة أو ساءت الأعراض.
    """ if is_ar else "Quick Emergency Procedures: Check blood sugar, break fast if <70 or >300 mg/dL.",
    "disclaimer": "⚠️ **إخلاء مسؤولية:** هذا التطبيق للأغراض التعليمية فقط وليس نصيحة طبية بديلة." if is_ar else "⚠️ Disclaimer: Educational purposes only.",
    "hero_h1": "مرحباً بكِ 🌙" if is_ar else "Welcome 🌙",
    "hero_p": "أنا مساعدكِ الطبي المتخصص في التوعية بمرض السكري خلال شهر رمضان المبارك." if is_ar else "I am your medical assistant for diabetes awareness during Ramadan.",
    "start_btn": "ابدأ المحادثة الآن 💬" if is_ar else "Start Chatting Now 💬",
    "about_h3": "حول السكري في رمضان 🩸" if is_ar else "About Diabetes in Ramadan 🩸",
    "about_p": "إدارة السكري خلال الصيام تتطلب وعياً طبياً دقيقاً؛ حيث تختلف احتياجات الجسم للطاقة والعلاج بين ساعات الصيام والإفطار. يهدف هذا المساعد لتزويدك بإرشادات فورية حول كيفية التعامل مع تقلبات السكر." if is_ar else "Managing diabetes during fasting requires precise medical awareness.",
    "how_help": "كيف أساعدكِ؟" if is_ar else "How can I help you?",
    "c1": "إرشادات غذائية" if is_ar else "Nutrition",
    "c2": "إدارة السكر" if is_ar else "Sugar Mgmt",
    "c3": "نمط حياة" if is_ar else "Lifestyle",
    "c4": "دعم فوري" if is_ar else "Instant Support",
    "tips_h2": "إرشادات طبية لصيام آمن 🍏" if is_ar else "Medical Guidelines for Safe Fasting 🍏",
    "tips_side_h2": "صيامكِ بوعيكِ أمانكِ" if is_ar else "Your Awareness, Your Safety",
    "tips_side_p": "اتبعي النصائح الطبية واستمتعي برمضان بصحة ونشاط دائم." if is_ar else "Follow medical advice for your safety.",
    "t1_h": "التعديل الدوائي:" if is_ar else "Medication Adjustment:",
    "t1_p": "لا تبدئي الصيام دون استشارة طبيبك لتعديل جرعات الأنسولين أو الأدوية." if is_ar else "Consult your doctor for medication.",
    "t2_h": "توازن الوجبات:" if is_ar else "Balanced Meals:",
    "t2_p": "ابدئي إفطارك بالتمر والماء، واجعلي وجبة السحور غنية بالألياف والبروتين." if is_ar else "Balance your Iftar and Suhoor.",
    "t3_h": "الحماية من الجفاف:" if is_ar else "Dehydration Protection:",
    "t3_p": "اشربي لترين من الماء على الأقل في الفترة ما بين الإفطار والسحور." if is_ar else "Drink plenty of water.",
    "t4_h": "الفحص الدوري:" if is_ar else "Regular Testing:",
    "t4_p": "قومي بقياس مستوى السكر في الدم 4 مرات يومياً على الأقل خلال الصيام." if is_ar else "Monitor blood sugar levels.",
    "footer_title": "رمضان بصحة" if is_ar else "Healthy Ramadan",
    "footer_p": "مساعدكِ الطبي الذكي المتخصص في رفع الوعي الصحي لمرضى السكري خلال الشهر الفضيل." if is_ar else "Your smart medical assistant.",
    "footer_quick": "روابط سريعة" if is_ar else "Quick Links",
    "footer_home": "الرئيسية 🏠" if is_ar else "Home 🏠",
    "footer_about": "حول السكري 🩸" if is_ar else "About Diabetes 🩸",
    "footer_tips": "نصائح وإرشادات 📋" if is_ar else "Tips & Guidelines 📋",
    "footer_contact": "تواصل معنا" if is_ar else "Contact Us",
    "back": "⬅️ عودة" if is_ar else "⬅️ Back",
    "placeholder": "اسألي عن السكري في رمضان..." if is_ar else "Ask about diabetes in Ramadan...",
    "sample_title": "أسئلة شائعة مقترحة 💡" if is_ar else "Common Questions 💡",
    "q1": "ماذا يجب أن آكل في السحور؟" if is_ar else "What to eat for Suhoor?",
    "q2": "متى يجب عليّ قياس السكر؟" if is_ar else "When to check sugar?",
    "q3": "هل ممارسة الرياضة آمنة؟" if is_ar else "Is exercise safe?"
}

# 3. كود الـ CSS الكامل
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    * {{ font-family: 'Cairo', sans-serif !important; direction: {"rtl" if is_ar else "ltr"}; text-align: {"right" if is_ar else "left"}; }}
    header, footer, .stDeployButton {{ visibility: hidden; }}
    .block-container {{ padding-top: 2rem !important; }}

    .floating-lang-btn {{
        position: fixed !important; bottom: 30px !important;
        {"left: 30px !important;" if is_ar else "right: 30px !important;"}
        background-color: #1b4332 !important; color: white !important;
        padding: 12px 25px !important; border-radius: 50px !important;
        text-decoration: none !important; z-index: 999999 !important;
        border: 2px solid white !important; box-shadow: 0px 4px 15px rgba(0,0,0,0.3); font-weight: bold !important;
    }}

    .hero-flex {{ display: flex; justify-content: space-between; align-items: center; background: #f8faf9; padding: 50px; border-radius: 30px; margin-bottom: 30px; }}
    .hero-text-container h1 {{ color: #1b4332; font-size: 3.5rem; }}
    .hero-text-container p {{ color: #2d6a4f; font-size: 1.3rem; }}
    
    .about-box {{ background: white; padding: 35px; border-radius: 25px; border: 1px solid #e5e7eb; margin-bottom: 40px; }}
    .card-container {{ background: white; padding: 25px; border-radius: 25px; border: 1px solid #eee; text-align: center; margin-bottom: 20px; transition: 0.3s; }}
    .card-icon {{ font-size: 2.5rem; margin-bottom: 15px; display: block; }}
    .card-title {{ color: #1b4332; font-weight: 700; }}

    .tips-layout {{ display: flex; gap: 25px; margin-bottom: 30px; flex-wrap: wrap; }}
    .green-side {{ background: #1b4332; color: white; padding: 40px; border-radius: 30px; flex: 1; min-width: 300px; display: flex; flex-direction: column; justify-content: center; }}
    .tips-list {{ flex: 2; background: white; border-radius: 25px; border: 1px solid #eee; overflow: hidden; min-width: 350px; }}
    .instruction-row {{ padding: 20px; border-bottom: 1px solid #f5f5f5; display: flex; align-items: center; }}
    .ins-icon {{ font-size: 1.5rem; {"margin-left: 15px;" if is_ar else "margin-right: 15px;"} background: #f0f7f4; padding: 10px; border-radius: 50%; }}

    .custom-footer {{ background: #1b4332; color: white; padding: 60px 40px; border-radius: 40px 40px 0 0; display: flex; justify-content: space-between; margin-top: 60px; flex-wrap: wrap; gap: 30px; }}
    .footer-links a {{ color: white !important; text-decoration: none; display: block; margin-bottom: 12px; }}

    div.stButton > button[kind="primary"] {{ background-color: #1b4332 !important; color: white !important; border-radius: 50px !important; padding: 12px 35px !important; border: none !important; }}
    div.stButton > button[kind="secondary"] {{ background-color: #d00000 !important; color: white !important; border-radius: 50px !important; padding: 12px 35px !important; border: none !important; }}

    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {{ display: none !important; }}
    div[aria-label="Chat message from user"] .stMarkdown {{ background-color: #1b4332 !important; color: white !important; border-radius: 20px 20px 2px 20px !important; padding: 12px 20px !important; margin-left: {"auto" if is_ar else "0"}; margin-right: {"0" if is_ar else "auto"}; width: fit-content !important; }}
    div[aria-label="Chat message from assistant"] .stMarkdown {{ background-color: #f0f2f6 !important; border-radius: 20px 20px 20px 2px !important; padding: 12px 20px !important; border: 1px solid #e5e7eb !important; width: fit-content !important; }}
    </style>
    <a href="?change={"en" if is_ar else "ar"}" target="_self" class="floating-lang-btn">{"English" if is_ar else "العربية"}</a>
""", unsafe_allow_html=True)

# --- الصفحة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown('<div id="top"></div>', unsafe_allow_html=True)
    col_t, col_e = st.columns([4, 2])
    with col_t: st.markdown(f'<h2 style="color:#1b4332;">{t["title"]}</h2>', unsafe_allow_html=True)
    with col_e: 
        if st.button(t["emergency_btn"], type="secondary"): st.error(t["emergency_msg"])
    st.warning(t["disclaimer"])
    st.markdown(f'<div class="hero-flex"><div><h1>{t["hero_h1"]}</h1><p>{t["hero_p"]}</p></div></div>', unsafe_allow_html=True)
    if st.button(t["start_btn"], type="primary"):
        st.session_state.page = 'chat'
        st.rerun()

    st.markdown(f'<div id="about" class="about-box"><h3>{t["about_h3"]}</h3><p>{t["about_p"]}</p></div>', unsafe_allow_html=True)
    st.markdown(f'<h2 style="color:#1b4332; text-align:center; margin-bottom:30px;">{t["how_help"]}</h2>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="card-container"><span class="card-icon">🥗</span><div class="card-title">{t["c1"]}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="card-container"><span class="card-icon">🩸</span><div class="card-title">{t["c2"]}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="card-container"><span class="card-icon">🏃</span><div class="card-title">{t["c3"]}</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="card-container"><span class="card-icon">🎧</span><div class="card-title">{t["c4"]}</div></div>', unsafe_allow_html=True)

    st.markdown(f'<h2 style="color:#1b4332; text-align:center; margin:30px 0;">{t["tips_h2"]}</h2>', unsafe_allow_html=True)
    st.markdown(f'''
        <div id="tips" class="tips-layout">
            <div class="green-side"><h2>{t["tips_side_h2"]}</h2><p>{t["tips_side_p"]}</p></div>
            <div class="tips-list">
                <div class="instruction-row"><span class="ins-icon">🩺</span><div><b>{t["t1_h"]}</b> {t["t1_p"]}</div></div>
                <div class="instruction-row"><span class="ins-icon">🥗</span><div><b>{t["t2_h"]}</b> {t["t2_p"]}</div></div>
                <div class="instruction-row"><span class="ins-icon">💧</span><div><b>{t["t3_h"]}</b> {t["t3_p"]}</div></div>
                <div class="instruction-row"><span class="ins-icon">📊</span><div><b>{t["t4_h"]}</b> {t["t4_p"]}</div></div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown(f'''
        <div class="custom-footer">
            <div class="footer-col"><h3>{t["footer_title"]}</h3><p>{t["footer_p"]}</p></div>
            <div class="footer-col footer-links" style="text-align:center;">
                <h4>{t["footer_quick"]}</h4>
                <a href="#top">{t["footer_home"]}</a><a href="#about">{t["footer_about"]}</a><a href="#tips">{t["footer_tips"]}</a>
            </div>
            <div class="footer-col"><h4>{t["footer_contact"]}</h4><p>📧 info@ramadanhealth.com</p></div>
        </div>
    ''', unsafe_allow_html=True)

# --- صفحة الشات ---
elif st.session_state.page == 'chat':
    if st.button(t["back"], type="primary"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown(f'<h2 style="color:#1b4332;">{t["title"]}</h2>', unsafe_allow_html=True)
    st.markdown(f"<h5>{t['sample_title']}</h5>", unsafe_allow_html=True)
    sq1, sq2, sq3 = st.columns(3)
    clicked_q = None
    with sq1: 
        if st.button(t["q1"], type="primary"): clicked_q = t["q1"]
    with sq2: 
        if st.button(t["q2"], type="primary"): clicked_q = t["q2"]
    with sq3: 
        if st.button(t["q3"], type="primary"): clicked_q = t["q3"]

    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    prompt = st.chat_input(t["placeholder"])
    if clicked_q: prompt = clicked_q

    if prompt:
        # عرض رسالة المستخدم فوراً
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        # معالجة الرد
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "You are a helpful medical assistant."}] + st.session_state.messages
            )
            ans = response.choices[0].message.content
            
            # عرض رد البوت وحفظه
            with st.chat_message("assistant"): st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
            
            # تحديث الصفحة بشكل صحيح لضمان بقاء الرسالة
            st.rerun()
        except Exception as e:
            st.error("Technical Error. Please check API Key.")