import streamlit as st
import pandas as pd
from google import genai

st.set_page_config(page_title="Şişecam Analiz Asistanı", layout="wide")
st.title("🎯 Şişecam Yapay Zeka Destekli Analiz & Karar Destek Sistemi")

# 1. API Anahtarını Buraya Yapıştır
API_KEY = 'AQ.Ab8RN6IIscoIW7s5qXVSm9B2GafKvfjYZEzB1q4qeCMeiGLmFg'
client = genai.Client(api_key=API_KEY)

# 8 KRİTERLİ KÜTÜPHANE
KNOWLEDGE_BASE = [
    # Süreç & İş Gücü
    {"yontem": "Zaman Etüdü", "kategori": "Süreç & İş Gücü", "kriterler": ["İNSAN", "PROSES", "MAKİNE", "AMBALAJ"], "amac": "Standart operasyon sürelerini belirlemek ve norm kadro hesabı yapmak."},
    {"yontem": "MTM / MOST", "kategori": "Süreç & İş Gücü", "kriterler": ["İNSAN", "PROSES"], "amac": "Operatör mikro hareketlerini standart zaman verileriyle analiz etmek."},
    {"yontem": "Spaghetti Diagram", "kategori": "Süreç & İş Gücü", "kriterler": ["İNSAN", "LOJİSTİK", "PROSES"], "amac": "Gereksiz yürüme yollarını ve tesis içi yerleşim israflarını haritalamak."},
    {"yontem": "Workload & Yük Dengeleme", "kategori": "Süreç & İş Gücü", "kriterler": ["İNSAN", "MAKİNE", "PROSES"], "amac": "İstasyonlar ve operatörler arası iş yükü dağılımını eşitlemek."},
    {"yontem": "Hat Dengeleme (Line Balancing)", "kategori": "Süreç & İş Gücü", "kriterler": ["MAKİNE", "AMBALAJ", "PROSES"], "amac": "Fazla yüklenen ve bekleyen istasyonları senkronize etmek."},
    {"yontem": "VSM (Değer Akış Haritalama)", "kategori": "Süreç & İş Gücü", "kriterler": ["PROSES", "LOJİSTİK", "MAKİNE"], "amac": "Tüm hat akışındaki israfları ve ara stokları görmek."},
    {"yontem": "Bottleneck (Darboğaz) Analizi", "kategori": "Süreç & İş Gücü", "kriterler": ["PROSES", "MAKİNE"], "amac": "Üretim akışını kısıtlayan en yavaş istasyonu belirleyip kapasiteyi açmak."},
    
    # Makine & Yatırım
    {"yontem": "OEE Analizi", "kategori": "Makine & Kapasite", "kriterler": ["MAKİNE", "PROSES", "KALİTE"], "amac": "Duruş, hız ve kalite kayıplarını tek bir verimlilik metriğinde izlemek."},
    {"yontem": "Kapasite & RCCP Planlama", "kategori": "Makine & Kapasite", "kriterler": ["MAKİNE", "PROSES"], "amac": "Sipariş talebine göre hatların gerçek kapasite doluluğunu planlamak."},
    {"yontem": "ROI & Break-even Analizi", "kategori": "Yatırım & Maliyet", "kriterler": ["MALİYET", "MAKİNE"], "amac": "Yeni otomasyon veya ekipman yatırımının geri dönüş süresini hesaplamak."},
    {"yontem": "AHP / Karar Matrisi", "kategori": "Yatırım & Maliyet", "kriterler": ["MAKİNE", "MALİYET", "PROSES"], "amac": "Alternatif ekipman veya tedarikçileri çok kriterli puanlamak."},
    
    # Ambalaj & Lojistik
    {"yontem": "DOE (Deney Tasarımı - Hafifletme)", "kategori": "Ambalaj Geliştirme", "kriterler": ["AMBALAJ", "PROSES", "MALİYET"], "amac": "Cam ağırlığı, et kalınlığı ve hammadde optimizasyonu sağlamak."},
    {"yontem": "ISTA Taşıma & Darbe Testleri", "kategori": "Ambalaj & Lojistik", "kriterler": ["AMBALAJ", "LOJİSTİK", "KALİTE"], "amac": "Nakliye esnasındaki sarsıntı, düşme ve palet mukavemetini test etmek."},
    {"yontem": "QFD & Malzeme Analizi", "kategori": "Ambalaj Geliştirme", "kriterler": ["AMBALAJ", "MALİYET", "KALİTE"], "amac": "Müşteri teknik beklentileriyle en uygun ambalaj malzemesini eşleştirmek."},
    {"yontem": "LCA (Yaşam Döngüsü Analizi)", "kategori": "Ambalaj & Sürdürülebilirlik", "kriterler": ["AMBALAJ", "PROSES", "MALİYET"], "amac": "Ambalajın karbon ayak izini ve çevresel sürdürülebilirlik etkisini ölçmek."},
    
    # Kalite & Kök Neden
    {"yontem": "5 Why & Ishikawa (Balık Kılçığı)", "kategori": "Kalite Problemleri", "kriterler": ["KALİTE", "İNSAN", "MAKİNE", "PROSES"], "amac": "Tekrarlayan proses veya operasyonel hatalarda kök nedene inmek."},
    {"yontem": "FMEA Analizi", "kategori": "Kalite Problemleri", "kriterler": ["KALİTE", "MAKİNE", "PROSES", "AMBALAJ"], "amac": "Hata oluşmadan önce risk öncelik katsayısını (RPN) belirlemek."},
    {"yontem": "SPC & Kontrol Kartları (Cp/Cpk)", "kategori": "Kalite & Veri", "kriterler": ["KALİTE", "VERİ", "PROSES"], "amac": "Üretim toleranslarının ve proses yeterliliğinin kararlılığını izlemek."},
    {"yontem": "8D Metodolojisi", "kategori": "Kalite Problemleri", "kriterler": ["KALİTE", "LOJİSTİK", "İNSAN"], "amac": "Müşteri şikayetlerinde kalıcı düzeltici faaliyetleri yönetmek."},
    
    # Veri & İstatistik
    {"yontem": "Regresyon & ANOVA Analizi", "kategori": "Veri Analizi", "kriterler": ["VERİ", "PROSES", "MAKİNE"], "amac": "Fırın/makine parametrelerinin ürün kalitesine etkisini modellemek."},
    {"yontem": "MSA / Gage R&R", "kategori": "Veri Analizi", "kriterler": ["VERİ", "İNSAN", "MAKİNE"], "amac": "Ölçüm cihazlarının ve operatör ölçüm sapmalarının güvenilirliğini test etmek."}
]

ALL_CRITERIA = ["İNSAN", "MAKİNE", "PROSES", "AMBALAJ", "MALİYET", "KALİTE", "LOJİSTİK", "VERİ"]

# Kullanıcı Arayüzü
proje_metni = st.text_area(
    "📝 Proje / Problem Tanımını Girin:",
    placeholder="Örn: Cam ambalajlar çok ağır, operatörler taşırken zorlanıyor.",
    height=100
)

if st.button("🚀 Problemi Analiz Et ve En Uygun Yöntemleri Belirle", type="primary"):
    if not proje_metni:
        st.warning("Lütfen bir problem açıklaması yazın.")
    elif API_KEY == "BURAYA_GEMINI_API_KEYINI_YAZ":
        st.error("Lütfen API anahtarınızı girin.")
    else:
        prompt = f"""
        Problem: "{proje_metni}"
        Kriter Havuzu: İNSAN, MAKİNE, PROSES, AMBALAJ, MALİYET, KALİTE, LOJİSTİK, VERİ
        
        Lütfen cevabını tam olarak şu 3 satır formatında ve kısa ver:
        KRITERLER: [En ilgili 2 veya 3 kriteri virgülle yaz]
        GEREKCE: [Tek cümlelik açıklama]
        AKSIYON: [Mühendisin sahada yapması gereken ilk pratik adım]
        """
        with st.spinner("Analiz ediliyor..."):
            try:
                # Sıfır argüman hatası, en sade çağrı
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )
                
                yanit_metni = response.text.strip()
                
                kriterler_listesi = []
                gerekce_metni = ""
                aksiyon_metni = ""
                
                for satir in yanit_metni.split("\n"):
                    satir = satir.strip()
                    if satir.upper().startswith("KRITERLER:"):
                        ham = satir.split(":", 1)[1]
                        for c in ALL_CRITERIA:
                            if c in ham.upper() and c not in kriterler_listesi:
                                kriterler_listesi.append(c)
                    elif satir.upper().startswith("GEREKCE:"):
                        gerekce_metni = satir.split(":", 1)[1].strip()
                    elif satir.upper().startswith("AKSIYON:"):
                        aksiyon_metni = satir.split(":", 1)[1].strip()
                
                if not kriterler_listesi:
                    for c in ALL_CRITERIA:
                        if c in yanit_metni.upper() and c not in kriterler_listesi:
                            kriterler_listesi.append(c)

                st.info(f"🧠 **Tespit Edilen Odak Kriterler:** {', '.join(kriterler_listesi) if kriterler_listesi else 'İNSAN, PROSES'}  \n📌 **Gerekçe:** {gerekce_metni if gerekce_metni else yanit_metni[:150]}")
                
                # Uyum Puanlama & En iyi 3-5 Yöntem
                puanli_yontemler = []
                ai_set = set(kriterler_listesi) if kriterler_listesi else {"İNSAN"}
                
                for item in KNOWLEDGE_BASE:
                    item_set = set(item["kriterler"])
                    kesisim = len(ai_set.intersection(item_set))
                    if kesisim > 0:
                        oran = int((kesisim / len(ai_set)) * 100)
                        if oran >= 50:
                            item_kopyasi = item.copy()
                            item_kopyasi["Uyum Puanı"] = f"%{oran}"
                            item_kopyasi["kesisim"] = kesisim
                            puanli_yontemler.append(item_kopyasi)
                
                puanli_yontemler = sorted(puanli_yontemler, key=lambda x: x["kesisim"], reverse=True)[:5]
                
                if puanli_yontemler:
                    st.subheader(f"📋 En Uygun Analiz Yöntemleri ({len(puanli_yontemler)} Adet Öneri)")
                    tablo = []
                    for y in puanli_yontemler:
                        tablo.append({
                            "Uyum": y["Uyum Puanı"],
                            "Önerilen Analiz Yöntemi": y["yontem"],
                            "Kategori": y["kategori"],
                            "Kapsadığı Kriterler": ", ".join(y["kriterler"]),
                            "Kullanım Amacı": y["amac"]
                        })
                    st.dataframe(pd.DataFrame(tablo), width='stretch', hide_index=True)
                    
                    if aksiyon_metni:
                        st.success(f"💡 **Önerilen İlk Mühendislik Adımı:** {aksiyon_metni}")
                else:
                    st.warning("Bu kriterlere doğrudan uyan bir analiz yöntemi bulunamadı.")
            except Exception as e:
                st.error(f"Hata: {e}")