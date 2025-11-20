import unittest
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.data_loader import get_data

class TestDataLoader(unittest.TestCase):
    
    def test_download_single_asset(self):
        """Test if downloading a single asset returns a valid DataFrame."""
        df = get_data("AAPL", period="1mo")
        self.assertFalse(df.empty, "Dataframe should not be empty for a valid ticker")
        self.assertTrue("AAPL" in df.columns, "Column AAPL should exist")

    def test_download_multiple_assets(self):
        """Test if downloading multiple assets returns correct columns."""
        tickers = "AAPL, MSFT"
        df = get_data(tickers, period="1mo")
        self.assertFalse(df.empty)
        self.assertEqual(len(df.columns), 2, "Should have 2 columns")
    
    def test_invalid_ticker(self):
        """Test robust handling of invalid tickers."""
        # INVALID_TICKER should be ignored or return empty, but not crash the app
        df = get_data("INVALID_XYZ_123", period="1mo")
        self.assertTrue(df.empty or "INVALID_XYZ_123" not in df.columns)

if __name__ == '__main__':
    unittest.main()