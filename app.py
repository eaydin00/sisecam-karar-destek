import streamlit as st
import pandas as pd
import json

st.set_page_config(
    page_title="Şişecam Analiz & Karar Destek Sistemi",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Şişecam Yapay Zeka Destekli Analiz & Karar Destek Sistemi")
st.markdown("Operasyonel, teknik ve analitik problemleri analiz ederek en uygun yöntem ve aksiyon planını belirleyen hibrit karar destek sistemi.")

# Kapsamlı Yöntem Kütüphanesi (Fallback & Doğrulama Havuzu)
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
    },
    {
        "name": "OEE (Toplam Ekipman Etkinliği) Analizi",
        "category": "Performans Yönetimi",
        "keywords": ["verim", "oee", "performans", "kayıp", "kullanılabilirlik", "hız kaybı"],
        "purpose": "Kullanılabilirlik, Performans ve Kalite oranlarını birleştirerek tesis etkinliğini ölçmek.",
        "action": "Vardiya bazlı OEE panosu oluşturup ana kayıp kategorilerine göre kaizen başlatın."
    },
    {
        "name": "SPC (İstatistiksel Süreç Kontrolü)",
        "category": "Kalite Güvence",
        "keywords": ["sapma", "tolerans", "ölçüm", "istatistik", "kontrol kartı", "dalgalanma"],
        "purpose": "Süreç değişkenliğini kontrol limitleri (UCL/LCL) içerisinde izleyip sapmaları önceden görmek.",
        "action": "Kritik proses parametreleri için X-bar R kontrol kartları açıp trend sapmalarını izleyin."
    },
    {
        "name": "Pareto (80/20) & ABC Analizi",
        "category": "Önceliklendirme",
        "keywords": ["öncelik", "en çok", "kaynak", "dağılım", "stok", "liste", "sınıflandırma"],
        "purpose": "Kayıpların %80'ine neden olan %20'lik ana odak noktalarını belirlemek.",
        "action": "Hata veya duruş verilerini sıklıklarına göre sıralayıp kümülatif etkiyi gösteren Pareto grafiği çizin."
    }
]

def analyze_with_gemini(problem_text: str, api_key: str):
    from google import genai
    from google.genai import types
    
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    Sen endüstri mühendisliği ve üretim operasyonları alanında uzman bir Karar Destek Danışmanısın.
    Aşağıda fabrikadaki bir mühendisin girdiği problem tanımı yer almaktadır:
    
    Problem: "{problem_text}"
    
    Bu probleme özel olarak:
    1. Problemin kök neden hipotezini ve odak alanlarını özetle.
    2. En uygun 3 analitik mühendislik yöntemini belirle (Örn: Zaman Etüdü, FMEA, Hat Dengeleme, SMED, SPC, 5S vb.).
    3. Bu yöntemlerin sahada nasıl uygulanacağına dair somut, adımsal bir aksiyon planı çıkar.
    
    Lütfen yanıtını profesyonel, maddeli ve temiz bir Türkçe ile oluştur.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

def analyze_rule_based(problem_text: str):
    text_lower = problem_text.lower()
    scored = []
    for m in METHODS_DB:
        score = sum(1 for kw in m["keywords"] if kw in text_lower)
        if score > 0:
            scored.append((score, m))
    
    scored.sort(key=lambda x: x[0], reverse=True)
    results = [m for _, m in scored[:4]]
    if not results:
        results = METHODS_DB[:3]
    return results

# Arayüz
problem_input = st.text_area(
    "📝 Proje / Problem Tanımını Girin:",
    placeholder="Örn: Paketleme istasyonunda çevrim süresi çok yavaş, operatörler akışa yetişemiyor ve çatlak hataları artıyor.",
    height=120
)

if st.button("🚀 Problemi Analiz Et ve En Uygun Yöntemleri Belirle", type="primary"):
    if not problem_input.strip():
        st.warning("Lütfen analiz edilecek bir problem tanımı girin.")
    else:
        api_key = st.secrets.get("GEMINI_API_KEY", None)
        success_gemini = False
        
        with st.spinner("Problem kriterleri analiz ediliyor..."):
            if api_key and api_key.startswith("AIza"):
                try:
                    ai_result = analyze_with_gemini(problem_input, api_key)
                    st.success("Yapay Zeka Destekli Analiz Tamamlandı")
                    st.markdown("### 📋 Mühendislik Değerlendirmesi & Aksiyon Planı")
                    st.markdown(ai_result)
                    success_gemini = True
                except Exception:
                    success_gemini = False

            if not success_gemini:
                results = analyze_rule_based(problem_input)
                st.success("Kural Tabanlı Analitik Eşleştirme Tamamlandı")
                
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
