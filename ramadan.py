import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة والخط
st.set_page_config(page_title="مساعد السكري الرمضاني", page_icon="🌙")

# 2. كود التنسيق (CSS) لتجميل الموقع
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    /* الخط العام والاتجاه */
    * { 
        font-family: 'Cairo', sans-serif !important; 
        direction: rtl;
    }

    /* تصميم فقاعة المستخدم (أخضر غامق) */
    .user-bubble {
        background-color: #1b4332;
        color: white;
        padding: 12px 18px;
        border-radius: 20px 20px 0px 20px;
        margin: 10px 0px 10px auto;
        width: fit-content;
        max-width: 80%;
        text-align: right;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }

    /* تصميم فقاعة المساعد (رصاصي فاتح) */
    .bot-bubble {
        background-color: #f0f2f6;
        color: #1e1e1e;
        padding: 12px 18px;
        border-radius: 20px 20px 20px 0px;
        margin: 10px auto 10px 0px;
        width: fit-content;
        max-width: 80%;
        text-align: right;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }

    /* إخفاء عناصر Streamlit الافتراضية المزعجة */
    [data-testid="stChatMessageAvatarUser"], 
    [data-testid="stChatMessageAvatarAssistant"],
    [data-testid="stChatMessageAvatar"] {
        display: none !important;
    }
    
    .stChatFloatingInputContainer {
        bottom: 20px;
    }
    
    /* تمركز العنوان والوصف */
    .main-title { text-align: center; color: #1b4332; font-weight: 700; }
    .sub-title { text-align: center; color: #555; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

# 3. واجهة التطبيق
st.markdown('<h1 class="main-title">🌙 مساعد السكري في رمضان</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">رفيقك الصحي لصيام آمن ومطمئن</p>', unsafe_allow_html=True)

# 4. الاتصال بـ OpenAI
# تأكدي أن مفتاح API موجود في الـ Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل بالتنسيق الجديد (الفقاعات الملونة)
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble">{message["content"]}</div>', unsafe_allow_html=True)

# صندوق الإدخال
if prompt := st.chat_input("كيف يمكنني مساعدتك؟"):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="user-bubble">{prompt}</div>', unsafe_allow_html=True)
    
    # طلب الرد من OpenAI
    with st.spinner("جاري التفكير..."):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "أنت مساعد طبي خبير لمرضى السكري في شهر رمضان. أجب بأسلوب ودود ومختصر وباللغة العربية."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ]
            )
            answer = response.choices[0].message.content
            
            # إضافة رد المساعد
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.markdown(f'<div class="bot-bubble">{answer}</div>', unsafe_allow_html=True)
            st.rerun() # لإعادة تحديث الصفحة وعرض الرسائل بترتيب صحيح
            
        except Exception as e:
            st.error("حدث خطأ في الاتصال، تأكدي من إعدادات الـ API.")