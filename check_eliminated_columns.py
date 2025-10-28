#!/usr/bin/env python3
"""
Eliminated Columns Verification

Silinen sütunların gerçekten silinip silinmediğini kontrol eder.
"""

import pandas as pd

def check_eliminated_columns():
    """Silinen sütunları kontrol et"""
    
    print("🔍 Silinen Sütunların Doğrulama Kontrolü")
    print("=" * 50)
    
    # Test edilecek dosyalar
    files_to_check = [
        'linkedin_jobs_cleaned_no_redundant_links.csv',
        'linkedin_jobs_cleaned_no_redundant_urn.csv'
    ]
    
    # Silinen sütunlar
    eliminated_columns = [
        'jobApplicantInsights/entityUrn',
        'workRemoteAllowed', 
        'link'
    ]
    
    for file_name in files_to_check:
        try:
            print(f"\n📂 Dosya: {file_name}")
            df = pd.read_csv(file_name)
            
            print(f"   • Toplam sütun: {len(df.columns)}")
            print(f"   • Silinen sütunların durumu:")
            
            for col in eliminated_columns:
                status = "VAR 😱" if col in df.columns else "SİLİNMİŞ ✅"
                print(f"     - {col}: {status}")
            
            # Hangi sütunlar var göster
            remaining_eliminated = [col for col in eliminated_columns if col in df.columns]
            if remaining_eliminated:
                print(f"   ⚠️  SİLİNMEMİŞ SÜTUNLAR: {len(remaining_eliminated)} adet")
            else:
                print(f"   ✅ Tüm hedef sütunlar başarıyla silinmiş")
                
        except FileNotFoundError:
            print(f"   ❌ Dosya bulunamadı: {file_name}")
        except Exception as e:
            print(f"   ❌ Hata: {e}")
    
    print(f"\n📋 SONUÇ KONTROLÜ:")
    print(f"Son dosyada hangi sütunlar kalmış kontrol edelim...")

if __name__ == "__main__":
    check_eliminated_columns() 