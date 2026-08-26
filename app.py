import streamlit as st
import pandas as pd

st.set_page_config(page_title="Şişecam Analiz & Karar Destek Sistemi", page_icon="🎯", layout="wide")

st.title("🎯 Şişecam Yapay Zeka Destekli Analiz & Karar Destek Sistemi")
st.markdown("Operasyonel ve analitik problemleri analiz ederek en uygun yöntemleri belirleyen akıllı karar destek paneli.")

# Yöntem Veritabanı
METHODS_DB = [
    {
        "name": "Zaman Etüdü & İş Örneklemesi",
        "category": "Operasyonel & Çevrim",
        "keywords": ["süre", "zaman", "çevrim", "yavaş", "hız", "bekleme", "gecikme", "operatör", "yetişemiyor"],
        "purpose": "Hattaki operasyon sürelerini standartlaştırmak ve gizli kayıpları tespit etmek.",
        "action": "Kritik darboğaz istasyonlarında 3 vardiya boyunca kronometraj ve frekans analizleri yapın."
    },
    {
        "name": "Hat Dengeleme & Yük Analizi",
        "category": "Kapasite & Akış",
        "keywords": ["darboğaz", "yığılma", "dengesiz", "istasyon", "akış", "hat", "kapasite", "yük"],
        "purpose": "İstasyonlar arası iş yükü dağılımını eşitleyip hat verimliliğini artırmak.",
        "action": "İstasyon çevrim zamanlarını takipli çizelgeye döküp en yüksek istasyondan iş paylaştırın."
    },
    {
        "name": "FMEA (Hata Türleri ve Etkileri Analizi)",
        "category": "Kalite & Risk",
        "keywords": ["hata", "çatlak", "kusur", "risk", "kalite", "fire", "hurda", "problem", "kırılma"],
        "purpose": "Olası hata modlarını şiddet, sıklık ve saptanabilirlik (RPN) puanlarıyla önceliklendirmek.",
        "action": "Kritik kalite hataları için multidisipliner ekiple FMEA tablosu oluşturup RPN > 100 riskleri önleyin."
    },
    {
        "name": "5 Neden (5 Why) Analizi & Balık Kılçığı",
        "category": "Kök Neden Analizi",
        "keywords": ["neden", "kök neden", "arıza", "sebep", "tekrarlayan", "neden kaynaklanıyor"],
        "purpose": "Tekrarlayan arıza veya problemlerin asıl kök sebebini hiyerarşik olarak bulmak.",
        "action": "Problem için 5 kez 'Neden?' sorusunu sorarak operatör/ekipman kaynaklı ana sebebi netleştirin."
    },
    {
        "name": "SMED (Hızlı Model/Kalıp Değişimi)",
        "category": "Duruş & Değişim",
        "keywords": ["kalıp", "ayar", "değişim", "duruş", "model", "setup", "hazırlık"],
        "purpose": "Kalıp ve ürün geçiş sürelerini minimize ederek duruş kayıplarını azaltmak.",
        "action": "İç kurulum adımlarını dış kurulum adımlarına çevirerek hat duruş süresini kısaltın."
    },
    {
        "name": "Ergonomi & 5S Analizi",
        "category": "İş Güvenliği & Çevre",
        "keywords": ["ağır", "zorlanıyor", "ergonomi", "yorgunluk", "düzen", "alan", "taşıma", "fiziksel"],
        "purpose": "Operatörün fiziksel zorlanmasını önlemek ve çalışma ortamını standardize etmek.",
        "action": "Taşıma ve kaldırma alanlarına ergonomik tutucular ekleyin ve 5S adımlarını uygulayın."
    },
    {
        "name": "OEE (Toplam Ekipman Etkinliği) Analizi",
        "category": "Verimlilik & Performans",
        "keywords": ["verim", "oee", "performans", "kayıp", "kullanılabilirlik", "hız kaybı"],
        "purpose": "Kullanılabilirlik, Performans ve Kalite oranlarını birleştirerek tesis etkinliğini ölçmek.",
        "action": "Vardiya bazlı OEE panosu oluşturup ana kayıp kategorisine odaklanın."
    }
]

problem_input = st.text_area(
    "📝 Proje / Problem Tanımını Girin:",
    placeholder="Örn: Cam ambalajlar çok ağır, operatörler taşırken zorlanıyor ve hatta çatlak hataları artıyor.",
    height=120
)

if st.button("🚀 Problemi Analiz Et ve En Uygun Yöntemleri Belirle", type="primary"):
    if not problem_input.strip():
        st.warning("Lütfen analiz edilecek bir problem tanımı girin.")
    else:
        with st.spinner("Problem kriterleri analiz ediliyor..."):
            text_lower = problem_input.lower()
            scored_methods = []

            for m in METHODS_DB:
                score = sum(1 for kw in m["keywords"] if kw in text_lower)
                if score > 0:
                    scored_methods.append((score, m))

            # Skor sırasına göre diz
            scored_methods.sort(key=lambda x: x[0], reverse=True)
            results = [m for _, m in scored_methods[:4]]

            # Eşleşme yoksa genel 3 temel yöntemi getir
            if not results:
                results = METHODS_DB[:3]

        st.success("Analiz tamamlandı!")

        st.subheader("🎯 Eşleşen Yöntemler & Karar Destek Tablosu")
        table_data = []
        for i, res in enumerate(results, 1):
            table_data.append({
                "Öncelik": f"#{i}",
                "Önerilen Metot": res["name"],
                "Kategori": res["category"],
                "Kullanım Amacı": res["purpose"]
            })
        st.table(pd.DataFrame(table_data))

        st.subheader("🛠️ Önerilen Saha Aksiyon Planı")
        for res in results:
            st.markdown(f"**• {res['name']}:** {res['action']}")
