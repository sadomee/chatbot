import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة
st.set_page_config(page_title="مساعد السكري الرمضاني", page_icon="🌙")

# 2. التنسيق (CSS) - النسخة "المبسطة جداً" لضمان العمل
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    /* تغيير الخط والاتجاه */
    * { 
        font-family: 'Cairo', sans-serif !important; 
    }
    
    /* إخفاء المربعات (face و art) */
    [data-testid="stChatMessageAvatar"] { 
        display: none !important; 
    }

    /* جعل الفقاعات تظهر بشكل مرتب وتدعم العربي والإنجليزي */
    [data-testid="stChatMessageContent"] {
        text-align: start !important;
        unicode-bidi: plaintext !important;
    }

    /* تلوين الفقاعات (المستخدم والمساعد) */
    .stChatMessage {
        border-radius: 15px !important;
        margin-bottom: 10px !important;
    }

    /* جعل العنوان والوصف في المنتصف */
    h1, .stMarkdown p { 
        text-align: center !important; 
        color: #1b4332; 
    }
    </style>
    """, unsafe_allow_html=True)

# 3. الاتصال بـ OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 4. واجهة التطبيق
st.title("🌙 مساعد السكري في رمضان")
st.write("رفيقك الصحي لصيام آمن ومطمئن")
st.divider()

# 5. منطق المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    # هنا السر: نحدد لون الفقاعة بناءً على من يتحدث
    avatar_style = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("كيف يمكنني مساعدتك؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "أنت مساعد طبي للسكري في رمضان."}, 
                          {"role": "user", "content": prompt}]
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except:
            st.error("عذراً، حدث خطأ")