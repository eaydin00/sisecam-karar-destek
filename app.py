import streamlit as st
import pandas as pd
from google import genai

st.set_page_config(
    page_title="Şişecam Analiz & Karar Destek Sistemi",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Şişecam Yapay Zeka Destekli Analiz & Karar Destek Sistemi")
st.markdown("Operasyonel, teknik ve analitik problemleri analiz ederek en uygun yöntemleri puanlayan ve somut aksiyonları belirleyen karar destek sistemi.")

problem_input = st.text_area(
    "📝 Proje / Problem Tanımını Girin:",
    placeholder="Örn: Paketleme istasyonunda çevrim süresi çok yavaş, operatörler akışa yetişemiyor ve çatlak hataları artıyor.",
    height=120
)

if st.button("🚀 Problemi Analiz Et ve Yöntemleri Puanla", type="primary"):
    if not problem_input.strip():
        st.warning("Lütfen analiz edilecek bir problem tanımı girin.")
    else:
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("Secrets içinde 'GEMINI_API_KEY' bulunamadı!")
        else:
            api_key = st.secrets["GEMINI_API_KEY"].strip()
            
            with st.spinner("Yapay zeka yöntemleri puanlıyor ve analizi hazırlıyor..."):
                client = genai.Client(api_key=api_key)
                
                prompt = f"""
                Sen endüstri mühendisliği, cam üretimi ve operasyonel mükemmellik alanında uzman kıdemli bir Karar Destek Danışmanısın.
                Aşağıdaki fabrika problemini detaylıca analiz et:
                
                Problem: "{problem_input}"
                
                Lütfen yanıtını tam olarak şu 3 ana başlık altında ve net bir dille oluştur:
                
                1. 🔍 **Kök Neden & Durum Değerlendirmesi:**
                   Problemin temel kaynaklarını (makine, süreç, insan, yerleşim vb.) net ve teknik bir dille özetle.
                
                2. 📊 **Analitik Yöntem Uygunluk ve Puanlama Tablosu:**
                   Bu problem için uygulanabilecek tüm alternatif mühendislik yöntemlerini değerlendir ve Markdown tablosu olarak sun.
                   Tablo kolonları:
                   | Öncelik | Önerilen Analiz Yöntemi | Uygunluk Puanı (100 Üzerinden) | Neden Bu Yöntem? (Beklenen Katkı) |
                   
                3. 🛠️ **Yöntem Bazlı Somut Saha Aksiyonları:**
                   (NOT: Günlük/haftalık fazlara, yapay takvimlere BÖLME. Doğrudan yöntem bazında sahada ne yapılacağını açıkla.)
                   Tabloda yüksek puan alan (uygun bulunan) yöntemlerin her biri için sahada atılacak somut, teknik adımları alt başlıklar halinde madde madde yaz.
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
                    st.success("Yapay Zeka Destekli Analiz ve Puanlama Tamamlandı")
                    st.markdown(response_text)
                else:
                    st.error("Sunucu yoğunluğu nedeniyle yanıt alınamadı. Lütfen birkaç saniye sonra tekrar deneyin.")
