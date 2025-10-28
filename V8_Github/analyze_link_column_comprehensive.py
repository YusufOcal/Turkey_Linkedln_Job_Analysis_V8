#!/usr/bin/env python3
"""
LinkedIn Jobs Dataset - Comprehensive Link Column Analysis

Bu script link sütununu kapsamlı olarak analiz eder:
1. Sütun karakteristikleri ve URL pattern analizi
2. Veri tutarlılığı ve format standardizasyonu
3. Veri tipi uyumluluğu kontrolü
4. Boş alan yoğunluğu ve doldurma stratejileri
5. Benzer sütunlarla redundancy kontrolü
6. İş değeri ve insight potansiyeli
"""

import pandas as pd
import numpy as np
import re
from urllib.parse import urlparse, parse_qs
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

def load_dataset():
    """Dataset'i yükle"""
    try:
        df = pd.read_csv('linkedin_jobs_cleaned_no_redundant_workplace.csv')
        print(f"✅ Dataset başarıyla yüklendi: {len(df):,} kayıt, {len(df.columns)} sütun")
        return df
    except Exception as e:
        print(f"❌ Dataset yükleme hatası: {e}")
        return None

def analyze_basic_characteristics(df, target_col):
    """Link sütununun temel karakteristikleri"""
    print("=" * 80)
    print(f"🔗 LINK SÜTUN ANALİZİ: {target_col}")
    print("=" * 80)
    
    print(f"📊 TEMEL KARAKTERİSTİKLER:")
    print(f"   • Sütun Adı: {target_col}")
    print(f"   • Veri Tipi: {df[target_col].dtype}")
    print(f"   • Toplam Kayıt: {len(df):,}")
    print(f"   • Null Olmayan: {df[target_col].count():,}")
    print(f"   • Null Değer: {df[target_col].isnull().sum():,}")
    print(f"   • Veri Tamlığı: {(df[target_col].count()/len(df)*100):.2f}%")
    print(f"   • Benzersiz URL: {df[target_col].nunique():,}")
    print(f"   • Benzersizlik Oranı: {(df[target_col].nunique()/df[target_col].count()*100):.2f}%")
    
    print(f"\n🌐 SÜTUN TEMSIL ETTİĞİ KAVRAM:")
    print(f"   • LinkedIn iş ilanlarının direkt URL'leri")
    print(f"   • Her URL benzersiz bir job posting'e işaret eder")
    print(f"   • İş arayanların ilanlara erişim noktası")
    print(f"   • LinkedIn platformunda canonical link yapısı")
    
    return {
        'total_records': len(df),
        'non_null_count': df[target_col].count(),
        'null_count': df[target_col].isnull().sum(),
        'unique_count': df[target_col].nunique(),
        'data_type': str(df[target_col].dtype)
    }

def analyze_url_patterns(df, target_col):
    """URL pattern ve format analizi"""
    print(f"\n🔍 URL PATTERN ANALİZİ:")
    print("-" * 50)
    
    # Sample URLs
    sample_urls = df[target_col].dropna().head(10).tolist()
    print(f"📋 ÖRNEK URL'LER:")
    for i, url in enumerate(sample_urls, 1):
        print(f"   {i:2d}. {url}")
    
    # URL components analysis
    print(f"\n🏗️  URL YAPISI ANALİZİ:")
    non_null_urls = df[target_col].dropna()
    
    if len(non_null_urls) > 0:
        # Protocol analysis
        protocols = []
        domains = []
        paths = []
        
        for url in non_null_urls.head(1000):  # Sample ilk 1000 URL
            try:
                parsed = urlparse(str(url))
                protocols.append(parsed.scheme)
                domains.append(parsed.netloc)
                paths.append(parsed.path)
            except:
                continue
        
        print(f"   • Protocol Dağılımı:")
        protocol_counts = Counter(protocols)
        for protocol, count in protocol_counts.most_common():
            print(f"     - {protocol}: {count:,} adet")
        
        print(f"   • Domain Dağılımı:")
        domain_counts = Counter(domains)
        for domain, count in domain_counts.most_common(5):
            print(f"     - {domain}: {count:,} adet")
        
        # Path pattern analysis
        print(f"   • Path Pattern Örnekleri:")
        unique_paths = list(set(paths))[:5]
        for path in unique_paths:
            print(f"     - {path}")
    
    return protocols, domains, paths

def check_data_consistency(df, target_col):
    """Veri tutarlılığı kontrolü"""
    print(f"\n⚠️  VERİ TUTARLILIK KONTROLÜ:")
    print("-" * 50)
    
    non_null_urls = df[target_col].dropna()
    issues = []
    
    # URL format validation
    invalid_urls = []
    valid_url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    for idx, url in non_null_urls.items():
        url_str = str(url).strip()
        if not valid_url_pattern.match(url_str):
            invalid_urls.append((idx, url_str))
            if len(invalid_urls) <= 5:  # İlk 5 örnek
                issues.append(f"Geçersiz URL format: {url_str}")
    
    print(f"📊 TUTARLILIK SONUÇLARI:")
    print(f"   • Toplam incelenen URL: {len(non_null_urls):,}")
    print(f"   • Geçersiz URL format: {len(invalid_urls):,}")
    print(f"   • Format tutarlılığı: {((len(non_null_urls)-len(invalid_urls))/len(non_null_urls)*100):.2f}%")
    
    if issues:
        print(f"\n🚨 TESPİT EDİLEN SORUNLAR:")
        for issue in issues[:10]:  # İlk 10 sorun
            print(f"   • {issue}")
    
    # LinkedIn domain consistency
    linkedin_domains = ['linkedin.com', 'www.linkedin.com', 'tr.linkedin.com']
    linkedin_count = 0
    other_domains = []
    
    for url in non_null_urls.head(1000):
        try:
            domain = urlparse(str(url)).netloc.lower()
            if any(ld in domain for ld in linkedin_domains):
                linkedin_count += 1
            else:
                other_domains.append(domain)
        except:
            continue
    
    print(f"\n🏢 DOMAIN TUTARLILIK:")
    print(f"   • LinkedIn domain'leri: {linkedin_count:,}")
    print(f"   • Diğer domain'ler: {len(other_domains):,}")
    
    if other_domains:
        print(f"   • Beklenmeyen domain örnekleri:")
        for domain in list(set(other_domains))[:5]:
            print(f"     - {domain}")
    
    return len(invalid_urls), linkedin_count, other_domains

def analyze_null_density(df, target_col):
    """Boş alan yoğunluğu analizi"""
    print(f"\n❓ BOŞ ALAN YOĞUNLUĞU ANALİZİ:")
    print("-" * 50)
    
    null_count = df[target_col].isnull().sum()
    null_percentage = (null_count / len(df)) * 100
    
    print(f"📊 BOŞ VERİ İSTATİSTİKLERİ:")
    print(f"   • Null değer sayısı: {null_count:,}")
    print(f"   • Null oranı: %{null_percentage:.2f}")
    print(f"   • Dolu veri oranı: %{100-null_percentage:.2f}")
    
    # Kritik seviye değerlendirmesi
    if null_percentage == 0:
        print(f"   ✅ Mükemmel: Hiç boş veri yok")
    elif null_percentage < 5:
        print(f"   ✅ İyi: Düşük null oranı")
    elif null_percentage < 15:
        print(f"   ⚠️  Orta: Kabul edilebilir null oranı")
    else:
        print(f"   🚨 Yüksek: Kritik null oranı")
    
    print(f"\n💡 BOŞ VERİ DOLDURMA STRATEJİLERİ:")
    if null_count > 0:
        print(f"   🎯 ÖNERİLEN STRATEJİLER:")
        print(f"      1. İş ID'sinden URL türetme:")
        print(f"         - Pattern: https://linkedin.com/jobs/view/{{job_id}}")
        print(f"         - 'id' sütununu kullanarak otomatik URL oluşturma")
        print(f"      2. Company URL'lerinden türetme:")
        print(f"         - Company bilgisi + job title kombinasyonu")
        print(f"      3. Default LinkedIn job search URL:")
        print(f"         - Genel LinkedIn jobs sayfasına yönlendirme")
        print(f"      4. Null bırakma:")
        print(f"         - Eğer URL kritik değilse null kabul edilebilir")
    else:
        print(f"   ✅ Doldurma gerekmez: Tam veri mevcut")
    
    return null_count, null_percentage

def check_data_type_compatibility(df, target_col):
    """Veri tipi uyumluluğu kontrolü"""
    print(f"\n🔧 VERİ TİPİ UYUMLULUK KONTROLÜ:")
    print("-" * 50)
    
    current_dtype = df[target_col].dtype
    print(f"📊 MEVCUT VERİ TİPİ: {current_dtype}")
    
    # URL'ler için ideal veri tipi string/object
    print(f"\n✅ VERİ TİPİ UYGUNLUK DEĞERLENDİRMESİ:")
    if current_dtype == 'object':
        print(f"   ✅ UYGUN: 'object' tipi URL'ler için ideal")
        print(f"   📋 Gerekçeler:")
        print(f"      • String veri saklama uygun")
        print(f"      • Variable length URL'ler desteklenir")
        print(f"      • Null value'lar uygun şekilde handle edilir")
        print(f"      • Memory efficiency makul seviyede")
        
        recommendation = "KORUNMALI"
    else:
        print(f"   ❌ UYGUNSUZ: '{current_dtype}' tipi URL'ler için uygun değil")
        print(f"   🔄 ÖNERİLEN VERİ TİPİ: 'object' (string)")
        print(f"   📋 Dönüşüm gerekçeleri:")
        print(f"      • URL'ler text data olarak saklanmalı")
        print(f"      • String operations için optimize edilmeli")
        
        recommendation = "OBJECT'E ÇEVRİLMELİ"
    
    print(f"\n🎯 ÖNERİ: Veri tipi {recommendation}")
    
    return current_dtype, recommendation

def analyze_format_standardization(df, target_col):
    """Format standardizasyonu analizi"""
    print(f"\n📐 FORMAT STANDARDİZASYONU ANALİZİ:")
    print("-" * 50)
    
    non_null_urls = df[target_col].dropna()
    standardization_issues = []
    
    # Case sensitivity analizi
    case_issues = []
    protocol_variations = []
    domain_variations = []
    
    for url in non_null_urls.head(1000):
        url_str = str(url).strip()
        
        # Protocol case variations
        if url_str.startswith('HTTP://'):
            protocol_variations.append('HTTP://')
        elif url_str.startswith('HTTPS://'):
            protocol_variations.append('HTTPS://')
        elif url_str.startswith('http://'):
            protocol_variations.append('http://')
        elif url_str.startswith('https://'):
            protocol_variations.append('https://')
        
        # Domain case variations
        try:
            domain = urlparse(url_str).netloc
            if domain != domain.lower():
                domain_variations.append((domain, domain.lower()))
        except:
            continue
    
    print(f"📊 STANDARDIZASYON DURUMU:")
    
    # Protocol standardization
    protocol_counts = Counter(protocol_variations)
    print(f"   • Protocol Varyasyonları:")
    for protocol, count in protocol_counts.items():
        print(f"     - {protocol}: {count:,} adet")
    
    # Domain case issues
    if domain_variations:
        print(f"   • Domain case issues: {len(domain_variations):,} adet")
        for original, corrected in domain_variations[:3]:
            print(f"     - '{original}' → '{corrected}'")
    
    # Standardization recommendations
    print(f"\n💡 STANDARDİZASYON ÖNERİLERİ:")
    
    standardization_needed = False
    
    if len(protocol_counts) > 1:
        standardization_needed = True
        print(f"   🔄 Protocol Standardization:")
        print(f"      • Tüm URL'leri 'https://' ile başlat")
        print(f"      • HTTP protokollerini HTTPS'e dönüştür")
        print(f"      • Büyük harf protocol'leri küçük harfe çevir")
    
    if domain_variations:
        standardization_needed = True
        print(f"   🔄 Domain Standardization:")
        print(f"      • Tüm domain'leri lowercase'e çevir")
        print(f"      • URL parsing tutarlılığını artır")
    
    if not standardization_needed:
        print(f"   ✅ Format zaten standardize")
    
    return standardization_needed, protocol_counts, domain_variations

def check_column_multiplication(df, target_col):
    """Sütun çoğullaşması kontrolü"""
    print(f"\n🔢 SÜTUN ÇOĞULLAŞMASI KONTROLÜ:")
    print("-" * 50)
    
    # Link ile ilgili sütunları ara
    link_related_columns = []
    url_related_columns = []
    
    for col in df.columns:
        col_lower = col.lower()
        if 'link' in col_lower or 'url' in col_lower:
            link_related_columns.append(col)
        # Company URL'leri de kontrol et
        if 'company' in col_lower and any(keyword in col_lower for keyword in ['url', 'link', 'website']):
            url_related_columns.append(col)
    
    print(f"📋 İLGİLİ SÜTUNLAR:")
    print(f"   • Link/URL sütunları: {len(link_related_columns)} adet")
    for col in link_related_columns:
        unique_count = df[col].nunique()
        null_pct = (df[col].isnull().sum() / len(df)) * 100
        print(f"     - {col}: {unique_count:,} benzersiz, %{null_pct:.1f} null")
    
    if url_related_columns:
        print(f"   • Company URL sütunları: {len(url_related_columns)} adet")
        for col in url_related_columns:
            unique_count = df[col].nunique()
            null_pct = (df[col].isnull().sum() / len(df)) * 100
            print(f"     - {col}: {unique_count:,} benzersiz, %{null_pct:.1f} null")
    
    # Çoğullaşma analizi
    total_url_columns = len(link_related_columns) + len(url_related_columns)
    
    print(f"\n🎯 ÇOĞULLAŞMA DEĞERLENDİRMESİ:")
    if total_url_columns == 1:
        print(f"   ✅ Tek sütun: Çoğullaşma yok")
        multiplication_analysis = "NO_MULTIPLICATION"
    elif total_url_columns <= 3:
        print(f"   ⚠️  Az sayıda URL sütunu: Kontrol edilmeli")
        multiplication_analysis = "MINIMAL_MULTIPLICATION"
    else:
        print(f"   🚨 Çok sayıda URL sütunu: Consolidation gerekebilir")
        multiplication_analysis = "SIGNIFICANT_MULTIPLICATION"
    
    return link_related_columns, url_related_columns, multiplication_analysis

def find_similar_columns(df, target_col):
    """Benzer sütunlarla redundancy kontrolü"""
    print(f"\n🔗 BENZER SÜTUNLAR İLE REDUNDANCY KONTROLÜ:")
    print("-" * 50)
    
    target_unique_count = df[target_col].nunique()
    similar_columns = []
    
    # ID sütunları ile karşılaştırma
    id_columns = [col for col in df.columns if 'id' in col.lower()]
    
    print(f"📊 REDUNDANCY ANALİZİ:")
    print(f"   • {target_col} benzersiz değer: {target_unique_count:,}")
    
    # ID sütunları ile correlation
    print(f"\n🆔 ID SÜTUNLARI İLE KORELASYON:")
    for col in id_columns:
        col_unique = df[col].nunique()
        print(f"   • {col}: {col_unique:,} benzersiz değer")
        
        # Aynı benzersizlik seviyesi kontrolü
        if col_unique == target_unique_count:
            similar_columns.append({
                'column': col,
                'unique_count': col_unique,
                'potential_redundancy': 'HIGH'
            })
            print(f"     🚨 AYNI BENZERSİZLİK SAYISI - Potansiyel redundancy!")
    
    # URL içeriğinden ID çıkarma analizi
    print(f"\n🔍 URL'LERDEN ID ÇIKARMA ANALİZİ:")
    sample_urls = df[target_col].dropna().head(10)
    
    extracted_ids = []
    for url in sample_urls:
        # LinkedIn job URL pattern: /jobs/view/JOBID
        match = re.search(r'/jobs/view/(\d+)', str(url))
        if match:
            job_id = match.group(1)
            extracted_ids.append(job_id)
    
    if extracted_ids:
        print(f"   • URL'lerden çıkarılan ID örnekleri:")
        for i, job_id in enumerate(extracted_ids[:5], 1):
            print(f"     {i}. {job_id}")
        
        # ID sütunu ile karşılaştırma
        if 'id' in df.columns:
            sample_ids = df['id'].head(10).astype(str).tolist()
            matches = len(set(extracted_ids) & set(sample_ids))
            print(f"   • 'id' sütunu ile eşleşme: {matches}/{len(extracted_ids)} örnekte")
            
            if matches > len(extracted_ids) * 0.8:  # %80 üzeri eşleşme
                print(f"     🚨 YÜKSEK REDUNDANCY: URL'ler 'id' sütunundan türetilebilir!")
                similar_columns.append({
                    'column': 'id',
                    'unique_count': df['id'].nunique(),
                    'potential_redundancy': 'DERIVABLE',
                    'derivation_rule': 'https://linkedin.com/jobs/view/{id}'
                })
    
    # Sonuç önerileri
    print(f"\n💡 REDUNDANCY ÖNERİLERİ:")
    if similar_columns:
        for sim in similar_columns:
            print(f"   🔄 {sim['column']} ile redundancy:")
            if sim.get('derivation_rule'):
                print(f"      • Türetme kuralı: {sim['derivation_rule']}")
                print(f"      • ÖNERİ: Link sütununu sil, ihtiyaçta ID'den türet")
            else:
                print(f"      • Detaylı analiz gerekli")
    else:
        print(f"   ✅ Belirgin redundancy tespit edilmedi")
    
    return similar_columns

def generate_insights_and_recommendations(df, target_col, analysis_results):
    """Insights ve öneriler oluştur"""
    print(f"\n💡 INSIGHTS VE STRATEJİK ÖNERİLER:")
    print("=" * 60)
    
    basic_stats = analysis_results['basic_stats']
    null_info = analysis_results['null_analysis']
    similar_cols = analysis_results['similar_columns']
    
    print(f"🎯 {target_col} SÜTUNU HAKKINDA:")
    print(f"   • Temsil ettiği: LinkedIn job posting URL'leri")
    print(f"   • Veri kalitesi: %{(basic_stats['non_null_count']/basic_stats['total_records']*100):.1f} tamlık")
    print(f"   • Benzersizlik: %{(basic_stats['unique_count']/basic_stats['non_null_count']*100):.1f}")
    
    # Business value assessment
    print(f"\n📊 İŞ DEĞERİ DEĞERLENDİRMESİ:")
    
    # URL'lerin business value'su
    if basic_stats['unique_count'] / basic_stats['non_null_count'] > 0.95:
        print(f"   ✅ Yüksek değer: Her URL benzersiz job posting")
        print(f"   🔗 Kullanım alanları:")
        print(f"      • Direkt iş ilanına erişim")
        print(f"      • External referencing")
        print(f"      • Web scraping için endpoint")
        print(f"      • User experience enhancement")
    else:
        print(f"   ⚠️  Orta değer: Bazı URL'ler tekrarlıyor")
    
    # Redundancy değerlendirmesi
    if similar_cols:
        print(f"\n🚨 REDUNDANCY BULGULARI:")
        for sim in similar_cols:
            if sim.get('derivation_rule'):
                print(f"   • {sim['column']} sütunından türetilebilir")
                print(f"   • Potansiyel bellek tasarrufu var")
                print(f"   • ÖNERI: Türetme metodunu değerlendir")
    
    # Optimizasyon önerileri
    print(f"\n🔧 OPTİMİZASYON ÖNERİLERİ:")
    
    # 1. Null handling
    if null_info['null_count'] > 0:
        print(f"   1️⃣ Null Değer Optimizasyonu:")
        print(f"      • {null_info['null_count']:,} adet null URL var")
        print(f"      • 'id' sütununu kullanarak türetme mümkün")
        print(f"      • URL pattern: https://linkedin.com/jobs/view/{{id}}")
    
    # 2. Storage optimization
    print(f"   2️⃣ Storage Optimizasyonu:")
    if similar_cols and any(sim.get('derivation_rule') for sim in similar_cols):
        print(f"      • URL'leri runtime'da türetme")
        print(f"      • Base URL + ID kombinasyonu")
        print(f"      • Memory footprint azaltma")
    else:
        print(f"      • Mevcut format optimize edilmiş görünüyor")
    
    # 3. Data quality improvements
    print(f"   3️⃣ Veri Kalitesi İyileştirmeleri:")
    print(f"      • URL format validation")
    print(f"      • Protocol standardization (https://)")
    print(f"      • Domain consistency kontrolü")
    
    # 4. Business intelligence enhancements
    print(f"   4️⃣ Business Intelligence Geliştirmeleri:")
    print(f"      • URL analytics (click tracking)")
    print(f"      • Geographic link analysis")
    print(f"      • Referral source tracking")
    
    # Kritik kararlar
    print(f"\n🎯 KRİTİK KARARLAR:")
    
    if similar_cols and any(sim.get('derivation_rule') for sim in similar_cols):
        print(f"   ⚠️  URL SÜTUNU ELİMİNASYONU DEĞERLENDİRİLEBİLİR:")
        print(f"      • Avantajlar: Memory tasarrufu, simple structure")
        print(f"      • Dezavantajlar: Runtime computation, dependency on ID")
        print(f"      • Öneri: Business requirement'lara göre karar ver")
    else:
        print(f"   ✅ URL SÜTUNU KORUNMALI:")
        print(f"      • Benzersiz business value sağlıyor")
        print(f"      • Direct access için kritik")
        print(f"      • Alternative yok")

def main():
    """Ana analiz fonksiyonu"""
    print("🚀 LinkedIn Jobs Dataset - Link Sütunu Kapsamlı Analizi")
    print("=" * 80)
    
    # Dataset yükle
    df = load_dataset()
    if df is None:
        return
    
    target_col = 'link'
    
    # Sütun varlığını kontrol et
    if target_col not in df.columns:
        print(f"❌ Hata: '{target_col}' sütunu bulunamadı!")
        available_link_cols = [col for col in df.columns if 'link' in col.lower() or 'url' in col.lower()]
        if available_link_cols:
            print(f"Mevcut benzer sütunlar: {available_link_cols}")
        return
    
    # Kapsamlı analiz
    try:
        # 1. Temel karakteristikler
        basic_stats = analyze_basic_characteristics(df, target_col)
        
        # 2. URL pattern analizi
        protocols, domains, paths = analyze_url_patterns(df, target_col)
        
        # 3. Veri tutarlılığı
        invalid_count, linkedin_count, other_domains = check_data_consistency(df, target_col)
        
        # 4. Null density
        null_count, null_percentage = analyze_null_density(df, target_col)
        
        # 5. Data type compatibility
        current_dtype, type_recommendation = check_data_type_compatibility(df, target_col)
        
        # 6. Format standardization
        standardization_needed, protocol_counts, domain_vars = analyze_format_standardization(df, target_col)
        
        # 7. Column multiplication
        link_cols, url_cols, multiplication = check_column_multiplication(df, target_col)
        
        # 8. Similar columns redundancy
        similar_columns = find_similar_columns(df, target_col)
        
        # 9. Comprehensive insights
        analysis_results = {
            'basic_stats': basic_stats,
            'null_analysis': {'null_count': null_count, 'null_percentage': null_percentage},
            'similar_columns': similar_columns,
            'standardization': standardization_needed,
            'multiplication': multiplication
        }
        
        generate_insights_and_recommendations(df, target_col, analysis_results)
        
        print(f"\n✅ Link sütunu kapsamlı analizi tamamlandı!")
        
    except Exception as e:
        print(f"❌ Analiz hatası: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 