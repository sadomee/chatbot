import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة
st.set_page_config(page_title="مساعد السكري الرمضاني", page_icon="🌙")

# 2. كود التنسيق الشامل (توسيط الكلام وحل مشكلة اليمين/اليسار)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    /* جعل كل شيء في الصفحة يبدأ من اليمين ويكون الخط كايرو */
    * { 
        font-family: 'Cairo', sans-serif !important; 
        direction: rtl; 
        text-align: center; /* توحيد مركزية النصوص */
    }

    /* تنسيق صفحة الترحيب ليكون كل شيء في النص */
    .welcome-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 40px 20px;
        background-color: #ffffff;
        border-radius: 25px;
        margin-top: 50px;
    }
    
    /* فقاعات المحادثة - جعل النص بداخلها لليمين لتسهيل القراءة */
    .user-bubble { 
        background-color: #1b4332; 
        color: white; 
        padding: 12px 18px; 
        border-radius: 20px 20px 0px 20px; 
        margin: 10px 0px 10px auto; 
        width: fit-content; 
        max-width: 85%; 
        text-align: right; 
    }
    
    .bot-bubble { 
        background-color: #f0f2f6; 
        color: #1e1e1e; 
        padding: 12px 18px; 
        border-radius: 20px 20px 20px 0px; 
        margin: 10px auto 10px 0px; 
        width: fit-content; 
        max-width: 85%; 
        text-align: right; 
    }

    /* إخفاء الأيقونات وسحق الإطار الأحمر */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"], [data-testid="stChatMessageAvatar"] { display: none !important; }
    div[data-testid="stChatInput"] { border: 1px solid #1b4332 !important; border-radius: 12px !important; }
    div[data-testid="stChatInput"]:focus-within { border-color: #1b4332 !important; box-shadow: 0 0 0 0.15rem rgba(27, 67, 50, 0.2) !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة التنقل
if "page" not in st.session_state:
    st.session_state.page = "welcome"

# --- الصفحة الأولى: الترحيب ---
if st.session_state.page == "welcome":
    st.markdown('<div class="welcome-container">', unsafe_allow_html=True)
    st.markdown('<h1 style="color: #1b4332;">🌙 مرحباً بكِ</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1.2em;">أنا مساعدكِ الطبي المتخصص في السكري خلال شهر رمضان.</p>', unsafe_allow_html=True)
    if st.button("ابدأ المحادثة الآن"):
        st.session_state.page = "chat"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- الصفحة الثانية: المحادثة ---
elif st.session_state.page == "chat":
    if st.button("⬅️ خروج"):
        st.session_state.page = "welcome"
        st.rerun()
    
    st.markdown('<h2 style="text-align: center; color: #1b4332;">مركز استشارات السكري</h2>', unsafe_allow_html=True)

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض الرسائل
    for message in st.session_state.messages:
        cls = "user-bubble" if message["role"] == "user" else "bot-bubble"
        st.markdown(f'<div class="{cls}">{message["content"]}</div>', unsafe_allow_html=True)

    if prompt := st.chat_input("اسأليني عن السكري في رمضان..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.markdown(f'<div class="user-bubble">{prompt}</div>', unsafe_allow_html=True)
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "أنت مساعد طبي ودود متخصص في السكري ورمضان. "
                            "قواعد الرد: "
                            "1. إذا قال المستخدم (هلا، مرحباً، كيف حالك)، رحب به بلباقة وأخبره أنك هنا لمساعدته في استفسارات السكري ورمضان. "
                            "2. إذا كان السؤال عن السكري أو رمضان، أجب بدقة طبية. "
                            "3. لأي موضوع آخر تماماً، اعتذر بلباقة وقل: 'عذراً، أنا مبرمج للرد على الاستفسارات المتعلقة بمرض السكري في رمضان فقط لضمان سلامتك.'"
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
            st.error("حدث خطأ في الاتصال.")