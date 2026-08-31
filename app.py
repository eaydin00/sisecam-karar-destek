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

# Kural Tabanlı Yedek Havuz
METHODS_DB = [
    {
        "name": "Zaman Etüdü & İş Örneklemesi",
        "category": "Operasyonel & Çevrim",
        "keywords": ["süre", "zaman", "çevrim", "yavaş", "hız", "bekleme", "gecikme", "operatör", "yetişemiyor"],
        "purpose": "Hattaki standart süreleri belirleyip gizli operasyonel kayıpları tespit etmek.",
        "action": "Kritik darboğaz istasyonlarında 3 vardiya boyunca kronometraj ve frekans analizi gerçekleştirin."
    },
    {
        "name": "Hat Dengeleme & Yük Dağıtımı",
        "category": "Kapasite & Akış",
        "keywords": ["darboğaz", "yığılma", "dengesiz", "istasyon", "akış", "hat", "kapasite", "yük"],
        "purpose": "İstasyonlar arası iş yükü dağılımını eşitleyerek hat verimliliğini maksimize etmek.",
        "action": "İstasyon çevrim zamanlarını takipli çizelgeye döküp en yüksek istasyondan diğerlerine iş paylaştırın."
    },
    {
        "name": "FMEA (Hata Türleri ve Etkileri Analizi)",
        "category": "Kalite & Risk",
        "keywords": ["hata", "çatlak", "kusur", "risk", "kalite", "fire", "hurda", "problem", "kırılma"],
        "purpose": "Olası hata modlarını Şiddet, Sıklık ve Saptanabilirlik (RPN) puanlarıyla önceliklendirmek.",
        "action": "Kritik kalite hataları için multidisipliner ekiple FMEA tablosu oluşturup RPN > 100 riskleri önleyin."
    },
    {
        "name": "5 Neden (5 Why) & Kök Neden Analizi",
        "category": "Problem Çözme",
        "keywords": ["neden", "kök neden", "arıza", "sebep", "tekrarlayan", "neden kaynaklanıyor"],
        "purpose": "Tekrarlayan arıza ve sapmaların temel kök sebebini tespit etmek.",
        "action": "Problemin kök sebebine inene kadar ardışık 'Neden?' sorularını sorup kalıcı aksiyon planı açın."
    },
    {
        "name": "SMED (Hızlı Model/Kalıp Değişimi)",
        "category": "Duruş & Değişim",
        "keywords": ["kalıp", "ayar", "değişim", "duruş", "model", "setup", "hazırlık"],
        "purpose": "Kalıp ve ürün geçiş sürelerini minimize ederek duruş kayıplarını azaltmak.",
        "action": "İç kurulum adımlarını dış kuruluma dönüştürerek hat duruş süresini kısaltın."
    },
    {
        "name": "Ergonomi & 5S Çalışma Alanı Düzenleme",
        "category": "İSG & Verimlilik",
        "keywords": ["ağır", "zorlanıyor", "ergonomi", "yorgunluk", "düzen", "alan", "taşıma", "fiziksel"],
        "purpose": "Operatörün fiziksel zorlanmasını azaltmak ve çalışma alanını standartlaştırmak.",
        "action": "Taşıma alanlarına ergonomik tutucu sistemler ekleyin ve 5S standartlarını devreye alın."
    }
]

problem_input = st.text_area(
    "📝 Proje / Problem Tanımını Girin:",
    placeholder="Örn: Paketleme istasyonunda çevrim süresi çok yavaş, operatörler akışa yetişemiyor ve çatlak hataları artıyor.",
    height=120
)

if st.button("🚀 Problemi Analiz Et ve En Uygun Yöntemleri Belirle", type="primary"):
    if not problem_input.strip():
        st.warning("Lütfen analiz edilecek bir problem tanımı girin.")
    else:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
        success_ai = False
        
        with st.spinner("Problem kriterleri yapay zeka ile analiz ediliyor..."):
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel("gemini-1.5-flash")
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
                    if response and response.text:
                        st.success("Yapay Zeka Destekli Analiz Tamamlandı")
                        st.markdown(response.text)
                        success_ai = True
                except Exception as e:
                    # Hata olursa sessizce yedek algoritmaya geç
                    success_ai = False

            if not success_ai:
                st.info("Kural Tabanlı Analitik Eşleştirme Tamamlandı")
                text_lower = problem_input.lower()
                scored = []
                for m in METHODS_DB:
                    score = sum(1 for kw in m["keywords"] if kw in text_lower)
                    if score > 0:
                        scored.append((score, m))
                scored.sort(key=lambda x: x[0], reverse=True)
                results = [m for _, m in scored[:3]] if scored else METHODS_DB[:3]
                
                table_data = []
                for i, res in enumerate(results, 1):
                    table_data.append({
                        "Öncelik": f"#{i}",
                        "Önerilen Metot": res["name"],
                        "Kategori": res["category"],
                        "Kullanım Amacı": res["purpose"]
                    })
                st.table(pd.DataFrame(table_data))
                for res in results:
                    st.markdown(f"**• {res['name']}:** {res['action']}")
