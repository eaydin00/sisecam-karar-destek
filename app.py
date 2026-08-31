import streamlit as st
import pandas as pd
from google import genai

st.set_page_config(
    page_title="Şişecam Analiz & Karar Destek Sistemi",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Şişecam Yapay Zeka Destekli Analiz & Karar Destek Sistemi")
st.markdown("Operasyonel ve teknik problemleri tanımlı analiz yöntemleri havuzuyla eşleştiren, puanlayan ve somut aksiyonları belirleyen karar destek sistemi.")

# Kurumsal Bilgi Tabanı / Onaylı Metot Havuzu
APPROVED_METHODS = """
1. Zaman Etüdü & İş Örneklemesi
2. Hat Dengeleme & Çevrim Zamanı Analizi
3. FMEA / PFMEA (Hata Türleri ve Etkileri Analizi)
4. 5 Neden (5 Why) & Kök Neden Analizi
5. Pareto Analizi (80/20 Kuralı)
6. Balık Kılçığı (Ishikawa) Diyagramı
7. SMED (Hızlı Model/Kalıp Değişimi)
8. SPC (İstatistiksel Proses Kontrol)
9. Ergonomi & 5S Çalışma Alanı Düzenleme
10. OEE (Toplam Ekipman Etkinliği) Analizi
11. Değer Akış Haritalama (VSM - Value Stream Mapping)
12. Poka-Yoke (Hata Önleyici Düzenekler)
"""

problem_input = st.text_area(
    "📝 Proje / Problem Tanımını Girin:",
    placeholder="Örn: Paketleme istasyonunda çevrim süresi çok yavaş, operatörler akışa yetişemiyor ve çatlak hataları artıyor.",
    height=120
)

if st.button("🚀 Problemi Analiz Et ve Yöntemleri Belirle", type="primary"):
    if not problem_input.strip():
        st.warning("Lütfen analiz edilecek bir problem tanımı girin.")
    else:
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("Secrets içinde 'GEMINI_API_KEY' bulunamadı!")
        else:
            api_key = st.secrets["GEMINI_API_KEY"].strip()
            
            with st.spinner("Yapay zeka tanımlı metot havuzunu tarıyor..."):
                client = genai.Client(api_key=api_key)
                
                prompt = f"""
                Sen kurumsal standartlara ve tanımlı metot havuzuna sıkı sıkıya bağlı bir Karar Destek Danışmanısın.

                KATI KURALLAR:
                1. YALNIZCA aşağıdaki "Onaylı Analiz Yöntemleri Havuzu"nda yer alan metotları kullan. Bu listede bulunmayan hiçbir yeni yöntem türetme veya önerme.
                2. Problem metninde açıkça belirtilmeyen süreç değişkenleri, makineler veya durumlar hakkında varsayımda bulunma. Yalnızca verilen metindeki ifadelere dayan.
                3. Öneri kurgusu: Öncelikle tam 1 adet "Ana Yöntem", ardından gerekliyse en fazla 2 adet "Destekleyici Yöntem" seç (Toplamda maksimum 3 yöntem).

                ONAYLI ANALİZ YÖNTEMLERİ HAVUZU:
                {APPROVED_METHODS}

                GİRİLEN PROBLEM:
                "{problem_input}"

                Lütfen çıktıyı şu başlıklar altında yapılandır:

                1. 🔍 **Problem Tespiti & Odak Noktası:**
                   Yalnızca verilen metindeki ifadelere dayalı kısa durum değerlendirmesi.

                2. 📊 **Yöntem Puanlama ve Karar Tablosu:**
                   (Yalnızca seçilen 1 Ana ve en fazla 2 Destekleyici yöntemi içeren Markdown tablosu)
                   | Rol | Önerilen Yöntem (Havuzdan) | Uygunluk Puanı (100 Üzerinden) | Seçim Gerekçesi |

                3. 🛠️ **Seçilen Yöntemler İçin Saha Aksiyonları:**
                   Seçilen bu 1 ana ve (varsa) destekleyici yöntemlerin her biri için sahada atılacak net ve doğrudan uygulama adımları.
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
                    st.success("Analiz Tamamlandı")
                    st.markdown(response_text)
                else:
                    st.error("Sunucu yoğunluğu nedeniyle yanıt alınamadı. Lütfen birkaç saniye sonra tekrar deneyin.")
