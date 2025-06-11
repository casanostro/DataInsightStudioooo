import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io

from data_processor import DataProcessor
from kpi_calculator import KPICalculator
from recommendation_engine import RecommendationEngine
from visualizations import SupplyChainVisualizations

# Page configuration
st.set_page_config(
    page_title="Supply Chain Analytics & Recommendations",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("📊 Supply Chain Data Storytelling & Reporting Tool")
    st.markdown("Transform your supply chain data into actionable business recommendations")
    
    # Initialize session state
    if 'processed_data' not in st.session_state:
        st.session_state.processed_data = None
    if 'kpis' not in st.session_state:
        st.session_state.kpis = None
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = None

    # Sidebar for file upload and filters
    with st.sidebar:
        st.header("📁 Data Upload")
        uploaded_file = st.file_uploader(
            "Upload your Excel/CSV data",
            type=["xlsx", "csv", "xls"],
            help="Upload supply chain data including stocks, sales, delays, costs, etc."
        )
        
        if uploaded_file is not None:
            # Process uploaded file
            processor = DataProcessor()
            
            try:
                with st.spinner("Processing uploaded data..."):
                    df = processor.load_data(uploaded_file)
                    st.session_state.processed_data = df
                    
                    # Calculate KPIs
                    kpi_calc = KPICalculator(df)
                    st.session_state.kpis = kpi_calc.calculate_all_kpis()
                    
                    # Generate recommendations
                    rec_engine = RecommendationEngine(df, st.session_state.kpis)
                    st.session_state.recommendations = rec_engine.generate_recommendations()
                
                st.success(f"✅ Data processed successfully! {len(df)} records loaded.")
                
                # Display basic data info
                with st.expander("📋 Data Overview"):
                    st.write(f"**Rows:** {len(df)}")
                    st.write(f"**Columns:** {len(df.columns)}")
                    st.write("**Column Names:**")
                    for col in df.columns:
                        st.write(f"- {col}")
                
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
                st.info("Please ensure your file contains supply chain data with appropriate columns.")
                return

    # Main content area
    if st.session_state.processed_data is not None:
        df = st.session_state.processed_data
        
        # Add filters in sidebar
        with st.sidebar:
            st.header("🔍 Filters")
            
            # Date range filter if date columns exist
            date_columns = df.select_dtypes(include=['datetime64']).columns.tolist()
            if date_columns:
                date_col = st.selectbox("Select Date Column", date_columns)
                min_date = df[date_col].min().date()
                max_date = df[date_col].max().date()
                
                date_range = st.date_input(
                    "Date Range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date
                )
                
                if len(date_range) == 2:
                    df = df[(df[date_col].dt.date >= date_range[0]) & 
                           (df[date_col].dt.date <= date_range[1])]
            
            # Categorical filters
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            for col in categorical_cols[:3]:  # Limit to first 3 categorical columns
                unique_values = df[col].dropna().unique()
                if len(unique_values) > 1 and len(unique_values) <= 50:  # Only show if reasonable number of options
                    selected_values = st.multiselect(
                        f"Filter by {col}",
                        options=unique_values,
                        default=unique_values
                    )
                    if selected_values:
                        df = df[df[col].isin(selected_values)]
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Dashboard", 
            "📈 Visualizations", 
            "🔍 KPI Analysis", 
            "🧠 Recommendations", 
            "📋 Raw Data"
        ])
        
        with tab1:
            st.header("Supply Chain Dashboard")
            
            # KPI cards
            if st.session_state.kpis:
                kpis = st.session_state.kpis
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Service Level", 
                        f"{kpis.get('service_level', 0):.1f}%",
                        delta=f"{kpis.get('service_level_trend', 0):.1f}%"
                    )
                
                with col2:
                    st.metric(
                        "Stock Turnover", 
                        f"{kpis.get('stock_turnover', 0):.1f}x",
                        delta=f"{kpis.get('turnover_trend', 0):.1f}%"
                    )
                
                with col3:
                    st.metric(
                        "OTIF Rate", 
                        f"{kpis.get('otif_rate', 0):.1f}%",
                        delta=f"{kpis.get('otif_trend', 0):.1f}%"
                    )
                
                with col4:
                    st.metric(
                        "Avg Lead Time", 
                        f"{kpis.get('avg_lead_time', 0):.1f} days",
                        delta=f"{kpis.get('lead_time_trend', 0):.1f}%"
                    )
            
            # Summary statistics
            st.subheader("📋 Data Summary")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Numeric Summary:**")
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    st.dataframe(df[numeric_cols].describe())
                else:
                    st.info("No numeric columns found for summary statistics.")
            
            with col2:
                st.write("**Data Quality:**")
                quality_metrics = {
                    'Total Rows': len(df),
                    'Total Columns': len(df.columns),
                    'Missing Values': df.isnull().sum().sum(),
                    'Duplicate Rows': df.duplicated().sum()
                }
                quality_df = pd.DataFrame(list(quality_metrics.items()), 
                                        columns=['Metric', 'Value'])
                st.dataframe(quality_df, hide_index=True)
        
        with tab2:
            st.header("📈 Interactive Visualizations")
            
            viz = SupplyChainVisualizations(df)
            
            # Chart selection
            chart_type = st.selectbox(
                "Select Visualization Type",
                ["Distribution Analysis", "Correlation Matrix", "Time Series", "Category Analysis"]
            )
            
            if chart_type == "Distribution Analysis":
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                if numeric_cols:
                    selected_col = st.selectbox("Select Column", numeric_cols)
                    fig = viz.create_distribution_plot(selected_col)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No numeric columns available for distribution analysis.")
            
            elif chart_type == "Correlation Matrix":
                fig = viz.create_correlation_matrix()
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Not enough numeric columns for correlation analysis.")
            
            elif chart_type == "Time Series":
                date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                
                if date_cols and numeric_cols:
                    date_col = st.selectbox("Select Date Column", date_cols)
                    value_col = st.selectbox("Select Value Column", numeric_cols)
                    fig = viz.create_time_series(date_col, value_col)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Date and numeric columns required for time series analysis.")
            
            elif chart_type == "Category Analysis":
                categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                
                if categorical_cols and numeric_cols:
                    cat_col = st.selectbox("Select Category Column", categorical_cols)
                    val_col = st.selectbox("Select Value Column", numeric_cols)
                    fig = viz.create_category_analysis(cat_col, val_col)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Category and numeric columns required for category analysis.")
        
        with tab3:
            st.header("🔍 KPI Analysis")
            
            if st.session_state.kpis:
                kpis = st.session_state.kpis
                
                st.subheader("Key Performance Indicators")
                
                # Create KPI summary table
                kpi_data = []
                for kpi_name, kpi_value in kpis.items():
                    if not kpi_name.endswith('_trend'):
                        trend_key = f"{kpi_name}_trend"
                        trend_value = kpis.get(trend_key, 0)
                        
                        # Determine status based on KPI type and value
                        if 'rate' in kpi_name.lower() or 'level' in kpi_name.lower():
                            status = "🟢 Good" if kpi_value >= 90 else "🟡 Average" if kpi_value >= 75 else "🔴 Poor"
                        elif 'time' in kpi_name.lower():
                            status = "🟢 Good" if kpi_value <= 7 else "🟡 Average" if kpi_value <= 14 else "🔴 Poor"
                        else:
                            status = "📊 Monitor"
                        
                        kpi_data.append({
                            'KPI': kpi_name.replace('_', ' ').title(),
                            'Value': f"{kpi_value:.2f}",
                            'Trend': f"{trend_value:+.1f}%",
                            'Status': status
                        })
                
                if kpi_data:
                    kpi_df = pd.DataFrame(kpi_data)
                    st.dataframe(kpi_df, hide_index=True, use_container_width=True)
                
                # Additional KPI insights
                st.subheader("📊 KPI Insights")
                
                # Performance alerts
                alerts = []
                if kpis.get('service_level', 100) < 95:
                    alerts.append("⚠️ Service level below target (95%)")
                if kpis.get('otif_rate', 100) < 90:
                    alerts.append("⚠️ OTIF rate needs improvement")
                if kpis.get('avg_lead_time', 0) > 14:
                    alerts.append("⚠️ Lead times are longer than ideal (>14 days)")
                
                if alerts:
                    st.warning("**Performance Alerts:**")
                    for alert in alerts:
                        st.write(alert)
                else:
                    st.success("✅ All key metrics are within acceptable ranges")
            
            else:
                st.info("KPI analysis will appear here once data is processed.")
        
        with tab4:
            st.header("🧠 Business Recommendations")
            
            if st.session_state.recommendations:
                recommendations = st.session_state.recommendations
                
                # Priority recommendations
                st.subheader("🔥 Priority Actions")
                priority_recs = [r for r in recommendations if r.get('priority') == 'High']
                for i, rec in enumerate(priority_recs, 1):
                    with st.container():
                        st.markdown(f"**{i}. {rec['title']}**")
                        st.write(rec['description'])
                        st.write(f"**Impact:** {rec['impact']}")
                        st.write(f"**Effort:** {rec['effort']}")
                        st.divider()
                
                # Medium priority recommendations
                if any(r.get('priority') == 'Medium' for r in recommendations):
                    st.subheader("📋 Medium Priority Actions")
                    medium_recs = [r for r in recommendations if r.get('priority') == 'Medium']
                    for i, rec in enumerate(medium_recs, 1):
                        with st.expander(f"{i}. {rec['title']}"):
                            st.write(rec['description'])
                            st.write(f"**Impact:** {rec['impact']}")
                            st.write(f"**Effort:** {rec['effort']}")
                
                # Low priority recommendations
                if any(r.get('priority') == 'Low' for r in recommendations):
                    st.subheader("💡 Future Considerations")
                    low_recs = [r for r in recommendations if r.get('priority') == 'Low']
                    for i, rec in enumerate(low_recs, 1):
                        with st.expander(f"{i}. {rec['title']}"):
                            st.write(rec['description'])
                            st.write(f"**Impact:** {rec['impact']}")
                            st.write(f"**Effort:** {rec['effort']}")
                
                # Export recommendations
                st.subheader("📤 Export Recommendations")
                if st.button("Generate Report"):
                    report_content = generate_report(recommendations, st.session_state.kpis)
                    st.download_button(
                        label="Download Report",
                        data=report_content,
                        file_name=f"supply_chain_recommendations_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
            
            else:
                st.info("Business recommendations will appear here once data is analyzed.")
        
        with tab5:
            st.header("📋 Raw Data")
            
            st.subheader("Filtered Dataset")
            st.write(f"Showing {len(df)} rows after applying filters")
            
            # Show data with pagination
            page_size = st.selectbox("Rows per page", [10, 25, 50, 100], index=1)
            
            total_pages = (len(df) - 1) // page_size + 1
            page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
            
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            
            st.dataframe(df.iloc[start_idx:end_idx], use_container_width=True)
            
            # Export data
            st.subheader("📤 Export Data")
            col1, col2 = st.columns(2)
            
            with col1:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download as CSV",
                    data=csv,
                    file_name=f"filtered_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                # Convert to Excel
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Data', index=False)
                
                st.download_button(
                    label="Download as Excel",
                    data=buffer.getvalue(),
                    file_name=f"filtered_data_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
    else:
        # Welcome message when no data is uploaded
        st.markdown("""
        ## Welcome to Supply Chain Analytics Tool
        
        This tool helps you analyze supply chain data and generate actionable business recommendations.
        
        ### 🚀 Getting Started
        1. **Upload your data** using the file uploader in the sidebar
        2. **Explore your data** through interactive visualizations
        3. **Analyze KPIs** including service levels, OTIF rates, and lead times
        4. **Get recommendations** based on your supply chain performance
        5. **Export reports** for stakeholder communication
        
        ### 📊 Supported Data Types
        - **Excel files** (.xlsx, .xls)
        - **CSV files** (.csv)
        
        ### 🔍 Expected Data Columns
        For best results, your data should include columns related to:
        - Dates (order dates, delivery dates, etc.)
        - Products or SKUs
        - Quantities (ordered, delivered, in stock)
        - Lead times or delivery delays
        - Suppliers or vendors
        - Costs or values
        
        Upload your file to get started! 👆
        """)

def generate_report(recommendations, kpis):
    """Generate a text report of recommendations and KPIs"""
    report = f"""
SUPPLY CHAIN ANALYSIS REPORT
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

=== KEY PERFORMANCE INDICATORS ===
"""
    
    if kpis:
        for kpi_name, kpi_value in kpis.items():
            if not kpi_name.endswith('_trend'):
                report += f"{kpi_name.replace('_', ' ').title()}: {kpi_value:.2f}\n"
    
    report += "\n=== BUSINESS RECOMMENDATIONS ===\n"
    
    for i, rec in enumerate(recommendations, 1):
        report += f"""
{i}. {rec['title']} (Priority: {rec.get('priority', 'Medium')})
   Description: {rec['description']}
   Impact: {rec['impact']}
   Effort: {rec['effort']}
"""
    
    return report

if __name__ == "__main__":
    main()
