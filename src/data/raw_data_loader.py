import os
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional

class RawDataLoader:
    """
    A class to handle the loading of raw Olist dataset files securely and immutably.
    This loader strictly reads CSV files and returns pandas DataFrames without performing any cleaning,
    transformation, or data modification.
    """
    
    # Expected core datasets in the Olist bundle
    EXPECTED_FILES = {
        "customers": "olist_customers_dataset.csv",
        "geolocation": "olist_geolocation_dataset.csv",
        "orders": "olist_orders_dataset.csv",
        "order_items": "olist_order_items_dataset.csv",
        "order_payments": "olist_order_payments_dataset.csv",
        "order_reviews": "olist_order_reviews_dataset.csv",
        "products": "olist_products_dataset.csv",
        "sellers": "olist_sellers_dataset.csv",
        "product_category_translation": "product_category_name_translation.csv"
    }
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize the RawDataLoader.
        
        Args:
            data_dir (str, optional): The base directory for the raw data. 
                                      Defaults to the project root's 'data/raw/olist'.
        """
        if data_dir is None:
            # Resolve relative to the project root assuming this file is under src/data/
            project_root = Path(__file__).resolve().parent.parent.parent
            self.data_dir = project_root / 'data' / 'raw' / 'olist'
        else:
            self.data_dir = Path(data_dir)
            
    def validate_directory(self) -> bool:
        """
        Check if the raw data directory exists.
        
        Returns:
            bool: True if the directory exists, False otherwise.
        """
        return self.data_dir.exists() and self.data_dir.is_dir()
        
    def validate_expected_files(self) -> Dict[str, bool]:
        """
        Check which of the expected Olist files are present in the directory.
        
        Returns:
            Dict[str, bool]: A dictionary mapping the logical dataset name to a boolean indicating presence.
        """
        presence = {}
        for logical_name, file_name in self.EXPECTED_FILES.items():
            file_path = self.data_dir / file_name
            presence[logical_name] = file_path.exists() and file_path.is_file()
        return presence
        
    def load_dataset(self, logical_name: str) -> pd.DataFrame:
        """
        Load a specific dataset into a Pandas DataFrame.
        
        Args:
            logical_name (str): The logical name of the dataset to load.
                                Valid options are the keys of EXPECTED_FILES.
                                
        Returns:
            pd.DataFrame: The loaded raw data.
            
        Raises:
            ValueError: If an invalid logical name is provided.
            FileNotFoundError: If the dataset file does not exist.
            pd.errors.EmptyDataError: If the CSV file is completely empty.
        """
        if logical_name not in self.EXPECTED_FILES:
            raise ValueError(f"Invalid dataset name '{logical_name}'. Supported datasets are: {list(self.EXPECTED_FILES.keys())}")
            
        file_name = self.EXPECTED_FILES[logical_name]
        file_path = self.data_dir / file_name
        
        if not file_path.exists():
            raise FileNotFoundError(f"The raw dataset file could not be found at: {file_path}")
            
        # We explicitly set keep_default_na=True (which is default) to not alter data, 
        # but avoid any other parsing that modifies values.
        # This is purely reading raw text into dataframe.
        return pd.read_csv(file_path)

    def load_all(self) -> Dict[str, pd.DataFrame]:
        """
        Load all available expected datasets.
        
        Returns:
            Dict[str, pd.DataFrame]: Dictionary mapping logical names to DataFrames.
        """
        dataframes = {}
        presence = self.validate_expected_files()
        for logical_name, is_present in presence.items():
            if is_present:
                dataframes[logical_name] = self.load_dataset(logical_name)
        return dataframes
