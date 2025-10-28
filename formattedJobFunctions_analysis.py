import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Load the dataset
print("🔍 FORMATTED JOB FUNCTIONS ANALYSIS")
print("="*50)

df = pd.read_csv('linkedin_jobs_dataset_with_datetime_and_urgency.csv')

# Identify formattedJobFunctions columns
job_function_cols = [col for col in df.columns if 'formattedJobFunctions' in col]
print(f"📊 Tespit edilen sütunlar: {job_function_cols}")
print(f"📈 Toplam sütun sayısı: {len(job_function_cols)}")

print("\n1. SÜTUN GRUBU TEMSİL ANALİZİ")
print("-"*40)
print("Bu sütunlar iş pozisyonlarının fonksiyonel kategorilerini temsil ediyor.")
print("Örneğin: 'Engineering', 'Sales', 'Marketing', 'Operations' gibi...")
print("Her bir sütun (0,1,2) muhtemelen birden fazla iş fonksiyonunu barındırıyor.")

print("\n2. SÜTUN YAPISAL ANALİZİ")
print("-"*40)

for col in job_function_cols:
    print(f"\n🔸 {col}:")
    print(f"   Veri tipi: {df[col].dtype}")
    print(f"   Toplam kayıt: {len(df[col])}")
    print(f"   Boş olmayan: {df[col].notna().sum()}")
    print(f"   Boş olan: {df[col].isna().sum()}")
    print(f"   Boş yüzdesi: {(df[col].isna().sum() / len(df[col]) * 100):.2f}%")
    print(f"   Unique değer sayısı: {df[col].nunique()}")
    
    # Sample values
    non_null_values = df[col].dropna().head(10)
    print(f"   Örnek değerler: {list(non_null_values)[:5]}")

print("\n3. VERİ TİPİ UYUMLULUK ANALİZİ")
print("-"*40)

for col in job_function_cols:
    print(f"\n🔸 {col} veri tipi analizi:")
    
    # Check current data type
    current_dtype = df[col].dtype
    print(f"   Mevcut veri tipi: {current_dtype}")
    
    # Check if all values are strings when not null
    non_null_data = df[col].dropna()
    if len(non_null_data) > 0:
        all_strings = all(isinstance(x, str) for x in non_null_data)
        print(f"   Tüm değerler string mi: {all_strings}")
        
        # Check for non-string values
        non_string_count = sum(1 for x in non_null_data if not isinstance(x, str))
        print(f"   String olmayan değer sayısı: {non_string_count}")

print("\n4. VERİ TUTARLILIĞI VE BENZERLIK ANALİZİ")
print("-"*40)

# Compare similarity between columns
similarity_analysis = {}
for i, col1 in enumerate(job_function_cols):
    for j, col2 in enumerate(job_function_cols):
        if i < j:  # Avoid duplicate comparisons
            # Calculate overlap
            set1 = set(df[col1].dropna())
            set2 = set(df[col2].dropna())
            
            intersection = len(set1.intersection(set2))
            union = len(set1.union(set2))
            jaccard_similarity = intersection / union if union > 0 else 0
            
            similarity_analysis[f"{col1} vs {col2}"] = {
                'jaccard_similarity': jaccard_similarity,
                'common_values': intersection,
                'total_unique': union
            }
            
            print(f"\n🔸 {col1} vs {col2}:")
            print(f"   Jaccard benzerlik: {jaccard_similarity:.3f}")
            print(f"   Ortak değer sayısı: {intersection}")
            print(f"   Toplam unique değer: {union}")

print("\n5. VERİ İÇERİK ANALİZİ")
print("-"*40)

all_job_functions = []
for col in job_function_cols:
    non_null_values = df[col].dropna().tolist()
    all_job_functions.extend(non_null_values)

# Most common job functions
job_function_counts = Counter(all_job_functions)
print(f"\nEn yaygın iş fonksiyonları:")
for func, count in job_function_counts.most_common(10):
    print(f"   {func}: {count} kez")

print(f"\nToplam unique iş fonksiyonu: {len(job_function_counts)}")

print("\n6. BOŞ VERİ ANALİZİ VE ÖNERİLER")
print("-"*40)

for col in job_function_cols:
    null_percentage = (df[col].isna().sum() / len(df[col]) * 100)
    print(f"\n🔸 {col}:")
    print(f"   Boş veri oranı: {null_percentage:.2f}%")
    
    if null_percentage > 50:
        print("   ⚠️  YÜKSEK BOŞ VERİ ORANI!")
        print("   📋 Öneriler:")
        print("      - Diğer sütunlardan veri çıkarımı")
        print("      - Job title'dan otomatik kategorilendirme")
        print("      - 'Unknown' veya 'General' kategorisi atama")
    elif null_percentage > 20:
        print("   ⚡ ORTA BOŞ VERİ ORANI")
        print("   📋 Öneriler:")
        print("      - Job title pattern matching")
        print("      - Company industry bazlı tahmin")
    else:
        print("   ✅ DÜŞÜK BOŞ VERİ ORANI - Kabul edilebilir")

print("\n7. STANDARTLAŞTIRMA ÖNERİLERİ")
print("-"*40)

# Case sensitivity analysis
case_issues = {}
for col in job_function_cols:
    values = df[col].dropna().tolist()
    lower_values = [str(v).lower() for v in values]
    
    # Find case variations
    case_variations = {}
    for original, lower in zip(values, lower_values):
        if lower in case_variations:
            case_variations[lower].add(original)
        else:
            case_variations[lower] = {original}
    
    # Find items with multiple case variations
    multi_case = {k: v for k, v in case_variations.items() if len(v) > 1}
    case_issues[col] = multi_case

for col, issues in case_issues.items():
    if issues:
        print(f"\n🔸 {col} - Büyük/küçük harf sorunları:")
        for lower_form, variations in list(issues.items())[:5]:  # Show first 5
            print(f"   '{lower_form}': {variations}")
    else:
        print(f"\n🔸 {col} - ✅ Büyük/küçük harf tutarlı")

print("\n8. SÜTUN ÇOKLUĞU VE YAPISAL ÖNERI")
print("-"*40)

print("🔍 Bu sütun grubu yapısal analizi:")
print(f"   - {len(job_function_cols)} adet ayrı sütun mevcut")
print("   - Her sütun bir iş fonksiyonu hiyerarşisini temsil ediyor olabilir")
print("   - Alternatif yaklaşımlar:")
print("     1. Liste formatına dönüştürme (JSON array)")
print("     2. Ana kategori + alt kategori ayrımı")
print("     3. Tek sütunda birleştirme (delimiter ile)")

# Check if there's a hierarchical pattern
print("\n📊 Hiyerarşik pattern analizi:")
for i, col in enumerate(job_function_cols):
    sample_values = df[col].dropna().head(20).tolist()
    print(f"   {col} örnek değerler: {sample_values[:3]}")

print("\n" + "="*50)
print("ANALİZ TAMAMLANDI!") 