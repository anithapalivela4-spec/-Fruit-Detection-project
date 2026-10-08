"""SPARQL queries for ontology query execution."""

PREFIXES = """
PREFIX : <http://www.semanticweb.org/ontologies/2026/fruit-disease#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""

def query_disease_details(disease_individual_name: str) -> str:
    """SPARQL to retrieve pathogen, severity, environmental factors for a disease."""
    return f"""
    {PREFIXES}
    SELECT ?diseaseLabel ?pathogenLabel ?severityLabel ?envLabel
    WHERE {{
        BIND(:{disease_individual_name} AS ?d)
        OPTIONAL {{ ?d rdfs:label ?diseaseLabel . }}
        OPTIONAL {{ 
            ?d :causedBy ?p .
            ?p rdfs:label ?pathogenLabel .
        }}
        OPTIONAL {{ 
            ?d :hasSeverity ?s .
            ?s rdfs:label ?severityLabel .
        }}
        OPTIONAL {{ 
            ?d :favoredBy ?env .
            ?env rdfs:label ?envLabel .
        }}
    }}
    """

def query_symptoms_for_disease(disease_individual_name: str) -> str:
    """SPARQL to retrieve all symptoms caused by a specific disease."""
    return f"""
    {PREFIXES}
    SELECT DISTINCT ?symptomLabel
    WHERE {{
        :{disease_individual_name} :causesSymptom ?s .
        ?s rdfs:label ?symptomLabel .
    }}
    """

def query_treatments_for_disease(disease_individual_name: str) -> str:
    """SPARQL to retrieve recommended treatments and their descriptions."""
    return f"""
    {PREFIXES}
    SELECT DISTINCT ?treatmentLabel ?description
    WHERE {{
        :{disease_individual_name} :treatedBy ?t .
        ?t rdfs:label ?treatmentLabel .
        OPTIONAL {{ ?t :description ?description . }}
    }}
    """

def query_preventions_for_disease(disease_individual_name: str) -> str:
    """SPARQL to retrieve prevention measures."""
    return f"""
    {PREFIXES}
    SELECT DISTINCT ?preventionLabel ?description
    WHERE {{
        :{disease_individual_name} :preventedBy ?prev .
        ?prev rdfs:label ?preventionLabel .
        OPTIONAL {{ ?prev :description ?description . }}
    }}
    """

def query_all_diseases_for_fruit(fruit_name: str) -> str:
    """SPARQL to list all diseases affecting a specified fruit."""
    return f"""
    {PREFIXES}
    SELECT DISTINCT ?disease ?diseaseLabel
    WHERE {{
        ?fruit a :Fruit ;
               rdfs:label "{fruit_name}" .
        ?disease :affectsFruit ?fruit ;
                 rdfs:label ?diseaseLabel .
    }}
    """
