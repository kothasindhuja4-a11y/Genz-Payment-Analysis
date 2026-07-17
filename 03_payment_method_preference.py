"""
03_payment_method_preference.py
Detailed Analysis of Payment Method Preferences

Purpose: In-depth analysis of each payment method's characteristics and adoption
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

class PaymentMethodAnalyzer:
    """Detailed analysis of payment method preferences"""
    
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)
        self.payment_methods = {
            'digital_wallet': 'Digital Wallets (Apple Pay, Google Pay)',
            'bnpl': 'Buy Now Pay Later',
            'credit_card': 'Credit Cards',
            'debit_card': 'Debit Cards',
            'paypal_venmo': 'PayPal/Venmo',
            'cryptocurrency': 'Cryptocurrency'
        }
    
    def analyze_primary_method(self):
        """Analyze primary payment method choice"""
        print("=" * 80)
        print("PRIMARY PAYMENT METHOD ANALYSIS")
        print("=" * 80)
        
        if 'primary_payment_method' in self.df.columns:
            primary_dist = self.df['primary_payment_method'].value_counts()
            primary_pct = (primary_dist / len(self.df) * 100).round(2)
            
            print("\nPrimary Payment Method Distribution:")
            for method, count in primary_dist.items():
                pct = primary_pct[method]
                print(f"  {method}: {count} ({pct}%)")
            
            # By generation
            print("\nPrimary Method by Generation:")
            for gen in self.df['generation'].unique():
                print(f"\n{gen}:")
                gen_data = self.df[self.df['generation'] == gen]
                gen_primary = gen_data['primary_payment_method'].value_counts()
                gen_pct = (gen_primary / len(gen_data) * 100).round(1)
                for method, count in gen_primary.items():
                    print(f"  {method}: {gen_pct[method]}%")
    
    def analyze_method_frequency(self):
        """Analyze usage frequency of each payment method"""
        print("\n" + "=" * 80)
        print("PAYMENT METHOD USAGE FREQUENCY")
        print("=" * 80)
        
        if 'payment_frequency' in self.df.columns:
            frequency_dist = self.df['payment_frequency'].value_counts()
            print("\nOverall Payment Frequency Distribution:")
            print(frequency_dist)
            
            print("\nAverage Payments per Month by Generation:")
            freq_by_gen = self.df.groupby('generation')['payment_frequency'].agg(lambda x: x.value_counts().index[0])
            print(freq_by_gen)
    
    def analyze_method_satisfaction(self):
        """Analyze satisfaction with current payment methods"""
        print("\n" + "=" * 80)
        print("PAYMENT METHOD SATISFACTION")
        print("=" * 80)
        
        if 'payment_satisfaction' in self.df.columns:
            print("\nOverall Satisfaction (1-5 scale):")
            print(f"Mean: {self.df['payment_satisfaction'].mean():.2f}")
            print(f"Median: {self.df['payment_satisfaction'].median():.2f}")
            print(f"Std Dev: {self.df['payment_satisfaction'].std():.2f}")
            
            print("\nSatisfaction by Generation:")
            sat_by_gen = self.df.groupby('generation')['payment_satisfaction'].agg(['mean', 'count'])
            print(sat_by_gen.round(2))
            
            print("\nSatisfaction Distribution:")
            print(self.df['payment_satisfaction'].value_counts().sort_index())
    
    def analyze_adoption_barriers(self):
        """Analyze barriers to payment method adoption"""
        print("\n" + "=" * 80)
        print("ADOPTION BARRIERS ANALYSIS")
        print("=" * 80)
        
        barrier_columns = [col for col in self.df.columns if 'barrier' in col.lower()]
        
        if barrier_columns:
            print(f"\nFound {len(barrier_columns)} barrier-related columns")
            
            # Count mentions of each barrier
            barrier_counts = {}
            for col in barrier_columns:
                if self.df[col].dtype == 'object':
                    barrier_counts[col] = self.df[col].value_counts()
            
            for barrier, counts in barrier_counts.items():
                print(f"\n{barrier}:")
                print(counts.head())
        else:
            print("\nNo barrier-specific columns found in dataset")
            print("Note: Consider adding barrier analysis to survey instrument")
    
    def analyze_use_cases(self):
        """Analyze use cases for different payment methods"""
        print("\n" + "=" * 80)
        print("PAYMENT METHOD USE CASES")
        print("=" * 80)
        
        use_case_columns = [col for col in self.df.columns if 'use_case' in col.lower()]
        
        if use_case_columns:
            for col in use_case_columns:
                print(f"\n{col}:")
                print(self.df[col].value_counts())
        else:
            print("No use case columns found")
            print("Survey could be enhanced with use case questions")
    
    def create_method_visualizations(self):
        """Create payment method specific visualizations"""
        print("\n" + "=" * 80)
        print("CREATING PAYMENT METHOD VISUALIZATIONS")
        print("=" * 80)
        
        # 1. Primary method pie chart
        if 'primary_payment_method' in self.df.columns:
            primary_dist = self.df['primary_payment_method'].value_counts()
            fig1 = px.pie(
                values=primary_dist.values,
                names=primary_dist.index,
                title='Primary Payment Method Distribution',
                template='plotly_white'
            )
            fig1.write_html("../visualizations/07_primary_payment_method.html")
            print("✓ Primary payment method visualization saved")
        
        # 2. Satisfaction by method
        if 'payment_satisfaction' in self.df.columns:
            fig2 = px.box(
                self.df,
                x='primary_payment_method',
                y='payment_satisfaction',
                title='Satisfaction by Payment Method',
                template='plotly_white'
            )
            fig2.write_html("../visualizations/08_satisfaction_by_method.html")
            print("✓ Satisfaction visualization saved")
        
        # 3. Generation preference comparison
        methods = ['digital_wallet', 'bnpl', 'credit_card', 'debit_card']
        data_for_plot = []
        
        for method in methods:
            if method in self.df.columns:
                for gen in self.df['generation'].unique():
                    gen_data = self.df[self.df['generation'] == gen]
                    adoption_rate = (gen_data[method] == 'Active User').sum() / len(gen_data) * 100
                    data_for_plot.append({
                        'Method': method,
                        'Generation': gen,
                        'Adoption': adoption_rate
                    })
        
        if data_for_plot:
            comparison_df = pd.DataFrame(data_for_plot)
            fig3 = px.bar(
                comparison_df,
                x='Method',
                y='Adoption',
                color='Generation',
                barmode='group',
                title='Payment Method Adoption by Generation',
                template='plotly_white'
            )
            fig3.write_html("../visualizations/09_method_by_generation.html")
            print("✓ Method comparison visualization saved")

def main():
    print("\n" + "=" * 80)
    print("GEN Z PAYMENT ANALYSIS - PAYMENT METHOD ANALYSIS")
    print("=" * 80)
    
    try:
        analyzer = PaymentMethodAnalyzer("../data/processed/payment_data_clean.csv")
        
        analyzer.analyze_primary_method()
        analyzer.analyze_method_frequency()
        analyzer.analyze_method_satisfaction()
        analyzer.analyze_adoption_barriers()
        analyzer.analyze_use_cases()
        analyzer.create_method_visualizations()
        
        print("\n" + "=" * 80)
        print("✓ PAYMENT METHOD ANALYSIS COMPLETE")
        print("=" * 80)
        
    except FileNotFoundError as e:
        print(f"\n⚠ Error: {e}")

if __name__ == "__main__":
    main()
