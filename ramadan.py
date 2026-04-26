import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة
st.set_page_config(page_title="مساعد السكري الرمضاني", page_icon="🌙")

# 2. كود التنسيق (CSS) لضبط النصوص لليمين وحذف المساحات البيضاء
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    /* ضبط الخط والاتجاه لليمين لجميع العناصر */
    * { 
        font-family: 'Cairo', sans-serif !important; 
        direction: rtl; 
        text-align: right; 
    }

    /* حذف المساحة البيضاء العلوية (Padding) */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }

    /* تنسيق صفحة الترحيب لتبدأ من اليمين وبدون مساحات زائدة */
    .welcome-container {
        padding: 20px 0px;
        margin-top: 0px;
    }

    /* تصميم فقاعات المحادثة */
    .user-bubble { 
        background-color: #1b4332; 
        color: white; 
        padding: 12px 18px; 
        border-radius: 20px 20px 0px 20px; 
        margin: 10px 0px 10px auto; 
        width: fit-content; 
        max-width: 85%; 
    }
    
    .bot-bubble { 
        background-color: #f0f2f6; 
        color: #1e1e1e; 
        padding: 12px 18px; 
        border-radius: 20px 20px 20px 0px; 
        margin: 10px auto 10px 0px; 
        width: fit-content; 
        max-width: 85%; 
    }

    /* إخفاء العناصر غير الضرورية */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"], [data-testid="stChatMessageAvatar"] { display: none !important; }
    div[data-testid="stChatInput"] { border: 1px solid #1b4332 !important; border-radius: 12px !important; }
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة التنقل بين الصفحات
if "page" not in st.session_state:
    st.session_state.page = "welcome"

# --- الصفحة الأولى: الترحيب (نصوص فقط وجهة اليمين) ---
if st.session_state.page == "welcome":
    st.markdown('<div class="welcome-container">', unsafe_allow_html=True)
    st.markdown('<h1 style="color: #1b4332; font-size: 2.2em; margin-bottom: 10px;">مرحباً بكِ</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1.3em; color: #333; margin-bottom: 5px;">أنا مساعدكِ الطبي المتخصص في التوعية بمرض السكري خلال شهر رمضان المبارك.</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1em; color: #666;">يمكنكِ البدء الآن للحصول على نصائح طبية مخصصة لصحة صيامكِ.</p>', unsafe_allow_html=True)
    st.write("")
    if st.button("ابدأ المحادثة الآن"):
        st.session_state.page = "chat"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- الصفحة الثانية: المحادثة ---
elif st.session_state.page == "chat":
    if st.button("⬅️ عودة للرئيسية"):
        st.session_state.page = "welcome"
        st.rerun()
    
    st.markdown('<h2 style="color: #1b4332; margin-bottom: 20px;">مركز استشارات السكري</h2>', unsafe_allow_html=True)

    # التحقق من وجود المفتاح في Secrets
    if "OPENAI_API_KEY" not in st.secrets:
        st.error("الرجاء إضافة OPENAI_API_KEY في إعدادات Secrets")
    else:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # عرض الرسائل
        for message in st.session_state.messages:
            cls = "user-bubble" if message["role"] == "user" else "bot-bubble"
            st.markdown(f'<div class="{cls}">{message["content"]}</div>', unsafe_allow_html=True)

        # صندوق الإدخال
        if prompt := st.chat_input("اكتبي استفساركِ الطبي هنا..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.markdown(f'<div class="user-bubble">{prompt}</div>', unsafe_allow_html=True)
            
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system", 
                            "content": (
                                "أنت مساعد طبي متخصص وحصري لمرض السكري في رمضان. "
                                "رحبي بالمستخدم عند التحية، وأجيبي فقط على أسئلة السكري ورمضان. "
                                "لأي موضوع آخر، اعتذري بلباقة قائلة أنك مخصصة فقط للسكري لضمان السلامة."
                            )
                        },
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    ]
                )
                answer = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.markdown(f'<div class="bot-bubble">{answer}</div>', unsafe_allow_html=True)
                st.rerun()
            except Exception as e:
                st.error("حدث خطأ، يرجى التأكد من رصيد وصلاحية مفتاح الـ API.")