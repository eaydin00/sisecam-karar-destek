import streamlit as st
import pandas as pd
from google import genai

st.set_page_config(
    page_title="Şişecam Analiz & Karar Destek Sistemi",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Şişecam Yapay Zeka Destekli Analiz & Karar Destek Sistemi")
st.markdown("Operasyonel ve teknik problemleri kurumsal analiz yöntemleri veritabanıyla eşleştiren ve puanlayan karar destek sistemi.")

# Birebir Excel Veritabanı
EXCEL_KNOWLEDGE_BASE = """
1. KATEGORİ: Süreç & İş Gücü Analizi
- Optimum personel sayısı belirleme -> Yöntemler: Zaman Etüdü, MTM / MOST | Amaç: İş yükünü ölçmek ve personel ihtiyacını bilimsel belirlemek
- Hat verimliliği artırma -> Yöntemler: Yük Dengeleme Analizi, Hat Dengeleme (Line Balancing), Yamazumi Analizi, VSM | Amaç: Fazla yüklenen ve bekleyen istasyonları tespit etmek
- Proses darboğazı bulma -> Yöntemler: Bottleneck Analysis, VSM | Amaç: Hat akışını hızlandırmak
- İş yükü dağılımı değerlendirme -> Yöntemler: Kapasite Analizi, Workload Analysis, Spaghetti Diagram | Amaç: İş adımlarındaki gereksiz hareketleri ve yük dağılımını görmek

2. KATEGORİ: Makine, Ekipman ve Kapasite Değerlendirme
- Makine kapasitesi belirleme -> Yöntemler: Kapasite Analizi, OEE, Cycle Time Measurement | Amaç: Bağlamalı/bağlamasız kapasiteyi belirleme
- Ekipman yatırım karar desteği -> Yöntemler: ROI Analizi, Break-even Analizi, Kapasite Kullanım Oranı Analizi | Amaç: Yatırımın geri dönüşünü hesaplamak
- Makine yükleme planlama -> Yöntemler: RCCP (Rough-cut Capacity Planning), Finite Capacity Planning | Amaç: Gerçek kapasiteye göre plan yapmak
- Makine karşılaştırma çalışması -> Yöntemler: Multi-Criteria Decision Making (AHP), Performans Benchmarking | Amaç: En uygun makineyi seçmek

3. KATEGORİ: Ambalaj Geliştirme & Performans Analizi
- Ambalaj malzemesi optimizasyonu -> Yöntemler: DOE (Deney Tasarımı), Regresyon Analizi | Amaç: En uygun kalınlık, katkı, bariyer değerini bulmak
- Ambalaj dayanım testleri -> Yöntemler: ISTA Testleri, Bariyer Analizi (OTR/WVTR), Seal Strength Testleri | Amaç: Darbe, taşıma ve raf performansını değerlendirmek
- Alternatif malzeme karşılaştırma -> Yöntemler: QFD, LCA Analizi, Maliyet-Kalite dengesi analizi | Amaç: Teknik ve maliyet açısından en uygun malzemeyi seçmek

4. KATEGORİ: Kalite Problemleri & Kök Neden Analizleri
- Proses kaynaklı kalite hataları -> Yöntemler: 5 Why, Ishikawa, Pareto, FMEA | Amaç: Kök neden bulmak
- Tekrarlayan hatalar -> Yöntemler: SPC, Kontrol Planı | Amaç: Hata olasılığını azaltmak
- Hata varyasyon takibi -> Yöntemler: Xbar-R Kartları, Cp, Cpk Analizi | Amaç: Prosesin kararlılığını ölçmek
- Müşteri şikayetleri -> Yöntemler: 8D Raporlama, Control Chart Analizi | Amaç: Sistemdeki zayıf noktaları belirlemek

5. KATEGORİ: Veri Analizi & İstatistiksel Değerlendirmeler
- Proses değişkenlerinin etki analizi -> Yöntemler: Regresyon Analizi, Korelasyon, ANOVA | Amaç: Değişkenlerin çıktı üzerindeki etkisini ölçmek
- Yeni ölçüm cihazı doğrulama -> Yöntemler: MSA / Gage R&R | Amaç: Ölçüm sisteminin güvenilirliğini doğrulamak
- Karşılaştırma çalışmaları -> Yöntemler: Hypothesis Test (t-test), Kruskal-Wallis | Amaç: İki veya daha fazla grubun farkını test etmek
"""

problem_input = st.text_area(
    "📝 Proje / Problem Tanımını Girin:",
    placeholder="Örn: 3 farklı makine arasında maliyet, hız ve enerjiye göre seçim yapılacak / Paketleme hattında çevrim süresi çok yavaş.",
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
            
            with st.spinner("Yapay zeka problem tipini ve yöntemleri eşleştiriyor..."):
                client = genai.Client(api_key=api_key)
                
                prompt = f"""
                Sen endüstri mühendisliği alanında uzman, karar ağacı prensibiyle çalışan bir Karar Destek Danışmanısın.

                KATI KARAR KURALLARI:
                1. YALNIZCA sana verilen "EXCEL BİLGİ TABANI"ndaki yöntemleri öner. Listede olmayan hiçbir yöntemi üretme.
                2. Problemde belirtilmeyen parametreler hakkında varsayım yapma.
                3. Çıktıda kesinlikle 1 adet "Ana Yöntem" ve problem durumuna göre en fazla 2 adet "Destekleyici Yöntem" seç (Toplam maks. 3 yöntem).
                
                EŞLEŞTİRME HARİTASI (SENARYO BAZLI MANTIK):
                - Çoklu Kriterli Makine Seçimi / Kıyaslama -> Ana Yöntem: Multi-Criteria Decision Making (AHP) | Destekleyici: Performans Benchmarking veya ROI Analizi
                - Personel Sayısı / İş Yükü Ölçümü -> Ana Yöntem: Zaman Etüdü veya MTM / MOST | Destekleyici: Workload Analysis
                - Hat Yükü / İstasyon Dengesizliği / Bekleme -> Ana Yöntem: Hat Dengeleme (Line Balancing) veya Yük Dengeleme | Destekleyici: Yamazumi / VSM
                - Hat Darboğazı / Akış Yavaşlığı -> Ana Yöntem: Bottleneck Analysis | Destekleyici: VSM / Kapasite Analizi
                - Makine Yatırım Dönüşü -> Ana Yöntem: ROI Analizi veya Break-even Analizi
                - Ambalaj Kalınlık/Katkı Optimizasyonu -> Ana Yöntem: DOE (Deney Tasarımı) | Destekleyici: Regresyon Analizi
                - Ambalaj Taşıma/Darbe/Dayanım -> Ana Yöntem: ISTA Testleri | Destekleyici: Bariyer Analizi / Seal Strength Testleri
                - Alternatif Malzeme Karşılaştırma -> Ana Yöntem: QFD veya Maliyet-Kalite Dengesi | Destekleyici: LCA Analizi
                - Proses Hatası Kök Neden Bulma -> Ana Yöntem: Ishikawa (Balık Kılçığı) veya 5 Why | Destekleyici: Pareto / FMEA
                - Tekrarlayan Hatalar & Proses Kararlılığı -> Ana Yöntem: SPC veya Xbar-R Kartları | Destekleyici: Cp, Cpk Analizi / Kontrol Planı
                - Müşteri Şikayeti Analizi -> Ana Yöntem: 8D Raporlama | Destekleyici: Control Chart Analizi
                - Değişkenlerin Etkisini Ölçme (Sıcaklık, Basınç vb.) -> Ana Yöntem: Regresyon Analizi veya ANOVA | Destekleyici: Korelasyon
                - Ölçüm Cihazı / Mastar Doğrulama -> Ana Yöntem: MSA / Gage R&R
                - İki Grup / Vardiya Karşılaştırması -> Ana Yöntem: Hypothesis Test (t-test) veya Kruskal-Wallis

                EXCEL BİLGİ TABANI:
                {EXCEL_KNOWLEDGE_BASE}

                GİRİLEN PROBLEM:
                "{problem_input}"

                Lütfen çıktıyı şu formatta oluştur:

                1. 🔍 **Problem Sınıflandırması:**
                   Problemin Excel'deki hangi Kategori ve Çalışma Tipine girdiği.

                2. 📊 **Yöntem Karar ve Uygunluk Tablosu (Markdown Tablosu):**
                   | Öncelik / Rol | Önerilen Analiz Yöntemi (Tablodan) | Çalışma Tipi & Kategori | Uygunluk Puanı (100 Üzerinden) | Seçim Gerekçesi |
                   
                3. 🛠️ **Yöntem Bazlı Somut Uygulama Adımları:**
                   Seçilen Ana ve Destekleyici yöntemlerin sahada adım adım nasıl icra edileceğini açıkla.
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
                    st.success("Analiz Başarıyla Tamamlandı")
                    st.markdown(response_text)
                else:
                    st.error("Sunucu yoğunluğu nedeniyle yanıt alınamadı. Lütfen birkaç saniye sonra tekrar deneyin.")
