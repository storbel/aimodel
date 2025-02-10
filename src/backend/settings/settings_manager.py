import os
import yaml
from typing import Dict, List, Any, Optional
import logging
from pathlib import Path

class ValidationError(Exception):
    """Custom exception for settings validation errors"""
    pass

class SettingsManager:
    """Manages application settings with validation and error handling"""
    
    DEFAULT_CONFIG = {
        "document_sources": [{
            "path": "/data/documents",
            "types": ["pdf", "xlsx", "png", "jpg"],
            "watch": True
        }],
        "extraction": {
            "docling": {
                "enable_ocr": True,
                "extract_tables": True,
                "extract_diagrams": True,
                "languages": ["fr", "en"]
            }
        },
        "preprocessing": {
            "clean": {
                "remove_duplicates": True,
                "fix_encoding": True,
                "normalize_text": True
            },
            "enrich": {
                "add_metadata": True,
                "generate_tags": True
            }
        },
        "vectorization": {
            "model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            "batch_size": 32,
            "dimension": 384
        },
        "faiss": {
            "index_type": "IVFFlat",
            "nlist": 100
        },
        "chatbot": {
            "model": "distilbert-base-multilingual-cased",
            "max_length": 512,
            "temperature": 0.7,
            "top_k": 5
        }
    }

    def __init__(self, config_path: str = "/config/settings.yaml"):
        """Initialize settings manager with config path"""
        self.config_path = config_path
        self.logger = logging.getLogger(__name__)
        self._settings: Dict[str, Any] = {}
        self._load_settings()

    def _load_settings(self) -> None:
        """Load settings from YAML file or create with defaults if not exists"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self._settings = yaml.safe_load(f)
                self.validate_settings(self._settings)
            else:
                self._settings = self.DEFAULT_CONFIG
                self._save_settings()
        except Exception as e:
            self.logger.error(f"Error loading settings: {str(e)}")
            raise

    def _save_settings(self) -> None:
        """Save current settings to YAML file"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                yaml.dump(self._settings, f, default_flow_style=False)
        except Exception as e:
            self.logger.error(f"Error saving settings: {str(e)}")
            raise

    def get_settings(self) -> Dict[str, Any]:
        """Return current settings"""
        return self._settings

    def update_settings(self, new_settings: Dict[str, Any]) -> None:
        """Update settings with validation"""
        try:
            self.validate_settings(new_settings)
            self._settings.update(new_settings)
            self._save_settings()
        except ValidationError as e:
            self.logger.error(f"Validation error: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Error updating settings: {str(e)}")
            raise

    def validate_settings(self, settings: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate settings structure and values"""
        errors = []
        
        # Check required sections
        required_sections = [
            "document_sources", "extraction", "preprocessing",
            "vectorization", "faiss", "chatbot"
        ]
        for section in required_sections:
            if section not in settings:
                errors.append(f"Missing required section: {section}")

        if errors:
            raise ValidationError("\n".join(errors))

        # Validate document sources
        if "document_sources" in settings:
            for source in settings["document_sources"]:
                if not isinstance(source.get("path"), str):
                    errors.append("Document source path must be a string")
                if not isinstance(source.get("types"), list):
                    errors.append("Document types must be a list")

        # Validate extraction settings
        if "extraction" in settings:
            docling = settings["extraction"].get("docling", {})
            if not isinstance(docling.get("languages", []), list):
                errors.append("Languages must be a list")

        # Validate vectorization settings
        if "vectorization" in settings:
            vec_settings = settings["vectorization"]
            if not isinstance(vec_settings.get("batch_size"), int):
                errors.append("Batch size must be an integer")
            if not isinstance(vec_settings.get("dimension"), int):
                errors.append("Vector dimension must be an integer")

        # Validate FAISS settings
        if "faiss" in settings:
            faiss_settings = settings["faiss"]
            if faiss_settings.get("index_type") not in ["IVFFlat", "Flat", "HNSW"]:
                errors.append("Invalid FAISS index type")

        # Validate chatbot settings
        if "chatbot" in settings:
            chatbot_settings = settings["chatbot"]
            if not isinstance(chatbot_settings.get("max_length"), int):
                errors.append("Max length must be an integer")
            if not 0 <= chatbot_settings.get("temperature", 0) <= 1:
                errors.append("Temperature must be between 0 and 1")

        return {"valid": len(errors) == 0, "errors": errors}

    def get_document_sources(self) -> List[Dict[str, Any]]:
        """Get configured document sources"""
        return self._settings.get("document_sources", [])

    def get_extraction_settings(self) -> Dict[str, Any]:
        """Get document extraction settings"""
        return self._settings.get("extraction", {})

    def get_vectorization_settings(self) -> Dict[str, Any]:
        """Get vectorization model settings"""
        return self._settings.get("vectorization", {})

    def get_faiss_settings(self) -> Dict[str, Any]:
        """Get FAISS index settings"""
        return self._settings.get("faiss", {})

    def get_chatbot_settings(self) -> Dict[str, Any]:
        """Get chatbot model settings"""
        return self._settings.get("chatbot", {})

    def validate_paths(self) -> List[str]:
        """Validate that configured paths exist and are accessible"""
        errors = []
        for source in self.get_document_sources():
            path = source.get("path")
            if not path:
                continue
            if not os.path.exists(path):
                errors.append(f"Path does not exist: {path}")
            elif not os.access(path, os.R_OK):
                errors.append(f"Path is not readable: {path}")
        return errors

if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    settings_manager = SettingsManager("config/settings.yaml")
    
    # Get current settings
    current_settings = settings_manager.get_settings()
    print("Current settings:", current_settings)
    
    # Validate paths
    path_errors = settings_manager.validate_paths()
    if path_errors:
        print("Path validation errors:", path_errors)