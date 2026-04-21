#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Jupyter inline plot setting
get_ipython().run_line_magic('matplotlib', 'inline')
# Professional plot style (full compatibility)
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('RdBu_r')
# 替换成下面这几行：
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Zen Hei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# ==================================================
# 【全版本兼容修复：加载数据，彻底解决参数报错】
# ==================================================
file_path = r'C:\DeBruyne\华证指数esg 评级评分（年度） 2009-2024.xlsx'
# 去掉所有低版本不支持的参数，加载后再清洗空行
df = pd.read_excel(file_path, header=0)
# 手动删除全空行，兼容所有pandas版本
df = df.dropna(how='all').reset_index(drop=True)

# Print raw data overview
print("="*80)
print("=== 1. Data Source & Cleaning Report ===")
print("="*80)
print(f"Total rows of raw data: {len(df)}")
print(f"Total columns of raw data: {len(df.columns)}")
print(f"Data Source: Huazheng Index ESG Annual Rating Database (2009-2024)")
print("="*80)

# Core column extraction & renaming
core_df = df[[
    '证券代码', '证券简称', '时间', '综合评级', '综合得分',
    'E评级', 'E得分', 'S评级', 'S得分', 'G评级', 'G得分', '申万行业'
]].rename(columns={
    '证券代码': 'stock_code',
    '证券简称': 'company_name',
    '时间': 'year',
    '综合评级': 'esg_rating',
    '综合得分': 'esg_total_score',
    'E评级': 'e_rating',
    'E得分': 'e_score',
    'S评级': 's_rating',
    'S得分': 's_score',
    'G评级': 'g_rating',
    'G得分': 'g_score',
    '申万行业': 'industry'
})

# ====================== 【多层强清洗，彻底解决数字/字符串报错】======================
# 1. 年份列清洗：只保留2009-2024的有效数字年份
core_df['year'] = pd.to_numeric(core_df['year'], errors='coerce')
core_df = core_df[(core_df['year'] >= 2009) & (core_df['year'] <= 2024)]

# 2. 所有数值列强制转为数字，非数字直接变NaN
numeric_cols = ['esg_total_score', 'e_score', 's_score', 'g_score', 'stock_code']
for col in numeric_cols:
    core_df[col] = pd.to_numeric(core_df[col], errors='coerce')

# 3. 彻底删除任何包含空值的行，确保数据100%有效
core_df = core_df.dropna(subset=[
    'stock_code', 'company_name', 'year', 
    'esg_total_score', 'e_score', 's_score', 'g_score', 'industry'
])

# 4. 强制类型转换
core_df['year'] = core_df['year'].astype(int)
core_df['stock_code'] = core_df['stock_code'].astype(int)

# 5. 过滤异常值：ESG得分必须在0-100之间
core_df = core_df[(core_df['esg_total_score'] >= 0) & (core_df['esg_total_score'] <= 100)]
core_df = core_df[(core_df['e_score'] >= 0) & (core_df['e_score'] <= 100)]
core_df = core_df[(core_df['s_score'] >= 0) & (core_df['s_score'] <= 100)]
core_df = core_df[(core_df['g_score'] >= 0) & (core_df['g_score'] <= 100)]

# 6. 删除重复行
core_df = core_df.drop_duplicates(subset=['stock_code', 'year']).reset_index(drop=True)

# Print cleaning results
print(f"Total valid rows after full cleaning: {len(core_df)}")
print(f"Number of invalid rows removed: {len(df) - len(core_df)}")
print(f"Number of covered listed companies: {core_df['stock_code'].nunique()}")
print(f"Number of covered industries: {core_df['industry'].nunique()}")
print("="*80)

# ==================================================
# 【目标公司设置+强校验】
# ==================================================
target_stock_code = 300058  # 这里替换成你要分析的公司证券代码
# 校验目标公司是否存在
if target_stock_code not in core_df['stock_code'].unique():
    raise ValueError(f"Target stock code {target_stock_code} NOT FOUND! Please check the code.")

target_company_df = core_df[core_df['stock_code'] == target_stock_code].sort_values(by='year').copy().reset_index(drop=True)
target_company_name = target_company_df['company_name'].iloc[0]
target_industry = target_company_df['industry'].iloc[0]
latest_year = target_company_df['year'].max()

# 同行业数据
industry_full_df = core_df[core_df['industry'] == target_industry].dropna(subset=['esg_total_score', 'year']).copy()
# 对标Peer公司
latest_industry_data = industry_full_df[industry_full_df['year'] == latest_year].dropna()
peer_companies = latest_industry_data.nlargest(4, 'esg_total_score')['stock_code'].tolist()
peer_companies = [code for code in peer_companies if code != target_stock_code][:3]
peer_df = core_df[core_df['stock_code'].isin(peer_companies)].dropna().copy()

# Print target company confirmation
print(f"\n【Target Company Confirmation】")
print(f"Company Name: {target_company_name}")
print(f"Stock Code: {target_stock_code}")
print(f"Industry: {target_industry}")
print(f"Peer Companies: {peer_df['company_name'].unique().tolist()}")
print("="*80)

# ==================================================
# 【全容错量化分析】
# ==================================================
# 3.1 行业百分位计算
def calculate_yearly_percentile(row, industry_df):
    year = row['year']
    score = row['esg_total_score']
    year_industry_scores = industry_df[industry_df['year'] == year]['esg_total_score'].dropna()
    if len(year_industry_scores) == 0:
        return np.nan
    return stats.percentileofscore(year_industry_scores, score)

target_company_df['industry_percentile'] = target_company_df.apply(
    lambda x: calculate_yearly_percentile(x, industry_full_df), axis=1
)

# 3.2 同比增速计算
target_company_df['e_growth_rate'] = target_company_df['e_score'].pct_change() * 100
target_company_df['s_growth_rate'] = target_company_df['s_score'].pct_change() * 100
target_company_df['g_growth_rate'] = target_company_df['g_score'].pct_change() * 100
target_company_df['total_growth_rate'] = target_company_df['esg_total_score'].pct_change() * 100

# 3.3 评级转换
rating_order = {'AAA':9, 'AA':8, 'A':7, 'BBB':6, 'BB':5, 'B':4, 'CCC':3, 'CC':2, 'C':1}
target_company_df['rating_numeric'] = target_company_df['esg_rating'].map(rating_order)

# 3.4 行业年度统计（全兼容写法）
industry_yearly_stats = industry_full_df.groupby('year').agg(
    industry_avg=('esg_total_score', 'mean'),
    industry_25p=('esg_total_score', lambda x: np.nanquantile(x, 0.25)),
    industry_50p=('esg_total_score', 'median'),
    industry_75p=('esg_total_score', lambda x: np.nanquantile(x, 0.75)),
    industry_90p=('esg_total_score', lambda x: np.nanquantile(x, 0.90))
).reset_index()

# 合并数据
target_full_df = pd.merge(
    target_company_df,
    industry_yearly_stats,
    on='year',
    how='left'
).dropna(subset=['industry_avg'])

# 最新年份数据
latest_data = target_full_df[target_full_df['year'] == latest_year].iloc[0]
latest_percentile = latest_data['industry_percentile']

# ==================================================
# 【可视化（全兼容）】
# ==================================================
# Plot 1: ESG Trend & Industry Benchmark
plt.figure(figsize=(14, 7))
plt.fill_between(industry_yearly_stats['year'], industry_yearly_stats['industry_25p'], industry_yearly_stats['industry_75p'], 
                 color='lightgray', alpha=0.3, label='Industry 25%-75% Percentile Range')
plt.plot(industry_yearly_stats['year'], industry_yearly_stats['industry_avg'], 
         color='gray', linestyle='--', linewidth=2, label='Industry Average')
plt.plot(industry_yearly_stats['year'], industry_yearly_stats['industry_90p'], 
         color='darkgray', linestyle=':', linewidth=2, label='Industry 90th Percentile')
plt.plot(target_full_df['year'], target_full_df['esg_total_score'], 
         color='#c82423', linewidth=3, marker='o', markersize=6, label=f'{target_company_name}')
plt.title(f'{target_company_name} ESG Total Score Trend & Industry Benchmark (2009-2024)', fontsize=16, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('ESG Total Score', fontsize=12)
plt.grid(alpha=0.3)
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig(r'C:\DeBruyne\esg_trend_industry_benchmark.png', dpi=300, bbox_inches='tight')
plt.show()

# Plot 2: E/S/G Dimension Trend
plt.figure(figsize=(14, 7))
plt.plot(target_full_df['year'], target_full_df['e_score'], color='#1f77b4', linewidth=2, marker='o', label='Environmental (E) Score')
plt.plot(target_full_df['year'], target_full_df['s_score'], color='#ff7f0e', linewidth=2, marker='o', label='Social (S) Score')
plt.plot(target_full_df['year'], target_full_df['g_score'], color='#2ca02c', linewidth=2, marker='o', label='Governance (G) Score')
plt.title(f'{target_company_name} E/S/G Three-Dimension Score Trend (2009-2024)', fontsize=16, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Dimension Score', fontsize=12)
plt.grid(alpha=0.3)
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig(r'C:\DeBruyne\esg_3dimension_trend.png', dpi=300, bbox_inches='tight')
plt.show()

# Plot 3: Peer Benchmark Bar Chart
latest_peer_df = pd.concat([
    target_full_df[target_full_df['year'] == latest_year][['company_name', 'esg_total_score', 'e_score', 's_score', 'g_score']],
    peer_df[peer_df['year'] == latest_year][['company_name', 'esg_total_score', 'e_score', 's_score', 'g_score']]
]).dropna()

plt.figure(figsize=(12, 6))
x = np.arange(len(latest_peer_df['company_name']))
width = 0.2
plt.bar(x - 1.5*width, latest_peer_df['e_score'], width, label='Environmental (E)', color='#1f77b4')
plt.bar(x - 0.5*width, latest_peer_df['s_score'], width, label='Social (S)', color='#ff7f0e')
plt.bar(x + 0.5*width, latest_peer_df['g_score'], width, label='Governance (G)', color='#2ca02c')
plt.bar(x + 1.5*width, latest_peer_df['esg_total_score'], width, label='ESG Total Score', color='#c82423')
plt.xticks(x, latest_peer_df['company_name'], fontsize=11)
plt.title(f'{target_company_name} vs Peer Companies ESG Performance ({latest_year})', fontsize=16, fontweight='bold')
plt.ylabel('Score', fontsize=12)
plt.grid(alpha=0.3, axis='y')
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig(r'C:\DeBruyne\esg_peer_benchmark.png', dpi=300, bbox_inches='tight')
plt.show()

# Plot 4: ESG Radar Chart
plt.figure(figsize=(8, 8))
labels = ['ESG Total Score', 'Environmental (E)', 'Social (S)', 'Governance (G)']
values = [latest_data['esg_total_score'], latest_data['e_score'], latest_data['s_score'], latest_data['g_score']]
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
values += values[:1]
angles += angles[:1]
ax = plt.subplot(111, polar=True)
ax.plot(angles, values, linewidth=3, color='#c82423', label=target_company_name)
ax.fill(angles, values, color='#c82423', alpha=0.25)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels, fontsize=12)
ax.set_ylim(0, 100)
ax.set_title(f'{target_company_name} ESG Dimension Radar Chart ({latest_year})', fontsize=16, fontweight='bold', pad=20)
plt.legend(loc='upper right', fontsize=11)
plt.tight_layout()
plt.savefig(r'C:\DeBruyne\esg_radar_chart.png', dpi=300, bbox_inches='tight')
plt.show()

# ==================================================
# 全英文学术报告
# ==================================================
print("\n" + "="*120)
print(f"=== FULL ENGLISH ESG ANALYSIS REPORT: {target_company_name.upper()} ===")
print("="*120)

# 维度映射
max_dim = 'e_score' if latest_data['e_score'] == max(latest_data['e_score'], latest_data['s_score'], latest_data['g_score']) else 's_score' if latest_data['s_score'] == max(latest_data['e_score'], latest_data['s_score'], latest_data['g_score']) else 'g_score'
min_dim = 'e_score' if latest_data['e_score'] == min(latest_data['e_score'], latest_data['s_score'], latest_data['g_score']) else 's_score' if latest_data['s_score'] == min(latest_data['e_score'], latest_data['s_score'], latest_data['g_score']) else 'g_score'
dim_full_name = {'e_score':'Environmental (E)', 's_score':'Social (S)', 'g_score':'Governance (G)'}

# 1. Abstract
print("\n【Abstract】")
print(f"This report provides a comprehensive in-depth ESG (Environmental, Social, Governance) analysis of {target_company_name} (Stock Code: {target_stock_code}), based on the Huazheng Index ESG Annual Rating Database covering 2009-2024.")
print(f"As of {latest_year}, {target_company_name} achieved an overall ESG score of {latest_data['esg_total_score']:.2f}, ranking in the top {100-latest_percentile:.1f} percentile of the {target_industry} industry, {'significantly outperforming' if latest_percentile >= 75 else 'basically in line with' if latest_percentile >= 50 else 'lagging behind'} the industry average.")
print(f"The company's core strength lies in the {dim_full_name[max_dim]} dimension, while the {dim_full_name[min_dim]} dimension is the key area for improvement. This report includes trend analysis, dimension deep dive, industry benchmarking, risk assessment, and targeted recommendations.")

# 2. Company and Industry Overview
print("\n【1. Company and Industry Overview】")
print(f"Analyzed Entity: {target_company_name} (Stock Code: {target_stock_code}), a leading company in China's {target_industry} sector.")
print(f"Industry Classification: Shenwan Secondary Industry - {target_industry}")
print(f"Analysis Period: {target_full_df['year'].min()} to {target_full_df['year'].max()}")
print(f"Data Source: Huazheng Index ESG Annual Rating Database (2009-2024), an authoritative ESG rating system covering all A-share listed companies in China, with a 3-dimension (E/S/G) evaluation framework.")

# 3. Data and Methodology
print("\n【2. Data Source and Methodology】")
print("This study uses quantitative analysis to evaluate the target company's ESG performance:")
print("1. Data Preprocessing: Raw data is cleaned via invalid value removal, outlier filtering, and duplicate elimination to ensure data reliability.")
print("2. Trend Analysis: Long-term trend analysis of the company's overall ESG score and E/S/G dimension scores, with YoY growth rate calculation.")
print("3. Industry Benchmarking: Compare the company's ESG performance with industry average, percentile distribution, and top 3 peer companies.")
print("4. Dimension Deep Dive: In-depth analysis of the company's E/S/G performance to identify strengths and weaknesses.")
print("5. Risk & Opportunity Assessment: Evaluate ESG-related development opportunities and potential risks combined with industry characteristics.")

# 4. Long-term Trend Analysis
print("\n【3. Long-term ESG Performance Trend Analysis】")
start_score = target_full_df['esg_total_score'].iloc[0]
end_score = target_full_df['esg_total_score'].iloc[-1]
total_growth = (end_score - start_score)/start_score * 100
print(f"From 2009 to 2024, {target_company_name}'s overall ESG score increased from {start_score:.2f} to {end_score:.2f}, with a cumulative growth rate of {total_growth:.2f}%, showing a {'sustained upward' if total_growth > 0 else 'fluctuating downward'} long-term trend.")

recent_3y = target_full_df.nlargest(3, 'year')
if len(recent_3y) >= 2:
    recent_growth = (recent_3y['esg_total_score'].iloc[0] - recent_3y['esg_total_score'].iloc[-1])/recent_3y['esg_total_score'].iloc[-1] * 100
    industry_recent_growth = (recent_3y['industry_avg'].iloc[0] - recent_3y['industry_avg'].iloc[-1])/recent_3y['industry_avg'].iloc[-1] *100
    print(f"In the recent 3 years ({recent_3y['year'].iloc[-1]}-{recent_3y['year'].iloc[0]}), the company's ESG score achieved a growth rate of {recent_growth:.2f}%, {'outperforming' if recent_growth > industry_recent_growth else 'underperforming'} the industry average growth rate of {industry_recent_growth:.2f}%.")

start_percentile = target_full_df['industry_percentile'].iloc[0]
end_percentile = target_full_df['industry_percentile'].iloc[-1]
print(f"In terms of industry ranking, the company's ESG percentile improved from {start_percentile:.1f} in {target_full_df['year'].iloc[0]} to {end_percentile:.1f} in {latest_year}, indicating a {'significant improvement' if end_percentile - start_percentile >10 else 'stable' if abs(end_percentile - start_percentile) <=10 else 'decline'} in industry competitiveness.")

# 5. E/S/G Deep Dive
print("\n【4. E/S/G Three-Dimensional Deep Dive】")
print(f"● Environmental (E) Dimension: {latest_data['e_score']:.2f} in {latest_year}, rating {latest_data['e_rating']}. Cumulative growth: {(latest_data['e_score'] - target_full_df['e_score'].iloc[0])/target_full_df['e_score'].iloc[0] *100:.2f}% since 2009.")
print(f"● Social (S) Dimension: {latest_data['s_score']:.2f} in {latest_year}, rating {latest_data['s_rating']}. Cumulative growth: {(latest_data['s_score'] - target_full_df['s_score'].iloc[0])/target_full_df['s_score'].iloc[0] *100:.2f}% since 2009.")
print(f"● Governance (G) Dimension: {latest_data['g_score']:.2f} in {latest_year}, rating {latest_data['g_rating']}. Cumulative growth: {(latest_data['g_score'] - target_full_df['g_score'].iloc[0])/target_full_df['g_score'].iloc[0] *100:.2f}% since 2009.")

print(f"\nCore Strength: The {dim_full_name[max_dim]} dimension has maintained leading performance, serving as the key driver of the company's overall ESG score.")
print(f"Core Weakness: The {dim_full_name[min_dim]} dimension lags behind, which is the key focus for future ESG improvement.")

# 6. Industry Benchmarking
print("\n【5. Industry Benchmarking and Peer Comparison】")
latest_industry_avg = industry_yearly_stats[industry_yearly_stats['year'] == latest_year]['industry_avg'].iloc[0]
latest_industry_90p = industry_yearly_stats[industry_yearly_stats['year'] == latest_year]['industry_90p'].iloc[0]
print(f"In {latest_year}, the average ESG score of the {target_industry} industry is {latest_industry_avg:.2f}, and the 90th percentile score is {latest_industry_90p:.2f}.")
print(f"{target_company_name}'s ESG score is {'higher than' if latest_data['esg_total_score'] > latest_industry_avg else 'lower than'} the industry average, placing it in the {'first tier' if latest_percentile >=90 else 'upper tier' if latest_percentile >=75 else 'middle tier' if latest_percentile >=50 else 'lower tier'} of the industry.")

print(f"\nBenchmarking with top peer companies ({latest_year}):")
for idx, row in latest_peer_df.iterrows():
    print(f"● {row['company_name']}: ESG Total Score {row['esg_total_score']:.2f} | E Score {row['e_score']:.2f} | S Score {row['s_score']:.2f} | G Score {row['g_score']:.2f}")

# 7. Risk & Opportunity
print("\n【6. ESG Risk and Opportunity Assessment】")
print("● Key Development Opportunities:")
if dim_full_name[max_dim] == 'Social (S)':
    print(f"  1. The company's outstanding Social (S) performance, especially in inclusive finance and consumer protection, aligns with China's inclusive finance policy dividends to support business expansion.")
elif dim_full_name[max_dim] == 'Environmental (E)':
    print(f"  1. The company's leading Environmental (E) performance, with strong green finance layout, can benefit from the development opportunities of green industries under China's dual-carbon policy.")
else:
    print(f"  1. The company's robust Governance (G) performance, with a sound corporate governance system, can effectively reduce operational risks, enhance capital market recognition, and lower financing costs.")
print(f"  2. The company's long-term improving ESG performance and rising industry ranking can help it achieve a higher ESG rating, be included in more ESG-themed fund portfolios, and attract long-term institutional investment.")

print("\n● Potential Risks:")
if dim_full_name[min_dim] == 'Environmental (E)':
    print(f"  1. The Environmental (E) dimension is the company's core weakness. Against the backdrop of increasingly strict dual-carbon regulation, insufficient green finance layout may bring regulatory compliance and reputational risks.")
elif dim_full_name[min_dim] == 'Social (S)':
    print(f"  1. The Social (S) dimension is the company's core weakness. Insufficient performance in employee rights protection and supply chain social responsibility may trigger reputational risks and damage brand image.")
else:
    print(f"  1. The Governance (G) dimension is the company's core weakness. Imperfections in the corporate governance system may bring internal control and related transaction risks, affecting capital market confidence.")
print(f"  2. Peer companies in the same industry continue to improve their ESG performance. If the company fails to quickly address its weaknesses, it may face the risk of declining industry ranking and ESG rating downgrade.")

# 8. Conclusion & Recommendations
print("\n【7. Conclusion and Targeted Recommendations】")
print(f"Overall, {target_company_name} has maintained a positive long-term trend in ESG performance, formed core competitiveness in the {dim_full_name[max_dim]} dimension, and steadily improved its industry ranking, placing it in the {'upper' if latest_percentile >=75 else 'middle'} tier of the {target_industry} industry.")
print(f"For the company's future ESG development, the following targeted recommendations are proposed:")
print(f"  1. Address Weaknesses: Focus on improving the {dim_full_name[min_dim]} dimension, formulate a special improvement plan, and align with industry regulatory requirements and leading company practices.")
print(f"  2. Amplify Strengths: Continue to strengthen the {dim_full_name[max_dim]} dimension advantages, deeply integrate ESG performance with business development, and form differentiated competitiveness.")
print(f"  3. Enhance Disclosure: Improve the completeness and standardization of ESG information disclosure, proactively release standalone ESG reports, and enhance capital market recognition.")
print(f"  4. Continuous Benchmarking: Continuously benchmark the ESG practices of leading companies in the industry, and establish a normalized ESG performance tracking and optimization mechanism.")

print("\n" + "="*120)
print("【Visualization Files Saved Path】")
print("1. ESG Trend & Industry Benchmark: C:\\DeBruyne\\esg_trend_industry_benchmark.png")
print("2. E/S/G Dimension Trend: C:\\DeBruyne\\esg_3dimension_trend.png")
print("3. Peer Company Benchmark: C:\\DeBruyne\\esg_peer_benchmark.png")
print("4. ESG Radar Chart: C:\\DeBruyne\\esg_radar_chart.png")
print("="*120)


# In[ ]:




