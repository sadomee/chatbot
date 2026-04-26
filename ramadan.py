import streamlit as st
from openai import OpenAI

# إعداد الصفحة مع أيقونة وعنوان
st.set_page_config(page_title="مساعد السكري الرمضاني", page_icon="🌙")
# كود تغيير الخط بشكل أقوى
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');

    /* هذا الجزء يستهدف كل عناصر الموقع ويجبرها على تغيير الخط */
    * {
        font-family: 'Cairo', sans-serif !important;
    }
    
    body, p, div, span, h1, h2, h3, h4, h5, h6, input, button, textarea {
        font-family: 'Cairo', sans-serif !important;
        text-align: right !important;
        direction: rtl !important;
    }

    /* تعديل خاص بمنطقة إدخال النص الأسفل */
    .stChatInputContainer textarea {
        font-family: 'Cairo', sans-serif !important;
    }
    </style>
    """, unsafe_allow_html=True)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- واجهة Sidebar الجانبية ---
with st.sidebar:
    st.markdown("### عن المساعد 🌙")
    st.info("نحن هنا لنساعدك في تنظيم سكرك خلال الشهر الفضيل بصورة آمنة.")
    st.write("---")
    st.write("💡 **نصيحة اليوم:** احرص على قياس السكر قبل الفطور بساعتين.")

# --- تحسين شكل العنوان ---
st.markdown("<h1 style='text-align: center; color: #2E7D32;'>🌙 مساعد السكري في رمضان</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>رفيقك الذكي لصيام صحي ومطمئن</p>", unsafe_allow_html=True)
st.divider()

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
                {"role": "system", "content": "أنت مساعد طبي متخصص لمرضى السكري في رمضان. لا تجب على مواضيع خارج هذا النطاق."}
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
            st.error("حدث خطأ تقني")