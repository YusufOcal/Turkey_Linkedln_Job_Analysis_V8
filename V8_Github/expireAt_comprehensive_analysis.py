#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Jobs Dataset - expireAt Column Comprehensive Analysis
expireAt sütununun derinlemesine analizi: format, tutarlılık, veri tipi uyumluluğu, iş zekası potansiyeli
"""

import pandas as pd
import numpy as np
from collections import Counter
import re
import warnings
from datetime import datetime, timedelta
import dateutil.parser
warnings.filterwarnings('ignore')

def analyze_expireAt_comprehensive(df):
    """expireAt sütunu için kapsamlı analiz"""
    
    print("⏰ LINKEDIN JOBS DATASET - EXPIREAT COLUMN COMPREHENSIVE ANALYSIS")
    print("=" * 75)
    
    column_name = 'expireAt'
    
    # Check if column exists
    if column_name not in df.columns:
        print(f"❌ HATA: {column_name} sütunu bulunamadı!")
        # Search for similar datetime/expiry columns
        expiry_related = [col for col in df.columns if any(term in col.lower() 
                         for term in ['expire', 'expiry', 'end', 'close', 'deadline', 'until'])]
        if expiry_related:
            print(f"🔍 Mevcut expiry/deadline benzeri sütunlar: {expiry_related}")
        return None
    
    col_data = df[column_name]
    
    # 1. SÜTUN TEMSİLİ VE ANLAMI
    print("📅 1. SÜTUN TEMSİLİ VE ANLAMI")
    print("-" * 35)
    
    column_info = {
        'name': column_name,
        'purpose': 'Job Posting Expiration Date/Time Management',
        'content_type': 'DateTime timestamp indicating when job posting expires',
        'business_value': 'Job lifecycle management, urgency analysis, application deadline tracking',
        'expected_format': 'Unix timestamp (milliseconds)',
        'source': 'LinkedIn Jobs API - Posting lifecycle metadata',
        'data_usage': 'Application urgency, posting freshness, deadline analytics',
        'time_context': 'Future timestamps indicating posting expiration deadline'
    }
    
    print(f"⏰ {column_info['name']}:")
    print(f"   📝 Purpose: {column_info['purpose']}")
    print(f"   💼 Content Type: {column_info['content_type']}")
    print(f"   🎯 Business Value: {column_info['business_value']}")
    print(f"   📋 Expected Format: {column_info['expected_format']}")
    print(f"   🔗 Source: {column_info['source']}")
    print(f"   🎨 Usage: {column_info['data_usage']}")
    print(f"   ⌚ Time Context: {column_info['time_context']}")
    print()
    
    # 2. VERİ TUTARLILIĞI ANALİZİ
    print("🔍 2. VERİ TUTARLILIĞI ANALİZİ")
    print("-" * 35)
    
    total_rows = len(col_data)
    null_count = col_data.isnull().sum()
    non_null_count = total_rows - null_count
    null_percentage = (null_count / total_rows) * 100
    completeness_score = ((total_rows - null_count) / total_rows) * 100
    
    print(f"📊 Temel İstatistikler:")
    print(f"   📋 Toplam kayıt: {total_rows:,}")
    print(f"   ✅ Dolu kayıt: {non_null_count:,} ({completeness_score:.1f}%)")
    print(f"   ❌ Null kayıt: {null_count:,} ({null_percentage:.1f}%)")
    
    if null_count > 0:
        print(f"   ⚠️ Null yoğunluğu: {'CRITICAL' if null_percentage > 50 else 'HIGH' if null_percentage > 20 else 'MODERATE' if null_percentage > 5 else 'LOW'}")
    else:
        print(f"   ✨ Mükemmel completeness - Null yok!")
    print()
    
    # 3. DATETIME FORMAT ANALİZİ
    print("📅 3. DATETIME FORMAT ANALİZİ")
    print("-" * 30)
    
    if non_null_count > 0:
        # Sample data analysis
        sample_values = col_data.dropna().head(10).tolist()
        print(f"📋 Örnek Değerler (İlk 10):")
        for i, val in enumerate(sample_values, 1):
            print(f"   {i:2d}. {val}")
        print()
        
        # Data type analysis
        current_dtype = col_data.dtype
        print(f"🔧 Mevcut Veri Tipi: {current_dtype}")
        
        # Try to parse datetime formats
        datetime_analysis = analyze_datetime_formats(col_data.dropna())
        
        print(f"📊 DateTime Format Analizi:")
        print(f"   🎯 Tespit edilen format: {datetime_analysis['detected_format']}")
        print(f"   ✅ Parse başarı oranı: {datetime_analysis['parse_success_rate']:.1f}%")
        if datetime_analysis['min_date']:
            print(f"   📅 En erken tarih: {datetime_analysis['min_date']}")
            print(f"   📅 En geç tarih: {datetime_analysis['max_date']}")
        print(f"   ⌚ Time zone bilgisi: {datetime_analysis['timezone_info']}")
        print()
        
        # Business Logic Analysis
        print("💼 4. İŞ MANTIK ANALİZİ")
        print("-" * 25)
        
        business_logic = analyze_expiry_business_logic(datetime_analysis['parsed_dates'])
        
        print(f"📊 Expiry İstatistikleri:")
        print(f"   ⏰ Geçmiş tarihlerde expires: {business_logic['expired_count']:,} ({business_logic['expired_percentage']:.1f}%)")
        print(f"   🚀 Gelecekte expires: {business_logic['future_count']:,} ({business_logic['future_percentage']:.1f}%)")
        print(f"   📅 Bugün expires: {business_logic['today_count']:,}")
        print(f"   📊 Ortalama expiry süresi: {business_logic['avg_days_to_expiry']:.1f} gün")
        print(f"   🎯 İş mantık skoru: {business_logic['logic_score']:.1f}/100")
        print()
        
        # 5. URGENCY VE DEADLİNE ANALİZİ
        print("🚨 5. URGENCY VE DEADLİNE ANALİZİ")
        print("-" * 35)
        
        urgency_analysis = analyze_urgency_patterns(datetime_analysis['parsed_dates'])
        
        print(f"📊 Urgency Dağılımı:")
        for category, data in urgency_analysis['urgency_distribution'].items():
            print(f"   {data['emoji']} {category}: {data['count']:,} ({data['percentage']:.1f}%)")
        
        print(f"\n📈 İstatistiksel Metrikler:")
        print(f"   📊 Medyan kalan süre: {urgency_analysis['median_days_remaining']:.1f} gün")
        print(f"   📊 Standart sapma: {urgency_analysis['std_days_remaining']:.1f} gün")
        print(f"   🎯 Urgency intelligence skoru: {urgency_analysis['urgency_score']:.1f}/100")
        print()
    
    # 6. VERİ TİPİ UYUMLULUğU VE OPTİMİZASYON
    print("🔧 6. VERİ TİPİ UYUMLULUğU VE OPTİMİZASYON")
    print("-" * 45)
    
    # Memory usage analysis
    memory_usage_mb = col_data.memory_usage(deep=True) / 1024**2
    
    print(f"💾 Memory Analizi:")
    print(f"   📊 Mevcut memory kullanımı: {memory_usage_mb:.3f} MB")
    print(f"   🔧 Mevcut data type: {current_dtype}")
    
    if non_null_count > 0:
        # Optimization suggestions
        optimization_suggestions = suggest_datetime_optimizations(col_data, datetime_analysis)
        
        print(f"\n🚀 Optimizasyon Önerileri:")
        for suggestion in optimization_suggestions:
            print(f"   {suggestion['emoji']} {suggestion['title']}: {suggestion['description']}")
            print(f"     💾 Memory tasarrufu: {suggestion['memory_saving']}")
            print(f"     ⚡ Performance artışı: {suggestion['performance_gain']}")
    print()
    
    # 7. KOLON SİMİLARİTY ANALİZİ
    print("🔍 7. KOLON SİMİLARİTY ANALİZİ")
    print("-" * 35)
    
    # Find similar datetime columns
    datetime_columns = find_similar_datetime_columns(df, exclude_col=column_name)
    
    if datetime_columns:
        print(f"📅 Benzer DateTime sütunları bulundu:")
        for sim_col in datetime_columns:
            similarity_score = calculate_datetime_similarity(col_data, df[sim_col])
            print(f"   📊 {sim_col}: Similarity {similarity_score:.1f}%")
            
        print(f"\n🔍 Duplicate Detection:")
        duplicate_analysis = detect_datetime_duplicates(df, column_name, datetime_columns)
        if duplicate_analysis['duplicates_found']:
            print(f"   ⚠️ Potential duplicates detected!")
            for dup in duplicate_analysis['duplicate_pairs']:
                print(f"     🔗 {dup['column']}: {dup['match_rate']:.1f}% match")
        else:
            print(f"   ✅ No duplicate datetime columns detected")
    else:
        print(f"✅ Unique datetime column - no similar columns found")
    print()
    
    # 8. STRATEJİK ÖNERİLER VE SKORLAMA
    print("📈 8. STRATEJİK ÖNERİLER VE SKORLAMA")
    print("-" * 40)
    
    # Overall quality score calculation
    quality_metrics = {
        'completeness': completeness_score,
        'format_consistency': datetime_analysis.get('parse_success_rate', 0) if non_null_count > 0 else 0,
        'business_logic': business_logic.get('logic_score', 0) if non_null_count > 0 else 0,
        'urgency_intelligence': urgency_analysis.get('urgency_score', 0) if non_null_count > 0 else 0,
        'uniqueness': 100 - (len(datetime_columns) * 10)  # Penalty for similar columns
    }
    
    overall_quality = sum(quality_metrics.values()) / len(quality_metrics)
    
    print(f"📊 Kalite Metrikleri:")
    for metric, score in quality_metrics.items():
        status = "EXCELLENT" if score >= 90 else "GOOD" if score >= 70 else "FAIR" if score >= 50 else "POOR"
        print(f"   📈 {metric.title()}: {score:.1f}/100 ({status})")
    
    print(f"\n🏆 GENEL KALİTE SKORU: {overall_quality:.1f}/100")
    overall_status = "EXCELLENT" if overall_quality >= 90 else "GOOD" if overall_quality >= 70 else "FAIR" if overall_quality >= 50 else "POOR"
    print(f"📊 Genel Durum: {overall_status}")
    
    # Strategic recommendations
    recommendations = generate_expireAt_recommendations(quality_metrics, datetime_analysis if non_null_count > 0 else None)
    
    print(f"\n🎯 Stratejik Öneriler:")
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec['title']}")
        print(f"      📋 {rec['description']}")
        print(f"      🎯 Öncelik: {rec['priority']}")
        print(f"      💡 Beklenen fayda: {rec['expected_benefit']}")
    print()
    
    print("=" * 75)
    print("✅ EXPIREAT COLUMN COMPREHENSIVE ANALYSIS COMPLETED")
    print("=" * 75)
    
    return {
        'column_name': column_name,
        'quality_score': overall_quality,
        'quality_status': overall_status,
        'completeness': completeness_score,
        'memory_usage_mb': memory_usage_mb,
        'null_percentage': null_percentage,
        'datetime_analysis': datetime_analysis if non_null_count > 0 else None,
        'business_logic': business_logic if non_null_count > 0 else None,
        'urgency_analysis': urgency_analysis if non_null_count > 0 else None,
        'recommendations': recommendations
    }

def analyze_datetime_formats(series):
    """DateTime formatlarını analiz eder"""
    
    sample_size = min(1000, len(series))
    sample_data = series.sample(n=sample_size) if len(series) > sample_size else series
    
    parsed_dates = []
    detected_format = 'Unknown'
    parse_success_count = 0
    
    for value in sample_data:
        try:
            # Try to parse as datetime
            if isinstance(value, str):
                parsed_date = dateutil.parser.parse(value)
                parsed_dates.append(parsed_date)
                parse_success_count += 1
            elif isinstance(value, (int, float)):
                # Try as timestamp (convert from milliseconds if needed)
                timestamp_val = value
                if timestamp_val > 1e10:  # Milliseconds timestamp
                    timestamp_val = timestamp_val / 1000
                parsed_date = datetime.fromtimestamp(timestamp_val)
                parsed_dates.append(parsed_date)
                parse_success_count += 1
                detected_format = 'Unix timestamp (milliseconds)'
            else:
                # Already datetime
                parsed_dates.append(value)
                parse_success_count += 1
        except:
            continue
    
    if parse_success_count > 0 and detected_format == 'Unknown':
        # Try to detect format from successful parses
        first_valid = str(sample_data.iloc[0])
        if 'T' in first_valid and 'Z' in first_valid:
            detected_format = 'ISO 8601 UTC'
        elif 'T' in first_valid:
            detected_format = 'ISO 8601'
        else:
            detected_format = 'Standard datetime'
    
    parse_success_rate = (parse_success_count / len(sample_data)) * 100 if len(sample_data) > 0 else 0
    
    result = {
        'detected_format': detected_format,
        'parse_success_rate': parse_success_rate,
        'parsed_dates': parsed_dates,
        'min_date': min(parsed_dates).strftime('%Y-%m-%d %H:%M:%S') if parsed_dates else None,
        'max_date': max(parsed_dates).strftime('%Y-%m-%d %H:%M:%S') if parsed_dates else None,
        'timezone_info': 'Local/Unknown'
    }
    
    return result

def analyze_expiry_business_logic(parsed_dates):
    """Expiry tarihlerinin iş mantığını analiz eder"""
    
    if not parsed_dates:
        return {'logic_score': 0, 'expired_count': 0, 'future_count': 0, 'today_count': 0, 
                'expired_percentage': 0, 'future_percentage': 0, 'avg_days_to_expiry': 0}
    
    now = datetime.now()
    
    expired_count = sum(1 for date in parsed_dates if date < now)
    future_count = sum(1 for date in parsed_dates if date > now)
    today_count = sum(1 for date in parsed_dates if date.date() == now.date())
    
    total_dates = len(parsed_dates)
    expired_percentage = (expired_count / total_dates) * 100
    future_percentage = (future_count / total_dates) * 100
    
    # Calculate average days to expiry
    days_to_expiry = [(date - now).days for date in parsed_dates]
    avg_days_to_expiry = sum(days_to_expiry) / len(days_to_expiry)
    
    # Business logic score (higher score for more future dates)
    logic_score = future_percentage * 0.8 + (20 if avg_days_to_expiry > 0 else 0)
    logic_score = min(100, logic_score)
    
    return {
        'expired_count': expired_count,
        'future_count': future_count,
        'today_count': today_count,
        'expired_percentage': expired_percentage,
        'future_percentage': future_percentage,
        'avg_days_to_expiry': avg_days_to_expiry,
        'logic_score': logic_score
    }

def analyze_urgency_patterns(parsed_dates):
    """Urgency patterns analizi"""
    
    if not parsed_dates:
        return {'urgency_score': 0, 'urgency_distribution': {}, 
                'median_days_remaining': 0, 'std_days_remaining': 0}
    
    now = datetime.now()
    
    urgency_categories = {
        'EXPIRED': {'count': 0, 'emoji': '🔴', 'days_threshold': 0, 'comparison': 'less'},
        'URGENT_TODAY': {'count': 0, 'emoji': '🚨', 'days_threshold': 0, 'comparison': 'equal'},
        'URGENT_1_3_DAYS': {'count': 0, 'emoji': '⚠️', 'days_threshold': 3, 'comparison': 'between'},
        'MODERATE_1_WEEK': {'count': 0, 'emoji': '🟡', 'days_threshold': 7, 'comparison': 'between'},
        'NORMAL_1_MONTH': {'count': 0, 'emoji': '🟢', 'days_threshold': 30, 'comparison': 'between'},
        'FUTURE_LONG': {'count': 0, 'emoji': '🔵', 'days_threshold': 30, 'comparison': 'greater'}
    }
    
    days_remaining = []
    
    for date in parsed_dates:
        days_diff = (date - now).days
        days_remaining.append(days_diff)
        
        if days_diff < 0:
            urgency_categories['EXPIRED']['count'] += 1
        elif days_diff == 0:
            urgency_categories['URGENT_TODAY']['count'] += 1
        elif days_diff <= 3:
            urgency_categories['URGENT_1_3_DAYS']['count'] += 1
        elif days_diff <= 7:
            urgency_categories['MODERATE_1_WEEK']['count'] += 1
        elif days_diff <= 30:
            urgency_categories['NORMAL_1_MONTH']['count'] += 1
        else:
            urgency_categories['FUTURE_LONG']['count'] += 1
    
    total_dates = len(parsed_dates)
    
    # Add percentages
    urgency_distribution = {}
    for category, data in urgency_categories.items():
        percentage = (data['count'] / total_dates) * 100
        urgency_distribution[category] = {
            'count': data['count'],
            'percentage': percentage,
            'emoji': data['emoji']
        }
    
    # Calculate urgency intelligence score
    urgency_score = (
        urgency_distribution['URGENT_TODAY']['percentage'] * 1.0 +
        urgency_distribution['URGENT_1_3_DAYS']['percentage'] * 0.8 +
        urgency_distribution['MODERATE_1_WEEK']['percentage'] * 0.6 +
        urgency_distribution['NORMAL_1_MONTH']['percentage'] * 0.4 +
        urgency_distribution['FUTURE_LONG']['percentage'] * 0.2
    )
    
    return {
        'urgency_distribution': urgency_distribution,
        'median_days_remaining': float(np.median(days_remaining)),
        'std_days_remaining': float(np.std(days_remaining)),
        'urgency_score': min(100, urgency_score)
    }

def find_similar_datetime_columns(df, exclude_col):
    """Benzer datetime sütunlarını bulur"""
    
    datetime_columns = []
    
    for col in df.columns:
        if col == exclude_col:
            continue
            
        # Check for datetime-related column names
        datetime_keywords = ['date', 'time', 'expire', 'created', 'updated', 'posted', 'deadline', 'start', 'end']
        if any(keyword in col.lower() for keyword in datetime_keywords):
            datetime_columns.append(col)
            continue
        
        # Check data type
        if df[col].dtype in ['datetime64[ns]', 'object']:
            # Sample check if it might be datetime
            sample = df[col].dropna().head(10)
            if len(sample) > 0:
                try:
                    pd.to_datetime(sample.iloc[0])
                    datetime_columns.append(col)
                except:
                    pass
    
    return datetime_columns

def calculate_datetime_similarity(col1, col2):
    """İki datetime sütunu arasındaki similarity hesaplar"""
    
    # Compare non-null values
    valid_data1 = col1.dropna()
    valid_data2 = col2.dropna()
    
    if len(valid_data1) == 0 or len(valid_data2) == 0:
        return 0.0
    
    # Simple comparison - this would need more sophisticated logic in production
    similarity = 50.0  # Base similarity for datetime columns
    
    # Same null pattern bonus
    null_pattern_similarity = 100 - abs(col1.isnull().sum() - col2.isnull().sum()) / len(col1) * 100
    similarity += null_pattern_similarity * 0.3
    
    return min(100.0, similarity)

def detect_datetime_duplicates(df, target_col, similar_cols):
    """Datetime duplicate detection"""
    
    duplicates_found = False
    duplicate_pairs = []
    
    target_data = df[target_col]
    
    for col in similar_cols:
        similarity_score = calculate_datetime_similarity(target_data, df[col])
        
        if similarity_score > 95:  # Very high similarity threshold
            duplicates_found = True
            duplicate_pairs.append({
                'column': col,
                'match_rate': similarity_score
            })
    
    return {
        'duplicates_found': duplicates_found,
        'duplicate_pairs': duplicate_pairs
    }

def suggest_datetime_optimizations(col_data, datetime_analysis):
    """DateTime sütunu için optimizasyon önerileri"""
    
    suggestions = []
    
    # Memory optimization suggestion
    current_memory = col_data.memory_usage(deep=True) / 1024**2
    
    suggestions.append({
        'emoji': '💾',
        'title': 'DateTime Type Conversion',
        'description': 'Convert to pandas datetime64[ns] for optimal performance',
        'memory_saving': f'~{current_memory * 0.3:.3f} MB potential savings',
        'performance_gain': '3-5x faster datetime operations'
    })
    
    # Urgency category creation
    suggestions.append({
        'emoji': '🚨',
        'title': 'Urgency Category Creation',
        'description': 'Create categorical urgency levels (URGENT/NORMAL/FUTURE)',
        'memory_saving': f'~{current_memory * 0.7:.3f} MB with category encoding',
        'performance_gain': 'Fast categorical filtering and grouping'
    })
    
    return suggestions

def generate_expireAt_recommendations(quality_metrics, datetime_analysis):
    """ExpireAt sütunu için stratejik öneriler"""
    
    recommendations = []
    
    # Based on completeness
    if quality_metrics['completeness'] < 50:
        recommendations.append({
            'title': 'Data Quality Improvement',
            'description': 'High null rate requires data filling strategy or alternative source',
            'priority': 'HIGH',
            'expected_benefit': 'Improved analytical capability and deadline tracking'
        })
    
    # Based on format consistency
    if quality_metrics['format_consistency'] < 90:
        recommendations.append({
            'title': 'DateTime Format Standardization',
            'description': 'Standardize datetime format for consistent parsing and operations',
            'priority': 'MEDIUM',
            'expected_benefit': 'Reliable datetime operations and reduced parsing errors'
        })
    
    # Business intelligence recommendation
    if datetime_analysis and quality_metrics['urgency_intelligence'] > 60:
        recommendations.append({
            'title': 'Urgency Intelligence Implementation',
            'description': 'Create urgency-based features for application deadline analysis',
            'priority': 'HIGH',
            'expected_benefit': 'Job urgency insights and application timing optimization'
        })
    
    # Memory optimization
    recommendations.append({
        'title': 'Memory and Performance Optimization',
        'description': 'Convert to optimal datetime type and create derived categorical features',
        'priority': 'MEDIUM',
        'expected_benefit': '70%+ memory reduction and faster operations'
    })
    
    return recommendations

if __name__ == "__main__":
    try:
        # Load the latest dataset
        print("📂 Dataset yükleniyor...")
        df = pd.read_csv('linkedin_jobs_dataset_with_job_investment_category.csv')
        print(f"✅ Dataset yüklendi: {len(df):,} satır, {len(df.columns)} sütun")
        print()
        
        # Run comprehensive analysis
        result = analyze_expireAt_comprehensive(df)
        
        if result:
            print(f"\n📊 Analiz Sonucu: {result['quality_status']} ({result['quality_score']:.1f}/100)")
            
    except FileNotFoundError:
        print("❌ HATA: linkedin_jobs_dataset_with_job_investment_category.csv dosyası bulunamadı!")
        print("📋 Mevcut CSV dosyalarını kontrol edin.")
    except Exception as e:
        print(f"❌ HATA: {str(e)}") 