#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Jobs Dataset - contentSource Business Insight Analysis
ContentSource sütununun business anlamı ve insight potansiyeli analizi
"""

import pandas as pd
import numpy as np
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

def analyze_contentSource_business_insights(df):
    """contentSource sütununun business meaning ve insight analizi"""
    
    print("💼 CONTENTSOURCE - BUSINESS MEANING & INSIGHT ANALYSIS")
    print("=" * 65)
    
    column_name = 'contentSource'
    
    if column_name not in df.columns:
        print(f"❌ HATA: {column_name} sütunu bulunamadı!")
        return None
    
    # 1. BUSINESS MEANING ANALİZİ
    print("🎯 1. CONTENTSOURCE NEYİ TEMSİL EDİYOR?")
    print("-" * 45)
    
    print("📋 LinkedIn Job Posting Pipeline Classification:")
    print()
    
    business_meanings = {
        'JOBS_PREMIUM_OFFLINE': {
            'meaning': 'Premium İş İlanları (Offline İşlenmiş)',
            'description': 'Şirketlerin ücretli olarak yayınladığı, LinkedIn tarafından offline sistemde işlenmiş premium iş ilanları',
            'quality_indicator': 'YÜKSEK - Ücretli ilan, daha detaylı bilgi',
            'company_investment': 'Ücretli ilan - şirket para ödemiş',
            'visibility': 'Yüksek görünürlük, öncelikli gösterim'
        },
        'JOBS_PREMIUM': {
            'meaning': 'Premium İş İlanları (Online İşlenmiş)', 
            'description': 'Şirketlerin ücretli olarak yayınladığı, LinkedIn tarafından online sistemde işlenmiş premium iş ilanları',
            'quality_indicator': 'YÜKSEK - Ücretli ilan, gerçek zamanlı işlenmiş',
            'company_investment': 'Ücretli ilan - şirket para ödemiş',
            'visibility': 'Yüksek görünürlük, gerçek zamanlı'
        },
        'JOBS_CREATE': {
            'meaning': 'Doğrudan Oluşturulan İş İlanları',
            'description': 'LinkedIn kullanıcıları tarafından doğrudan oluşturulan, ücretsiz veya basic düzeyde iş ilanları',
            'quality_indicator': 'STANDART - Ücretsiz/temel ilan',
            'company_investment': 'Düşük/yok - ücretsiz ilan',
            'visibility': 'Normal görünürlük'
        }
    }
    
    value_counts = df[column_name].value_counts()
    
    for value, count in value_counts.items():
        if value in business_meanings:
            info = business_meanings[value]
            percentage = (count / len(df)) * 100
            print(f"🏷️ {value} ({count:,} ilan - {percentage:.1f}%):")
            print(f"   📝 Anlam: {info['meaning']}")
            print(f"   💼 Açıklama: {info['description']}")
            print(f"   🎯 Kalite: {info['quality_indicator']}")
            print(f"   💰 Yatırım: {info['company_investment']}")
            print(f"   👁️ Görünürlük: {info['visibility']}")
            print()
    
    # 2. BUSİNESS INSIGHT POTANSİYELİ
    print("💡 2. BUSİNESS INSIGHT POTANSİYELİ")
    print("-" * 35)
    
    insights = []
    
    # Company investment pattern analysis
    premium_total = value_counts.get('JOBS_PREMIUM_OFFLINE', 0) + value_counts.get('JOBS_PREMIUM', 0)
    create_total = value_counts.get('JOBS_CREATE', 0)
    premium_percentage = (premium_total / len(df)) * 100
    create_percentage = (create_total / len(df)) * 100
    
    print(f"📊 Premium vs Basic Job Distribution:")
    print(f"   💰 Premium İlanlar: {premium_total:,} ({premium_percentage:.1f}%)")
    print(f"   🆓 Basic İlanlar: {create_total:,} ({create_percentage:.1f}%)")
    print()
    
    if premium_percentage > 80:
        insights.append("🎯 Premium-dominant market: Şirketler LinkedIn'de aktif olarak ücretli ilan kullanıyor")
    elif create_percentage > 50:
        insights.append("🎯 Cost-conscious market: Şirketler daha çok ücretsiz ilanları tercih ediyor")
    else:
        insights.append("🎯 Balanced market: Premium ve basic ilan kullanımı dengeli")
    
    # 3. CROSS-COLUMN INSIGHT POTENTIAL
    print("🔍 3. DİĞER SÜTUNLARLA İNSIGHT POTANSİYELİ")
    print("-" * 40)
    
    potential_correlations = []
    
    # Check salary correlation potential
    if 'salary/max' in df.columns:
        print("💰 Salary Analysis Potential:")
        print("   🎯 Premium ilanların maaş ortalaması daha yüksek mi?")
        print("   📊 JOBS_PREMIUM vs JOBS_CREATE maaş karşılaştırması")
        potential_correlations.append("salary_correlation")
    
    # Check company size correlation
    if 'company_size_category' in df.columns:
        print("🏢 Company Size Analysis Potential:")
        print("   🎯 Büyük şirketler daha çok premium ilan kullanıyor mu?")
        print("   📊 Company size vs content source distribution")
        potential_correlations.append("company_size_correlation")
    
    # Check experience level correlation
    if 'formattedExperienceLevel' in df.columns:
        print("👨‍💼 Experience Level Analysis Potential:")
        print("   🎯 Senior pozisyonlar daha çok premium'da mı?")
        print("   📊 Experience level vs premium content relationship")
        potential_correlations.append("experience_correlation")
    
    # Check industry correlation
    if 'formattedIndustries/0' in df.columns:
        print("🏭 Industry Analysis Potential:")
        print("   🎯 Hangi sektörler daha çok premium ilan kullanıyor?")
        print("   📊 Industry vs premium content distribution")
        potential_correlations.append("industry_correlation")
    
    print()
    
    # 4. PRACTICAL BUSINESS QUESTIONS
    print("❓ 4. BU SÜTUNLA CEVAPLANA BİLECEK İŞ SORULARI")
    print("-" * 50)
    
    business_questions = [
        "💰 Premium ilan veren şirketlerin maaş teklifleri daha yüksek mi?",
        "🎯 Hangi sektörler LinkedIn'de en çok premium ilan kullanıyor?",
        "📈 Premium ilanların başvuru oranları daha yüksek mi?",
        "🏢 Büyük şirketler küçük şirketlere göre daha mı çok premium kullanıyor?",
        "👨‍💼 Senior seviye pozisyonlar daha çok premium'da mı yayınlanıyor?",
        "⏰ Premium ilanların süresi daha mı uzun?",
        "🌍 Hangi lokasyonlarda premium ilan kullanımı daha yaygın?",
        "📊 Premium ilanların detay seviyesi (açıklama uzunluğu) daha mı fazla?"
    ]
    
    for i, question in enumerate(business_questions, 1):
        print(f"   {i}. {question}")
    print()
    
    # 5. INSIGHT VALUE ASSESSMENT
    print("🎯 5. INSIGHT VALUE ASSESSMENT")
    print("-" * 30)
    
    print("✅ YÜKSEK VALUE INSIGHTS:")
    print("   💰 Premium ilan analizi: Hangi şirketler ne kadar yatırım yapıyor?")
    print("   📊 Market segmentasyonu: Premium vs basic ilan kullanım patterns")
    print("   🎯 Job quality assessment: Premium ilanların kalite farkı")
    print("   💼 Company behavior analysis: Şirket ilan stratejileri")
    print()
    
    print("📈 POTENTIAL CORRELATIONS:")
    for correlation in potential_correlations:
        if correlation == "salary_correlation":
            print("   💰 Salary-Premium Correlation: Premium ilanlar = daha yüksek maaş?")
        elif correlation == "company_size_correlation":
            print("   🏢 Company Size-Premium: Büyük şirket = premium kullanımı?")
        elif correlation == "experience_correlation":
            print("   👨‍💼 Experience-Premium: Senior pozisyon = premium ilan?")
        elif correlation == "industry_correlation":
            print("   🏭 Industry-Premium: Hangi sektör premium kullanıyor?")
    print()
    
    # 6. ACTIONABLE INSIGHTS
    print("🚀 6. ACTIONABLE INSIGHTS")
    print("-" * 25)
    
    actionable_insights = []
    
    if premium_percentage > 70:
        actionable_insights.append("💡 Premium market opportunity: Bu dataset'te şirketler premium ilan kullanmaya istekli")
    
    if create_percentage > 30:
        actionable_insights.append("💡 Cost-effective opportunity: Önemli bir kesim ücretsiz ilan kullanıyor")
    
    actionable_insights.extend([
        "📊 Premium pricing strategy: Premium ilan kullanan şirketlerin maaş tekliflerini analiz et",
        "🎯 Market segmentation: Premium vs basic kullanıcı şirketleri segment et",
        "💼 Sales strategy: Hangi şirket tiplerini premium'a yönlendirmek mantıklı?",
        "📈 Product development: Premium özelliklerin değerini ölç"
    ])
    
    for i, insight in enumerate(actionable_insights, 1):
        print(f"   {i}. {insight}")
    print()
    
    # 7. SÜTUN VALUE RECOMMENDATION
    print("🏆 7. FINAL RECOMMENDATION")
    print("-" * 25)
    
    insight_score = 0
    
    # Business value scoring
    if len(potential_correlations) > 0: insight_score += 25
    if premium_percentage > 20 and premium_percentage < 80: insight_score += 25  # Good variance
    if len(business_questions) > 5: insight_score += 20
    insight_score += 30  # Base business value
    
    print(f"📊 Business Insight Score: {insight_score}/100")
    
    if insight_score >= 80:
        recommendation = "KEEP & ANALYZE - High business value"
        action = "Cross-column analysis yaparak insights çıkar"
    elif insight_score >= 60:
        recommendation = "KEEP - Moderate business value"
        action = "Category type conversion + basic insights"
    elif insight_score >= 40:
        recommendation = "CONSIDER - Limited business value"
        action = "Evaluate cost vs benefit"
    else:
        recommendation = "LOW VALUE - Consider deletion"
        action = "Remove unless specific use case"
    
    print(f"🎯 Recommendation: {recommendation}")
    print(f"💡 Action: {action}")
    print()
    
    return {
        'insight_score': insight_score,
        'recommendation': recommendation,
        'action': action,
        'potential_correlations': potential_correlations,
        'business_questions': business_questions,
        'premium_percentage': premium_percentage,
        'create_percentage': create_percentage
    }

if __name__ == "__main__":
    try:
        print("📂 Dataset yükleniyor...")
        df = pd.read_csv('linkedin_jobs_dataset_insights_completed.csv')
        print(f"✅ Dataset yüklendi: {len(df):,} kayıt, {len(df.columns)} sütun")
        print()
        
        result = analyze_contentSource_business_insights(df)
        
        if result:
            print("✅ Business insight analizi tamamlandı!")
        else:
            print("❌ Analiz başarısız!")
            
    except Exception as e:
        print(f"❌ HATA: {str(e)}") 