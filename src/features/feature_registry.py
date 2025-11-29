"""Feature registry for managing optional features."""

import yaml
from pathlib import Path
from typing import Dict, Any


class FeatureRegistry:
    """Manage feature flags and availability."""
    
    def __init__(self):
        """Initialize feature registry."""
        self.config_path = Path(__file__).parent.parent.parent / "config" / "features.yaml"
        self.features = self._load_features()
    
    def _load_features(self) -> Dict[str, Any]:
        """Load feature configuration."""
        if not self.config_path.exists():
            return {}
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            return config.get('features', {})
    
    def is_enabled(self, feature_name: str) -> bool:
        """Check if a feature is enabled."""
        feature = self.features.get(feature_name, {})
        return feature.get('enabled', False)
    
    def get_config(self, feature_name: str) -> Dict[str, Any]:
        """Get feature configuration."""
        return self.features.get(feature_name, {})
