import pandas as pd
import re
from typing import List, Dict, Set


class MetricGrouper:
    """
    Flexible column grouping system for extracting related metrics from large datasets.
    Uses keyword-based pattern matching instead of hardcoded column names.
    """

    def __init__(self, df: pd.DataFrame):
        """Initialize with a pandas DataFrame."""
        self.df = df
        self.columns = df.columns.tolist()

    def find_columns_by_keywords(
        self, keywords: List[str], exclude_keywords: List[str] = None, case_sensitive: bool = False
    ) -> List[str]:
        """
        Find columns containing any of the specified keywords.

        Args:
            keywords: List of keywords to search for in column names
            exclude_keywords: Keywords to exclude from results
            case_sensitive: Whether to match case-sensitively

        Returns:
            List of matching column names
        """
        exclude_keywords = exclude_keywords or []
        matches = []

        for col in self.columns:
            # Clean column name (remove 'additional_info.' prefix for matching)
            clean_col = col.replace("additional_info.", "")

            # Convert to lowercase if not case sensitive
            search_col = clean_col if case_sensitive else clean_col.lower()

            # Check if any keyword matches
            keyword_match = any((kw if case_sensitive else kw.lower()) in search_col for kw in keywords)

            # Check if any exclude keyword matches
            exclude_match = any((kw if case_sensitive else kw.lower()) in search_col for kw in exclude_keywords)

            if keyword_match and not exclude_match:
                matches.append(col)

        return matches

    def get_metric_subset(
        self, group_name: str, keywords: List[str], exclude_keywords: List[str] = None
    ) -> pd.DataFrame:
        """
        Extract a subset of the dataframe for a specific metric group.

        Args:
            group_name: Name for this metric group (for display)
            keywords: Keywords to identify relevant columns
            exclude_keywords: Keywords to exclude

        Returns:
            DataFrame with only the matching columns (plus 'name' if it exists)
        """
        matching_cols = self.find_columns_by_keywords(keywords, exclude_keywords)

        # Always include 'name' column if it exists
        if "name" in self.columns:
            result_cols = ["name"] + [col for col in matching_cols if col != "name"]
        else:
            result_cols = matching_cols

        return self.df[result_cols].copy()

    def preview_group(
        self, group_name: str, keywords: List[str], exclude_keywords: List[str] = None, limit: int = 5
    ) -> Dict:
        """
        Preview what columns would be extracted for a metric group.

        Returns:
            Dictionary with group info and sample data
        """
        matching_cols = self.find_columns_by_keywords(keywords, exclude_keywords)
        subset = self.get_metric_subset(group_name, keywords, exclude_keywords)

        return {
            "group_name": group_name,
            "num_columns": len(matching_cols),
            "columns": matching_cols,
            "sample_data": subset.head(limit),
        }

    def discover_patterns(self, sample_size: int = 10) -> Dict[str, List[str]]:
        """
        Discover common patterns in column names to help identify groupings.

        Returns:
            Dictionary of pattern categories with example columns
        """
        patterns = {
            "goals": [],
            "shots": [],
            "corners": [],
            "cards": [],
            "possession": [],
            "fouls": [],
            "xg": [],
            "percentage": [],
            "avg": [],
            "total": [],
        }

        for col in self.columns[:sample_size]:
            clean_col = col.replace("additional_info.", "").lower()
            for pattern in patterns.keys():
                if pattern in clean_col:
                    patterns[pattern].append(col)

        return {k: v for k, v in patterns.items() if v}
