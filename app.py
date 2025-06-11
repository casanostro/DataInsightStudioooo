import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io

from data_processor import DataProcessor
from kpi_calculator import KPICalculator
from recommendation_engine import RecommendationEngine
from visualizations import SupplyChainVisualizations
from translations import get_text, get_language_options

# Page configuration
st.set_page_config(
    page_title="Supply Chain Analytics & Recommendations",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Initialize session state for language
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    
    # Language selector in sidebar
    with st.sidebar:
        st.markdown("---")
        language_options = get_language_options()
        selected_language = st.selectbox(
            get_text('select_language', st.session_state.language),
            options=list(language_options.keys()),
            format_func=lambda x: language_options[x],
            index=list(language_options.keys()).index(st.session_state.language),
            key="language_selector"
        )
        
        if selected_language != st.session_state.language:
            st.session_state.language = selected_language
            st.rerun()
    
    # Use translated texts
    lang = st.session_state.language
    
    st.title(get_text('main_title', lang))
    st.markdown(get_text('main_subtitle', lang))
    
    # Initialize session state
    if 'processed_data' not in st.session_state:
        st.session_state.processed_data = None
    if 'kpis' not in st.session_state:
        st.session_state.kpis = None
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = None

    # Sidebar for file upload and filters
    with st.sidebar:
        st.header(get_text('data_upload', lang))
        uploaded_file = st.file_uploader(
            get_text('upload_file', lang),
            type=["xlsx", "csv", "xls"],
            help=get_text('upload_help', lang)
        )
        
        if uploaded_file is not None:
            # Process uploaded file
            processor = DataProcessor()
            
            try:
                with st.spinner(get_text('processing_data', lang)):
                    df = processor.load_data(uploaded_file)
                    st.session_state.processed_data = df
                    
                    # Calculate KPIs
                    kpi_calc = KPICalculator(df)
                    st.session_state.kpis = kpi_calc.calculate_all_kpis()
                    
                    # Generate recommendations
                    rec_engine = RecommendationEngine(df, st.session_state.kpis)
                    st.session_state.recommendations = rec_engine.generate_recommendations()
                
                st.success(f"{get_text('data_processed', lang)} {len(df)} {get_text('records_loaded', lang)}")
                
                # Display basic data info
                with st.expander(get_text('data_overview', lang)):
                    st.write(f"**{get_text('rows', lang)}:** {len(df)}")
                    st.write(f"**{get_text('columns', lang)}:** {len(df.columns)}")
                    st.write(f"**{get_text('column_names', lang)}:**")
                    for col in df.columns:
                        st.write(f"- {col}")
                
            except Exception as e:
                st.error(f"{get_text('error_processing', lang)} {str(e)}")
                st.info(get_text('ensure_supply_chain', lang))
                return

    # Main content area
    if st.session_state.processed_data is not None:
        df = st.session_state.processed_data
        
        # Add filters in sidebar
        with st.sidebar:
            st.header(get_text('filters', lang))
            
            # Date range filter if date columns exist
            date_columns = df.select_dtypes(include=['datetime64']).columns.tolist()
            if date_columns:
                date_col = st.selectbox(get_text('select_date_column', lang), date_columns)
                min_date = df[date_col].min().date()
                max_date = df[date_col].max().date()
                
                date_range = st.date_input(
                    get_text('date_range', lang),
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
                        f"{get_text('filter_by', lang)} {col}",
                        options=unique_values,
                        default=unique_values
                    )
                    if selected_values:
                        df = df[df[col].isin(selected_values)]
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            get_text('dashboard', lang), 
            get_text('visualizations', lang), 
            get_text('kpi_analysis', lang), 
            get_text('recommendations', lang), 
            get_text('raw_data', lang)
        ])
        
        with tab1:
            st.header(get_text('supply_chain_dashboard', lang))
            
            # KPI cards
            if st.session_state.kpis:
                kpis = st.session_state.kpis
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        get_text('service_level', lang), 
                        f"{kpis.get('service_level', 0):.1f}%",
                        delta=f"{kpis.get('service_level_trend', 0):.1f}%"
                    )
                
                with col2:
                    st.metric(
                        get_text('stock_turnover', lang), 
                        f"{kpis.get('stock_turnover', 0):.1f}x",
                        delta=f"{kpis.get('turnover_trend', 0):.1f}%"
                    )
                
                with col3:
                    st.metric(
                        get_text('otif_rate', lang), 
                        f"{kpis.get('otif_rate', 0):.1f}%",
                        delta=f"{kpis.get('otif_trend', 0):.1f}%"
                    )
                
                with col4:
                    st.metric(
                        get_text('avg_lead_time', lang), 
                        f"{kpis.get('avg_lead_time', 0):.1f} {get_text('days', lang)}",
                        delta=f"{kpis.get('lead_time_trend', 0):.1f}%"
                    )
            
            # Summary statistics
            st.subheader(get_text('data_summary', lang))
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**{get_text('numeric_summary', lang)}**")
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    st.dataframe(df[numeric_cols].describe())
                else:
                    st.info(get_text('no_numeric_columns', lang))
            
            with col2:
                st.write(f"**{get_text('data_quality', lang)}**")
                quality_metrics = {
                    get_text('total_rows', lang): len(df),
                    get_text('total_columns', lang): len(df.columns),
                    get_text('missing_values', lang): df.isnull().sum().sum(),
                    get_text('duplicate_rows', lang): df.duplicated().sum()
                }
                quality_df = pd.DataFrame(list(quality_metrics.items()), 
                                        columns=[get_text('metric', lang), get_text('value', lang)])
                st.dataframe(quality_df, hide_index=True)
        
        with tab2:
            st.header(get_text('interactive_viz', lang))
            
            viz = SupplyChainVisualizations(df)
            
            # Chart selection
            chart_type = st.selectbox(
                get_text('select_viz_type', lang),
                [get_text('distribution_analysis', lang), get_text('correlation_matrix', lang), 
                 get_text('time_series', lang), get_text('category_analysis', lang)]
            )
            
            if chart_type == get_text('distribution_analysis', lang):
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                if numeric_cols:
                    selected_col = st.selectbox(get_text('select_column', lang), numeric_cols)
                    fig = viz.create_distribution_plot(selected_col)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning(get_text('no_numeric_for_distribution', lang))
            
            elif chart_type == get_text('correlation_matrix', lang):
                fig = viz.create_correlation_matrix()
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning(get_text('not_enough_numeric', lang))
            
            elif chart_type == get_text('time_series', lang):
                date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                
                if date_cols and numeric_cols:
                    date_col = st.selectbox(get_text('select_date_column_viz', lang), date_cols)
                    value_col = st.selectbox(get_text('select_value_column', lang), numeric_cols)
                    fig = viz.create_time_series(date_col, value_col)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning(get_text('date_numeric_required', lang))
            
            elif chart_type == get_text('category_analysis', lang):
                categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                
                if categorical_cols and numeric_cols:
                    cat_col = st.selectbox(get_text('select_category_column', lang), categorical_cols)
                    val_col = st.selectbox(get_text('select_value_column', lang), numeric_cols)
                    fig = viz.create_category_analysis(cat_col, val_col)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning(get_text('category_numeric_required', lang))
        
        with tab3:
            st.header(get_text('kpi_analysis_title', lang))
            
            if st.session_state.kpis:
                kpis = st.session_state.kpis
                
                st.subheader(get_text('key_performance_indicators', lang))
                
                # Create KPI summary table
                kpi_data = []
                for kpi_name, kpi_value in kpis.items():
                    if not kpi_name.endswith('_trend'):
                        trend_key = f"{kpi_name}_trend"
                        trend_value = kpis.get(trend_key, 0)
                        
                        # Determine status based on KPI type and value
                        if 'rate' in kpi_name.lower() or 'level' in kpi_name.lower():
                            status = get_text('good', lang) if kpi_value >= 90 else get_text('average', lang) if kpi_value >= 75 else get_text('poor', lang)
                        elif 'time' in kpi_name.lower():
                            status = get_text('good', lang) if kpi_value <= 7 else get_text('average', lang) if kpi_value <= 14 else get_text('poor', lang)
                        else:
                            status = get_text('monitor', lang)
                        
                        kpi_data.append({
                            get_text('kpi', lang): kpi_name.replace('_', ' ').title(),
                            get_text('value', lang): f"{kpi_value:.2f}",
                            get_text('trend', lang): f"{trend_value:+.1f}%",
                            get_text('status', lang): status
                        })
                
                if kpi_data:
                    kpi_df = pd.DataFrame(kpi_data)
                    st.dataframe(kpi_df, hide_index=True, use_container_width=True)
                
                # Additional KPI insights
                st.subheader(get_text('kpi_insights', lang))
                
                # Performance alerts
                alerts = []
                if kpis.get('service_level', 100) < 95:
                    alerts.append(get_text('service_level_below', lang))
                if kpis.get('otif_rate', 100) < 90:
                    alerts.append(get_text('otif_needs_improvement', lang))
                if kpis.get('avg_lead_time', 0) > 14:
                    alerts.append(get_text('lead_times_long', lang))
                
                if alerts:
                    st.warning(get_text('performance_alerts', lang))
                    for alert in alerts:
                        st.write(alert)
                else:
                    st.success(get_text('metrics_acceptable', lang))
            
            else:
                st.info(get_text('kpi_after_processing', lang))
        
        with tab4:
            st.header(get_text('business_recommendations', lang))
            
            if st.session_state.recommendations:
                recommendations = st.session_state.recommendations
                
                # Priority recommendations
                st.subheader(get_text('priority_actions', lang))
                priority_recs = [r for r in recommendations if r.get('priority') == 'High']
                for i, rec in enumerate(priority_recs, 1):
                    with st.container():
                        st.markdown(f"**{i}. {rec['title']}**")
                        st.write(rec['description'])
                        st.write(f"{get_text('impact', lang)} {rec['impact']}")
                        st.write(f"{get_text('effort', lang)} {rec['effort']}")
                        st.divider()
                
                # Medium priority recommendations
                if any(r.get('priority') == 'Medium' for r in recommendations):
                    st.subheader(get_text('medium_priority_actions', lang))
                    medium_recs = [r for r in recommendations if r.get('priority') == 'Medium']
                    for i, rec in enumerate(medium_recs, 1):
                        with st.expander(f"{i}. {rec['title']}"):
                            st.write(rec['description'])
                            st.write(f"{get_text('impact', lang)} {rec['impact']}")
                            st.write(f"{get_text('effort', lang)} {rec['effort']}")
                
                # Low priority recommendations
                if any(r.get('priority') == 'Low' for r in recommendations):
                    st.subheader(get_text('future_considerations', lang))
                    low_recs = [r for r in recommendations if r.get('priority') == 'Low']
                    for i, rec in enumerate(low_recs, 1):
                        with st.expander(f"{i}. {rec['title']}"):
                            st.write(rec['description'])
                            st.write(f"{get_text('impact', lang)} {rec['impact']}")
                            st.write(f"{get_text('effort', lang)} {rec['effort']}")
                
                # Export recommendations
                st.subheader(get_text('export_recommendations', lang))
                if st.button(get_text('generate_report', lang)):
                    report_content = generate_report(recommendations, st.session_state.kpis, lang)
                    st.download_button(
                        label=get_text('download_report', lang),
                        data=report_content,
                        file_name=f"supply_chain_recommendations_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
            
            else:
                st.info(get_text('recommendations_after_analysis', lang))
        
        with tab5:
            st.header(get_text('raw_data_title', lang))
            
            st.subheader(get_text('filtered_dataset', lang))
            st.write(f"{get_text('showing_rows', lang)} {len(df)} {get_text('rows_after_filters', lang)}")
            
            # Show data with pagination
            page_size = st.selectbox(get_text('rows_per_page', lang), [10, 25, 50, 100], index=1)
            
            total_pages = (len(df) - 1) // page_size + 1
            page = st.number_input(get_text('page', lang), min_value=1, max_value=total_pages, value=1)
            
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            
            st.dataframe(df.iloc[start_idx:end_idx], use_container_width=True)
            
            # Export data
            st.subheader(get_text('export_data', lang))
            col1, col2 = st.columns(2)
            
            with col1:
                csv = df.to_csv(index=False)
                st.download_button(
                    label=get_text('download_csv', lang),
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
                    label=get_text('download_excel', lang),
                    data=buffer.getvalue(),
                    file_name=f"filtered_data_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
    else:
        # Welcome message when no data is uploaded
        st.markdown(f"""
        ## {get_text('welcome_title', lang)}
        
        {get_text('welcome_description', lang)}
        
        ### {get_text('getting_started', lang)}
        1. {get_text('step_1', lang)}
        2. {get_text('step_2', lang)}
        3. {get_text('step_3', lang)}
        4. {get_text('step_4', lang)}
        5. {get_text('step_5', lang)}
        
        ### {get_text('supported_data_types', lang)}
        - {get_text('excel_files', lang)}
        - {get_text('csv_files', lang)}
        
        ### {get_text('expected_columns', lang)}
        {get_text('expected_description', lang)}
        - {get_text('dates_info', lang)}
        - {get_text('products_info', lang)}
        - {get_text('quantities_info', lang)}
        - {get_text('lead_times_info', lang)}
        - {get_text('suppliers_info', lang)}
        - {get_text('costs_info', lang)}
        
        {get_text('upload_prompt', lang)}
        """)

def generate_report(recommendations, kpis, language='en'):
    """Generate a text report of recommendations and KPIs"""
    report = f"""
{get_text('report_title', language)}
{get_text('generated_on', language)} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{get_text('kpi_section', language)}
"""
    
    if kpis:
        for kpi_name, kpi_value in kpis.items():
            if not kpi_name.endswith('_trend'):
                report += f"{kpi_name.replace('_', ' ').title()}: {kpi_value:.2f}\n"
    
    report += f"\n{get_text('recommendations_section', language)}\n"
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            report += f"""
{i}. {rec['title']} ({get_text('priority_label', language)} {rec.get('priority', 'Medium')})
   Description: {rec['description']}
   {get_text('impact', language)} {rec['impact']}
   {get_text('effort', language)} {rec['effort']}
"""
    else:
        report += f"{get_text('no_recommendations', language)}\n"
    
    report += f"\n{get_text('report_footer', language)}"
    return report

if __name__ == "__main__":
    main()
