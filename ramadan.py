import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Ramadan Diabetes AI", page_icon="🌙")

# جلب المفتاح من Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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
            # هنا التعديل السحري: ندمج التعليمات الصارمة مع تاريخ المحادثة
            messages_to_send = [
                {
                    "role": "system", 
                    "content": (
                        "أنت مساعد طبي متخصص وحصري لمرضى السكري في شهر رمضان فقط. "
                        "مهامك: تقديم نصائح غذائية، توقيت الأدوية، وتحذيرات هبوط السكر في رمضان. "
                        "قاعدة صارمة: لا تجب على أي سؤال خارج موضوع السكري ورمضان. "
                        "إذا سألك المستخدم عن أي شيء آخر (مثل الطبخ العام، الدراسة، الرياضة، البرمجة، أو أسئلة عامة)، "
                        "اعتذر بلطف وقل: 'عذراً، أنا مبرمج لتقديم المساعدة الطبية لمرضى السكري في رمضان فقط لأضمن لك أدق المعلومات.'"
                    )
                }
            ]
            
            # إضافة الأسئلة السابقة ليتذكر المساعد سياق الكلام
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
            st.error("حدث خطأ في الاتصال بـ OpenAI")
            st.info(f"نص الخطأ التقني: {e}")