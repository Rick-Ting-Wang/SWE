"""
Configuration tests
"""
import os
import unittest
from config import Config, DevelopmentConfig, ProductionConfig, TestingConfig, config


class TestConfig(unittest.TestCase):
    """Test configuration classes"""

    def test_base_config(self):
        """Test base configuration"""
        base_config = Config()

        # Test default values
        self.assertEqual(base_config.DB_HOST, 'localhost')
        self.assertEqual(base_config.DB_PORT, 3306)
        self.assertEqual(base_config.DB_NAME, 'komodo')
        self.assertEqual(base_config.DB_USER, 'root')
        self.assertEqual(base_config.DB_PASSWORD, 'mysql')
        self.assertEqual(base_config.APP_NAME, "Komodo Hub")

    def test_development_config(self):
        """Test development configuration"""
        dev_config = DevelopmentConfig()
        self.assertTrue(dev_config.DEBUG)

    def test_production_config(self):
        """Test production configuration"""
        prod_config = ProductionConfig()
        self.assertFalse(prod_config.DEBUG)

    def test_testing_config(self):
        """Test testing configuration"""
        test_config = TestingConfig()
        self.assertTrue(test_config.TESTING)
        self.assertTrue(test_config.DEBUG)
        self.assertEqual(test_config.DB_NAME, 'komodo_test')

    def test_config_mapping(self):
        """Test configuration mapping"""
        self.assertIn('development', config)
        self.assertIn('production', config)
        self.assertIn('testing', config)
        self.assertIn('default', config)

        # Test that all config classes are valid
        for config_name, config_class in config.items():
            instance = config_class()
            self.assertTrue(hasattr(instance, 'DB_HOST'))
            self.assertTrue(hasattr(instance, 'DB_NAME'))
            self.assertTrue(hasattr(instance, 'SECRET_KEY'))


if __name__ == '__main__':
    unittest.main()