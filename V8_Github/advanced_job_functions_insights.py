import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

print("🚀 ADVANCED JOB FUNCTIONS INSIGHTS")
print("="*50)

# Load the transformed dataset
df = pd.read_csv('linkedin_jobs_with_combined_functions.csv')

print("1. DEEPş MÜLTİ-FUNCTION ANALİZİ")
print("-"*40)

# Analyze multi-function patterns in depth
print("🔬 Fonksiyon Kombinasyonu Derinlik Analizi:")

# Function co-occurrence matrix
all_individual_functions = []
for func_string in df['job_functions_combined']:
    if func_string != 'Not Specified':
        functions = [f.strip() for f in func_string.split('|')]
        all_individual_functions.extend(functions)

function_counter = Counter(all_individual_functions)
top_functions = [func for func, count in function_counter.most_common(10)]

# Co-occurrence analysis
cooccurrence_matrix = {}
for func_string in df['job_functions_combined']:
    if func_string != 'Not Specified' and '|' in func_string:
        functions = [f.strip() for f in func_string.split('|')]
        for i, func1 in enumerate(functions):
            for j, func2 in enumerate(functions):
                if i != j and func1 in top_functions and func2 in top_functions:
                    pair = tuple(sorted([func1, func2]))
                    cooccurrence_matrix[pair] = cooccurrence_matrix.get(pair, 0) + 1

print("\n🔗 En güçlü fonksiyon ilişkileri:")
sorted_pairs = sorted(cooccurrence_matrix.items(), key=lambda x: x[1], reverse=True)
for (func1, func2), count in sorted_pairs[:15]:
    total_func1 = function_counter[func1]
    total_func2 = function_counter[func2]
    correlation_strength = count / min(total_func1, total_func2) * 100
    print(f"   {func1} ↔ {func2}: {count} ({correlation_strength:.1f}% bağlantı gücü)")

print("\n2. SEKTÖREL TREND ANALİZİ")
print("-"*40)

# Define industry clusters
industry_clusters = {
    'TECH_ECOSYSTEM': ['Information Technology', 'Engineering', 'Design', 'Product Management'],
    'BUSINESS_GROWTH': ['Business Development', 'Sales', 'Marketing', 'Strategy/Planning'],
    'ANALYTICS_INTELLIGENCE': ['Analyst', 'Research', 'Consulting', 'Finance'],
    'OPERATIONS_MANAGEMENT': ['Project Management', 'Production', 'Supply Chain', 'Quality Assurance'],
    'HUMAN_CENTERED': ['Human Resources', 'Training', 'Customer Service', 'Art/Creative'],
    'SPECIALIZED_PROFESSIONAL': ['Legal', 'Education', 'Writing/Editing', 'General Business']
}

print("🏭 Sektörel Cluster Analizi:")
cluster_stats = {}

for cluster_name, cluster_functions in industry_clusters.items():
    cluster_jobs = df[df['job_functions_combined'].str.contains('|'.join(cluster_functions), na=False)]
    cluster_stats[cluster_name] = {
        'job_count': len(cluster_jobs),
        'percentage': len(cluster_jobs) / len(df) * 100,
        'avg_functions_per_job': cluster_jobs['job_functions_combined'].str.count('\|').mean() + 1
    }
    
    print(f"\n📊 {cluster_name}:")
    print(f"   İş sayısı: {cluster_stats[cluster_name]['job_count']:,}")
    print(f"   Pazar payı: %{cluster_stats[cluster_name]['percentage']:.1f}")
    print(f"   Ortalama fonksiyon/iş: {cluster_stats[cluster_name]['avg_functions_per_job']:.1f}")

print("\n3. HİBRİT POZISYON ANALİZİ")
print("-"*40)

# Analyze hybrid positions
print("🔀 Cross-cluster hibrit pozisyonları:")
cross_cluster_jobs = []

for idx, row in df.iterrows():
    func_string = row['job_functions_combined']
    if func_string != 'Not Specified' and '|' in func_string:
        functions = [f.strip() for f in func_string.split('|')]
        
        # Check which clusters this job spans
        job_clusters = []
        for cluster_name, cluster_functions in industry_clusters.items():
            if any(func in cluster_functions for func in functions):
                job_clusters.append(cluster_name)
        
        if len(job_clusters) > 1:
            cross_cluster_jobs.append({
                'index': idx,
                'functions': func_string,
                'clusters': job_clusters,
                'cluster_count': len(job_clusters)
            })

hybrid_stats = Counter([job['cluster_count'] for job in cross_cluster_jobs])
print(f"Toplam hibrit pozisyon: {len(cross_cluster_jobs):,} (%{len(cross_cluster_jobs)/len(df)*100:.1f})")

for cluster_count, count in sorted(hybrid_stats.items()):
    print(f"   {cluster_count} cluster'a yayılan: {count:,} pozisyon")

# Most common cross-cluster combinations
cluster_combinations = Counter([tuple(sorted(job['clusters'])) for job in cross_cluster_jobs])
print(f"\n🔥 En yaygın cluster kombinasyonları:")
for combo, count in cluster_combinations.most_common(10):
    percentage = count / len(cross_cluster_jobs) * 100
    print(f"   {' + '.join(combo)}: {count} (%{percentage:.1f})")

print("\n4. PAZAR FIRSATLARI VE GELİŞİM TRENDLERİ")
print("-"*40)

# Market gap analysis
print("💎 Pazar Fırsatı Analizi:")

# Underrepresented combinations
all_combinations = []
for func_string in df['job_functions_combined']:
    if func_string != 'Not Specified' and '|' in func_string:
        functions = sorted([f.strip() for f in func_string.split('|')])
        if len(functions) == 2:  # Focus on 2-function combinations
            all_combinations.append(tuple(functions))

combination_counts = Counter(all_combinations)
total_combinations = len(combination_counts)

print(f"Toplam 2-fonksiyon kombinasyonu: {total_combinations}")

# Find underrepresented but potentially valuable combinations
valuable_but_rare = []
for (func1, func2), count in combination_counts.items():
    if count < 20 and count > 2:  # Rare but existing
        func1_popularity = function_counter.get(func1, 0)
        func2_popularity = function_counter.get(func2, 0)
        potential_score = (func1_popularity + func2_popularity) / count
        valuable_but_rare.append({
            'combination': f"{func1} + {func2}",
            'count': count,
            'potential_score': potential_score
        })

valuable_but_rare.sort(key=lambda x: x['potential_score'], reverse=True)

print(f"\n🔍 Düşük rekabet, yüksek potansiyel kombinasyonları:")
for item in valuable_but_rare[:10]:
    print(f"   {item['combination']}: {item['count']} pozisyon (Potansiyel: {item['potential_score']:.1f})")

print("\n5. STRATEJİK YETENEK PROFİLLEME")
print("-"*40)

# Skill demand profiling
print("🎯 Yetenek Profili Talep Analizi:")

# High-demand skill combinations
high_demand_combinations = [combo for combo, count in combination_counts.most_common(20)]

print("En talep edilen ikili beceri setleri:")
for i, (func1, func2) in enumerate(high_demand_combinations[:10], 1):
    count = combination_counts[(func1, func2)]
    print(f"   {i:2d}. {func1} + {func2}: {count} pozisyon")

# Emerging skill patterns
print(f"\n🚀 Gelişen Trend Patterns:")
emerging_patterns = []

# Find combinations involving newer fields
modern_functions = ['Product Management', 'Strategy/Planning', 'Design', 'Art/Creative']
for func_string in df['job_functions_combined']:
    if func_string != 'Not Specified':
        functions = [f.strip() for f in func_string.split('|')]
        modern_count = sum(1 for func in functions if func in modern_functions)
        if modern_count > 0 and len(functions) > 1:
            emerging_patterns.append(func_string)

emerging_counter = Counter(emerging_patterns)
print("Modern skill pattern'ları:")
for pattern, count in emerging_counter.most_common(10):
    print(f"   {pattern}: {count}")

print("\n6. ACTIONABLE BUSINESS INSIGHTları")
print("-"*40)

print("💼 STRATEJİK ÖNERİLER:")

# Calculate market saturation
tech_saturation = (function_counter['Information Technology'] + function_counter['Engineering']) / sum(function_counter.values()) * 100
business_saturation = (function_counter['Business Development'] + function_counter['Sales']) / sum(function_counter.values()) * 100

print(f"\n1. 📈 PAZAR DOYGUNLUK ANALİZİ:")
print(f"   - Teknik roller doygunluk: %{tech_saturation:.1f}")
print(f"   - İş geliştirme doygunluk: %{business_saturation:.1f}")
if tech_saturation > 50:
    print("   ⚠️  Teknik pazar doygun! Hibrit beceriler önerilir.")
if business_saturation < 20:
    print("   ✅ İş geliştirme alanında alan var!")

print(f"\n2. 🎯 HİBRİT FIRKATLARI:")
hybrid_percentage = len(cross_cluster_jobs) / len(df) * 100
print(f"   - Hibrit pozisyon oranı: %{hybrid_percentage:.1f}")
print(f"   - Cross-functional beceri setleri kritik!")
print(f"   - En değerli kombinasyon: TECH + BUSINESS")

print(f"\n3. 💡 NIche FRSATLARI:")
niche_functions = [func for func, count in function_counter.items() if count < 200]
print(f"   - {len(niche_functions)} adet niche alan tespit edildi")
print(f"   - Bu alanlarda uzmanlaşma avantajlı!")
print(f"   - Örnekler: {niche_functions[:5]}")

print(f"\n4. 🚀 GELECEKTREENDLER:")
future_combinations = [
    'Information Technology + Design',
    'Engineering + Business Development',
    'Analyst + Marketing',
    'Product Management + Research'
]
print("   Gelecek trendleri:")
for combo in future_combinations:
    functions = [f.strip() for f in combo.split(' + ')]
    if len(functions) == 2:
        existing = combination_counts.get(tuple(sorted(functions)), 0)
        print(f"   - {combo}: {existing} mevcut pozisyon (Büyüme potansiyeli!)")

print("\n7. YATIRIMÇ KORELASYON ANALİZİ")
print("-"*40)

# Correlation with investment types if available
if 'job_investment_type' in df.columns:
    print("💰 Yatırım Tipi - Fonksiyon Korelasyonu:")
    investment_function_cross = pd.crosstab(df['job_investment_type'], 
                                          df['job_functions_combined'].str.contains('Information Technology|Engineering', na=False))
    print(investment_function_cross)

print("\n" + "="*50)
print("ADVANCED INSIGHTS GENERATION TAMAMLANDI!")
print(f"📊 Analiz edilen toplam pattern: {len(combination_counts):,}")
print(f"🔍 Tespit edilen fırsat alanı: {len(valuable_but_rare)}")
print(f"🚀 Hibrit pozisyon oranı: %{len(cross_cluster_jobs)/len(df)*100:.1f}") 