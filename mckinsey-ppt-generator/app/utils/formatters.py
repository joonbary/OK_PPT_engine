"""
Formatting utilities for the PPT generation system
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import json


def format_datetime(dt: datetime, format_string: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format datetime object to string
    
    Args:
        dt: Datetime object
        format_string: Format string
        
    Returns:
        Formatted datetime string
    """
    if not dt:
        return ""
    return dt.strftime(format_string)


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: File size in bytes
        
    Returns:
        Formatted file size string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f} minutes"
    else:
        hours = seconds / 3600
        return f"{hours:.2f} hours"


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format value as percentage
    
    Args:
        value: Value to format (0-1 range)
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    percentage = value * 100
    return f"{percentage:.{decimals}f}%"


def format_number(number: float, decimals: int = 0, thousands_separator: str = ",") -> str:
    """
    Format number with thousands separator
    
    Args:
        number: Number to format
        decimals: Number of decimal places
        thousands_separator: Separator for thousands
        
    Returns:
        Formatted number string
    """
    if decimals > 0:
        formatted = f"{number:,.{decimals}f}"
    else:
        formatted = f"{int(number):,}"
    
    if thousands_separator != ",":
        formatted = formatted.replace(",", thousands_separator)
    
    return formatted


def format_currency(amount: float, currency: str = "USD", symbol_position: str = "before") -> str:
    """
    Format currency amount
    
    Args:
        amount: Amount to format
        currency: Currency code
        symbol_position: Position of currency symbol (before/after)
        
    Returns:
        Formatted currency string
    """
    symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
        "KRW": "₩"
    }
    
    symbol = symbols.get(currency, currency)
    formatted_amount = format_number(amount, 2)
    
    if symbol_position == "before":
        return f"{symbol}{formatted_amount}"
    else:
        return f"{formatted_amount} {symbol}"


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to specified length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to append if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    truncate_at = max_length - len(suffix)
    return text[:truncate_at] + suffix


def format_list_as_bullets(items: List[str], bullet: str = "•") -> str:
    """
    Format list as bulleted text
    
    Args:
        items: List of items
        bullet: Bullet character
        
    Returns:
        Formatted bulleted list
    """
    return "\n".join([f"{bullet} {item}" for item in items])


def format_json_pretty(data: Any, indent: int = 2) -> str:
    """
    Format JSON data with pretty printing
    
    Args:
        data: Data to format
        indent: Indentation level
        
    Returns:
        Pretty-printed JSON string
    """
    return json.dumps(data, indent=indent, ensure_ascii=False, default=str)


def capitalize_words(text: str) -> str:
    """
    Capitalize first letter of each word
    
    Args:
        text: Text to capitalize
        
    Returns:
        Capitalized text
    """
    return " ".join(word.capitalize() for word in text.split())


def snake_to_camel(snake_str: str) -> str:
    """
    Convert snake_case to camelCase
    
    Args:
        snake_str: Snake case string
        
    Returns:
        Camel case string
    """
    components = snake_str.split('_')
    return components[0] + ''.join(x.capitalize() for x in components[1:])


def camel_to_snake(camel_str: str) -> str:
    """
    Convert camelCase to snake_case
    
    Args:
        camel_str: Camel case string
        
    Returns:
        Snake case string
    """
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()