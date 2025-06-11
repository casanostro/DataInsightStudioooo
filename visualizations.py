import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

class SupplyChainVisualizations:
    """
    Create interactive visualizations for supply chain data analysis
    """
    
    def __init__(self, data):
        """
        Initialize with supply chain data
        
        Args:
            data (pd.DataFrame): Supply chain dataset
        """
        self.data = data
        self.color_palette = px.colors.qualitative.Set3
    
    def create_distribution_plot(self, column):
        """
        Create distribution plot for a numeric column
        
        Args:
            column (str): Column name to analyze
            
        Returns:
            plotly.graph_objects.Figure: Distribution plot
        """
        if column not in self.data.columns:
            return None
        
        if not pd.api.types.is_numeric_dtype(self.data[column]):
            return None
        
        # Remove null values
        data_clean = self.data[column].dropna()
        
        if len(data_clean) == 0:
            return None
        
        # Create subplot with histogram and box plot
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=(f'Distribution of {column.title()}', 'Box Plot'),
            vertical_spacing=0.1,
            row_heights=[0.7, 0.3]
        )
        
        # Histogram
        fig.add_trace(
            go.Histogram(
                x=data_clean,
                nbinsx=30,
                name='Distribution',
                marker_color=self.color_palette[0],
                opacity=0.7
            ),
            row=1, col=1
        )
        
        # Box plot
        fig.add_trace(
            go.Box(
                x=data_clean,
                name='',
                marker_color=self.color_palette[1],
                showlegend=False
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            title=f'Statistical Analysis: {column.title()}',
            height=600,
            showlegend=False
        )
        
        # Add statistics annotation
        stats_text = f"Mean: {data_clean.mean():.2f}<br>Median: {data_clean.median():.2f}<br>Std: {data_clean.std():.2f}"
        fig.add_annotation(
            text=stats_text,
            xref="paper", yref="paper",
            x=0.02, y=0.98,
            showarrow=False,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="gray",
            borderwidth=1
        )
        
        return fig
    
    def create_correlation_matrix(self):
        """
        Create correlation matrix heatmap for numeric columns
        
        Returns:
            plotly.graph_objects.Figure: Correlation heatmap
        """
        # Get numeric columns
        numeric_data = self.data.select_dtypes(include=[np.number])
        
        if numeric_data.shape[1] < 2:
            return None
        
        # Calculate correlation matrix
        corr_matrix = numeric_data.corr()
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=np.round(corr_matrix.values, 2),
            texttemplate="%{text}",
            textfont={"size": 10},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title='Correlation Matrix of Numeric Variables',
            xaxis_title='Variables',
            yaxis_title='Variables',
            height=600
        )
        
        return fig
    
    def create_time_series(self, date_column, value_column):
        """
        Create time series plot
        
        Args:
            date_column (str): Date column name
            value_column (str): Value column name
            
        Returns:
            plotly.graph_objects.Figure: Time series plot
        """
        if (date_column not in self.data.columns or 
            value_column not in self.data.columns):
            return None
        
        # Sort by date
        df_sorted = self.data.sort_values(date_column)
        
        # Create time series plot
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_sorted[date_column],
            y=df_sorted[value_column],
            mode='lines+markers',
            name=value_column.title(),
            line=dict(color=self.color_palette[0]),
            marker=dict(size=4)
        ))
        
        # Add trend line
        if len(df_sorted) > 2:
            z = np.polyfit(range(len(df_sorted)), df_sorted[value_column].fillna(0), 1)
            p = np.poly1d(z)
            
            fig.add_trace(go.Scatter(
                x=df_sorted[date_column],
                y=p(range(len(df_sorted))),
                mode='lines',
                name='Trend',
                line=dict(color='red', dash='dash'),
                opacity=0.7
            ))
        
        fig.update_layout(
            title=f'{value_column.title()} Over Time',
            xaxis_title=date_column.title(),
            yaxis_title=value_column.title(),
            height=500
        )
        
        return fig
    
    def create_category_analysis(self, category_column, value_column):
        """
        Create category analysis visualization
        
        Args:
            category_column (str): Category column name
            value_column (str): Value column name
            
        Returns:
            plotly.graph_objects.Figure: Category analysis plot
        """
        if (category_column not in self.data.columns or 
            value_column not in self.data.columns):
            return None
        
        # Group by category and calculate statistics
        grouped = self.data.groupby(category_column)[value_column].agg([
            'mean', 'median', 'sum', 'count', 'std'
        ]).reset_index()
        
        # Sort by mean value
        grouped = grouped.sort_values('mean', ascending=False)
        
        # Limit to top 15 categories for readability
        if len(grouped) > 15:
            grouped = grouped.head(15)
        
        # Create subplot with bar chart and box plot
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Average by Category', 'Distribution by Category'),
            column_widths=[0.6, 0.4]
        )
        
        # Bar chart
        fig.add_trace(
            go.Bar(
                x=grouped['mean'],
                y=grouped[category_column],
                orientation='h',
                name='Average',
                marker_color=self.color_palette[0],
                text=grouped['mean'].round(2),
                textposition='auto'
            ),
            row=1, col=1
        )
        
        # Box plot for each category
        categories = grouped[category_column].tolist()
        for i, cat in enumerate(categories):
            category_data = self.data[self.data[category_column] == cat][value_column].dropna()
            
            if len(category_data) > 0:
                fig.add_trace(
                    go.Box(
                        y=category_data,
                        name=str(cat)[:20],  # Truncate long names
                        boxpoints='outliers',
                        marker_color=self.color_palette[i % len(self.color_palette)],
                        showlegend=False
                    ),
                    row=1, col=2
                )
        
        fig.update_layout(
            title=f'{value_column.title()} Analysis by {category_column.title()}',
            height=max(400, len(categories) * 30),
            showlegend=False
        )
        
        fig.update_xaxes(title_text=f"Average {value_column.title()}", row=1, col=1)
        fig.update_yaxes(title_text=category_column.title(), row=1, col=1)
        fig.update_yaxes(title_text=value_column.title(), row=1, col=2)
        
        return fig
    
    def create_kpi_dashboard(self, kpis):
        """
        Create KPI dashboard visualization
        
        Args:
            kpis (dict): Dictionary of KPI values
            
        Returns:
            plotly.graph_objects.Figure: KPI dashboard
        """
        if not kpis:
            return None
        
        # Filter out trend values for the main display
        main_kpis = {k: v for k, v in kpis.items() if not k.endswith('_trend')}
        
        if len(main_kpis) < 2:
            return None
        
        # Create gauge charts for key KPIs
        kpi_names = list(main_kpis.keys())[:4]  # Limit to 4 KPIs
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[name.replace('_', ' ').title() for name in kpi_names],
            specs=[[{"type": "indicator"}, {"type": "indicator"}],
                   [{"type": "indicator"}, {"type": "indicator"}]]
        )
        
        positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
        
        for i, kpi_name in enumerate(kpi_names):
            if i >= 4:
                break
                
            value = main_kpis[kpi_name]
            
            # Determine gauge range and thresholds based on KPI type
            if 'rate' in kpi_name.lower() or 'level' in kpi_name.lower():
                gauge_range = [0, 100]
                threshold_high = 90
                threshold_low = 75
            elif 'turnover' in kpi_name.lower():
                gauge_range = [0, max(15, value * 1.5)]
                threshold_high = 8
                threshold_low = 4
            elif 'time' in kpi_name.lower():
                gauge_range = [0, max(30, value * 1.5)]
                threshold_high = 7  # Lower is better for time
                threshold_low = 14
            else:
                gauge_range = [0, max(100, value * 1.2)]
                threshold_high = value * 0.9
                threshold_low = value * 0.7
            
            # Determine color based on performance
            if 'time' in kpi_name.lower():  # Lower is better
                if value <= threshold_high:
                    color = "green"
                elif value <= threshold_low:
                    color = "yellow"
                else:
                    color = "red"
            else:  # Higher is better
                if value >= threshold_high:
                    color = "green"
                elif value >= threshold_low:
                    color = "yellow"
                else:
                    color = "red"
            
            fig.add_trace(go.Indicator(
                mode = "gauge+number+delta",
                value = value,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': kpi_name.replace('_', ' ').title()},
                delta = {'reference': kpis.get(f'{kpi_name}_trend', 0)},
                gauge = {
                    'axis': {'range': gauge_range},
                    'bar': {'color': color},
                    'steps': [
                        {'range': [gauge_range[0], threshold_low], 'color': "lightgray"},
                        {'range': [threshold_low, threshold_high], 'color': "gray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': threshold_high
                    }
                }
            ), row=positions[i][0], col=positions[i][1])
        
        fig.update_layout(
            title="Supply Chain KPI Dashboard",
            height=600
        )
        
        return fig
    
    def create_trend_analysis(self, date_column, metrics_columns):
        """
        Create trend analysis for multiple metrics over time
        
        Args:
            date_column (str): Date column name
            metrics_columns (list): List of metric column names
            
        Returns:
            plotly.graph_objects.Figure: Trend analysis plot
        """
        if date_column not in self.data.columns:
            return None
        
        # Filter existing columns
        existing_metrics = [col for col in metrics_columns if col in self.data.columns]
        
        if not existing_metrics:
            return None
        
        # Sort by date
        df_sorted = self.data.sort_values(date_column)
        
        fig = go.Figure()
        
        for i, metric in enumerate(existing_metrics):
            fig.add_trace(go.Scatter(
                x=df_sorted[date_column],
                y=df_sorted[metric],
                mode='lines+markers',
                name=metric.title(),
                line=dict(color=self.color_palette[i % len(self.color_palette)]),
                marker=dict(size=4)
            ))
        
        fig.update_layout(
            title='Trend Analysis of Key Metrics',
            xaxis_title=date_column.title(),
            yaxis_title='Values',
            height=500,
            hovermode='x unified'
        )
        
        return fig
    
    def create_performance_comparison(self, category_column, metrics):
        """
        Create performance comparison across categories
        
        Args:
            category_column (str): Category column name
            metrics (list): List of metric column names
            
        Returns:
            plotly.graph_objects.Figure: Performance comparison plot
        """
        if category_column not in self.data.columns:
            return None
        
        # Filter existing metrics
        existing_metrics = [col for col in metrics if col in self.data.columns]
        
        if not existing_metrics:
            return None
        
        # Group by category
        grouped = self.data.groupby(category_column)[existing_metrics].mean().reset_index()
        
        # Create grouped bar chart
        fig = go.Figure()
        
        for i, metric in enumerate(existing_metrics):
            fig.add_trace(go.Bar(
                name=metric.title(),
                x=grouped[category_column],
                y=grouped[metric],
                marker_color=self.color_palette[i % len(self.color_palette)]
            ))
        
        fig.update_layout(
            title=f'Performance Comparison by {category_column.title()}',
            xaxis_title=category_column.title(),
            yaxis_title='Average Values',
            barmode='group',
            height=500
        )
        
        return fig
