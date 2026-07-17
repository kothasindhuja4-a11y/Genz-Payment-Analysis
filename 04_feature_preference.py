"""
04_feature_preference.py
Analysis of Payment Feature Preferences

Purpose: Understand which payment features matter most to different generations
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class FeatureAnalyzer:
    """Analyze payment feature preferences"""
    
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)
        self.features = {
            'speed_importance': 'Speed/Quick Checkout',
            'security_importance': 'Security/Fraud Protection',
            'privacy_importance': 'Data Privacy',
            'ease_of_use_importance': 'Ease of Use',
            'rewards_importance': 'Rewards/Cashback',
            'mobility_importance': 'Mobile Compatibility',
            'biometric_importance': 'Biometric Authentication',
            'sustainability_importance': 'Environmental Sustainability'
        }
    
    def feature_importance_ranking(self):
        """Rank feature importance across all respondents"""
        print("=" * 80)
        print("FEATURE IMPORTANCE RANKING")
        print("=" * 80)
        
        print("\nOverall Feature Importance (1-5 scale):")
        print("-" * 60)
        
        feature_means = {}
        for col, label in self.features.items():
            if col in self.df.columns:
                mean_val = self.df[col].mean()
                std_val = self.df[col].std()
                feature_means[label] = mean_val
                print(f"{label:.<40} {mean_val:>6.2f} ± {std_val:.2f}")
        
        # Sorted ranking
        sorted_features = sorted(feature_means.items(), key=lambda x: x[1], reverse=True)
        print("\nRanked by Importance:")
        print("-" * 60)
        for i, (feature, score) in enumerate(sorted_features, 1):
            print(f"{i}. {feature:.<40} {score:.2f}")
        
        return feature_means
    
    def feature_by_generation(self):
        """Compare feature importance across generations"""
        print("\n" + "=" * 80)
        print("FEATURE IMPORTANCE BY GENERATION")
        print("=" * 80)
        
        valid_features = [col for col in self.features.keys() if col in self.df.columns]
        
        gen_feature_importance = self.df.groupby('generation')[valid_features].mean()
        
        print("\nAverage Feature Importance Ratings by Generation:")
        print("-" * 80)
        print(gen_feature_importance.round(2))
        
        # Identify generation-specific priorities
        print("\n\nGeneration-Specific Feature Priorities:")
        print("-" * 80)
        
        for gen in self.df['generation'].unique():
            gen_data = self.df[self.df['generation'] == gen]
            gen_means = gen_data[valid_features].mean()
            top_3 = gen_means.nlargest(3)
            
            print(f"\n{gen}:")
            for i, (feature, score) in enumerate(top_3.items(), 1):
                feature_label = self.features.get(feature, feature)
                print(f"  {i}. {feature_label:.<40} {score:.2f}")
    
    def feature_generational_differences(self):
        """Identify significant generational differences in feature preference"""
        print("\n" + "=" * 80)
        print("GENERATIONAL DIFFERENCES IN FEATURE PREFERENCES")
        print("=" * 80)
        
        valid_features = [col for col in self.features.keys() if col in self.df.columns]
        
        print("\nFeature Preference Range (Max - Min across generations):")
        print("-" * 80)
        
        differences = {}
        for feature in valid_features:
            gen_means = self.df.groupby('generation')[feature].mean()
            diff = gen_means.max() - gen_means.min()
            differences[feature] = diff
            
            feature_label = self.features.get(feature, feature)
            print(f"{feature_label:.<40} {diff:.2f} points")
            
            # Show which generation prefers most/least
            max_gen = gen_means.idxmax()
            min_gen = gen_means.idxmin()
            print(f"  Most important to {max_gen}: {gen_means[max_gen]:.2f}")
            print(f"  Least important to {min_gen}: {gen_means[min_gen]:.2f}")
        
        return differences
    
    def genz_feature_profile(self):
        """Create detailed Gen Z feature preference profile"""
        print("\n" + "=" * 80)
        print("GEN Z FEATURE PREFERENCE PROFILE")
        print("=" * 80)
        
        genz_data = self.df[self.df['generation'] == 'Gen Z']
        others_data = self.df[self.df['generation'] != 'Gen Z']
        
        print(f"\nSample Size: {len(genz_data)} Gen Z respondents")
        print("-" * 80)
        
        valid_features = [col for col in self.features.keys() if col in self.df.columns]
        
        print("\nGen Z vs. Other Generations Feature Preferences:")
        print("-" * 80)
        
        for feature in valid_features:
            genz_mean = genz_data[feature].mean()
            others_mean = others_data[feature].mean()
            diff = genz_mean - others_mean
            direction = "↑" if diff > 0 else "↓"
            
            feature_label = self.features.get(feature, feature)
            print(f"\n{feature_label}:")
            print(f"  Gen Z: {genz_mean:.2f}")
            print(f"  Others: {others_mean:.2f}")
            print(f"  Difference: {diff:+.2f} {direction}")
    
    def feature_correlation_analysis(self):
        """Analyze correlations between feature preferences"""
        print("\n" + "=" * 80)
        print("FEATURE CORRELATION ANALYSIS")
        print("=" * 80)
        
        valid_features = [col for col in self.features.keys() if col in self.df.columns]
        
        correlation_matrix = self.df[valid_features].corr()
        
        print("\nHighest Correlations Between Features:")
        print("-" * 80)
        
        # Extract upper triangle to avoid duplicates
        mask = np.triu(np.ones_like(correlation_matrix, dtype=bool), k=1)
        correlations = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                corr_val = correlation_matrix.iloc[i, j]
                correlations.append({
                    'Feature1': self.features.get(valid_features[i], valid_features[i]),
                    'Feature2': self.features.get(valid_features[j], valid_features[j]),
                    'Correlation': corr_val
                })
        
        correlations_sorted = sorted(correlations, key=lambda x: abs(x['Correlation']), reverse=True)
        
        for i, corr in enumerate(correlations_sorted[:10], 1):
            print(f"\n{i}. {corr['Feature1']} ↔ {corr['Feature2']}")
            print(f"   Correlation: {corr['Correlation']:.3f}")
    
    def create_visualizations(self):
        """Create feature preference visualizations"""
        print("\n" + "=" * 80)
        print("CREATING FEATURE VISUALIZATIONS")
        print("=" * 80)
        
        valid_features = [col for col in self.features.keys() if col in self.df.columns]
        
        # 1. Overall feature importance bar chart
        feature_means = self.df[valid_features].mean()
        feature_labels = [self.features.get(f, f) for f in valid_features]
        
        fig1 = px.bar(
            x=feature_means.values,
            y=feature_labels,
            orientation='h',
            title='Average Feature Importance (All Respondents)',
            labels={'x': 'Importance Rating (1-5)', 'y': 'Feature'},
            template='plotly_white'
        )
        fig1.write_html("../visualizations/10_feature_importance_overall.html")
        print("✓ Overall feature importance saved")
        
        # 2. Radar chart for generation comparison
        generations = self.df['generation'].unique()
        gen_data = self.df.groupby('generation')[valid_features].mean()
        
        fig2 = go.Figure()
        
        for gen in generations:
            fig2.add_trace(go.Scatterpolar(
                r=gen_data.loc[gen].values,
                theta=feature_labels,
                fill='toself',
                name=gen
            ))
        
        fig2.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            showlegend=True,
            title='Feature Importance Comparison Across Generations',
            template='plotly_white'
        )
        fig2.write_html("../visualizations/11_feature_radar_comparison.html")
        print("✓ Feature radar comparison saved")
        
        # 3. Heatmap of features by generation
        fig3 = go.Figure(data=go.Heatmap(
            z=gen_data.values,
            x=feature_labels,
            y=gen_data.index,
            colorscale='RdYlGn',
            zmin=1,
            zmax=5
        ))
        fig3.update_layout(
            title='Feature Importance Heatmap by Generation',
            xaxis_title='Feature',
            yaxis_title='Generation',
            template='plotly_white'
        )
        fig3.write_html("../visualizations/12_feature_heatmap.html")
        print("✓ Feature heatmap saved")
        
        # 4. Box plot for feature distributions
        feature_data = []
        for feature in valid_features[:4]:  # Top 4 features
            temp_df = pd.DataFrame({
                'Feature': self.features.get(feature, feature),
                'Importance': self.df[feature],
                'Generation': self.df['generation']
            })
            feature_data.append(temp_df)
        
        plot_df = pd.concat(feature_data)
        
        fig4 = px.box(
            plot_df,
            x='Feature',
            y='Importance',
            color='Generation',
            title='Feature Importance Distribution by Generation',
            template='plotly_white'
        )
        fig4.write_html("../visualizations/13_feature_distribution.html")
        print("✓ Feature distribution saved")

def main():
    print("\n" + "=" * 80)
    print("GEN Z PAYMENT ANALYSIS - FEATURE PREFERENCE ANALYSIS")
    print("=" * 80)
    
    try:
        analyzer = FeatureAnalyzer("../data/processed/payment_data_clean.csv")
        
        feature_importance = analyzer.feature_importance_ranking()
        analyzer.feature_by_generation()
        differences = analyzer.feature_generational_differences()
        analyzer.genz_feature_profile()
        analyzer.feature_correlation_analysis()
        analyzer.create_visualizations()
        
        print("\n" + "=" * 80)
        print("✓ FEATURE PREFERENCE ANALYSIS COMPLETE")
        print("=" * 80)
        
    except FileNotFoundError as e:
        print(f"\n⚠ Error: {e}")

if __name__ == "__main__":
    main()
