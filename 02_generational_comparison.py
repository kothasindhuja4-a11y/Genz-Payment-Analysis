"""
02_generational_comparison.py
Comparative Analysis across Generations

Purpose: Statistical comparison of payment preferences across generational cohorts
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import chi2_contingency, f_oneway, ttest_ind
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

class GenerationalComparator:
    """Compare payment preferences across generations"""
    
    def __init__(self, data_path):
        """Initialize with data"""
        self.df = pd.read_csv(data_path)
        self.generations = ['Gen Z', 'Alpha Gen Z', 'Millennial', 'Gen X', 'Boomer']
        self.alpha_order = ['Gen Z', 'Millennial', 'Gen X', 'Boomer']
        
    def chi_square_test(self, var1, var2):
        """Perform chi-square test for independence"""
        contingency_table = pd.crosstab(self.df[var1], self.df[var2])
        chi2, p_value, dof, expected = chi2_contingency(contingency_table)
        
        return {
            'chi2': chi2,
            'p_value': p_value,
            'dof': dof,
            'significant': p_value < 0.05
        }
    
    def compare_payment_methods(self):
        """Compare payment method adoption across generations"""
        print("=" * 80)
        print("GENERATIONAL PAYMENT METHOD COMPARISON")
        print("=" * 80)
        
        payment_methods = ['digital_wallet', 'bnpl', 'credit_card', 
                          'debit_card', 'paypal_venmo']
        
        print("\nPayment Method Adoption Rates by Generation (%):")
        results = {}
        
        for method in payment_methods:
            if method in self.df.columns:
                cross_tab = pd.crosstab(
                    self.df['generation'], 
                    self.df[method] == 'Active User',
                    normalize='index'
                ) * 100
                
                results[method] = cross_tab[True]
                print(f"\n{method.upper()}:")
                print(cross_tab[True].round(2))
                
                # Chi-square test
                test_result = self.chi_square_test('generation', method)
                print(f"Chi-square test p-value: {test_result['p_value']:.4f}")
                print(f"Significant difference: {'Yes ✓' if test_result['significant'] else 'No'}")
        
        return pd.DataFrame(results)
    
    def compare_feature_importance(self):
        """Compare feature importance ratings across generations"""
        print("\n" + "=" * 80)
        print("FEATURE IMPORTANCE COMPARISON")
        print("=" * 80)
        
        features = ['speed_importance', 'security_importance', 'privacy_importance',
                   'ease_of_use_importance', 'rewards_importance', 'mobility_importance']
        
        print("\nAverage Feature Importance Ratings by Generation (1-5 scale):")
        feature_comparison = self.df.groupby('generation')[features].mean()
        print(feature_comparison.round(3))
        
        # Statistical tests for each feature
        print("\n" + "-" * 80)
        print("ANOVA Results (testing for generation differences):")
        print("-" * 80)
        
        for feature in features:
            groups = [group[feature].values for name, group in self.df.groupby('generation')]
            f_stat, p_value = f_oneway(*groups)
            
            print(f"\n{feature.upper()}:")
            print(f"  F-statistic: {f_stat:.4f}")
            print(f"  P-value: {p_value:.4f}")
            print(f"  Significant: {'Yes ✓' if p_value < 0.05 else 'No'}")
        
        return feature_comparison
    
    def compare_genz_vs_others(self):
        """Specific comparison of Gen Z vs. other generations"""
        print("\n" + "=" * 80)
        print("GEN Z vs. OTHER GENERATIONS COMPARISON")
        print("=" * 80)
        
        genz_data = self.df[self.df['generation'] == 'Gen Z']
        others_data = self.df[self.df['generation'] != 'Gen Z']
        
        print(f"\nGen Z Sample Size: {len(genz_data)}")
        print(f"Other Generations Sample Size: {len(others_data)}")
        
        # Payment method comparison
        print("\n" + "-" * 80)
        print("PAYMENT METHOD COMPARISON:")
        print("-" * 80)
        
        payment_methods = ['digital_wallet', 'bnpl', 'credit_card', 
                          'debit_card', 'paypal_venmo']
        
        for method in payment_methods:
            if method in self.df.columns:
                genz_rate = (genz_data[method] == 'Active User').sum() / len(genz_data) * 100
                others_rate = (others_data[method] == 'Active User').sum() / len(others_data) * 100
                diff = genz_rate - others_rate
                
                print(f"\n{method.upper()}:")
                print(f"  Gen Z: {genz_rate:.1f}%")
                print(f"  Others: {others_rate:.1f}%")
                print(f"  Difference: {diff:+.1f} percentage points")
        
        # Feature importance comparison
        print("\n" + "-" * 80)
        print("FEATURE IMPORTANCE COMPARISON:")
        print("-" * 80)
        
        features = ['speed_importance', 'security_importance', 'privacy_importance']
        
        for feature in features:
            genz_mean = genz_data[feature].mean()
            others_mean = others_data[feature].mean()
            diff = genz_mean - others_mean
            
            # T-test
            t_stat, p_value = ttest_ind(genz_data[feature], others_data[feature])
            
            print(f"\n{feature.upper()}:")
            print(f"  Gen Z Mean: {genz_mean:.2f}")
            print(f"  Others Mean: {others_mean:.2f}")
            print(f"  Difference: {diff:+.2f}")
            print(f"  T-test p-value: {p_value:.4f}")
            print(f"  Significant: {'Yes ✓' if p_value < 0.05 else 'No'}")
    
    def bnpl_adoption_comparison(self):
        """Deep dive into BNPL adoption across generations"""
        print("\n" + "=" * 80)
        print("BNPL ADOPTION DEEP DIVE")
        print("=" * 80)
        
        print("\nBNPL Awareness Funnel by Generation:")
        print("-" * 60)
        
        for gen in self.alpha_order:
            gen_data = self.df[self.df['generation'] == gen]
            
            aware = (gen_data['bnpl_awareness'] == 'Yes').sum() if 'bnpl_awareness' in gen_data.columns else 0
            aware_pct = aware / len(gen_data) * 100 if len(gen_data) > 0 else 0
            
            bnpl_col = 'bnpl_adoption' if 'bnpl_adoption' in gen_data.columns else 'bnpl_user' if 'bnpl_user' in gen_data.columns else None
            if bnpl_col:
                users = (gen_data[bnpl_col] == ('Active User' if bnpl_col == 'bnpl_adoption' else 'Yes')).sum()
                user_pct = users / len(gen_data) * 100 if len(gen_data) > 0 else 0
                conversion = users / aware * 100 if aware > 0 else 0
                satisfied = gen_data[gen_data[bnpl_col] == ('Active User' if bnpl_col == 'bnpl_adoption' else 'Yes')]['bnpl_satisfaction'].mean() if 'bnpl_satisfaction' in gen_data.columns else np.nan
            else:
                users = 0
                user_pct = 0
                conversion = 0
                satisfied = np.nan
            
            print(f"\n{gen}:")
            print(f"  Aware: {aware_pct:.1f}% ({aware} respondents)")
            print(f"  Active Users: {user_pct:.1f}% ({users} respondents)")
            print(f"  Awareness→Adoption: {conversion:.1f}% conversion")
            print(f"  Satisfaction: {satisfied:.2f}/5.0" if not np.isnan(satisfied) else "  Satisfaction: N/A")
    
    def digital_wallet_analysis(self):
        """Analyze digital wallet adoption across generations"""
        print("\n" + "=" * 80)
        print("DIGITAL WALLET ADOPTION ANALYSIS")
        print("=" * 80)
        
        if 'digital_wallet' in self.df.columns:
            print("\nDigital Wallet Usage by Generation:")
            print("-" * 60)
            
            dw_cross = pd.crosstab(
                self.df['generation'],
                self.df['digital_wallet'],
                normalize='index'
            ) * 100
            
            print(dw_cross.round(2))
            
            # Active users analysis
            dw_active = self.df[self.df['digital_wallet'] == 'Active User']
            print(f"\n\nTotal Digital Wallet Active Users: {len(dw_active)} ({len(dw_active)/len(self.df)*100:.1f}%)")
            
            print("\nDigital Wallet Usage by Generation (Active Users Only):")
            for gen in self.alpha_order:
                gen_active = dw_active[dw_active['generation'] == gen]
                print(f"  {gen}: {len(gen_active)}")
    
    def create_comparison_visualizations(self):
        """Create comparative visualizations"""
        print("\n" + "=" * 80)
        print("CREATING COMPARISON VISUALIZATIONS")
        print("=" * 80)
        
        # Prepare data for visualizations
        payment_methods = ['digital_wallet', 'bnpl', 'credit_card', 'debit_card']
        adoption_by_gen = {}
        
        for method in payment_methods:
            if method in self.df.columns:
                adoption_by_gen[method] = (
                    self.df.groupby('generation')[method]
                    .apply(lambda x: (x == 'Active User').sum() / len(x) * 100)
                )
        
        adoption_df = pd.DataFrame(adoption_by_gen).reset_index()
        
        # 1. Grouped bar chart
        fig1 = go.Figure()
        for method in payment_methods:
            if method in adoption_df.columns:
                fig1.add_trace(go.Bar(
                    x=adoption_df['generation'],
                    y=adoption_df[method],
                    name=method
                ))
        
        fig1.update_layout(
            title='Payment Method Adoption by Generation',
            xaxis_title='Generation',
            yaxis_title='Adoption Rate (%)',
            barmode='group',
            template='plotly_white'
        )
        fig1.write_html("../visualizations/05_payment_adoption_comparison.html")
        print("✓ Payment adoption comparison saved")
        
        # 2. Heatmap of payment methods by generation
        pivot_data = adoption_df.set_index('generation')
        fig2 = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale='Viridis'
        ))
        fig2.update_layout(
            title='Payment Method Adoption Heatmap',
            xaxis_title='Payment Method',
            yaxis_title='Generation'
        )
        fig2.write_html("../visualizations/06_payment_adoption_heatmap.html")
        print("✓ Payment adoption heatmap saved")

def main():
    """Main execution"""
    print("\n" + "=" * 80)
    print("GEN Z PAYMENT ANALYSIS - GENERATIONAL COMPARISON")
    print("=" * 80)
    
    try:
        comparator = GenerationalComparator("../data/processed/payment_data_clean.csv")
        
        payment_comparison = comparator.compare_payment_methods()
        feature_comparison = comparator.compare_feature_importance()
        comparator.compare_genz_vs_others()
        comparator.bnpl_adoption_comparison()
        comparator.digital_wallet_analysis()
        comparator.create_comparison_visualizations()
        
        print("\n" + "=" * 80)
        print("✓ GENERATIONAL COMPARISON ANALYSIS COMPLETE")
        print("=" * 80)
        
    except FileNotFoundError as e:
        print(f"\n⚠ Error: {e}")
        print("Please ensure processed data exists at: ../data/processed/payment_data_clean.csv")

if __name__ == "__main__":
    main()
