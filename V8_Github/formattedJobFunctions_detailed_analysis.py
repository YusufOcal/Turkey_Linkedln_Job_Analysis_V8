import pandas as pd
import numpy as np
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Load the dataset
print("🔍 FORMATTED JOB FUNCTIONS - DETAYLI ANALİZ")
print("="*60)

df = pd.read_csv('linkedin_jobs_dataset_with_datetime_and_urgency.csv')

# Job function columns
job_function_cols = [col for col in df.columns if 'formattedJobFunctions' in col]

print("1. SÜTUN İÇERİK DETAYLI İNCELEME")
print("-"*40)

for col in job_function_cols:
    print(f"\n🔸 {col} detaylı analiz:")
    print(f"   Boş veri oranı: {(df[col].isna().sum() / len(df) * 100):.2f}%")
    print(f"   Unique değer sayısı: {df[col].nunique()}")
    
    # Top values
    value_counts = df[col].value_counts().head(10)
    print(f"   En yaygın değerler:")
    for value, count in value_counts.items():
        print(f"      {value}: {count} ({count/len(df)*100:.1f}%)")

print("\n2. DİĞER SÜTUNLAR İLE KORELASYON ANALİZİ")
print("-"*40)

# Check relationship with job title
print("\n🔍 Job Title ile İlişki Analizi:")
if 'title' in df.columns:
    sample_titles_functions = df[['title'] + job_function_cols].head(20)
    print("Örnek Title - Function eşleştirmeleri:")
    for idx, row in sample_titles_functions.iterrows():
        title = row['title']
        functions = [row[col] for col in job_function_cols if pd.notna(row[col])]
        print(f"   '{title}' -> {functions}")
        if idx >= 5:  # Show only first 5
            break

# Check relationship with company industry
print("\n🔍 Company Industry ile İlişki Analizi:")
if 'companyIndustry' in df.columns:
    industry_function_analysis = df.groupby('companyIndustry')[job_function_cols[0]].value_counts().head(20)
    print("Industry - Function eşleştirmeleri (Top 20):")
    for (industry, function), count in industry_function_analysis.items():
        print(f"   {industry} -> {function}: {count}")

print("\n3. HİYERAŞİK YAPI ANALİZİ")
print("-"*40)

print("🔍 Sütunlar arası hiyerarşi kontrolü:")
hierarchy_patterns = []

for idx in range(min(100, len(df))):  # First 100 rows
    row_functions = []
    for col in job_function_cols:
        if pd.notna(df.iloc[idx][col]):
            row_functions.append(df.iloc[idx][col])
    
    if len(row_functions) > 1:
        hierarchy_patterns.append(tuple(row_functions))

# Analyze patterns
pattern_counts = Counter(hierarchy_patterns)
print(f"Toplam hiyerarşi paterni: {len(pattern_counts)}")
print("\nEn yaygın hiyerarşi paternleri:")
for pattern, count in pattern_counts.most_common(10):
    print(f"   {' -> '.join(pattern)}: {count} kez")

print("\n4. VERİ KALİTESİ SORUNLARI TESPİTİ")
print("-"*40)

# Check for inconsistencies
print("🔍 Tutarsızlık analizi:")

# Check if later columns have values when earlier ones are empty
inconsistency_count = 0
for idx in range(len(df)):
    has_0 = pd.notna(df.iloc[idx]['formattedJobFunctions/0'])
    has_1 = pd.notna(df.iloc[idx]['formattedJobFunctions/1'])
    has_2 = pd.notna(df.iloc[idx]['formattedJobFunctions/2'])
    
    # Logical inconsistency: having /1 or /2 without /0
    if (has_1 and not has_0) or (has_2 and not has_0):
        inconsistency_count += 1

print(f"Hiyerarşik tutarsızlık sayısı: {inconsistency_count}")
print(f"Tutarsızlık oranı: {(inconsistency_count/len(df)*100):.2f}%")

# Check for duplicate values in same row
duplicate_in_row_count = 0
for idx in range(len(df)):
    row_values = []
    for col in job_function_cols:
        if pd.notna(df.iloc[idx][col]):
            row_values.append(df.iloc[idx][col])
    
    if len(row_values) != len(set(row_values)):
        duplicate_in_row_count += 1

print(f"Aynı satırda tekrar eden değer sayısı: {duplicate_in_row_count}")
print(f"Tekrar oranı: {(duplicate_in_row_count/len(df)*100):.2f}%")

print("\n5. BENZER SÜTUNLAR İLE KARŞILAŞTIRMA")
print("-"*40)

# Check if there are other similar columns
similar_cols = []
for col in df.columns:
    if 'function' in col.lower() or 'category' in col.lower() or 'type' in col.lower():
        if col not in job_function_cols:
            similar_cols.append(col)

print(f"Benzer amaca hizmet edebilecek sütunlar: {similar_cols}")

for similar_col in similar_cols[:3]:  # Analyze first 3
    if similar_col in df.columns:
        print(f"\n🔸 {similar_col} karşılaştırması:")
        print(f"   Unique değer sayısı: {df[similar_col].nunique()}")
        print(f"   Boş veri oranı: {(df[similar_col].isna().sum()/len(df)*100):.2f}%")
        
        # Sample values
        sample_values = df[similar_col].dropna().head(5).tolist()
        print(f"   Örnek değerler: {sample_values}")

print("\n6. DÖNÜŞTÜRMEVEİYİLEŞTİRME ÖNERİLERİ")
print("-"*40)

print("🎯 ÖNERİLER:")

print("\n1. YAPISAL DÖNÜŞÜM:")
print("   ✅ 3 ayrı sütunu tek sütuna birleştir")
print("   ✅ JSON array formatı: ['func1', 'func2', 'func3']")
print("   ✅ Pipe-separated format: 'func1|func2|func3'")
print("   ✅ Primary/Secondary/Tertiary structure")

print("\n2. VERİ KALİTESİ İYİLEŞTİRME:")
print(f"   ⚠️  formattedJobFunctions/1: %41.24 boş veri - Title'dan çıkarım yapılabilir")
print(f"   ⚠️  formattedJobFunctions/2: %77.88 boş veri - Opsiyonel alan haline getir")
print("   ✅ Hiyerarşik tutarlılık kontrolü")
print("   ✅ Tekrar eden değerleri temizle")

print("\n3. STANDARTLAŞTIRMA:")
print("   ✅ Büyük/küçük harf zaten tutarlı")
print("   ✅ 35 unique kategori - makul sayı")
print("   ✅ Kategorileri gruplayabilir (IT + Engineering = Tech)")

print("\n4. SÜTUN BİRLEŞTİRME ÖNERİSİ:")
print("   🔄 Önerilen yaklaşım: ")
print("   - Primary Job Function (formattedJobFunctions/0)")
print("   - Secondary Job Functions (1,2 birleştirilmiş)")
print("   - Bu yapı daha anlamlı ve verimli")

print("\n7. İŞ ZEKASI ÇIKARIMLARİ")
print("-"*40)

print("📊 İş Fonksiyonu Dağılımı:")
all_functions = []
for col in job_function_cols:
    all_functions.extend(df[col].dropna().tolist())

function_counter = Counter(all_functions)
total_functions = sum(function_counter.values())

print(f"Toplam fonksiyon atama sayısı: {total_functions}")
print("\nFonksiyon kategori paylaşımı:")
for func, count in function_counter.most_common(10):
    percentage = (count / total_functions) * 100
    print(f"   {func}: {percentage:.1f}% ({count} pozisyon)")

print(f"\n🎯 KRİTİK TESPİTLER:")
print(f"   - IT + Engineering = %{((function_counter['Information Technology'] + function_counter['Engineering']) / total_functions) * 100:.1f} (Teknik roller dominantı)")
print(f"   - Business Development: %{(function_counter['Business Development'] / total_functions) * 100:.1f}")
print(f"   - Sales + Marketing: %{((function_counter['Sales'] + function_counter['Marketing']) / total_functions) * 100:.1f}")

print("\n" + "="*60)
print("DETAYLI ANALİZ TAMAMLANDI!") 