"""
Column Mapper Module - BOM Reconciliation Application
Intelligent column mapping with fuzzy matching
Author: Master Engineer Erik Armenta
"""

import pandas as pd
from difflib import SequenceMatcher
from typing import Dict, Optional, Tuple, List

from config import (
    COLUMN_PATTERNS, SAP_COLUMN_PATTERNS, HPLM_COLUMN_PATTERNS,
    SIMILARITY_THRESHOLD, HIGH_SIMILARITY_THRESHOLD
)


def calculate_similarity(str1: str, str2: str) -> float:
    """
    Calculate similarity between two strings using SequenceMatcher.
    
    Args:
        str1: First string
        str2: Second string
        
    Returns:
        Similarity score between 0.0 and 1.0
    """
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()


def find_similar_columns(
    df_columns: List[str],
    target_patterns: List[str],
    threshold: float = SIMILARITY_THRESHOLD
) -> Tuple[Optional[str], float]:
    """
    Find the most similar column name from a DataFrame based on target patterns.
    
    Args:
        df_columns: List of column names from DataFrame
        target_patterns: List of pattern strings to match against
        threshold: Minimum similarity threshold
        
    Returns:
        Tuple of (best_match_column, confidence_score)
        Returns (None, 0.0) if no match above threshold
    """
    best_match = None
    best_score = 0.0
    
    for col in df_columns:
        col_lower = str(col).lower().strip()
        
        for pattern in target_patterns:
            # Exact match gets highest score
            if col_lower == pattern.lower():
                return col, 1.0
            
            # Check if pattern is contained in column name
            if pattern.lower() in col_lower or col_lower in pattern.lower():
                score = 0.9
                if score > best_score:
                    best_score = score
                    best_match = col
            
            # Fuzzy matching
            similarity = calculate_similarity(col_lower, pattern)
            if similarity > best_score and similarity >= threshold:
                best_score = similarity
                best_match = col
    
    return best_match, best_score


def map_bom_columns(df: pd.DataFrame, source_name: str = "") -> Dict[str, any]:
    """
    Map DataFrame columns to standardized BOM column names.
    
    Args:
        df: DataFrame to map
        source_name: Name of the source (SAP or HPLM)
        
    Returns:
        Dictionary with mapping results
    """
    mapping = {}
    missing_columns = []
    
    df_columns = df.columns.tolist()
    
    # Select appropriate patterns based on source
    if source_name == "SAP":
        patterns_dict = SAP_COLUMN_PATTERNS
    elif source_name == "HPLM":
        patterns_dict = HPLM_COLUMN_PATTERNS
    else:
        patterns_dict = COLUMN_PATTERNS
    
    # Map each required column type
    for col_type, patterns in patterns_dict.items():
        matched_col, confidence = find_similar_columns(df_columns, patterns)
        
        if matched_col:
            mapping[col_type] = {
                'column': matched_col,
                'confidence': confidence
            }
        else:
            mapping[col_type] = {
                'column': None,
                'confidence': 0.0
            }
            missing_columns.append(col_type)
    
    # Validate mapping - part_number is critical
    is_valid = mapping['part_number']['column'] is not None
    
    mapping['is_valid'] = is_valid
    mapping['missing_columns'] = missing_columns
    mapping['source_name'] = source_name
    
    return mapping


def validate_mapping(mapping: Dict) -> Tuple[bool, str]:
    """
    Validate that critical columns are mapped.
    
    Args:
        mapping: Mapping dictionary from map_bom_columns
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not mapping['is_valid']:
        missing = ', '.join(mapping['missing_columns'])
        return False, f"No se pudo mapear columnas críticas: {missing}"
    
    # Check confidence for part_number
    if mapping['part_number']['confidence'] < SIMILARITY_THRESHOLD:
        return False, f"Confianza baja en mapeo de Part Number ({mapping['part_number']['confidence']:.2f})"
    
    return True, ""


def create_standardized_dataframe(df: pd.DataFrame, mapping: Dict) -> pd.DataFrame:
    """
    Create a new DataFrame with standardized column names based on mapping.
    
    Args:
        df: Original DataFrame
        mapping: Mapping dictionary from map_bom_columns
        
    Returns:
        DataFrame with standardized column names
    """
    df_standardized = pd.DataFrame()
    
    # Map columns to standardized names
    for col_type in ['part_number', 'quantity', 'unit', 'description']:
        if mapping[col_type]['column']:
            df_standardized[col_type] = df[mapping[col_type]['column']].copy()
        else:
            # Create empty column if not mapped
            df_standardized[col_type] = None
    
    # Add source identifier
    df_standardized['source'] = mapping.get('source_name', 'Unknown')
    
    return df_standardized


def get_mapping_summary(mapping: Dict) -> str:
    """
    Generate a human-readable summary of the column mapping.
    
    Args:
        mapping: Mapping dictionary from map_bom_columns
        
    Returns:
        Formatted string with mapping summary
    """
    summary_lines = []
    
    for col_type in ['part_number', 'quantity', 'unit', 'description']:
        col_info = mapping[col_type]
        if col_info['column']:
            confidence_pct = col_info['confidence'] * 100
            emoji = "✅" if col_info['confidence'] >= HIGH_SIMILARITY_THRESHOLD else "⚠️"
            summary_lines.append(
                f"{emoji} **{col_type.replace('_', ' ').title()}**: "
                f"`{col_info['column']}` (Confianza: {confidence_pct:.0f}%)"
            )
        else:
            summary_lines.append(
                f"❌ **{col_type.replace('_', ' ').title()}**: No mapeado"
            )
    
    return "\n".join(summary_lines)
