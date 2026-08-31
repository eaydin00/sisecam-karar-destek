import streamlit as st
import pandas as pd
from google import genai

st.set_page_config(
    page_title="Şişecam Analiz & Karar Destek Sistemi",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Şişecam Yapay Zeka Destekli Analiz & Karar Destek Sistemi")
st.markdown("Operasyonel, teknik ve analitik problemleri analiz ederek en uygun yöntem ve aksiyon planını belirleyen karar destek sistemi.")

problem_input = st.text_area(
    "📝 Proje / Problem Tanımını Girin:",
    placeholder="Örn: Paketleme istasyonunda çevrim süresi çok yavaş, operatörler akışa yetişemiyor ve çatlak hataları artıyor.",
    height=120
)

if st.button("🚀 Problemi Analiz Et ve En Uygun Yöntemleri Belirle", type="primary"):
    if not problem_input.strip():
        st.warning("Lütfen analiz edilecek bir problem tanımı girin.")
    else:
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("Secrets içinde 'GEMINI_API_KEY' bulunamadı!")
        else:
            api_key = st.secrets["GEMINI_API_KEY"].strip()
            
            with st.spinner("Yapay zeka analizi hazırlıyor..."):
                client = genai.Client(api_key=api_key)
                
                prompt = f"""
                Sen endüstri mühendisliği, cam üretimi ve operasyonel mükemmellik alanında uzman kıdemli bir danışmansın.
                Aşağıdaki fabrika problemini detaylıca analiz et:
                
                Problem: "{problem_input}"
                
                Lütfen şu başlıklar altında kapsamlı ve profesyonel bir rapor üret:
                1. 🔍 **Kök Neden & Problem Özeti:** Problemin olası mekanik, insani veya süreçsel kök nedenleri.
                2. 🎯 **Önerilen Mühendislik Metotları:** Bu probleme özel en kritik 3 analiz yöntemi (Neden seçildiğini ve ne sağlayacağını açıkla).
                3. 🛠️ **Adım Adım Saha Aksiyon Planı:** Mühendislerin sahada uygulayacağı kronolojik adımlar.
                """
                
                response_text = None
                candidate_models = ["gemini-3.6-flash", "gemini-2.5-flash", "gemini-2.5-pro"]
                
                for model_name in candidate_models:
                    try:
                        resp = client.models.generate_content(
                            model=model_name,
                            contents=prompt
                        )
                        if resp and resp.text:
                            response_text = resp.text
                            break
                    except Exception:
                        continue
                
                if response_text:
                    st.success("Yapay Zeka Destekli Analiz Tamamlandı")
                    st.markdown(response_text)
                else:
                    st.error("Google sunucularındaki geçici yoğunluk nedeniyle yanıt alınamadı. Lütfen birkaç saniye sonra tekrar deneyin.")
