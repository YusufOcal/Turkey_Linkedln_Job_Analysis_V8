import pandas as pd

print("🔍 YENİ DATASET SÜTUN KONTROLÜ")
print("="*40)

# Load the transformed dataset
df = pd.read_csv('linkedin_jobs_with_combined_functions.csv')

print(f"📊 Toplam sütun sayısı: {len(df.columns)}")

# Check for job function related columns
job_related_cols = [col for col in df.columns if 'job' in col.lower() or 'function' in col.lower()]

print(f"\n📋 İş fonksiyonu ile ilgili sütunlar:")
for col in job_related_cols:
    print(f"   - {col}")

print(f"\n🆕 Transformation sonrası oluşturulan yeni sütun:")
if 'job_functions_combined' in df.columns:
    print(f"   ✅ job_functions_combined")
    print(f"   📈 Örnek değerler:")
    sample_values = df['job_functions_combined'].dropna().head(5)
    for i, value in enumerate(sample_values, 1):
        print(f"      {i}. {value}")
    
    print(f"\n📊 İstatistikler:")
    print(f"   - Toplam kayıt: {len(df['job_functions_combined'])}")
    print(f"   - Boş olmayan: {df['job_functions_combined'].notna().sum()}")
    print(f"   - 'Not Specified': {(df['job_functions_combined'] == 'Not Specified').sum()}")
    print(f"   - Çoklu fonksiyon: {df['job_functions_combined'].str.contains('|', na=False).sum()}")
else:
    print("   ❌ job_functions_combined sütunu bulunamadı!")

print(f"\n🗑️ Silinen sütunlar (artık mevcut değil):")
expected_deleted = ['jobFunctions/0', 'jobFunctions/1', 'jobFunctions/2', 
                   'formattedJobFunctions/0', 'formattedJobFunctions/1', 'formattedJobFunctions/2']
for col in expected_deleted:
    if col in df.columns:
        print(f"   ⚠️  {col} - HALA MEVCUT!")
    else:
        print(f"   ✅ {col} - başarıyla silindi")

print(f"\n📋 Tüm sütun adları:")
for i, col in enumerate(df.columns, 1):
    print(f"   {i:2d}. {col}")

print(f"\n" + "="*40)
print("SÜTUN KONTROLÜ TAMAMLANDI!") 