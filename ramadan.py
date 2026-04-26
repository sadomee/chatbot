import streamlit as st
from openai import OpenAI

# 1. إعداد الصفحة
st.set_page_config(page_title="مساعد السكري الرمضاني", page_icon="🌙")

# 2. التنسيق الجمالي (بدون تخريب الأيقونات)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    * {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
    }
    
    .stApp {
        background-color: #f9f9f9;
    }

    /* جعل العنوان في المنتصف وبألوان جميلة */
    .main-title {
        text-align: center;
        color: #2E7D32;
        font-size: 2.5rem;
        margin-bottom: 0px;
    }
    
    .sub-title {
        text-align: center;
        color: #666;
        margin-bottom: 20px;
    }

    /* إصلاح اتجاه نصوص الرسائل */
    [data-testid="stChatMessageContent"] {
        text-align: right !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. واجهة المستخدم
st.markdown('<h1 class="main-title">🌙 مساعد السكري في رمضان</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">رفيقك الصحي لصيام آمن ومطمئن</p>', unsafe_allow_html=True)
st.divider()

# 4. الاتصال بـ OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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
                {"role": "system", "content": "أنت مساعد طبي متخصص لمرضى السكري في رمضان فقط. أجب بوضوح واختصار باللغة العربية."}
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
            st.error("حدث خطأ في الاتصال، تأكدي من الرصيد أو الإعدادات.")