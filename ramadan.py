import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Ramadan Diabetes AI " , page_icon="🌙")

# ملاحظة: مفتاح الـ API الخاص بك يظهر هنا، يفضل دائماً إبقاؤه سرياً
client = OpenAI(api_key="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")

st.title("🌙 مساعد السكري في رمضان (AI)")

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
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "أنت مساعد طبي خبير في السكري ورمضان."},
                    {"role": "user", "content": prompt}
                ]
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error("حدث خطأ في الاتصال بـ OpenAI")
            st.info(f"نص الخطأ التقني: {e}")
