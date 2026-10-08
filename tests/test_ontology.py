from django.test import TestCase
from ontology_engine.ontology_loader import OntologyLoader
from ontology_engine.reasoner import OntologyReasoner

class OntologyTests(TestCase):
    def test_ontology_loads_successfully(self):
        """Test RDFLib loads OWL file and parses triples."""
        graph = OntologyLoader.get_graph()
        self.assertGreater(len(graph), 50)

    def test_reasoner_mango_anthracnose(self):
        """Test OntologyReasoner evaluates Mango Anthracnose input."""
        reasoner = OntologyReasoner()
        result = reasoner.reason({
            'fruit': 'Mango',
            'disease': 'Mango Anthracnose',
            'confidence': 94.5
        })
        self.assertEqual(result['fruit'], 'Mango')
        self.assertEqual(result['disease'], 'Mango Anthracnose')
        self.assertEqual(result['severity'], 'High')
        self.assertIn('Colletotrichum', result['pathogen'])
        self.assertGreater(len(result['symptoms']), 0)
        self.assertGreater(len(result['treatments']), 0)
        self.assertIn('Semantic', result['explanation'])

    def test_reasoner_healthy_specimen(self):
        """Test reasoning for healthy fruit specimen."""
        reasoner = OntologyReasoner()
        result = reasoner.reason({
            'fruit': 'Apple',
            'disease': 'Apple Healthy',
            'confidence': 98.0
        })
        self.assertTrue(result['is_healthy'])
        self.assertEqual(result['severity'], 'Healthy')
