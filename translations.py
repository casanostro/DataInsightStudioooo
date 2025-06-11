"""
Multilingual translations for the Supply Chain Analytics tool
Supports: French, English, Spanish (Mexican), Russian
"""

TRANSLATIONS = {
    'fr': {
        'page_title': 'Analyse de Chaîne d\'Approvisionnement et Recommandations',
        'main_title': '📊 Outil de Storytelling et Reporting de Données Supply Chain',
        'main_subtitle': 'Transformez vos données de chaîne d\'approvisionnement en recommandations business actionnables',
        
        # Sidebar
        'data_upload': '📁 Téléchargement de Données',
        'upload_file': 'Téléchargez vos données Excel/CSV',
        'upload_help': 'Téléchargez des données de chaîne d\'approvisionnement incluant stocks, ventes, délais, coûts, etc.',
        'filters': '🔍 Filtres',
        'select_date_column': 'Sélectionnez la Colonne Date',
        'date_range': 'Plage de Dates',
        'filter_by': 'Filtrer par',
        'data_overview': '📋 Aperçu des Données',
        'rows': 'Lignes',
        'columns': 'Colonnes',
        'column_names': 'Noms des Colonnes',
        
        # Processing messages
        'processing_data': 'Traitement des données téléchargées...',
        'data_processed': '✅ Données traitées avec succès !',
        'records_loaded': 'enregistrements chargés.',
        'error_processing': '❌ Erreur lors du traitement du fichier :',
        'ensure_supply_chain': 'Assurez-vous que votre fichier contient des données de chaîne d\'approvisionnement avec les colonnes appropriées.',
        
        # Tabs
        'dashboard': '📊 Tableau de Bord',
        'visualizations': '📈 Visualisations',
        'kpi_analysis': '🔍 Analyse KPI',
        'recommendations': '🧠 Recommandations',
        'raw_data': '📋 Données Brutes',
        
        # Dashboard
        'supply_chain_dashboard': 'Tableau de Bord Supply Chain',
        'service_level': 'Niveau de Service',
        'stock_turnover': 'Rotation des Stocks',
        'otif_rate': 'Taux OTIF',
        'avg_lead_time': 'Délai Moyen',
        'days': 'jours',
        'data_summary': '📋 Résumé des Données',
        'numeric_summary': 'Résumé Numérique :',
        'no_numeric_columns': 'Aucune colonne numérique trouvée pour les statistiques résumées.',
        'data_quality': 'Qualité des Données :',
        'total_rows': 'Total Lignes',
        'total_columns': 'Total Colonnes',
        'missing_values': 'Valeurs Manquantes',
        'duplicate_rows': 'Lignes Dupliquées',
        'metric': 'Métrique',
        'value': 'Valeur',
        
        # Visualizations
        'interactive_viz': '📈 Visualisations Interactives',
        'select_viz_type': 'Sélectionnez le Type de Visualisation',
        'distribution_analysis': 'Analyse de Distribution',
        'correlation_matrix': 'Matrice de Corrélation',
        'time_series': 'Série Temporelle',
        'category_analysis': 'Analyse par Catégorie',
        'select_column': 'Sélectionnez la Colonne',
        'no_numeric_for_distribution': 'Aucune colonne numérique disponible pour l\'analyse de distribution.',
        'not_enough_numeric': 'Pas assez de colonnes numériques pour l\'analyse de corrélation.',
        'select_date_column_viz': 'Sélectionnez la Colonne Date',
        'select_value_column': 'Sélectionnez la Colonne Valeur',
        'date_numeric_required': 'Colonnes de date et numériques requises pour l\'analyse de série temporelle.',
        'select_category_column': 'Sélectionnez la Colonne Catégorie',
        'category_numeric_required': 'Colonnes de catégorie et numériques requises pour l\'analyse par catégorie.',
        
        # KPI Analysis
        'kpi_analysis_title': '🔍 Analyse KPI',
        'key_performance_indicators': 'Indicateurs Clés de Performance',
        'kpi': 'KPI',
        'trend': 'Tendance',
        'status': 'Statut',
        'kpi_insights': '📊 Insights KPI',
        'performance_alerts': '**Alertes de Performance :**',
        'service_level_below': '⚠️ Niveau de service en dessous de l\'objectif (95%)',
        'otif_needs_improvement': '⚠️ Le taux OTIF nécessite une amélioration',
        'lead_times_long': '⚠️ Les délais sont plus longs qu\'idéal (>14 jours)',
        'metrics_acceptable': '✅ Toutes les métriques clés sont dans des plages acceptables',
        'kpi_after_processing': 'L\'analyse KPI apparaîtra ici une fois les données traitées.',
        
        # Recommendations
        'business_recommendations': '🧠 Recommandations Business',
        'priority_actions': '🔥 Actions Prioritaires',
        'impact': '**Impact :**',
        'effort': '**Effort :**',
        'medium_priority_actions': '📋 Actions Priorité Moyenne',
        'future_considerations': '💡 Considérations Futures',
        'export_recommendations': '📤 Exporter les Recommandations',
        'generate_report': 'Générer le Rapport',
        'download_report': 'Télécharger le Rapport',
        'recommendations_after_analysis': 'Les recommandations business apparaîtront ici une fois les données analysées.',
        
        # Raw Data
        'raw_data_title': '📋 Données Brutes',
        'filtered_dataset': 'Jeu de Données Filtré',
        'showing_rows': 'Affichage de',
        'rows_after_filters': 'lignes après application des filtres',
        'rows_per_page': 'Lignes par page',
        'page': 'Page',
        'export_data': '📤 Exporter les Données',
        'download_csv': 'Télécharger CSV',
        'download_excel': 'Télécharger Excel',
        
        # Status indicators
        'good': '🟢 Bon',
        'average': '🟡 Moyen',
        'poor': '🔴 Faible',
        'monitor': '📊 Surveiller',
        
        # Language selector
        'select_language': 'Sélectionnez la langue',
        'language': 'Langue'
    },
    
    'en': {
        'page_title': 'Supply Chain Analytics & Recommendations',
        'main_title': '📊 Supply Chain Data Storytelling & Reporting Tool',
        'main_subtitle': 'Transform your supply chain data into actionable business recommendations',
        
        # Sidebar
        'data_upload': '📁 Data Upload',
        'upload_file': 'Upload your Excel/CSV data',
        'upload_help': 'Upload supply chain data including stocks, sales, delays, costs, etc.',
        'filters': '🔍 Filters',
        'select_date_column': 'Select Date Column',
        'date_range': 'Date Range',
        'filter_by': 'Filter by',
        'data_overview': '📋 Data Overview',
        'rows': 'Rows',
        'columns': 'Columns',
        'column_names': 'Column Names',
        
        # Processing messages
        'processing_data': 'Processing uploaded data...',
        'data_processed': '✅ Data processed successfully!',
        'records_loaded': 'records loaded.',
        'error_processing': '❌ Error processing file:',
        'ensure_supply_chain': 'Please ensure your file contains supply chain data with appropriate columns.',
        
        # Tabs
        'dashboard': '📊 Dashboard',
        'visualizations': '📈 Visualizations',
        'kpi_analysis': '🔍 KPI Analysis',
        'recommendations': '🧠 Recommendations',
        'raw_data': '📋 Raw Data',
        
        # Dashboard
        'supply_chain_dashboard': 'Supply Chain Dashboard',
        'service_level': 'Service Level',
        'stock_turnover': 'Stock Turnover',
        'otif_rate': 'OTIF Rate',
        'avg_lead_time': 'Avg Lead Time',
        'days': 'days',
        'data_summary': '📋 Data Summary',
        'numeric_summary': 'Numeric Summary:',
        'no_numeric_columns': 'No numeric columns found for summary statistics.',
        'data_quality': 'Data Quality:',
        'total_rows': 'Total Rows',
        'total_columns': 'Total Columns',
        'missing_values': 'Missing Values',
        'duplicate_rows': 'Duplicate Rows',
        'metric': 'Metric',
        'value': 'Value',
        
        # Visualizations
        'interactive_viz': '📈 Interactive Visualizations',
        'select_viz_type': 'Select Visualization Type',
        'distribution_analysis': 'Distribution Analysis',
        'correlation_matrix': 'Correlation Matrix',
        'time_series': 'Time Series',
        'category_analysis': 'Category Analysis',
        'select_column': 'Select Column',
        'no_numeric_for_distribution': 'No numeric columns available for distribution analysis.',
        'not_enough_numeric': 'Not enough numeric columns for correlation analysis.',
        'select_date_column_viz': 'Select Date Column',
        'select_value_column': 'Select Value Column',
        'date_numeric_required': 'Date and numeric columns required for time series analysis.',
        'select_category_column': 'Select Category Column',
        'category_numeric_required': 'Category and numeric columns required for category analysis.',
        
        # KPI Analysis
        'kpi_analysis_title': '🔍 KPI Analysis',
        'key_performance_indicators': 'Key Performance Indicators',
        'kpi': 'KPI',
        'trend': 'Trend',
        'status': 'Status',
        'kpi_insights': '📊 KPI Insights',
        'performance_alerts': '**Performance Alerts:**',
        'service_level_below': '⚠️ Service level below target (95%)',
        'otif_needs_improvement': '⚠️ OTIF rate needs improvement',
        'lead_times_long': '⚠️ Lead times are longer than ideal (>14 days)',
        'metrics_acceptable': '✅ All key metrics are within acceptable ranges',
        'kpi_after_processing': 'KPI analysis will appear here once data is processed.',
        
        # Recommendations
        'business_recommendations': '🧠 Business Recommendations',
        'priority_actions': '🔥 Priority Actions',
        'impact': '**Impact:**',
        'effort': '**Effort:**',
        'medium_priority_actions': '📋 Medium Priority Actions',
        'future_considerations': '💡 Future Considerations',
        'export_recommendations': '📤 Export Recommendations',
        'generate_report': 'Generate Report',
        'download_report': 'Download Report',
        'recommendations_after_analysis': 'Business recommendations will appear here once data is analyzed.',
        
        # Raw Data
        'raw_data_title': '📋 Raw Data',
        'filtered_dataset': 'Filtered Dataset',
        'showing_rows': 'Showing',
        'rows_after_filters': 'rows after applying filters',
        'rows_per_page': 'Rows per page',
        'page': 'Page',
        'export_data': '📤 Export Data',
        'download_csv': 'Download CSV',
        'download_excel': 'Download Excel',
        
        # Status indicators
        'good': '🟢 Good',
        'average': '🟡 Average',
        'poor': '🔴 Poor',
        'monitor': '📊 Monitor',
        
        # Language selector
        'select_language': 'Select Language',
        'language': 'Language'
    },
    
    'es': {
        'page_title': 'Análisis de Cadena de Suministro y Recomendaciones',
        'main_title': '📊 Herramienta de Storytelling y Reportes de Datos de Cadena de Suministro',
        'main_subtitle': 'Transforme sus datos de cadena de suministro en recomendaciones empresariales accionables',
        
        # Sidebar
        'data_upload': '📁 Carga de Datos',
        'upload_file': 'Suba sus datos Excel/CSV',
        'upload_help': 'Suba datos de cadena de suministro incluyendo inventarios, ventas, retrasos, costos, etc.',
        'filters': '🔍 Filtros',
        'select_date_column': 'Seleccione Columna de Fecha',
        'date_range': 'Rango de Fechas',
        'filter_by': 'Filtrar por',
        'data_overview': '📋 Resumen de Datos',
        'rows': 'Filas',
        'columns': 'Columnas',
        'column_names': 'Nombres de Columnas',
        
        # Processing messages
        'processing_data': 'Procesando datos subidos...',
        'data_processed': '✅ ¡Datos procesados exitosamente!',
        'records_loaded': 'registros cargados.',
        'error_processing': '❌ Error procesando archivo:',
        'ensure_supply_chain': 'Por favor asegúrese de que su archivo contenga datos de cadena de suministro con columnas apropiadas.',
        
        # Tabs
        'dashboard': '📊 Tablero',
        'visualizations': '📈 Visualizaciones',
        'kpi_analysis': '🔍 Análisis KPI',
        'recommendations': '🧠 Recomendaciones',
        'raw_data': '📋 Datos Crudos',
        
        # Dashboard
        'supply_chain_dashboard': 'Tablero de Cadena de Suministro',
        'service_level': 'Nivel de Servicio',
        'stock_turnover': 'Rotación de Inventario',
        'otif_rate': 'Tasa OTIF',
        'avg_lead_time': 'Tiempo de Entrega Promedio',
        'days': 'días',
        'data_summary': '📋 Resumen de Datos',
        'numeric_summary': 'Resumen Numérico:',
        'no_numeric_columns': 'No se encontraron columnas numéricas para estadísticas de resumen.',
        'data_quality': 'Calidad de Datos:',
        'total_rows': 'Total de Filas',
        'total_columns': 'Total de Columnas',
        'missing_values': 'Valores Faltantes',
        'duplicate_rows': 'Filas Duplicadas',
        'metric': 'Métrica',
        'value': 'Valor',
        
        # Visualizations
        'interactive_viz': '📈 Visualizaciones Interactivas',
        'select_viz_type': 'Seleccione Tipo de Visualización',
        'distribution_analysis': 'Análisis de Distribución',
        'correlation_matrix': 'Matriz de Correlación',
        'time_series': 'Serie de Tiempo',
        'category_analysis': 'Análisis por Categoría',
        'select_column': 'Seleccione Columna',
        'no_numeric_for_distribution': 'No hay columnas numéricas disponibles para análisis de distribución.',
        'not_enough_numeric': 'No hay suficientes columnas numéricas para análisis de correlación.',
        'select_date_column_viz': 'Seleccione Columna de Fecha',
        'select_value_column': 'Seleccione Columna de Valor',
        'date_numeric_required': 'Se requieren columnas de fecha y numéricas para análisis de serie de tiempo.',
        'select_category_column': 'Seleccione Columna de Categoría',
        'category_numeric_required': 'Se requieren columnas de categoría y numéricas para análisis por categoría.',
        
        # KPI Analysis
        'kpi_analysis_title': '🔍 Análisis KPI',
        'key_performance_indicators': 'Indicadores Clave de Rendimiento',
        'kpi': 'KPI',
        'trend': 'Tendencia',
        'status': 'Estado',
        'kpi_insights': '📊 Insights KPI',
        'performance_alerts': '**Alertas de Rendimiento:**',
        'service_level_below': '⚠️ Nivel de servicio por debajo del objetivo (95%)',
        'otif_needs_improvement': '⚠️ La tasa OTIF necesita mejora',
        'lead_times_long': '⚠️ Los tiempos de entrega son más largos de lo ideal (>14 días)',
        'metrics_acceptable': '✅ Todas las métricas clave están dentro de rangos aceptables',
        'kpi_after_processing': 'El análisis KPI aparecerá aquí una vez que se procesen los datos.',
        
        # Recommendations
        'business_recommendations': '🧠 Recomendaciones Empresariales',
        'priority_actions': '🔥 Acciones Prioritarias',
        'impact': '**Impacto:**',
        'effort': '**Esfuerzo:**',
        'medium_priority_actions': '📋 Acciones de Prioridad Media',
        'future_considerations': '💡 Consideraciones Futuras',
        'export_recommendations': '📤 Exportar Recomendaciones',
        'generate_report': 'Generar Reporte',
        'download_report': 'Descargar Reporte',
        'recommendations_after_analysis': 'Las recomendaciones empresariales aparecerán aquí una vez que se analicen los datos.',
        
        # Raw Data
        'raw_data_title': '📋 Datos Crudos',
        'filtered_dataset': 'Conjunto de Datos Filtrado',
        'showing_rows': 'Mostrando',
        'rows_after_filters': 'filas después de aplicar filtros',
        'rows_per_page': 'Filas por página',
        'page': 'Página',
        'export_data': '📤 Exportar Datos',
        'download_csv': 'Descargar CSV',
        'download_excel': 'Descargar Excel',
        
        # Status indicators
        'good': '🟢 Bueno',
        'average': '🟡 Promedio',
        'poor': '🔴 Malo',
        'monitor': '📊 Monitorear',
        
        # Language selector
        'select_language': 'Seleccionar Idioma',
        'language': 'Idioma'
    },
    
    'ru': {
        'page_title': 'Аналитика цепи поставок и рекомендации',
        'main_title': '📊 Инструмент визуализации и отчетности данных цепи поставок',
        'main_subtitle': 'Превратите данные цепи поставок в практические бизнес-рекомендации',
        
        # Sidebar
        'data_upload': '📁 Загрузка данных',
        'upload_file': 'Загрузите ваши данные Excel/CSV',
        'upload_help': 'Загрузите данные цепи поставок, включая запасы, продажи, задержки, затраты и т.д.',
        'filters': '🔍 Фильтры',
        'select_date_column': 'Выберите столбец даты',
        'date_range': 'Диапазон дат',
        'filter_by': 'Фильтровать по',
        'data_overview': '📋 Обзор данных',
        'rows': 'Строки',
        'columns': 'Столбцы',
        'column_names': 'Названия столбцов',
        
        # Processing messages
        'processing_data': 'Обработка загруженных данных...',
        'data_processed': '✅ Данные успешно обработаны!',
        'records_loaded': 'записей загружено.',
        'error_processing': '❌ Ошибка обработки файла:',
        'ensure_supply_chain': 'Пожалуйста, убедитесь, что ваш файл содержит данные цепи поставок с соответствующими столбцами.',
        
        # Tabs
        'dashboard': '📊 Панель управления',
        'visualizations': '📈 Визуализации',
        'kpi_analysis': '🔍 Анализ KPI',
        'recommendations': '🧠 Рекомендации',
        'raw_data': '📋 Сырые данные',
        
        # Dashboard
        'supply_chain_dashboard': 'Панель управления цепи поставок',
        'service_level': 'Уровень сервиса',
        'stock_turnover': 'Оборачиваемость запасов',
        'otif_rate': 'Показатель OTIF',
        'avg_lead_time': 'Среднее время выполнения',
        'days': 'дней',
        'data_summary': '📋 Сводка данных',
        'numeric_summary': 'Числовая сводка:',
        'no_numeric_columns': 'Числовые столбцы не найдены для сводной статистики.',
        'data_quality': 'Качество данных:',
        'total_rows': 'Всего строк',
        'total_columns': 'Всего столбцов',
        'missing_values': 'Пропущенные значения',
        'duplicate_rows': 'Дублированные строки',
        'metric': 'Метрика',
        'value': 'Значение',
        
        # Visualizations
        'interactive_viz': '📈 Интерактивные визуализации',
        'select_viz_type': 'Выберите тип визуализации',
        'distribution_analysis': 'Анализ распределения',
        'correlation_matrix': 'Корреляционная матрица',
        'time_series': 'Временные ряды',
        'category_analysis': 'Анализ по категориям',
        'select_column': 'Выберите столбец',
        'no_numeric_for_distribution': 'Нет числовых столбцов для анализа распределения.',
        'not_enough_numeric': 'Недостаточно числовых столбцов для корреляционного анализа.',
        'select_date_column_viz': 'Выберите столбец даты',
        'select_value_column': 'Выберите столбец значений',
        'date_numeric_required': 'Для анализа временных рядов требуются столбцы даты и числовые столбцы.',
        'select_category_column': 'Выберите столбец категории',
        'category_numeric_required': 'Для анализа по категориям требуются столбцы категорий и числовые столбцы.',
        
        # KPI Analysis
        'kpi_analysis_title': '🔍 Анализ KPI',
        'key_performance_indicators': 'Ключевые показатели эффективности',
        'kpi': 'KPI',
        'trend': 'Тренд',
        'status': 'Статус',
        'kpi_insights': '📊 Аналитические выводы KPI',
        'performance_alerts': '**Предупреждения о производительности:**',
        'service_level_below': '⚠️ Уровень сервиса ниже цели (95%)',
        'otif_needs_improvement': '⚠️ Показатель OTIF требует улучшения',
        'lead_times_long': '⚠️ Время выполнения дольше идеального (>14 дней)',
        'metrics_acceptable': '✅ Все ключевые метрики в пределах допустимых диапазонов',
        'kpi_after_processing': 'Анализ KPI появится здесь после обработки данных.',
        
        # Recommendations
        'business_recommendations': '🧠 Бизнес-рекомендации',
        'priority_actions': '🔥 Приоритетные действия',
        'impact': '**Влияние:**',
        'effort': '**Усилия:**',
        'medium_priority_actions': '📋 Действия средней приоритетности',
        'future_considerations': '💡 Будущие соображения',
        'export_recommendations': '📤 Экспорт рекомендаций',
        'generate_report': 'Создать отчет',
        'download_report': 'Скачать отчет',
        'recommendations_after_analysis': 'Бизнес-рекомендации появятся здесь после анализа данных.',
        
        # Raw Data
        'raw_data_title': '📋 Сырые данные',
        'filtered_dataset': 'Отфильтрованный набор данных',
        'showing_rows': 'Показано',
        'rows_after_filters': 'строк после применения фильтров',
        'rows_per_page': 'Строк на странице',
        'page': 'Страница',
        'export_data': '📤 Экспорт данных',
        'download_csv': 'Скачать CSV',
        'download_excel': 'Скачать Excel',
        
        # Status indicators
        'good': '🟢 Хорошо',
        'average': '🟡 Средне',
        'poor': '🔴 Плохо',
        'monitor': '📊 Мониторить',
        
        # Language selector
        'select_language': 'Выберите язык',
        'language': 'Язык'
    }
}

def get_text(key, language='en'):
    """
    Get translated text for a given key and language
    
    Args:
        key (str): Translation key
        language (str): Language code ('en', 'fr', 'es', 'ru')
    
    Returns:
        str: Translated text or key if not found
    """
    return TRANSLATIONS.get(language, {}).get(key, TRANSLATIONS.get('en', {}).get(key, key))

def get_language_options():
    """
    Get available language options for selection
    
    Returns:
        dict: Dictionary mapping language codes to display names
    """
    return {
        'en': 'English',
        'fr': 'Français',
        'es': 'Español (México)',
        'ru': 'Русский'
    }