import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st

class DataProcessor:
    """
    Handles data loading, cleaning, and preprocessing for supply chain data
    """
    
    def __init__(self):
        self.data = None
        self.original_data = None
    
    def load_data(self, uploaded_file):
        """
        Load data from uploaded file (CSV or Excel)
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            pd.DataFrame: Processed dataframe
        """
        try:
            # Determine file type and load accordingly
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                # Try to read Excel file, handle multiple sheets
                excel_file = pd.ExcelFile(uploaded_file)
                if len(excel_file.sheet_names) > 1:
                    # If multiple sheets, use the first one or let user choose
                    sheet_name = excel_file.sheet_names[0]
                    df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                else:
                    df = pd.read_excel(uploaded_file)
            else:
                raise ValueError("Unsupported file format")
            
            # Store original data
            self.original_data = df.copy()
            
            # Clean and process the data
            df = self.clean_data(df)
            
            # Store processed data
            self.data = df
            
            return df
            
        except Exception as e:
            raise Exception(f"Error loading file: {str(e)}")
    
    def clean_data(self, df):
        """
        Clean and preprocess the dataframe
        
        Args:
            df (pd.DataFrame): Raw dataframe
            
        Returns:
            pd.DataFrame: Cleaned dataframe
        """
        # Make a copy to avoid modifying original
        df_clean = df.copy()
        
        # Remove completely empty rows and columns
        df_clean = df_clean.dropna(how='all')
        df_clean = df_clean.dropna(axis=1, how='all')
        
        # Standardize column names
        df_clean.columns = df_clean.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Detect and convert date columns
        df_clean = self._detect_and_convert_dates(df_clean)
        
        # Convert numeric columns
        df_clean = self._convert_numeric_columns(df_clean)
        
        # Handle missing values
        df_clean = self._handle_missing_values(df_clean)
        
        return df_clean
    
    def _detect_and_convert_dates(self, df):
        """
        Detect and convert date columns
        """
        date_columns = []
        
        for col in df.columns:
            # Skip if already datetime
            if df[col].dtype == 'datetime64[ns]':
                continue
                
            # Look for date-like column names
            date_keywords = ['date', 'time', 'created', 'updated', 'delivery', 'order', 'ship']
            if any(keyword in col.lower() for keyword in date_keywords):
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                    date_columns.append(col)
                except:
                    pass
            
            # Try to convert if it looks like a date
            elif df[col].dtype == 'object':
                # Sample a few values to check if they look like dates
                sample_values = df[col].dropna().head(5).astype(str)
                date_like_count = 0
                
                for val in sample_values:
                    # Check for common date patterns
                    if any(pattern in val for pattern in ['/', '-', ':', 'T']):
                        try:
                            pd.to_datetime(val)
                            date_like_count += 1
                        except:
                            pass
                
                # If majority look like dates, convert the column
                if date_like_count >= len(sample_values) * 0.6:
                    try:
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                        date_columns.append(col)
                    except:
                        pass
        
        return df
    
    def _convert_numeric_columns(self, df):
        """
        Convert columns to numeric where appropriate
        """
        for col in df.columns:
            if df[col].dtype == 'object':
                # Try to convert to numeric
                # First, clean the column (remove currency symbols, commas, etc.)
                cleaned_series = df[col].astype(str).str.replace(r'[^\d.-]', '', regex=True)
                
                # Try to convert to numeric
                numeric_series = pd.to_numeric(cleaned_series, errors='coerce')
                
                # If more than 50% of non-null values are numeric, convert
                non_null_count = df[col].notna().sum()
                numeric_count = numeric_series.notna().sum()
                
                if non_null_count > 0 and (numeric_count / non_null_count) > 0.5:
                    df[col] = numeric_series
        
        return df
    
    def _handle_missing_values(self, df):
        """
        Handle missing values in the dataset
        """
        # For numeric columns, we'll leave NaN as is (will be handled in analysis)
        # For categorical columns, we might fill with 'Unknown' if needed
        
        for col in df.columns:
            if df[col].dtype == 'object':
                # Only fill if there are very few missing values (< 5%)
                missing_pct = df[col].isnull().sum() / len(df)
                if missing_pct < 0.05:
                    df[col] = df[col].fillna('Unknown')
        
        return df
    
    def get_data_summary(self, df):
        """
        Get a summary of the dataset
        
        Args:
            df (pd.DataFrame): Dataframe to summarize
            
        Returns:
            dict: Summary statistics
        """
        summary = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'numeric_columns': len(df.select_dtypes(include=[np.number]).columns),
            'categorical_columns': len(df.select_dtypes(include=['object', 'category']).columns),
            'date_columns': len(df.select_dtypes(include=['datetime64']).columns),
            'missing_values': df.isnull().sum().sum(),
            'duplicate_rows': df.duplicated().sum()
        }
        
        return summary
    
    def detect_supply_chain_columns(self, df):
        """
        Detect columns that are relevant for supply chain analysis
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            dict: Dictionary mapping column types to actual column names
        """
        column_mapping = {
            'date_columns': [],
            'product_columns': [],
            'quantity_columns': [],
            'cost_columns': [],
            'supplier_columns': [],
            'location_columns': [],
            'time_columns': []
        }
        
        # Define keywords for different types of columns
        keywords = {
            'product': ['product', 'item', 'sku', 'part', 'material', 'goods'],
            'quantity': ['quantity', 'qty', 'amount', 'volume', 'stock', 'inventory', 'units'],
            'cost': ['cost', 'price', 'value', 'amount', 'revenue', 'sales'],
            'supplier': ['supplier', 'vendor', 'provider', 'source'],
            'location': ['location', 'warehouse', 'site', 'region', 'zone', 'depot'],
            'time': ['lead_time', 'delivery_time', 'delay', 'duration', 'cycle_time']
        }
        
        # Check each column against keywords
        for col in df.columns:
            col_lower = col.lower()
            
            # Check for date columns (already detected)
            if df[col].dtype == 'datetime64[ns]':
                column_mapping['date_columns'].append(col)
            
            # Check for other column types
            for col_type, keyword_list in keywords.items():
                if any(keyword in col_lower for keyword in keyword_list):
                    column_mapping[f'{col_type}_columns'].append(col)
        
        return column_mapping
