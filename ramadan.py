import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة
st.set_page_config(page_title="مساعد السكري الرمضاني", page_icon="🌙")

# 2. كود التنسيق (CSS) - النسخة المضادة للون الأحمر
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    * { font-family: 'Cairo', sans-serif !important; direction: rtl; }

    /* تصميم فقاعة المستخدم (أخضر غامق) */
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

    /* تصميم فقاعة المساعد (رصاصي فاتح) */
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

    /* إخفاء الأيقونات والمربعات نهائياً */
    [data-testid="stChatMessageAvatarUser"], 
    [data-testid="stChatMessageAvatarAssistant"],
    [data-testid="stChatMessageAvatar"],
    .stChatMessage [data-testid="stChatMessageAvatar"] {
        display: none !important;
    }

    /* --- الحل الجذري للإطار الأحمر --- */
    /* استهداف الصندوق في كل حالاته (التركيز، النشاط، وحتى الخطأ) */
    div[data-testid="stChatInput"] {
        border: 1px solid #1b4332 !important; /* أخضر دائماً */
        border-radius: 12px !important;
    }

    /* إجبار الإطار على اللون الأخضر عند الضغط (Focus) ومنع الأحمر */
    div[data-testid="stChatInput"]:focus-within {
        border-color: #1b4332 !important;
        box-shadow: 0 0 0 0.2rem rgba(27, 67, 50, 0.2) !important;
    }

    /* حذف أي إطار أحمر ناتج عن الـ Validation الخاص بـ Streamlit */
    div[data-testid="stChatInput"] > div {
        border: none !important;
        box-shadow: none !important;
    }

    .stChatInputContainer textarea {
        border: none !important;
        box-shadow: none !important;
        background-color: transparent !important;
    }
    
    /* منع ظهور اللون الأحمر عند ترك الصندوق فارغاً */
    [data-baseweb="textarea"] {
        border-color: transparent !important;
    }
    /* ------------------------------------------- */

    .main-title { text-align: center; color: #1b4332; font-weight: 700; margin-top: -20px; }
    .sub-title { text-align: center; color: #555; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 3. واجهة التطبيق
st.markdown('<h1 class="main-title">🌙 مساعد السكري في رمضان</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">رفيقك الصحي لصيام آمن ومطمئن</p>', unsafe_allow_html=True)

# 4. إعداد OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. عرض الرسائل
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble">{message["content"]}</div>', unsafe_allow_html=True)

# 6. صندوق الإدخال
if prompt := st.chat_input("كيف يمكنني مساعدتك؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="user-bubble">{prompt}</div>', unsafe_allow_html=True)
    
    with st.spinner("جاري التحضير..."):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "أنت مساعد طبي خبير لمرضى السكري في رمضان."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ]
            )
            answer = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.markdown(f'<div class="bot-bubble">{answer}</div>', unsafe_allow_html=True)
            st.rerun()
        except Exception as e:
            st.error("تأكدي من رصيد الـ API.")