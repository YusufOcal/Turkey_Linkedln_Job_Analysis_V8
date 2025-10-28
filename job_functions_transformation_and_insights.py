import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

print("🔄 JOB FUNCTIONS TRANSFORMATION & INSIGHTS")
print("="*50)

# Load the dataset
df = pd.read_csv('linkedin_jobs_dataset_optimized_step8.csv')

print("1. MEVCUT DURUM ANALİZİ")
print("-"*30)

# Identify columns
formatted_cols = [col for col in df.columns if 'formattedJobFunctions' in col]
job_func_cols = [col for col in df.columns if col.startswith('jobFunctions') and 'formatted' not in col]

print(f"📊 formattedJobFunctions sütunları: {formatted_cols}")
print(f"📊 jobFunctions sütunları (silinecek): {job_func_cols}")

# Check current state
print(f"\nMevcut sütun sayısı: {len(df.columns)}")
print(f"Silinecek sütun sayısı: {len(job_func_cols)}")
print(f"Birleştirilecek sütun sayısı: {len(formatted_cols)}")

print("\n2. SÜTUN BİRLEŞTİRME TRANSFORMASYONU")
print("-"*30)

def merge_job_functions(row):
    """Merge job function columns into a single formatted string"""
    functions = []
    for col in formatted_cols:
        if pd.notna(row[col]) and str(row[col]).strip():
            functions.append(str(row[col]).strip())
    
    if functions:
        return ' | '.join(functions)
    else:
        return 'Not Specified'

# Create merged column
print("🔄 Sütunlar birleştiriliyor...")
df['job_functions_combined'] = df.apply(merge_job_functions, axis=1)

# Validate transformation
print(f"✅ Yeni sütun oluşturuldu: job_functions_combined")
print(f"Toplam kayıt: {len(df['job_functions_combined'])}")
print(f"Boş olmayan: {df['job_functions_combined'].notna().sum()}")
print(f"'Not Specified' olan: {(df['job_functions_combined'] == 'Not Specified').sum()}")

# Sample results
print("\n📋 Birleştirme örnekleri:")
sample_data = df[['job_functions_combined'] + formatted_cols].head(10)
for idx, row in sample_data.iterrows():
    original = [str(row[col]) if pd.notna(row[col]) else 'NaN' for col in formatted_cols]
    combined = row['job_functions_combined']
    print(f"   {original} -> '{combined}'")

print("\n3. SÜTUN SİLME OPERASYONU")
print("-"*30)

# Delete jobFunctions columns
columns_to_delete = job_func_cols + formatted_cols
print(f"🗑️  Silinecek sütunlar: {columns_to_delete}")

df_cleaned = df.drop(columns=columns_to_delete)
print(f"✅ {len(columns_to_delete)} sütun silindi")
print(f"Yeni sütun sayısı: {len(df_cleaned.columns)}")

print("\n4. VERİ KALİTESİ KONTROLÜ")
print("-"*30)

# Quality checks
quality_stats = {
    'total_records': len(df_cleaned),
    'specified_functions': (df_cleaned['job_functions_combined'] != 'Not Specified').sum(),
    'not_specified': (df_cleaned['job_functions_combined'] == 'Not Specified').sum(),
    'specification_rate': ((df_cleaned['job_functions_combined'] != 'Not Specified').sum() / len(df_cleaned)) * 100
}

print(f"📊 Kalite metrikleri:")
print(f"   Toplam kayıt: {quality_stats['total_records']:,}")
print(f"   Belirtilmiş fonksiyon: {quality_stats['specified_functions']:,}")
print(f"   Belirtilmemiş: {quality_stats['not_specified']:,}")
print(f"   Tamamlanma oranı: {quality_stats['specification_rate']:.1f}%")

print("\n5. İŞ ZEKASI INSIGHTları")
print("-"*30)

# Function distribution analysis
all_functions = []
for func_string in df_cleaned['job_functions_combined']:
    if func_string != 'Not Specified':
        functions = [f.strip() for f in func_string.split('|')]
        all_functions.extend(functions)

function_counts = Counter(all_functions)
total_function_mentions = len(all_functions)

print(f"📈 Fonksiyon Dağılımı Analysis:")
print(f"Toplam fonksiyon mention: {total_function_mentions:,}")
print(f"Unique fonksiyon sayısı: {len(function_counts)}")

print(f"\n🏆 Top 15 İş Fonksiyonları:")
for i, (func, count) in enumerate(function_counts.most_common(15), 1):
    percentage = (count / total_function_mentions) * 100
    print(f"   {i:2d}. {func}: {count:,} ({percentage:.1f}%)")

print("\n6. İLERİ DÜZEY BUSINESS INSIGHTS")
print("-"*30)

# Multi-function analysis
multi_function_jobs = df_cleaned[df_cleaned['job_functions_combined'].str.contains('|', na=False)]
single_function_jobs = df_cleaned[(df_cleaned['job_functions_combined'] != 'Not Specified') & 
                                  (~df_cleaned['job_functions_combined'].str.contains('|', na=False))]

print(f"🔍 Fonksiyon Çeşitliliği Analizi:")
print(f"   Tek fonksiyon işler: {len(single_function_jobs):,} ({len(single_function_jobs)/len(df_cleaned)*100:.1f}%)")
print(f"   Çoklu fonksiyon işler: {len(multi_function_jobs):,} ({len(multi_function_jobs)/len(df_cleaned)*100:.1f}%)")

# Function combination analysis
print(f"\n🔗 En Yaygın Fonksiyon Kombinasyonları:")
multi_func_patterns = Counter(multi_function_jobs['job_functions_combined'])
for pattern, count in multi_func_patterns.most_common(10):
    percentage = (count / len(multi_function_jobs)) * 100
    print(f"   '{pattern}': {count} ({percentage:.1f}%)")

# Industry insights
print(f"\n🏭 Sektör Bazlı Fonksiyon Analizi:")
tech_functions = ['Information Technology', 'Engineering', 'Design']
business_functions = ['Business Development', 'Sales', 'Marketing']
analytical_functions = ['Analyst', 'Research', 'Consulting']

tech_jobs = df_cleaned[df_cleaned['job_functions_combined'].str.contains('|'.join(tech_functions), na=False)]
business_jobs = df_cleaned[df_cleaned['job_functions_combined'].str.contains('|'.join(business_functions), na=False)]
analytical_jobs = df_cleaned[df_cleaned['job_functions_combined'].str.contains('|'.join(analytical_functions), na=False)]

print(f"   Teknik roller: {len(tech_jobs):,} ({len(tech_jobs)/len(df_cleaned)*100:.1f}%)")
print(f"   İş geliştirme rolleri: {len(business_jobs):,} ({len(business_jobs)/len(df_cleaned)*100:.1f}%)")
print(f"   Analitik roller: {len(analytical_jobs):,} ({len(analytical_jobs)/len(df_cleaned)*100:.1f}%)")

print("\n7. KORELASYON VE TREENDLERİ")
print("-"*30)

# Check correlation with salary if available
if 'salary' in df_cleaned.columns:
    print("💰 Maaş Korelasyon Analizi:")
    
    # Tech vs non-tech salary comparison
    tech_salaries = df_cleaned[df_cleaned['job_functions_combined'].str.contains('Information Technology|Engineering', na=False)]['salary'].dropna()
    non_tech_salaries = df_cleaned[~df_cleaned['job_functions_combined'].str.contains('Information Technology|Engineering', na=False)]['salary'].dropna()
    
    if len(tech_salaries) > 0 and len(non_tech_salaries) > 0:
        print(f"   Teknik roller ortalama maaş: ${tech_salaries.mean():,.0f}")
        print(f"   Teknik olmayan roller ortalama maaş: ${non_tech_salaries.mean():,.0f}")
        print(f"   Teknik rol maaş avantajı: %{((tech_salaries.mean() / non_tech_salaries.mean() - 1) * 100):.1f}")

# Check correlation with urgency
if 'job_urgency_category' in df_cleaned.columns:
    print(f"\n⏰ Aciliyet Korelasyon Analizi:")
    urgency_function_cross = pd.crosstab(df_cleaned['job_urgency_category'], 
                                        df_cleaned['job_functions_combined'].str.contains('Information Technology|Engineering', na=False))
    print("   Teknik roller urgency dağılımı:")
    for urgency in df_cleaned['job_urgency_category'].unique():
        if pd.notna(urgency):
            tech_ratio = urgency_function_cross.loc[urgency, True] / urgency_function_cross.loc[urgency].sum() * 100
            print(f"      {urgency}: %{tech_ratio:.1f} teknik rol")

print("\n8. ACTIONABLE INSIGHTS")
print("-"*30)

print("🎯 STRATEJİK ÖNERİLER:")

# Top insights
it_percentage = (function_counts['Information Technology'] / total_function_mentions) * 100
eng_percentage = (function_counts['Engineering'] / total_function_mentions) * 100
tech_dominance = it_percentage + eng_percentage

print(f"1. 📊 PAZARA HAKİMİYET:")
print(f"   - Teknik roller pazar payı: %{tech_dominance:.1f}")
print(f"   - IT: %{it_percentage:.1f}, Engineering: %{eng_percentage:.1f}")
print(f"   - Rekabet stratejisi: Teknik yeteneklere odaklan!")

print(f"\n2. 🔄 ÇOKLu FONKSİYON TRENDİ:")
multi_func_percentage = (len(multi_function_jobs) / len(df_cleaned)) * 100
print(f"   - %{multi_func_percentage:.1f} pozisyon çoklu fonksiyon gerektiriyor")
print(f"   - Hibrit beceri setleri değerli!")
print(f"   - Cross-functional deneyim avantajı!")

print(f"\n3. 💡 FARKLILAŞMA ÖNERİLERİ:")
rare_functions = [func for func, count in function_counts.items() if count < 100]
print(f"   - {len(rare_functions)} adet nadir fonksiyon tespit edildi")
print(f"   - Niche alanlar: {rare_functions[:5]}")
print(f"   - Düşük rekabet, yüksek değer potansiyeli!")

print("\n✅ TRANSFORMATION TAMAMLANDI!")
print(f"Yeni dataset: {len(df_cleaned)} kayıt x {len(df_cleaned.columns)} sütun")

# Save the transformed dataset
output_file = 'linkedin_jobs_dataset_optimized_step9.csv'
df_cleaned.to_csv(output_file, index=False)
print(f"💾 Kaydedildi: {output_file}")

print("\n" + "="*50)
print("INSIGHT GENERATION BAŞARILI!") 