import pandas as pd
import numpy as np
import re
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

print("🔍 JOBAPPLICANTINSIGHTS/ENTITYURN ANALYSIS")
print("="*60)

# Load the dataset
df = pd.read_csv('linkedin_jobs_with_combined_functions.csv')

target_column = 'jobApplicantInsights/entityUrn'

print("1. SÜTUN TEMSİL ANALİZİ")
print("-"*40)
print("Bu sütun LinkedIn'in iş başvuru insights sisteminin entity URN'lerini temsil ediyor.")
print("URN (Uniform Resource Name): LinkedIn'in internal tracking identifier'ı")
print("Muhtemel amaçlar:")
print("  - Başvuru istatistikleri tracking")
print("  - İş ilanının başvuru performans metrikleri")
print("  - LinkedIn'in internal analytics sistemi")
print("  - Başvuran profil kategorilerinin analizi")

print(f"\n2. TEMEL VERİ YAPISI ANALİZİ")
print("-"*40)

if target_column not in df.columns:
    print(f"❌ '{target_column}' sütunu bulunamadı!")
    print("Mevcut benzer sütunlar:")
    similar_cols = [col for col in df.columns if 'applicant' in col.lower() or 'insight' in col.lower() or 'urn' in col.lower()]
    for col in similar_cols:
        print(f"  - {col}")
    exit()

print(f"📊 Temel istatistikler:")
print(f"   Veri tipi: {df[target_column].dtype}")
print(f"   Toplam kayıt: {len(df[target_column])}")
print(f"   Boş olmayan: {df[target_column].notna().sum()}")
print(f"   Boş olan: {df[target_column].isna().sum()}")
print(f"   Boş yüzdesi: {(df[target_column].isna().sum() / len(df[target_column]) * 100):.2f}%")
print(f"   Unique değer sayısı: {df[target_column].nunique()}")

# Sample values
print(f"\n📋 Örnek değerler:")
non_null_values = df[target_column].dropna().head(10)
for i, value in enumerate(non_null_values, 1):
    print(f"   {i:2d}. {value}")

print(f"\n3. VERİ TİPİ UYUMLULUK ANALİZİ")
print("-"*40)

non_null_data = df[target_column].dropna()
print(f"Boş olmayan veri sayısı: {len(non_null_data)}")

if len(non_null_data) > 0:
    # Check data type consistency
    all_strings = all(isinstance(x, str) for x in non_null_data)
    print(f"Tüm değerler string mi: {all_strings}")
    
    # Check for URN pattern
    urn_pattern = r'^urn:li:[a-zA-Z]+:[a-zA-Z0-9\-_]+'
    valid_urns = 0
    invalid_urns = []
    
    for value in non_null_data:
        if isinstance(value, str):
            if re.match(urn_pattern, value):
                valid_urns += 1
            else:
                invalid_urns.append(value)
    
    print(f"\nURN Format Analizi:")
    print(f"   Geçerli URN formatı: {valid_urns}")
    print(f"   Geçersiz format: {len(invalid_urns)}")
    print(f"   Format uyumluluk: {(valid_urns / len(non_null_data) * 100):.2f}%")
    
    if invalid_urns and len(invalid_urns) <= 10:
        print(f"   Geçersiz format örnekleri: {invalid_urns[:5]}")

print(f"\n4. URN YAPISAL ANALİZİ")
print("-"*40)

if len(non_null_data) > 0:
    # Parse URN structure
    urn_components = []
    urn_types = []
    
    for value in non_null_data:
        if isinstance(value, str) and value.startswith('urn:li:'):
            parts = value.split(':')
            if len(parts) >= 3:
                urn_type = parts[2] if len(parts) > 2 else 'unknown'
                urn_types.append(urn_type)
                urn_components.append({
                    'full_urn': value,
                    'type': urn_type,
                    'id': ':'.join(parts[3:]) if len(parts) > 3 else ''
                })
    
    type_counter = Counter(urn_types)
    print(f"URN Type Dağılımı:")
    for urn_type, count in type_counter.most_common(10):
        percentage = (count / len(urn_types)) * 100
        print(f"   {urn_type}: {count} ({percentage:.1f}%)")
    
    # Length analysis
    if urn_components:
        lengths = [len(comp['full_urn']) for comp in urn_components]
        print(f"\nURN Uzunluk Analizi:")
        print(f"   Minimum uzunluk: {min(lengths)}")
        print(f"   Maximum uzunluk: {max(lengths)}")
        print(f"   Ortalama uzunluk: {np.mean(lengths):.1f}")

print(f"\n5. VERİ TUTARLILIĞI VE PATTERN ANALİZİ")
print("-"*40)

# Check for duplicates
duplicate_count = df[target_column].duplicated().sum()
unique_ratio = df[target_column].nunique() / df[target_column].notna().sum() * 100

print(f"Veri Tutarlılığı:")
print(f"   Tekrar eden değer: {duplicate_count}")
print(f"   Unique oranı: {unique_ratio:.2f}%")

if duplicate_count > 0:
    print(f"   ⚠️ Duplicate değerler tespit edildi!")
    duplicated_values = df[df[target_column].duplicated()][target_column].value_counts().head(5)
    print(f"   En çok tekrarlanan değerler:")
    for value, count in duplicated_values.items():
        print(f"      '{value}': {count} kez")

# Pattern consistency
print(f"\nPattern Tutarlılığı:")
if len(non_null_data) > 0:
    # Check for different patterns
    patterns = {}
    for value in non_null_data.head(100):  # Sample first 100
        if isinstance(value, str):
            pattern = re.sub(r'[a-zA-Z0-9\-_]+', 'X', value)
            patterns[pattern] = patterns.get(pattern, 0) + 1
    
    print(f"   Tespit edilen pattern sayısı: {len(patterns)}")
    for pattern, count in Counter(patterns).most_common(5):
        print(f"      '{pattern}': {count} kez")

print(f"\n6. BOŞ VERİ ANALİZİ VE ÖNERİLER")
print("-"*40)

null_percentage = (df[target_column].isna().sum() / len(df[target_column]) * 100)
print(f"Boş veri oranı: {null_percentage:.2f}%")

if null_percentage > 50:
    print("⚠️ YÜKSEK BOŞ VERİ ORANI!")
    print("📋 Öneriler:")
    print("   - Bu sütun opsiyonel olabilir (analytics feature)")
    print("   - 'NOT_AVAILABLE' değeri ile doldur")
    print("   - Sütunu sil (business value düşükse)")
    print("   - Job ID'den generate edilebilir mi kontrol et")
elif null_percentage > 20:
    print("⚡ ORTA BOŞ VERİ ORANI")
    print("📋 Öneriler:")
    print("   - Pattern-based generation")
    print("   - Job ID + timestamp kombinasyonu")
    print("   - Default URN structure oluştur")
else:
    print("✅ DÜŞÜK BOŞ VERİ ORANI - Kabul edilebilir")

print(f"\n7. BENZER SÜTUNLAR İLE KARŞILAŞTIRMA")
print("-"*40)

# Find similar columns
similar_columns = []
for col in df.columns:
    if col != target_column:
        if ('urn' in col.lower() or 
            'entity' in col.lower() or 
            'id' in col.lower() or
            'insight' in col.lower() or
            'applicant' in col.lower()):
            similar_columns.append(col)

print(f"Benzer amaca hizmet edebilecek sütunlar:")
for col in similar_columns:
    print(f"   - {col}")
    if col in df.columns:
        similarity_check = False
        try:
            # Check for overlapping non-null values
            col_data = df[col].dropna()
            target_data = df[target_column].dropna()
            
            if len(col_data) > 0 and len(target_data) > 0:
                # Check if both are string type
                if (col_data.dtype == 'object' and target_data.dtype == 'object'):
                    common_count = len(set(col_data.astype(str)) & set(target_data.astype(str)))
                    if common_count > 0:
                        print(f"      ⚠️ {common_count} ortak değer tespit edildi!")
                        similarity_check = True
                
                print(f"      Unique değer sayısı: {df[col].nunique()}")
                print(f"      Boş veri oranı: {(df[col].isna().sum()/len(df)*100):.1f}%")
        except:
            print(f"      Karşılaştırma hatası")

print(f"\n8. STANDARTLAŞTIRMA ÖNERİLERİ")
print("-"*40)

# Case sensitivity and format issues
if len(non_null_data) > 0:
    # Check for case variations in URN structure
    case_issues = []
    format_issues = []
    
    for value in non_null_data.head(50):  # Sample check
        if isinstance(value, str):
            if not value.startswith('urn:li:'):
                format_issues.append(value)
            if value != value.lower() and 'urn:li:' in value.lower():
                case_issues.append(value)
    
    print(f"Format Standardizasyon:")
    print(f"   Case sensitivity sorunları: {len(case_issues)}")
    print(f"   Format sorunları: {len(format_issues)}")
    
    if case_issues:
        print(f"   Case sorunları örnekleri: {case_issues[:3]}")
    if format_issues:
        print(f"   Format sorunları örnekleri: {format_issues[:3]}")
    
    if not case_issues and not format_issues:
        print("   ✅ Format tutarlı")

print(f"\n9. BUSINESS VALUE VE TRANSFORMATıON ÖNERİLERİ")
print("-"*40)

print("💼 Business Value Analizi:")
print(f"   - URN'ler LinkedIn'in internal tracking sistemi")
print(f"   - Başvuru insights'ları için kullanılıyor olabilir")
print(f"   - Analytics ve reporting için değerli")

print(f"\n🔄 Transformation Önerileri:")

if null_percentage > 50:
    print("   1. SÜTUN SİLME ÖNERİSİ:")
    print("      - %50+ boş veri business value'yu düşürüyor")
    print("      - Internal tracking için gerekli olmayabilir")
    print("      - Analiz için kritik değil")
elif unique_ratio < 50:
    print("   1. VERİ KALİTESİ GELİŞTİRME:")
    print("      - Duplicate değerleri temizle")
    print("      - Unique constraint ekle")
    print("      - Data validation rules")
else:
    print("   1. VERİ STANDARDIZASYONU:")
    print("      - Format validation")
    print("      - Case normalization")
    print("      - URN structure validation")

print(f"\n2. ALTERNATİF YAKLAŞIMLAR:")
print("   - Entity type'a göre kategorize et")
print("   - URN'den metadata çıkar")
print("   - Başvuru tracking için kullan")
print("   - Analytics dashboard entegrasyonu")

print(f"\n10. KRİTİK ÖNERİLER VE SONRAKİ ADIMLAR")
print("-"*40)

print("🚨 KRİTİK BULGULAR:")

if null_percentage > 70:
    print("   ⚠️ YÜKSEK BOŞ VERİ - Sütunu silmeyi düşün!")
elif duplicate_count > len(non_null_data) * 0.1:
    print("   ⚠️ YÜKSEK DUPLICATE - Data integrity problemi!")
elif unique_ratio < 30:
    print("   ⚠️ DÜŞÜK UNIQUE ORAN - Veri kalitesi sorunu!")

if len(similar_columns) > 3:
    print("   ⚠️ ÇOK FAZLA BENZER SÜTUN - Redundancy riski!")

print(f"\n🎯 SONRAKİ ADIM ÖNERİLERİ:")
print("   1. URN pattern validation implement et")
print("   2. Null values için default generation strategy")
print("   3. Duplicate cleaning procedure")
print("   4. Business stakeholder'larla value confirmation")
print("   5. Performance impact analizi")

print(f"\n" + "="*60)
print("ANALYSIS COMPLETED!")

# Summary stats
print(f"\n📊 ÖZET:")
print(f"   Veri kalitesi: {'DÜŞÜK' if null_percentage > 50 else 'ORTA' if null_percentage > 20 else 'YÜKSEK'}")
print(f"   Business value: {'DÜŞÜK' if null_percentage > 70 else 'ORTA' if duplicate_count > 100 else 'YÜKSEK'}")
print(f"   Transformation önceliği: {'YÜKSEK' if null_percentage > 50 or duplicate_count > 100 else 'ORTA'}") 