import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة
st.set_page_config(page_title="مساعد السكري الرمضاني", page_icon="🌙")

# 2. التنسيق (إخفاء الأيقونات وسحق الإطار الأحمر)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    * { font-family: 'Cairo', sans-serif !important; direction: rtl; }

    /* إخفاء الأيقونات نهائياً */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"], [data-testid="stChatMessageAvatar"] {
        display: none !important;
    }

    /* فقاعات المحادثة */
    .user-bubble { background-color: #1b4332; color: white; padding: 12px 18px; border-radius: 20px 20px 0px 20px; margin: 10px 0px 10px auto; width: fit-content; max-width: 85%; text-align: right; }
    .bot-bubble { background-color: #f0f2f6; color: #1e1e1e; padding: 12px 18px; border-radius: 20px 20px 20px 0px; margin: 10px auto 10px 0px; width: fit-content; max-width: 85%; text-align: right; }

    /* سحق الإطار الأحمر عند الكتابة */
    div[data-testid="stChatInput"] { border: 1px solid #1b4332 !important; border-radius: 12px !important; }
    div[data-testid="stChatInput"]:focus-within { border-color: #1b4332 !important; box-shadow: 0 0 0 0.15rem rgba(27, 67, 50, 0.2) !important; }
    [data-baseweb="textarea"] { border-color: transparent !important; }
    .stChatInputContainer textarea { border: none !important; box-shadow: none !important; }
    
    .main-title { text-align: center; color: #1b4332; font-weight: 700; margin-top: -20px; }
    .sub-title { text-align: center; color: #555; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🌙 مساعد السكري في رمضان</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">رفيقك الصحي لصيام آمن ومطمئن</p>', unsafe_allow_html=True)

# 4. الربط بـ OpenAI
if "OPENAI_API_KEY" not in st.secrets:
    st.error("الرجاء إضافة المفتاح في Secrets")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. عرض الرسائل
for message in st.session_state.messages:
    cls = "user-bubble" if message["role"] == "user" else "bot-bubble"
    st.markdown(f'<div class="{cls}">{message["content"]}</div>', unsafe_allow_html=True)

# 6. صندوق الإدخال مع منطق التخصيص
if prompt := st.chat_input("كيف يمكنني مساعدتك؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="user-bubble">{prompt}</div>', unsafe_allow_html=True)
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "أنت مساعد طبي متخصص حصرياً في مرض السكري خلال شهر رمضان فقط. "
                        "قواعدك الصارمة: "
                        "1. أجب فقط على الأسئلة المتعلقة بالسكري، التغذية لمريض السكري، والأدوية في رمضان. "
                        "2. إذا سألك المستخدم عن أي موضوع آخر (مثل الطبخ العام، الرياضة غير المرتبطة بالسكري، السياسة، العلوم، إلخ)، "
                        "يجب أن تعتذر بلباقة وتقول: 'عذراً، أنا مخصص فقط لتقديم النصائح المتعلقة بالسكري في رمضان.'"
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
        st.error(f"حدث خطأ: {str(e)}")