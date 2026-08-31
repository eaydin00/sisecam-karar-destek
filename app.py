import streamlit as st
import pandas as pd
import google.generativeai as genai

st.set_page_config(
    page_title="Şişecam Analiz & Karar Destek Sistemi",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Şişecam Yapay Zeka Destekli Analiz & Karar Destek Sistemi")
st.markdown("Operasyonel, teknik ve analitik problemleri analiz ederek en uygun yöntem ve aksiyon planını belirleyen hibrit karar destek sistemi.")

problem_input = st.text_area(
    "📝 Proje / Problem Tanımını Girin:",
    placeholder="Örn: Paketleme istasyonunda çevrim süresi çok yavaş, operatörler akışa yetişemiyor ve çatlak hataları artıyor.",
    height=120
)

if st.button("🚀 Problemi Analiz Et ve En Uygun Yöntemleri Belirle", type="primary"):
    if not problem_input.strip():
        st.warning("Lütfen analiz edilecek bir problem tanımı girin.")
    else:
        # Secrets kontrolü
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("Secrets içinde 'GEMINI_API_KEY' bulunamadı! Lütfen Streamlit Secrets alanını kontrol edin.")
        else:
            api_key = st.secrets["GEMINI_API_KEY"].strip()
            
            with st.spinner("Yapay zeka analizi hazırlanıyor..."):
                try:
                    genai.configure(api_key=api_key)
                    # En güncel kararlı flash modeli
                    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
                    
                    prompt = f"""
                    Sen endüstri mühendisliği, cam üretimi ve operasyonel mükemmellik alanında uzman kıdemli bir danışmansın.
                    Aşağıdaki fabrika problemini detaylıca analiz et:
                    
                    Problem: "{problem_input}"
                    
                    Lütfen şu başlıklar altında kapsamlı ve profesyonel bir rapor üret:
                    1. 🔍 **Kök Neden & Problem Özeti:** Problemin olası mekanik, insani veya süreçsel kök nedenleri.
                    2. 🎯 **Önerilen Mühendislik Metotları:** Bu probleme özel en kritik 3 analiz yöntemi (Neden seçildiğini ve ne sağlayacağını açıkla).
                    3. 🛠️ **Adım Adım Saha Aksiyon Planı:** Mühendislerin sahada uygulayacağı kronolojik adımlar.
                    """
                    
                    response = model.generate_content(prompt)
                    st.success("Yapay Zeka Destekli Analiz Tamamlandı")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Yapay zeka çağrısında hata oluştu: {str(e)}")
