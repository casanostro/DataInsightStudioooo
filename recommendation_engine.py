import pandas as pd
import numpy as np
from datetime import datetime

class RecommendationEngine:
    """
    Generates business recommendations based on supply chain KPIs and data analysis
    """
    
    def __init__(self, data, kpis):
        """
        Initialize with supply chain data and calculated KPIs
        
        Args:
            data (pd.DataFrame): Supply chain dataset
            kpis (dict): Calculated KPIs
        """
        self.data = data
        self.kpis = kpis
        self.recommendations = []
    
    def generate_recommendations(self):
        """
        Generate comprehensive business recommendations
        
        Returns:
            list: List of recommendation dictionaries
        """
        self.recommendations = []
        
        # Generate recommendations based on different KPIs
        self._analyze_service_level()
        self._analyze_otif_performance()
        self._analyze_lead_times()
        self._analyze_stock_turnover()
        self._analyze_cost_efficiency()
        self._analyze_data_quality()
        self._generate_strategic_recommendations()
        
        # Sort recommendations by priority
        priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
        self.recommendations.sort(key=lambda x: priority_order.get(x.get('priority', 'Medium'), 1))
        
        return self.recommendations
    
    def _analyze_service_level(self):
        """
        Analyze service level performance and generate recommendations
        """
        service_level = self.kpis.get('service_level', 85)
        
        if service_level < 90:
            priority = 'High' if service_level < 80 else 'Medium'
            
            self.recommendations.append({
                'title': 'Improve Service Level Performance',
                'description': f'Current service level of {service_level:.1f}% is below industry benchmark of 90%. Consider implementing demand forecasting improvements, safety stock optimization, and supplier performance management programs.',
                'impact': 'High - Direct impact on customer satisfaction and retention',
                'effort': 'Medium - Requires process improvements and supplier collaboration',
                'priority': priority,
                'category': 'Service Excellence'
            })
            
            # Additional specific recommendations based on data
            if self._has_columns(['supplier', 'vendor']):
                self.recommendations.append({
                    'title': 'Implement Supplier Scorecards',
                    'description': 'Establish supplier performance scorecards to track delivery reliability, quality, and responsiveness. Focus improvement efforts on underperforming suppliers.',
                    'impact': 'Medium - Improved supplier accountability and performance',
                    'effort': 'Low - Can be implemented with existing data',
                    'priority': 'Medium',
                    'category': 'Supplier Management'
                })
        
        elif service_level > 98:
            self.recommendations.append({
                'title': 'Optimize Service Level Costs',
                'description': f'Service level of {service_level:.1f}% is exceptionally high. Evaluate if this level of service is cost-effective or if resources can be optimized without significantly impacting customer satisfaction.',
                'impact': 'Medium - Potential cost savings',
                'effort': 'Low - Analysis and minor adjustments',
                'priority': 'Low',
                'category': 'Cost Optimization'
            })
    
    def _analyze_otif_performance(self):
        """
        Analyze On-Time In-Full delivery performance
        """
        otif_rate = self.kpis.get('otif_rate', 82)
        
        if otif_rate < 85:
            priority = 'High' if otif_rate < 75 else 'Medium'
            
            self.recommendations.append({
                'title': 'Enhance OTIF Delivery Performance',
                'description': f'OTIF rate of {otif_rate:.1f}% needs improvement. Focus on production planning accuracy, transportation reliability, and inventory positioning. Implement exception management processes for critical orders.',
                'impact': 'High - Critical for customer satisfaction and competitive advantage',
                'effort': 'High - Requires cross-functional coordination',
                'priority': priority,
                'category': 'Delivery Excellence'
            })
            
            # Time-based recommendations if date data available
            if self._has_date_columns():
                self.recommendations.append({
                    'title': 'Implement Real-time Order Tracking',
                    'description': 'Deploy real-time order tracking and early warning systems to identify potential delays before they impact customer deliveries.',
                    'impact': 'Medium - Proactive issue resolution',
                    'effort': 'Medium - Technology implementation required',
                    'priority': 'Medium',
                    'category': 'Technology Enhancement'
                })
    
    def _analyze_lead_times(self):
        """
        Analyze lead time performance
        """
        avg_lead_time = self.kpis.get('avg_lead_time', 10)
        lead_time_variance = self.kpis.get('lead_time_variance', 3)
        
        if avg_lead_time > 14:
            self.recommendations.append({
                'title': 'Reduce Average Lead Times',
                'description': f'Current average lead time of {avg_lead_time:.1f} days is above optimal range. Investigate bottlenecks in the supply chain, streamline processes, and consider supplier consolidation or relocation.',
                'impact': 'High - Reduced working capital and improved customer responsiveness',
                'effort': 'High - Requires supply chain redesign',
                'priority': 'High',
                'category': 'Process Optimization'
            })
        
        if lead_time_variance and lead_time_variance > avg_lead_time * 0.3:
            self.recommendations.append({
                'title': 'Improve Lead Time Consistency',
                'description': f'High lead time variance ({lead_time_variance:.1f} days) indicates unpredictable delivery performance. Focus on process standardization and supplier performance management.',
                'impact': 'Medium - More predictable planning and customer expectations',
                'effort': 'Medium - Process improvements and supplier training',
                'priority': 'Medium',
                'category': 'Process Standardization'
            })
    
    def _analyze_stock_turnover(self):
        """
        Analyze inventory turnover performance
        """
        stock_turnover = self.kpis.get('stock_turnover', 6)
        
        if stock_turnover < 4:
            self.recommendations.append({
                'title': 'Improve Inventory Turnover',
                'description': f'Stock turnover of {stock_turnover:.1f}x is below optimal range. Consider implementing ABC analysis, reducing slow-moving inventory, and improving demand forecasting accuracy.',
                'impact': 'High - Reduced carrying costs and improved cash flow',
                'effort': 'Medium - Inventory management process improvements',
                'priority': 'High',
                'category': 'Inventory Optimization'
            })
            
            # Product-specific analysis if available
            if self._has_columns(['product', 'item', 'sku']):
                self.recommendations.append({
                    'title': 'Implement SKU Rationalization',
                    'description': 'Conduct SKU-level analysis to identify slow-moving products. Consider discontinuing low-turnover items or implementing different inventory strategies for different product categories.',
                    'impact': 'Medium - Simplified operations and reduced costs',
                    'effort': 'Medium - Analysis and stakeholder alignment required',
                    'priority': 'Medium',
                    'category': 'Product Portfolio'
                })
        
        elif stock_turnover > 12:
            self.recommendations.append({
                'title': 'Evaluate Stock-out Risks',
                'description': f'Very high stock turnover ({stock_turnover:.1f}x) may indicate potential stock-out risks. Ensure adequate safety stock levels while maintaining efficiency.',
                'impact': 'Medium - Balance between efficiency and service level',
                'effort': 'Low - Safety stock analysis and adjustment',
                'priority': 'Low',
                'category': 'Risk Management'
            })
    
    def _analyze_cost_efficiency(self):
        """
        Analyze cost-related metrics and generate recommendations
        """
        if 'total_cost' in self.kpis and 'cost_variance' in self.kpis:
            cost_variance = self.kpis['cost_variance']
            total_cost = self.kpis['total_cost']
            
            # High cost variance indicates inconsistent pricing/costs
            if cost_variance > total_cost * 0.1:  # If variance is more than 10% of total
                self.recommendations.append({
                    'title': 'Standardize Cost Management',
                    'description': 'High cost variance detected. Implement standardized pricing agreements, volume discounts, and cost monitoring processes to reduce cost volatility.',
                    'impact': 'Medium - More predictable cost structure',
                    'effort': 'Medium - Contract renegotiation and process implementation',
                    'priority': 'Medium',
                    'category': 'Cost Management'
                })
        
        # General cost optimization recommendations
        if self._has_columns(['supplier', 'vendor']):
            self.recommendations.append({
                'title': 'Explore Supplier Consolidation',
                'description': 'Analyze supplier base for consolidation opportunities. Reducing supplier count can lead to better pricing, simplified management, and improved relationships.',
                'impact': 'Medium - Cost savings and operational efficiency',
                'effort': 'High - Requires supplier evaluation and migration',
                'priority': 'Low',
                'category': 'Strategic Sourcing'
            })
    
    def _analyze_data_quality(self):
        """
        Analyze data quality and recommend improvements
        """
        total_rows = len(self.data)
        missing_values = self.data.isnull().sum().sum()
        missing_percentage = (missing_values / (total_rows * len(self.data.columns))) * 100
        
        if missing_percentage > 10:
            self.recommendations.append({
                'title': 'Improve Data Quality',
                'description': f'Data completeness is {100-missing_percentage:.1f}%. Implement data governance processes, mandatory field validation, and regular data quality audits to improve analytics accuracy.',
                'impact': 'High - Better decision-making and accurate analytics',
                'effort': 'Medium - Process and system improvements',
                'priority': 'Medium',
                'category': 'Data Management'
            })
        
        # Check for date range coverage
        date_columns = self.data.select_dtypes(include=['datetime64']).columns
        if len(date_columns) > 0:
            date_col = date_columns[0]
            date_range = (self.data[date_col].max() - self.data[date_col].min()).days
            
            if date_range < 90:  # Less than 3 months of data
                self.recommendations.append({
                    'title': 'Expand Historical Data Collection',
                    'description': 'Limited historical data range may impact trend analysis and forecasting accuracy. Consider extending data collection period for better insights.',
                    'impact': 'Medium - Improved forecasting and trend analysis',
                    'effort': 'Low - Data collection process adjustment',
                    'priority': 'Low',
                    'category': 'Analytics Enhancement'
                })
    
    def _generate_strategic_recommendations(self):
        """
        Generate strategic, high-level recommendations
        """
        # Digital transformation recommendation
        self.recommendations.append({
            'title': 'Implement Supply Chain Digitalization',
            'description': 'Consider implementing advanced analytics, AI-powered forecasting, and IoT solutions for real-time supply chain visibility and predictive capabilities.',
            'impact': 'High - Competitive advantage and operational excellence',
            'effort': 'High - Significant technology investment required',
            'priority': 'Low',
            'category': 'Digital Transformation'
        })
        
        # Sustainability recommendation
        self.recommendations.append({
            'title': 'Develop Sustainability Metrics',
            'description': 'Incorporate environmental and sustainability KPIs into supply chain performance measurement. Track carbon footprint, sustainable sourcing, and circular economy initiatives.',
            'impact': 'Medium - Brand value and regulatory compliance',
            'effort': 'Medium - New metrics and reporting processes',
            'priority': 'Low',
            'category': 'Sustainability'
        })
        
        # Risk management recommendation
        if len(self.recommendations) > 3:  # Only if there are performance issues
            self.recommendations.append({
                'title': 'Implement Risk Management Framework',
                'description': 'Given the identified performance gaps, establish a comprehensive supply chain risk management framework including supplier risk assessment, scenario planning, and contingency procedures.',
                'impact': 'High - Business continuity and resilience',
                'effort': 'High - Cross-functional initiative required',
                'priority': 'Medium',
                'category': 'Risk Management'
            })
    
    def _has_columns(self, keywords):
        """
        Check if data contains columns with specific keywords
        """
        for col in self.data.columns:
            if any(keyword.lower() in col.lower() for keyword in keywords):
                return True
        return False
    
    def _has_date_columns(self):
        """
        Check if data contains date columns
        """
        return len(self.data.select_dtypes(include=['datetime64']).columns) > 0
    
    def get_recommendation_summary(self):
        """
        Get a summary of recommendations by priority and category
        """
        summary = {
            'total_recommendations': len(self.recommendations),
            'by_priority': {},
            'by_category': {}
        }
        
        for rec in self.recommendations:
            priority = rec.get('priority', 'Medium')
            category = rec.get('category', 'General')
            
            summary['by_priority'][priority] = summary['by_priority'].get(priority, 0) + 1
            summary['by_category'][category] = summary['by_category'].get(category, 0) + 1
        
        return summary
