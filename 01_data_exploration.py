"""
01_data_exploration.py
Exploratory Data Analysis for Gen Z Payment Analysis

Purpose: Load data, perform initial exploration, and generate summary statistics
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Configuration
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class PaymentDataExplorer:
    """Exploratory Data Analysis for payment preferences data"""
    
    def __init__(self, data_path):
        """Initialize and load data"""
        self.df = pd.read_csv(data_path)
        self.generations = ['Gen Z', 'Alpha Gen Z', 'Millennial', 'Gen X', 'Boomer']
        
    def load_data(self):
        """Load and display basic data information"""
        print("=" * 80)
        print("DATA OVERVIEW")
        print("=" * 80)
        print(f"\nDataset Shape: {self.df.shape}")
        print(f"Total Records: {len(self.df)}")
        print(f"Total Columns: {self.df.shape[1]}")
        
        print("\nData Types:")
        print(self.df.dtypes)
        
        print("\nMissing Values:")
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        missing_df = pd.DataFrame({
            'Column': missing.index,
            'Missing_Count': missing.values,
            'Missing_Percentage': missing_pct.values
        }).sort_values('Missing_Percentage', ascending=False)
        print(missing_df[missing_df['Missing_Count'] > 0])
        
        return self.df
    
    def demographic_analysis(self):
        """Analyze demographic distribution"""
        print("\n" + "=" * 80)
        print("DEMOGRAPHIC ANALYSIS")
        print("=" * 80)
        
        # Generation distribution
        print("\nGeneration Distribution:")
        gen_dist = self.df['generation'].value_counts()
        print(gen_dist)
        print(f"\nPercentage Distribution:")
        print((gen_dist / len(self.df) * 100).round(2))
        
        # Age statistics
        print("\nAge Statistics by Generation:")
        age_stats = self.df.groupby('generation')['age'].describe()
        print(age_stats.round(2))
        
        # Gender distribution
        print("\nGender Distribution:")
        print(self.df['gender'].value_counts())
        
        # Location distribution
        print("\nTop 10 Locations:")
        if 'region' in self.df.columns:
            print(self.df['region'].value_counts().head(10))
        elif 'location' in self.df.columns:
            print(self.df['location'].value_counts().head(10))
        else:
            print("No 'region' or 'location' column found")
        
        # Income distribution
        print("\nIncome Distribution:")
        if 'income_level' in self.df.columns:
            print(self.df['income_level'].value_counts().sort_index())
        elif 'income_bracket' in self.df.columns:
            print(self.df['income_bracket'].value_counts().sort_index())
        else:
            print("No 'income_level' or 'income_bracket' column found")
        
        return {
            'generations': gen_dist,
            'age_stats': age_stats,
            'gender': self.df['gender'].value_counts(),
            'income': self.df['income_bracket'].value_counts()
        }
    
    def payment_method_usage(self):
        """Analyze payment method adoption"""
        print("\n" + "=" * 80)
        print("PAYMENT METHOD USAGE")
        print("=" * 80)
        
        payment_methods = ['digital_wallet', 'bnpl', 'credit_card', 
                          'debit_card', 'paypal_venmo', 'cryptocurrency']
        
        # Overall adoption rates
        print("\nOverall Payment Method Adoption Rates:")
        adoption_rates = {}
        for method in payment_methods:
            if method in self.df.columns:
                rate = (self.df[method] == 'Active User').sum() / len(self.df) * 100
                adoption_rates[method] = rate
                print(f"{method}: {rate:.2f}%")
        
        # By generation
        print("\nPayment Method Adoption by Generation:")
        for method in payment_methods:
            if method in self.df.columns:
                print(f"\n{method.upper()}:")
                gen_adoption = (self.df.groupby('generation')[method] == 'Active User').sum()
                gen_total = self.df.groupby('generation').size()
                gen_pct = (gen_adoption / gen_total * 100).round(2)
                print(gen_pct)
        
        return adoption_rates
    
    def feature_importance_analysis(self):
        """Analyze feature importance ratings"""
        print("\n" + "=" * 80)
        print("FEATURE IMPORTANCE ANALYSIS")
        print("=" * 80)
        
        features = ['speed_importance', 'security_importance', 'privacy_importance',
                   'ease_of_use_importance', 'rewards_importance', 'mobility_importance']
        
        # Overall feature importance
        print("\nOverall Feature Importance (Average Rating 1-5):")
        feature_means = self.df[features].mean().sort_values(ascending=False)
        print(feature_means.round(2))
        
        # By generation
        print("\nFeature Importance by Generation:")
        gen_features = self.df.groupby('generation')[features].mean().round(2)
        print(gen_features)
        
        return gen_features
    
    def bnpl_analysis(self):
        """Analyze BNPL adoption and satisfaction"""
        print("\n" + "=" * 80)
        print("BUY NOW PAY LATER (BNPL) ANALYSIS")
        print("=" * 80)
        
        print("\nBNPL Awareness by Generation:")
        if 'bnpl_awareness' in self.df.columns:
            bnpl_awareness = pd.crosstab(self.df['generation'], self.df['bnpl_awareness'], 
                                         normalize='index') * 100
            print(bnpl_awareness.round(2))
        else:
            print("bnpl_awareness column not found; skipping awareness breakdown")
        
        print("\nBNPL Adoption by Generation:")
        adoption_col = 'bnpl_adoption' if 'bnpl_adoption' in self.df.columns else 'bnpl_user' if 'bnpl_user' in self.df.columns else None
        if adoption_col:
            bnpl_adoption = pd.crosstab(self.df['generation'], self.df[adoption_col], 
                                        normalize='index') * 100
            print(bnpl_adoption.round(2))

            bnpl_users = self.df[self.df[adoption_col] == ('Active User' if adoption_col == 'bnpl_adoption' else 'Yes')]
            if len(bnpl_users) > 0:
                if 'bnpl_satisfaction' in self.df.columns:
                    print(f"\nBNPL Satisfaction (Average, 1-5): {bnpl_users['bnpl_satisfaction'].mean():.2f}")
                    print("\nBNPL Satisfaction by Generation:")
                    bnpl_sat = bnpl_users.groupby('generation')['bnpl_satisfaction'].mean()
                    print(bnpl_sat.round(2))
                else:
                    print("bnpl_satisfaction column not found; skipping BNPL satisfaction analysis")
        else:
            print("No BNPL adoption column found; cannot compute BNPL adoption by generation")
        
        return bnpl_adoption
    
    def security_privacy_analysis(self):
        """Analyze security and privacy concerns"""
        print("\n" + "=" * 80)
        print("SECURITY & PRIVACY ANALYSIS")
        print("=" * 80)
        
        print("\nData Privacy Importance (Average Rating 1-5):")
        privacy_importance = self.df.groupby('generation')['privacy_importance'].mean()
        print(privacy_importance.round(2))
        
        print("\nSecurity Concerns (Average Rating 1-5):")
        security_concerns = self.df.groupby('generation')['security_importance'].mean()
        print(security_concerns.round(2))
        
        print("\nBiometric Authentication Interest by Generation:")
        if 'biometric_interest' in self.df.columns:
            biometric = pd.crosstab(self.df['generation'], 
                                   self.df['biometric_interest'], 
                                   normalize='index') * 100
            print(biometric.round(2))
        
        return security_concerns
    
    def create_visualizations(self):
        """Create key exploratory visualizations"""
        print("\n" + "=" * 80)
        print("CREATING VISUALIZATIONS")
        print("=" * 80)
        
        # 1. Generation Distribution
        fig1 = px.bar(self.df['generation'].value_counts().reset_index(name='Count'),
                     x='generation', y='Count',
                     title='Survey Respondents by Generation',
                     labels={'generation': 'Generation', 'Count': 'Number of Respondents'},
                     template='plotly_white')
        fig1.write_html("../visualizations/01_generation_distribution.html")
        print("✓ Generation distribution visualization saved")
        
        # 2. Age Distribution by Generation
        fig2 = px.box(self.df, x='generation', y='age',
                     title='Age Distribution by Generation',
                     template='plotly_white')
        fig2.write_html("../visualizations/02_age_distribution.html")
        print("✓ Age distribution visualization saved")
        
        # 3. Payment Method Adoption
        payment_methods = ['digital_wallet', 'bnpl', 'credit_card', 
                          'debit_card', 'paypal_venmo']
        adoption_data = []
        for method in payment_methods:
            if method in self.df.columns:
                rate = (self.df[method] == 'Active User').sum() / len(self.df) * 100
                adoption_data.append({'Method': method, 'Adoption Rate': rate})
        
        fig3 = px.bar(adoption_data, x='Method', y='Adoption Rate',
                     title='Payment Method Adoption Rates (Overall)',
                     template='plotly_white')
        fig3.write_html("../visualizations/03_payment_method_adoption.html")
        print("✓ Payment method adoption visualization saved")
        
        # 4. Feature Importance
        features = ['speed_importance', 'security_importance', 'privacy_importance',
                   'ease_of_use_importance', 'rewards_importance']
        feature_means = self.df[features].mean().sort_values(ascending=False)
        
        fig4 = px.bar(x=feature_means.values, y=feature_means.index,
                     orientation='h',
                     title='Average Feature Importance (1-5 Scale)',
                     template='plotly_white')
        fig4.write_html("../visualizations/04_feature_importance.html")
        print("✓ Feature importance visualization saved")
        
    def generate_summary_report(self):
        """Generate summary statistics report"""
        print("\n" + "=" * 80)
        print("GENERATING SUMMARY REPORT")
        print("=" * 80)
        
        report = f"""
# Exploratory Data Analysis Summary Report
## Gen Z Payment Analysis Project

### Executive Summary
- Total Survey Respondents: {len(self.df)}
- Data Collection Period: [To be filled]
- Response Quality: [To be assessed]

### Key Demographics
- Generations Surveyed: {len(self.df['generation'].unique())}
- Age Range: {self.df['age'].min():.0f} - {self.df['age'].max():.0f} years
- Average Age: {self.df['age'].mean():.1f} years

### Payment Method Highlights
- Most Common Payment Methods: [To be determined from analysis]
- Highest Adoption Rate: [To be determined]
- Generational Differences: [Significant/Moderate/Minor]

### Key Findings
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

### Next Steps
- Statistical significance testing
- Generational comparison analysis
- Feature importance ranking by cohort
- BNPL and digital wallet deep dive

---
Generated: {pd.Timestamp.now()}
"""
        
        with open("../docs/eda_summary.md", "w") as f:
            f.write(report)
        
        print("✓ Summary report generated")

def main():
    """Main execution function"""
    print("\n" + "=" * 80)
    print("GEN Z PAYMENT ANALYSIS - EXPLORATORY DATA ANALYSIS")
    print("=" * 80)
    
    # Initialize explorer
    import os
    # Get correct path whether running from root or analysis folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_path = os.path.join(project_root, "data", "processed", "payment_data_clean.csv")
    explorer = PaymentDataExplorer(data_path)
    
    # Run analyses
    try:
        data = explorer.load_data()
        demographics = explorer.demographic_analysis()
        payments = explorer.payment_method_usage()
        features = explorer.feature_importance_analysis()
        bnpl = explorer.bnpl_analysis()
        security = explorer.security_privacy_analysis()
        explorer.create_visualizations()
        explorer.generate_summary_report()
        
        print("\n" + "=" * 80)
        print("✓ EXPLORATORY DATA ANALYSIS COMPLETE")
        print("=" * 80)
        print("\nOutput Files:")
        print("- Visualizations: visualizations/0*.html")
        print("- Summary Report: docs/eda_summary.md")
        
    except FileNotFoundError:
        print("\n⚠ Data file not found. Please ensure processed data exists at:")
        print("  ../data/processed/payment_data_clean.csv")
        print("\nTo get started, you can:")
        print("1. Place your survey data in data/raw/")
        print("2. Run data processing scripts")
        print("3. Then run this exploratory analysis")

if __name__ == "__main__":
    main()
