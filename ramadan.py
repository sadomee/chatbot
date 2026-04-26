import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة
st.set_page_config(page_title="مساعد السكري الرمضاني", page_icon="🌙")

# 2. كود التنسيق (CSS) - وضعته بطريقة تمنع حدوث أخطاء
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    /* 1. تصميم الخلفية العامة */
    .stApp {
        background: linear-gradient(180deg, #f0f7f4 0%, #ffffff 100%);
        font-family: 'Cairo', sans-serif !important;
    }

    /* 2. تحسين شكل العنوان */
    h1 {
        color: #1b4332 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        font-weight: 700 !important;
    }

    /* 3. تجميل فقاعات المحادثة */
    [data-testid="stChatMessage"] {
        background-color: white !important;
        border-radius: 15px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
        margin-bottom: 15px !important;
        padding: 10px !important;
    }

    /* 4. تعديل صندوق الإدخال */
    .stChatInputContainer {
        padding-bottom: 20px !important;
    }

    /* 5. ضبط النصوص والاتجاهات */
    * {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
    }
    </style>
    """, unsafe_allow_html=True)

# إضافة "بطاقة ترحيب" أنيقة في البداية
st.info("💡 **مرحباً بكِ في مساعدكِ الرمضاني.** اسأليني عن تنظيم السكر، الوجبات الصحية، أو متى يجب عليكِ الإفطار.")

# 3. الاتصال بـ OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 4. العنوان والواجهة
st.title("🌙 مساعد السكري في رمضان")
st.write("رفيقك الصحي لصيام آمن")
st.divider()

# 5. نظام الرسائل (Chat Logic)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("كيف يمكنني مساعدتك؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        try:
            messages_to_send = [
                {"role": "system", "content": "أنت مساعد طبي لمرضى السكري في رمضان فقط. أجب باختصار وباللغة العربية."}
            ]
            for m in st.session_state.messages:
                messages_to_send.append({"role": m["role"], "content": m["content"]})

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages_to_send
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error("عذراً، حدث خطأ تقني.")