#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Jobs Dataset - expireAt Business Insight Analysis
expireAt sütunun iş zekası analizi ve stratejik değer keşfi
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def analyze_expireAt_business_intelligence(df):
    """expireAt sütunu için iş zekası analizi"""
    
    print("🚀 LINKEDIN JOBS DATASET - EXPIREAT BUSINESS INSIGHT ANALYSIS")
    print("=" * 70)
    
    column_name = 'expireAt'
    
    if column_name not in df.columns:
        print(f"❌ HATA: {column_name} sütunu bulunamadı!")
        return None
    
    col_data = df[column_name]
    
    # Convert timestamps to datetime
    print("🔄 Timestamp dönüştürme işlemi...")
    df_work = df.copy()
    df_work['expire_datetime'] = pd.to_datetime(df_work[column_name], unit='ms')
    df_work['days_to_expire'] = (df_work['expire_datetime'] - datetime.now()).dt.days
    
    # 1. İŞ ZEKAsi VE MARKET INTELLİGENCE
    print("\n💼 1. İŞ ZEKAsi VE MARKET INTELLİGENCE")
    print("-" * 45)
    
    print("📊 ExpireAt İş Anlamı:")
    print("   🎯 Job Posting Lifecycle Management")
    print("   📈 Application Urgency Intelligence")
    print("   ⏰ Market Timing Optimization")
    print("   🚀 Employer Posting Strategy Analysis")
    print("   💡 Candidate Application Timing Insights")
    print()
    
    # Market timing analysis
    market_intelligence = analyze_market_timing_patterns(df_work)
    
    print("🌟 Market Intelligence Bulgular:")
    print(f"   ⏰ Ortalama job posting süresi: {market_intelligence['avg_posting_duration']:.1f} gün")
    print(f"   📊 En yaygın posting süresi: {market_intelligence['mode_posting_duration']} gün")
    print(f"   🎯 İdeal application zamanı: İlk {market_intelligence['ideal_application_window']} gün")
    print(f"   🚨 Acil iş oranı: {market_intelligence['urgent_job_percentage']:.1f}%")
    print(f"   📈 Premium posting indicatörü: {market_intelligence['premium_posting_indicator']}")
    print()
    
    # 2. URGENCY PATTERNS VE EMPLOYER BEHAVIOR
    print("🚨 2. URGENCY PATTERNS VE EMPLOYER BEHAVIOR")
    print("-" * 50)
    
    urgency_insights = analyze_employer_urgency_behavior(df_work)
    
    print("📊 Employer Urgency Behavior:")
    for pattern, data in urgency_insights['urgency_patterns'].items():
        print(f"   {data['emoji']} {pattern}: {data['count']:,} jobs ({data['percentage']:.1f}%)")
        print(f"      💡 Insight: {data['business_insight']}")
    
    print(f"\n🎯 Strategic Urgency Intelligence:")
    print(f"   📈 High urgency job market: {urgency_insights['high_urgency_market']}")
    print(f"   ⚡ Fast hiring preference: {urgency_insights['fast_hiring_percentage']:.1f}% employers")
    print(f"   📊 Application competition level: {urgency_insights['competition_level']}")
    print()
    
    # 3. SEASONAL VE TEMPORAL PATTERNS
    print("📅 3. SEASONAL VE TEMPORAL PATTERNS")
    print("-" * 40)
    
    temporal_patterns = analyze_temporal_posting_patterns(df_work)
    
    print("📊 Temporal Posting Intelligence:")
    print(f"   📅 Peak posting months: {', '.join(temporal_patterns['peak_months'])}")
    print(f"   📉 Low activity months: {', '.join(temporal_patterns['low_months'])}")
    print(f"   ⏰ Average posting lifecycle: {temporal_patterns['avg_lifecycle_days']:.1f} gün")
    print(f"   🎯 Best application timing: {temporal_patterns['best_application_timing']}")
    print()
    
    # 4. CROSS-COLUMN CORRELATION ANALYSIS
    print("🔗 4. CROSS-COLUMN CORRELATION ANALYSIS")
    print("-" * 45)
    
    correlation_insights = analyze_expiry_correlations(df_work)
    
    print("📊 ExpireAt Correlation Insights:")
    for correlation, data in correlation_insights.items():
        print(f"   🔗 {correlation}:")
        print(f"      📈 Correlation strength: {data['strength']}")
        print(f"      💡 Business insight: {data['insight']}")
        print(f"      🎯 Actionable intelligence: {data['actionable']}")
    print()
    
    # 5. INVESTMENT LEVEL VE PREMIUM PATTERNS
    print("💰 5. INVESTMENT LEVEL VE PREMIUM PATTERNS")
    print("-" * 45)
    
    if 'job_investment_type' in df_work.columns:
        investment_patterns = analyze_investment_vs_expiry(df_work)
        
        print("📊 Investment vs Expiry Patterns:")
        for inv_type, inv_data in investment_patterns.items():
            if inv_type == 'premium_intelligence':
                continue
            print(f"   💎 {inv_type}:")
            print(f"      ⏰ Ortalama expiry süresi: {inv_data['avg_days']:.1f} gün")
            print(f"      📊 Job count: {inv_data['count']:,} ({inv_data['percentage']:.1f}%)")
            print(f"      🎯 Urgency level: {inv_data['urgency_level']}")
            print(f"      💡 Business strategy: {inv_data['business_strategy']}")
        print()
        
        premium_intelligence = investment_patterns.get('premium_intelligence', {})
        if premium_intelligence:
            print("🌟 Premium Posting Intelligence:")
            print(f"   💰 Premium jobs average expiry: {premium_intelligence['premium_avg_days']:.1f} gün")
            print(f"   🆓 Organic jobs average expiry: {premium_intelligence['organic_avg_days']:.1f} gün")
            print(f"   📊 Premium posting advantage: {premium_intelligence['premium_advantage']}")
            print(f"   🎯 Investment ROI indicator: {premium_intelligence['roi_indicator']}")
    else:
        print("   ⚠️ job_investment_type sütunu bulunamadı - investment analizi atlandı")
    print()
    
    # 6. PREDICTIVE INSIGHTS VE RECOMMENDATIONS
    print("🔮 6. PREDICTIVE INSIGHTS VE RECOMMENDATIONS")
    print("-" * 50)
    
    predictive_insights = generate_predictive_insights(df_work)
    
    print("🎯 Predictive Intelligence:")
    for insight_type, data in predictive_insights.items():
        print(f"   🔮 {insight_type}:")
        print(f"      📊 Prediction: {data['prediction']}")
        print(f"      📈 Confidence: {data['confidence']}")
        print(f"      💡 Business value: {data['business_value']}")
    print()
    
    # 7. STRATEGIC TRANSFORMATION RECOMMENDATIONS
    print("🚀 7. STRATEGIC TRANSFORMATION RECOMMENDATIONS")
    print("-" * 55)
    
    transformation_strategy = generate_transformation_strategy(df_work, {
        'market_intelligence': market_intelligence,
        'urgency_insights': urgency_insights,
        'temporal_patterns': temporal_patterns,
        'correlation_insights': correlation_insights
    })
    
    print("📋 ExpireAt Transformation Strategy:")
    for i, strategy in enumerate(transformation_strategy, 1):
        print(f"   {i}. 🎯 {strategy['title']}")
        print(f"      📋 Description: {strategy['description']}")
        print(f"      💰 Business value: {strategy['business_value']}")
        print(f"      ⚡ Implementation: {strategy['implementation']}")
        print(f"      📊 Expected impact: {strategy['expected_impact']}")
    print()
    
    print("=" * 70)
    print("✅ EXPIREAT BUSINESS INSIGHT ANALYSIS COMPLETED")
    print("=" * 70)
    
    return {
        'market_intelligence': market_intelligence,
        'urgency_insights': urgency_insights,
        'temporal_patterns': temporal_patterns,
        'correlation_insights': correlation_insights,
        'transformation_strategy': transformation_strategy
    }

def analyze_market_timing_patterns(df):
    """Market timing patterns analizi"""
    
    current_time = datetime.now()
    
    # Calculate posting duration (approximate)
    df['days_to_expire'] = (df['expire_datetime'] - current_time).dt.days
    
    # Filter reasonable ranges
    reasonable_range = (df['days_to_expire'] >= -30) & (df['days_to_expire'] <= 365)
    df_filtered = df[reasonable_range]
    
    avg_posting_duration = df_filtered['days_to_expire'].mean()
    mode_posting_duration = df_filtered['days_to_expire'].mode().iloc[0] if len(df_filtered['days_to_expire'].mode()) > 0 else 30
    
    # Urgency analysis
    urgent_jobs = df_filtered[df_filtered['days_to_expire'] <= 7]
    urgent_percentage = (len(urgent_jobs) / len(df_filtered)) * 100
    
    # Ideal application window (typically first 1/3 of posting period)
    ideal_window = max(1, int(avg_posting_duration / 3))
    
    # Premium posting indicator (longer postings usually indicate premium features)
    premium_threshold = df_filtered['days_to_expire'].quantile(0.75)
    premium_indicator = "High" if premium_threshold > 30 else "Medium" if premium_threshold > 14 else "Low"
    
    return {
        'avg_posting_duration': avg_posting_duration,
        'mode_posting_duration': mode_posting_duration,
        'ideal_application_window': ideal_window,
        'urgent_job_percentage': urgent_percentage,
        'premium_posting_indicator': premium_indicator
    }

def analyze_employer_urgency_behavior(df):
    """Employer urgency behavior analizi"""
    
    current_time = datetime.now()
    df['days_to_expire'] = (df['expire_datetime'] - current_time).dt.days
    
    urgency_patterns = {
        'IMMEDIATE_HIRE': {
            'count': len(df[df['days_to_expire'] <= 3]),
            'emoji': '🚨',
            'business_insight': 'Critical hiring needs - immediate staffing gaps'
        },
        'FAST_HIRE': {
            'count': len(df[(df['days_to_expire'] > 3) & (df['days_to_expire'] <= 14)]),
            'emoji': '⚡',
            'business_insight': 'Urgent but planned hiring - competitive positions'
        },
        'STANDARD_HIRE': {
            'count': len(df[(df['days_to_expire'] > 14) & (df['days_to_expire'] <= 30)]),
            'emoji': '📋',
            'business_insight': 'Standard hiring process - quality-focused recruitment'
        },
        'EXTENDED_HIRE': {
            'count': len(df[df['days_to_expire'] > 30]),
            'emoji': '🎯',
            'business_insight': 'Strategic hiring - specialized roles or extensive vetting'
        }
    }
    
    total_jobs = len(df)
    
    # Add percentages
    for pattern in urgency_patterns:
        urgency_patterns[pattern]['percentage'] = (urgency_patterns[pattern]['count'] / total_jobs) * 100
    
    # Overall insights
    fast_hiring = urgency_patterns['IMMEDIATE_HIRE']['percentage'] + urgency_patterns['FAST_HIRE']['percentage']
    high_urgency_market = "Yes" if fast_hiring > 30 else "Moderate" if fast_hiring > 15 else "Low"
    
    competition_level = "High" if fast_hiring > 25 else "Medium" if fast_hiring > 15 else "Low"
    
    return {
        'urgency_patterns': urgency_patterns,
        'high_urgency_market': high_urgency_market,
        'fast_hiring_percentage': fast_hiring,
        'competition_level': competition_level
    }

def analyze_temporal_posting_patterns(df):
    """Temporal posting patterns analizi"""
    
    # Extract month from expiry dates
    df['expire_month'] = df['expire_datetime'].dt.month
    df['expire_year'] = df['expire_datetime'].dt.year
    
    # Month distribution
    month_counts = df['expire_month'].value_counts().sort_index()
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Peak and low months
    peak_months = month_counts.nlargest(3).index.tolist()
    low_months = month_counts.nsmallest(3).index.tolist()
    
    peak_month_names = [month_names[m-1] for m in peak_months]
    low_month_names = [month_names[m-1] for m in low_months]
    
    # Average lifecycle
    current_time = datetime.now()
    df['days_to_expire'] = (df['expire_datetime'] - current_time).dt.days
    avg_lifecycle = df['days_to_expire'].mean()
    
    # Best application timing
    best_timing = "Within first 3-5 days" if avg_lifecycle < 20 else "Within first week" if avg_lifecycle < 30 else "Within first 2 weeks"
    
    return {
        'peak_months': peak_month_names,
        'low_months': low_month_names,
        'avg_lifecycle_days': avg_lifecycle,
        'best_application_timing': best_timing
    }

def analyze_expiry_correlations(df):
    """ExpireAt ile diğer sütunlar arasındaki korelasyonları analiz eder"""
    
    correlations = {}
    
    # Salary correlation (if exists)
    salary_cols = [col for col in df.columns if 'salary' in col.lower() and df[col].dtype in ['int64', 'float64']]
    if salary_cols:
        salary_col = salary_cols[0]
        correlation = df['days_to_expire'].corr(df[salary_col])
        if abs(correlation) > 0.1:
            correlations['Salary vs Expiry'] = {
                'strength': f"{correlation:.3f} ({'Strong' if abs(correlation) > 0.5 else 'Moderate' if abs(correlation) > 0.3 else 'Weak'})",
                'insight': 'Higher salary jobs may have longer posting periods' if correlation > 0 else 'Higher salary jobs may have shorter posting periods',
                'actionable': 'Target high-value positions early' if correlation < 0 else 'Quality positions worth waiting for'
            }
    
    # Company size correlation (if exists)
    if 'company_size_category' in df.columns:
        # Create numeric mapping for analysis
        size_mapping = {'SMALL': 1, 'MEDIUM': 2, 'LARGE': 3, 'ENTERPRISE': 4}
        df['company_size_numeric'] = df['company_size_category'].map(size_mapping)
        correlation = df['days_to_expire'].corr(df['company_size_numeric'])
        if abs(correlation) > 0.1:
            correlations['Company Size vs Expiry'] = {
                'strength': f"{correlation:.3f} ({'Strong' if abs(correlation) > 0.5 else 'Moderate' if abs(correlation) > 0.3 else 'Weak'})",
                'insight': 'Larger companies may have longer hiring processes' if correlation > 0 else 'Larger companies may have faster hiring',
                'actionable': 'Adjust application strategy by company size'
            }
    
    # Experience requirements correlation
    if 'desc_experience_years' in df.columns:
        correlation = df['days_to_expire'].corr(df['desc_experience_years'])
        if abs(correlation) > 0.1:
            correlations['Experience vs Expiry'] = {
                'strength': f"{correlation:.3f} ({'Strong' if abs(correlation) > 0.5 else 'Moderate' if abs(correlation) > 0.3 else 'Weak'})",
                'insight': 'Senior positions may have longer posting periods' if correlation > 0 else 'Senior positions may be filled quickly',
                'actionable': 'Prioritize experience-level appropriate timing'
            }
    
    return correlations

def analyze_investment_vs_expiry(df):
    """Investment type vs expiry patterns analizi"""
    
    if 'job_investment_type' not in df.columns:
        return {}
    
    current_time = datetime.now()
    df['days_to_expire'] = (df['expire_datetime'] - current_time).dt.days
    
    investment_patterns = {}
    
    for inv_type in df['job_investment_type'].unique():
        if pd.isna(inv_type):
            continue
            
        subset = df[df['job_investment_type'] == inv_type]
        avg_days = subset['days_to_expire'].mean()
        count = len(subset)
        percentage = (count / len(df)) * 100
        
        # Determine urgency level
        if avg_days <= 7:
            urgency = "HIGH"
            strategy = "Fast application required"
        elif avg_days <= 21:
            urgency = "MEDIUM"
            strategy = "Standard application timing"
        else:
            urgency = "LOW"
            strategy = "Quality application focus"
        
        investment_patterns[inv_type] = {
            'avg_days': float(avg_days),
            'count': int(count),
            'percentage': float(percentage),
            'urgency_level': urgency,
            'business_strategy': strategy
        }
    
    # Premium intelligence
    premium_types = ['PREMIUM_OFFLINE', 'PREMIUM_ONLINE']
    organic_types = ['ORGANIC']
    
    premium_data = df[df['job_investment_type'].isin(premium_types)]
    organic_data = df[df['job_investment_type'].isin(organic_types)]
    
    if len(premium_data) > 0 and len(organic_data) > 0:
        premium_avg = premium_data['days_to_expire'].mean()
        organic_avg = organic_data['days_to_expire'].mean()
        
        advantage = "Premium jobs stay live longer" if premium_avg > organic_avg else "Organic jobs stay live longer"
        roi_indicator = "High" if abs(premium_avg - organic_avg) > 7 else "Medium" if abs(premium_avg - organic_avg) > 3 else "Low"
        
        investment_patterns['premium_intelligence'] = {
            'premium_avg_days': float(premium_avg),
            'organic_avg_days': float(organic_avg),
            'premium_advantage': advantage,
            'roi_indicator': roi_indicator
        }
    
    return investment_patterns

def generate_predictive_insights(df):
    """Predictive insights oluşturur"""
    
    current_time = datetime.now()
    df['days_to_expire'] = (df['expire_datetime'] - current_time).dt.days
    
    insights = {}
    
    # Job market urgency prediction
    urgent_ratio = len(df[df['days_to_expire'] <= 14]) / len(df)
    if urgent_ratio > 0.3:
        insights['Market Urgency Trend'] = {
            'prediction': 'High urgency job market - fast hiring trends dominant',
            'confidence': 'High' if urgent_ratio > 0.4 else 'Medium',
            'business_value': 'Candidates should apply quickly, employers expect fast responses'
        }
    
    # Application timing optimization
    median_expiry = df['days_to_expire'].median()
    insights['Optimal Application Timing'] = {
        'prediction': f'Apply within first {int(median_expiry/3)} days for best success rate',
        'confidence': 'High',
        'business_value': 'Maximize application success through strategic timing'
    }
    
    # Posting lifecycle prediction
    avg_lifecycle = df['days_to_expire'].mean()
    if avg_lifecycle > 30:
        insights['Posting Lifecycle'] = {
            'prediction': 'Extended posting periods indicate quality-focused hiring',
            'confidence': 'Medium',
            'business_value': 'Focus on application quality over speed'
        }
    
    return insights

def generate_transformation_strategy(df, analysis_results):
    """Transformation strategy oluşturur"""
    
    strategies = []
    
    # Urgency categorization
    strategies.append({
        'title': 'Urgency Intelligence Categories',
        'description': 'Create URGENT/NORMAL/EXTENDED categories based on days to expiry',
        'business_value': 'Enable urgency-based job filtering and application prioritization',
        'implementation': 'Transform expireAt into categorical urgency levels',
        'expected_impact': 'Improved job discovery and application timing optimization'
    })
    
    # Temporal features
    strategies.append({
        'title': 'Temporal Feature Engineering',
        'description': 'Extract month, quarter, and seasonal posting patterns',
        'business_value': 'Seasonal hiring trend analysis and market timing insights',
        'implementation': 'Create derived temporal features from expireAt',
        'expected_impact': 'Market intelligence and seasonal trend identification'
    })
    
    # Application deadline alerts
    strategies.append({
        'title': 'Application Deadline Intelligence',
        'description': 'Convert to days remaining for real-time urgency tracking',
        'business_value': 'Real-time application deadline monitoring and alerts',
        'implementation': 'Create days_remaining calculated field',
        'expected_impact': 'Enhanced user experience and application success rates'
    })
    
    # Memory optimization
    strategies.append({
        'title': 'Memory and Performance Optimization',
        'description': 'Convert to datetime64[ns] and create categorical derivatives',
        'business_value': 'Faster operations and reduced memory footprint',
        'implementation': 'DateTime conversion + categorical encoding',
        'expected_impact': '70%+ memory reduction with enhanced functionality'
    })
    
    return strategies

if __name__ == "__main__":
    try:
        # Load the latest dataset
        print("📂 Dataset yükleniyor...")
        df = pd.read_csv('linkedin_jobs_dataset_with_job_investment_category.csv')
        print(f"✅ Dataset yüklendi: {len(df):,} satır, {len(df.columns)} sütun")
        print()
        
        # Run business intelligence analysis
        result = analyze_expireAt_business_intelligence(df)
        
        if result:
            print(f"\n📊 Business Intelligence Analysis completed successfully!")
            
    except FileNotFoundError:
        print("❌ HATA: linkedin_jobs_dataset_with_job_investment_category.csv dosyası bulunamadı!")
        print("📋 Mevcut CSV dosyalarını kontrol edin.")
    except Exception as e:
        print(f"❌ HATA: {str(e)}") 