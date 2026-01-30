"""Evidently AI monitoring setup"""

from typing import Dict, List, Optional
from src.config import settings

# Evidently will be imported when needed
evidently_available = False
try:
    from evidently import ColumnMapping
    from evidently.metric_preset import DataDriftPreset, DataQualityPreset
    from evidently.report import Report
    evidently_available = True
except ImportError:
    print("Warning: Evidently not available")


class EvidentlyMonitor:
    """Evidently AI monitoring for RAG system"""
    
    def __init__(self):
        self.reference_data: Optional[List[Dict]] = None
        self.column_mapping = ColumnMapping(
            target=None,
            prediction="answer",
            numerical_features=["answer_length", "retrieval_count"],
            categorical_features=["model", "status"]
        )
    
    def set_reference_data(self, data: List[Dict]):
        """Set reference data for drift detection"""
        self.reference_data = data
    
    def check_data_quality(self, current_data: List[Dict]) -> Dict:
        """Check data quality"""
        if not evidently_available or not self.reference_data:
            return {}
        
        report = Report(metrics=[DataQualityPreset()])
        report.run(
            reference_data=self.reference_data,
            current_data=current_data,
            column_mapping=self.column_mapping
        )
        
        return report.as_dict()
    
    def check_data_drift(self, current_data: List[Dict]) -> Dict:
        """Check for data drift"""
        if not evidently_available or not self.reference_data:
            return {}
        
        report = Report(metrics=[DataDriftPreset()])
        report.run(
            reference_data=self.reference_data,
            current_data=current_data,
            column_mapping=self.column_mapping
        )
        
        return report.as_dict()


evidently_monitor = EvidentlyMonitor()


def setup_evidently_monitoring():
    """Setup Evidently monitoring"""
    if not settings.enable_evidently:
        return
    
    if not evidently_available:
        print("Warning: Evidently not installed, skipping setup")
        return
    
    print("Evidently monitoring enabled")



