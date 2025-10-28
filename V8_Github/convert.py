import pandas as pd

# Girdi ve çıktı dosya adları
input_file = 'linkedin_jobs_dataset_optimized_step13.csv'
output_file = 'linkedin_jobs_dataset_optimized_step13.xlsx'

try:
    # CSV dosyasını oku
    df = pd.read_csv(input_file)
    print(f"✅ CSV dosyası yüklendi: {input_file}")
    
    # Excel dosyasına yaz
    df.to_excel(output_file, index=False, engine='openpyxl')
    print(f"✅ XLSX dosyası oluşturuldu: {output_file}")

except FileNotFoundError:
    print(f"❌ Hata: {input_file} dosyası bulunamadı.")
except ImportError:
    print("❌ Hata: Gerekli kütüphane eksik. Lütfen 'pip install pandas openpyxl' komutunu çalıştırın.")
except Exception as e:
    print(f"❌ Beklenmeyen bir hata oluştu: {e}")
