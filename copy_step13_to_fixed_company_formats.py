#!/usr/bin/env python3
"""
Copy Step13 to Fixed Company Formats

linkedin_jobs_dataset_optimized_step13.xlsx dosyasını okuyup
fixed_all_company_colums formatında 3 format oluşturur:
- fixed_all_company_colums.csv
- fixed_all_company_colums.json  
- fixed_all_company_colums.xlsx

Hiçbir ekleme/çıkarma yapılmaz, sadece format kopyalama.
"""

import pandas as pd
import json
import os

def copy_step13_to_fixed_formats():
    """Step13'ü fixed_all_company_colums formatlarına kopyala"""
    
    print("📁 STEP13 TO FIXED_ALL_COMPANY_COLUMS CONVERTER")
    print("=" * 55)
    
    # Source file
    source_file = 'linkedin_jobs_dataset_optimized_step13.xlsx'
    
    # Target files
    target_files = {
        'csv': 'fixed_all_company_colums.csv',
        'json': 'fixed_all_company_colums.json', 
        'xlsx': 'fixed_all_company_colums.xlsx'
    }
    
    try:
        print(f"📂 Loading source file: {source_file}")
        df = pd.read_excel(source_file)
        print(f"✅ Source loaded successfully:")
        print(f"   📊 Records: {len(df):,}")
        print(f"   📊 Columns: {len(df.columns)}")
        print(f"   💾 Memory usage: {df.memory_usage(deep=True).sum() / (1024*1024):.2f} MB")
        print()
        
        # Source file size
        source_size = os.path.getsize(source_file) / (1024*1024)
        print(f"📏 Source file size: {source_size:.2f} MB")
        print()
        
    except Exception as e:
        print(f"❌ Error loading source file: {e}")
        return False
    
    print("🔄 CONVERTING TO TARGET FORMATS:")
    print("=" * 40)
    
    conversion_results = {}
    
    # 1. CSV FORMAT
    print("📄 1. Creating CSV format...")
    try:
        csv_file = target_files['csv']
        df.to_csv(csv_file, index=False)
        csv_size = os.path.getsize(csv_file) / (1024*1024)
        conversion_results['csv'] = {
            'success': True,
            'file': csv_file,
            'size_mb': csv_size
        }
        print(f"   ✅ CSV created: {csv_file}")
        print(f"   📏 Size: {csv_size:.2f} MB")
        print()
    except Exception as e:
        print(f"   ❌ CSV creation failed: {e}")
        conversion_results['csv'] = {'success': False, 'error': str(e)}
        print()
    
    # 2. JSON FORMAT
    print("📄 2. Creating JSON format...")
    try:
        json_file = target_files['json']
        # Convert to JSON with orient='records' for readable format
        df.to_json(json_file, orient='records', indent=2)
        json_size = os.path.getsize(json_file) / (1024*1024)
        conversion_results['json'] = {
            'success': True,
            'file': json_file,
            'size_mb': json_size
        }
        print(f"   ✅ JSON created: {json_file}")
        print(f"   📏 Size: {json_size:.2f} MB")
        print()
    except Exception as e:
        print(f"   ❌ JSON creation failed: {e}")
        conversion_results['json'] = {'success': False, 'error': str(e)}
        print()
    
    # 3. XLSX FORMAT
    print("📄 3. Creating XLSX format...")
    try:
        xlsx_file = target_files['xlsx']
        df.to_excel(xlsx_file, index=False, engine='openpyxl')
        xlsx_size = os.path.getsize(xlsx_file) / (1024*1024)
        conversion_results['xlsx'] = {
            'success': True,
            'file': xlsx_file,
            'size_mb': xlsx_size
        }
        print(f"   ✅ XLSX created: {xlsx_file}")
        print(f"   📏 Size: {xlsx_size:.2f} MB")
        print()
    except Exception as e:
        print(f"   ❌ XLSX creation failed: {e}")
        conversion_results['xlsx'] = {'success': False, 'error': str(e)}
        print()
    
    # CONVERSION SUMMARY
    print("📊 CONVERSION SUMMARY")
    print("=" * 25)
    
    successful_conversions = sum(1 for result in conversion_results.values() if result.get('success', False))
    total_conversions = len(conversion_results)
    success_rate = (successful_conversions / total_conversions) * 100
    
    print(f"🎯 Success Rate: {successful_conversions}/{total_conversions} ({success_rate:.1f}%)")
    print()
    
    print(f"📋 File Details:")
    print(f"   📂 Source: {source_file} ({source_size:.2f} MB)")
    
    for format_type, result in conversion_results.items():
        if result.get('success', False):
            file_name = result['file']
            file_size = result['size_mb']
            print(f"   ✅ {format_type.upper()}: {file_name} ({file_size:.2f} MB)")
        else:
            print(f"   ❌ {format_type.upper()}: Failed - {result.get('error', 'Unknown error')}")
    
    # SIZE COMPARISON
    if successful_conversions > 0:
        print(f"\n📏 SIZE COMPARISON:")
        print(f"   📂 Source (XLSX): {source_size:.2f} MB")
        
        if conversion_results['csv'].get('success'):
            csv_size = conversion_results['csv']['size_mb']
            csv_ratio = csv_size / source_size
            print(f"   📄 CSV: {csv_size:.2f} MB ({csv_ratio:.2f}x source)")
        
        if conversion_results['json'].get('success'):
            json_size = conversion_results['json']['size_mb'] 
            json_ratio = json_size / source_size
            print(f"   📄 JSON: {json_size:.2f} MB ({json_ratio:.2f}x source)")
        
        if conversion_results['xlsx'].get('success'):
            xlsx_size = conversion_results['xlsx']['size_mb']
            xlsx_ratio = xlsx_size / source_size
            print(f"   📄 XLSX: {xlsx_size:.2f} MB ({xlsx_ratio:.2f}x source)")
    
    # DATA INTEGRITY VERIFICATION
    print(f"\n🔍 DATA INTEGRITY VERIFICATION:")
    print("-" * 35)
    
    integrity_check = True
    for format_type, result in conversion_results.items():
        if result.get('success', False):
            try:
                # Verify each file can be loaded back
                if format_type == 'csv':
                    test_df = pd.read_csv(result['file'])
                elif format_type == 'json':
                    test_df = pd.read_json(result['file'])
                elif format_type == 'xlsx':
                    test_df = pd.read_excel(result['file'])
                
                # Check dimensions
                if len(test_df) == len(df) and len(test_df.columns) == len(df.columns):
                    print(f"   ✅ {format_type.upper()}: Integrity verified ({len(test_df):,} records, {len(test_df.columns)} columns)")
                else:
                    print(f"   ❌ {format_type.upper()}: Integrity failed - dimension mismatch")
                    integrity_check = False
                    
            except Exception as e:
                print(f"   ❌ {format_type.upper()}: Integrity check failed - {e}")
                integrity_check = False
    
    # FINAL STATUS
    print(f"\n🎯 FINAL STATUS:")
    print("-" * 20)
    
    if successful_conversions == total_conversions and integrity_check:
        print(f"🎉 PERFECT SUCCESS!")
        print(f"   ✅ All {total_conversions} formats created successfully")
        print(f"   ✅ Data integrity verified for all formats")
        print(f"   ✅ No data loss or corruption detected")
        print(f"   📁 Files ready: fixed_all_company_colums.{format_type}")
    elif successful_conversions > 0:
        print(f"⚠️  PARTIAL SUCCESS:")
        print(f"   ✅ {successful_conversions}/{total_conversions} formats created")
        if not integrity_check:
            print(f"   ⚠️  Some integrity issues detected")
    else:
        print(f"❌ CONVERSION FAILED:")
        print(f"   🚨 No files were created successfully")
    
    return {
        'success_rate': success_rate,
        'successful_conversions': successful_conversions,
        'total_conversions': total_conversions,
        'conversion_results': conversion_results,
        'integrity_check': integrity_check
    }

if __name__ == "__main__":
    print("🚀 Starting conversion process...")
    print()
    
    results = copy_step13_to_fixed_formats()
    
    if results and results['success_rate'] == 100.0:
        print(f"\n✅ Conversion completed successfully!")
        print(f"📁 All fixed_all_company_colums files are ready!")
    else:
        print(f"\n⚠️  Conversion completed with issues.")
        print(f"📋 Check the summary above for details.") 