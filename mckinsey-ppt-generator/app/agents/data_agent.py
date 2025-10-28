"""
Data Visualization Agent for chart and graph recommendations
"""

from typing import Dict, Any, List
from .base_agent import BaseAgent


class DataVisualizationAgent(BaseAgent):
    """
    Agent responsible for data visualization recommendations
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("DataVisualizationAgent", config)
        
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        Validate input for data visualization
        """
        return "data" in input_data or "metrics" in input_data
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate data visualization recommendations
        """
        data = input_data.get("data", {})
        metrics = input_data.get("metrics", [])
        
        visualizations = []
        
        # Analyze data and recommend appropriate chart types
        if isinstance(data, dict):
            if "time_series" in str(data).lower():
                visualizations.append({
                    "type": "line_chart",
                    "title": "Trend Analysis",
                    "x_axis": "Time",
                    "y_axis": "Value",
                    "recommended": True
                })
            
            if "comparison" in str(data).lower() or len(data) > 1:
                visualizations.append({
                    "type": "bar_chart",
                    "title": "Comparative Analysis",
                    "orientation": "vertical",
                    "recommended": True
                })
            
            if "percentage" in str(data).lower() or "proportion" in str(data).lower():
                visualizations.append({
                    "type": "pie_chart",
                    "title": "Distribution Analysis",
                    "show_percentages": True,
                    "recommended": True
                })
        
        # Default visualization if no specific recommendations
        if not visualizations:
            visualizations.append({
                "type": "column_chart",
                "title": "Data Overview",
                "recommended": False
            })
        
        return {
            "visualizations": visualizations,
            "best_practices": [
                "Use consistent color schemes",
                "Limit to 5-7 data points per chart",
                "Include clear labels and legends",
                "Ensure accessibility compliance"
            ],
            "data_insights": self._analyze_data(data)
        }
    
    def _analyze_data(self, data: Any) -> List[str]:
        """
        Analyze data and provide insights
        """
        insights = []
        
        if isinstance(data, dict):
            insights.append(f"Dataset contains {len(data)} categories")
            
        if isinstance(data, list):
            insights.append(f"Dataset contains {len(data)} data points")
            
        # Add more sophisticated analysis here
        insights.append("Consider highlighting key trends")
        insights.append("Focus on actionable insights")
        
        return insights
    
    def get_capabilities(self) -> List[str]:
        """
        Get agent capabilities
        """
        return [
            "Recommend chart types",
            "Analyze data patterns",
            "Suggest visualization best practices",
            "Optimize data presentation"
        ]