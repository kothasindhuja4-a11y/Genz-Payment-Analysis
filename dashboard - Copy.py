"""
Quick Payment Analysis Dashboard - Works with sample data
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os
import json

# Load data
import os
script_dir = os.getcwd()  # Use current directory
data_path = os.path.join(script_dir, "data", "processed", "payment_data_clean.csv")

if not os.path.exists(data_path):
    print(f"❌ Error: Data not found at {data_path}")
    print("Run: python validate_data.py data/raw/sample_survey_responses.csv")
    print("Or replace the raw dataset and validate it with validate_data.py")
    exit(1)


def add_sample_data_disclaimer(fig):
    disclaimer = "⚠️ Synthetic sample data only — current results are based on generated sample data and are not real findings."
    title_text = fig.layout.title.text if fig.layout.title and fig.layout.title.text else ''
    fig.update_layout(
        title={'text': f"{title_text}<br><sup>{disclaimer}</sup>"},
        margin=dict(b=120),
    )
    annotations = list(fig.layout.annotations) if fig.layout.annotations else []
    annotations.append({
        'text': disclaimer,
        'xref': 'paper',
        'yref': 'paper',
        'x': 0.5,
        'y': -0.15,
        'showarrow': False,
        'font': {'size': 10, 'color': 'red'},
        'align': 'center',
    })
    fig.update_layout(annotations=annotations)


df = pd.read_csv(data_path)
output_dir = os.path.join(script_dir, "visualizations")
os.makedirs(output_dir, exist_ok=True)

print("\n" + "="*80)
print("📊 GEN Z PAYMENT ANALYSIS - CREATING INTERACTIVE DASHBOARD")
print("⚠️ Note: current results are based on synthetic sample data and not final survey findings.")
print("="*80)

# 1. GENERATION DISTRIBUTION
print("\n✓ Creating: Generation Distribution...")
fig1 = px.pie(
    df['generation'].value_counts().reset_index(),
    values='count', names='generation',
    title='📊 Respondents by Generation'
)
add_sample_data_disclaimer(fig1)
fig1.write_html(f"{output_dir}/01_generation_distribution.html")

# 2. PAYMENT METHOD FREQUENCY
print("✓ Creating: Payment Methods...")
payment_cols = [col for col in df.columns if 'frequency' in col and 'importance' not in col]
payment_data = []
for col in payment_cols:
    method = col.replace('_frequency', '').replace('_', ' ').title()
    payment_data.append({'Method': method, 'Frequency': df[col].mean()})

payment_df = pd.DataFrame(payment_data).sort_values('Frequency')
fig2 = px.bar(payment_df, x='Frequency', y='Method', orientation='h',
               title='💳 Average Payment Method Frequency (1-5 scale)',
               color='Frequency', color_continuous_scale='Blues')
add_sample_data_disclaimer(fig2)
fig2.write_html(f"{output_dir}/02_payment_methods.html")

# 3. FEATURE IMPORTANCE
print("✓ Creating: Feature Importance...")
feature_cols = [col for col in df.columns if 'importance' in col]
feature_data = []
for col in feature_cols:
    feature = col.replace('_importance', '').replace('_', ' ').title()
    feature_data.append({'Feature': feature, 'Score': df[col].mean()})

feature_df = pd.DataFrame(feature_data).sort_values('Score')
fig3 = px.bar(feature_df, x='Score', y='Feature', orientation='h',
               title='⭐ Feature Importance (1-5 scale)',
               color='Score', color_continuous_scale='Greens')
add_sample_data_disclaimer(fig3)
fig3.write_html(f"{output_dir}/03_feature_importance.html")

# 4. SATISFACTION BY GENERATION
print("✓ Creating: Satisfaction by Generation...")
gen_data = df.groupby('generation')[['payment_satisfaction', 'trust_score']].mean().reset_index()
fig4 = go.Figure()
fig4.add_trace(go.Bar(x=gen_data['generation'], y=gen_data['payment_satisfaction'], 
                      name='Payment Satisfaction', marker_color='lightblue'))
fig4.add_trace(go.Bar(x=gen_data['generation'], y=gen_data['trust_score'], 
                      name='Trust Score', marker_color='lightcoral'))
fig4.update_layout(title='😊 Satisfaction & Trust by Generation',
                   xaxis_title='Generation', yaxis_title='Score (1-5)',
                   barmode='group', hovermode='x unified')
add_sample_data_disclaimer(fig4)
fig4.write_html(f"{output_dir}/04_satisfaction_by_generation.html")

# 5. BNPL ADOPTION
print("✓ Creating: BNPL Adoption...")
bnpl_counts = df['bnpl_user'].value_counts()
fig5 = px.pie(
    values=bnpl_counts.values, names=bnpl_counts.index,
    title=f'🛍️ BNPL (Buy Now Pay Later) Adoption<br><sub>{(bnpl_counts["Yes"]/len(df)*100):.1f}% of users</sub>',
    color_discrete_map={'Yes': '#3498db', 'No': '#ecf0f1'}
)
add_sample_data_disclaimer(fig5)
fig5.write_html(f"{output_dir}/05_bnpl_adoption.html")

# 6. INCOME VS SATISFACTION
print("✓ Creating: Income vs Satisfaction...")
income_order = ['<$25k', '$25k-$50k', '$50k-$100k', '$100k-$250k', '>$250k']
income_sat = df.groupby('income_level')['payment_satisfaction'].mean().reindex(income_order)
fig6 = px.bar(x=income_sat.index, y=income_sat.values,
              title='💰 Payment Satisfaction by Income Level',
              labels={'x': 'Income Level', 'y': 'Average Satisfaction (1-5)'},
              color=income_sat.values, color_continuous_scale='Oranges')
fig6.update_xaxes(tickangle=-45)
add_sample_data_disclaimer(fig6)
fig6.write_html(f"{output_dir}/06_income_vs_satisfaction.html")

# 7. MOBILE PREFERENCE BY GENERATION
print("✓ Creating: Mobile Preference...")
mobile_cross = pd.crosstab(df['generation'], df['mobile_preference'], normalize='index') * 100
mobile_cross = mobile_cross.reset_index().melt(id_vars='generation', 
                                                var_name='Preference', value_name='Percentage')
fig7 = px.bar(mobile_cross, x='generation', y='Percentage', color='Preference',
              title='📱 Mobile-First Preference by Generation',
              labels={'generation': 'Generation', 'Percentage': 'Percentage (%)'},
              color_discrete_map={'Yes': '#27ae60', 'No': '#e74c3c'})
add_sample_data_disclaimer(fig7)
fig7.write_html(f"{output_dir}/07_mobile_preference.html")

# 8. CRYPTO EXPERIENCE
print("✓ Creating: Cryptocurrency Experience...")
crypto_counts = df['crypto_experience'].value_counts()
fig8 = px.pie(
    values=crypto_counts.values, names=crypto_counts.index,
    title='₿ Cryptocurrency Experience Distribution',
    color_discrete_sequence=px.colors.qualitative.Pastel
)
add_sample_data_disclaimer(fig8)
fig8.write_html(f"{output_dir}/08_crypto_experience.html")

# 9. PRIMARY PAYMENT METHOD
print("✓ Creating: Primary Payment Method...")
primary_counts = df['primary_payment_method'].value_counts()
fig9 = px.pie(
    values=primary_counts.values, names=primary_counts.index,
    title='🏆 Primary Payment Method Used',
    labels={method: method.replace('_', ' ').title() for method in primary_counts.index}
)
add_sample_data_disclaimer(fig9)
fig9.write_html(f"{output_dir}/09_primary_payment_method.html")

# 10. SECURITY & PRIVACY CONCERNS
print("✓ Creating: Security & Privacy Analysis...")
concern_data = pd.DataFrame({
    'Concern Type': ['Security', 'Privacy'],
    'Average Score': [df['security_concern'].mean(), df['privacy_concern'].mean()]
})
fig10 = px.bar(concern_data, x='Concern Type', y='Average Score',
               title='🔒 Security & Privacy Concerns (1-5 scale)',
               labels={'Average Score': 'Average Concern Level'},
               color='Average Score', color_continuous_scale='Reds')
add_sample_data_disclaimer(fig10)
fig10.write_html(f"{output_dir}/10_security_privacy.html")

# GENERATE SUMMARY REPORT
print("\n✓ Generating Summary Report...")
report = {
    'total_respondents': len(df),
    'generation_breakdown': df['generation'].value_counts().to_dict(),
    'average_metrics': {
        'payment_satisfaction': float(df['payment_satisfaction'].mean()),
        'trust_score': float(df['trust_score'].mean()),
        'security_concern': float(df['security_concern'].mean()),
        'privacy_concern': float(df['privacy_concern'].mean()),
    },
    'adoption_rates': {
        'bnpl': float((df['bnpl_user'] == 'Yes').sum() / len(df) * 100),
        'mobile_preference': float((df['mobile_preference'] == 'Yes').sum() / len(df) * 100),
    },
    'primary_method_distribution': df['primary_payment_method'].value_counts().to_dict(),
    'top_features': df[[col for col in df.columns if 'importance' in col]].mean().sort_values(ascending=False).head(5).to_dict(),
}

report['data_source'] = 'synthetic'
with open(os.path.join(script_dir, 'docs/analysis_report.json'), 'w') as f:
    json.dump(report, f, indent=2)

print("\n" + "="*80)
print("✅ DASHBOARD CREATION COMPLETE!")
print("="*80)
print("\n📊 KEY FINDINGS:")
print(f"  • Total Respondents: {report['total_respondents']}")
print(f"  • Payment Satisfaction: {report['average_metrics']['payment_satisfaction']:.2f}/5.0")
print(f"  • Trust Score: {report['average_metrics']['trust_score']:.2f}/5.0")
print(f"  • BNPL Adoption: {report['adoption_rates']['bnpl']:.1f}%")
print(f"  • Mobile Preference: {report['adoption_rates']['mobile_preference']:.1f}%")

print("\n📈 YOUR DASHBOARD IS READY!")
print(f"   Location: visualizations/")
print("\n📁 Generated Files:")
print("   1. 01_generation_distribution.html")
print("   2. 02_payment_methods.html")
print("   3. 03_feature_importance.html")
print("   4. 04_satisfaction_by_generation.html")
print("   5. 05_bnpl_adoption.html")
print("   6. 06_income_vs_satisfaction.html")
print("   7. 07_mobile_preference.html")
print("   8. 08_crypto_experience.html")
print("   9. 09_primary_payment_method.html")
print("   10. 10_security_privacy.html")

print("\n🌐 HOW TO VIEW:")
print("   1. Open File Explorer")
print("   2. Navigate to: visualizations/")
print("   3. Double-click any .html file to open in browser")
print("   4. Click, hover, and zoom for interactive exploration!")

print("\n" + "="*80 + "\n")
