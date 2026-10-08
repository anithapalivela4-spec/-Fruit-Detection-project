import os
import logging
from pathlib import Path
import rdflib
from rdflib.namespace import RDF, RDFS, OWL

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_OWL_PATH = BASE_DIR / 'ontology' / 'fruit_disease.owl'

class OntologyLoader:
    _instance = None
    _graph = None

    @classmethod
    def get_graph(cls, owl_path=None):
        """Singleton graph loader for the Fruit Disease Ontology."""
        if cls._graph is None:
            cls.load_ontology(owl_path)
        return cls._graph

    @classmethod
    def load_ontology(cls, owl_path=None):
        path = owl_path or DEFAULT_OWL_PATH
        g = rdflib.Graph()
        if not os.path.exists(path):
            logger.warning(f"Ontology file not found at {path}. Returning empty graph.")
            cls._graph = g
            return g
        
        try:
            g.parse(str(path), format='xml')
            logger.info(f"Ontology loaded successfully from {path} with {len(g)} triples.")
        except Exception as e:
            logger.error(f"Error parsing OWL ontology: {e}. Attempting turtle fallback.")
            ttl_path = BASE_DIR / 'ontology' / 'ontology_schema.ttl'
            if os.path.exists(ttl_path):
                g.parse(str(ttl_path), format='turtle')
        
        cls._graph = g
        return cls._graph

    @classmethod
    def reload(cls, owl_path=None):
        cls._graph = None
        return cls.load_ontology(owl_path)
