"""
Base Agent class for AI-powered PPT generation
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from loguru import logger


class BaseAgent(ABC):
    """
    Abstract base class for all AI agents in the PPT generation system
    """
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize base agent
        
        Args:
            name: Name of the agent
            config: Configuration dictionary for the agent
        """
        self.name = name
        self.config = config or {}
        self.logger = logger.bind(agent=name)
        
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data and return results
        
        Args:
            input_data: Input data for processing
            
        Returns:
            Processed results
        """
        pass
    
    @abstractmethod
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        Validate input data before processing
        
        Args:
            input_data: Input data to validate
            
        Returns:
            True if input is valid, False otherwise
        """
        pass
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute agent processing with validation
        
        Args:
            input_data: Input data for processing
            
        Returns:
            Processing results with metadata
        """
        try:
            # Validate input
            if not await self.validate_input(input_data):
                return {
                    "success": False,
                    "error": "Invalid input data",
                    "agent": self.name
                }
            
            # Process data
            result = await self.process(input_data)
            
            return {
                "success": True,
                "result": result,
                "agent": self.name
            }
            
        except Exception as e:
            self.logger.error(f"Agent execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }
    
    def get_capabilities(self) -> List[str]:
        """
        Get list of agent capabilities
        
        Returns:
            List of capability descriptions
        """
        return []
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get agent configuration
        
        Returns:
            Configuration dictionary
        """
        return self.config