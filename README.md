#  INUREAI SYSTEM 

##  Results 

###  FINAL OUTPUT


**Expected vs Actual**: EXACT MATCH

```json
{
  "url": "https://api.nexus-logistics.com/v2/shipments/create",
  "method": "POST",
  "headers": { "Authorization": "Bearer <YOUR_API_KEY>" },
  "body": {
    "origin_id": "Warehouse A",
    "weight_kg": 50.0,
    "service_code": "EXP",
    "dest_address": {
      "street": "123 Main St",
      "city": "New York",
      "country_code": "US"
    }
  }
}
```

##  Files 

| File                                                           | Status          | Purpose                                   |
| -------------------------------------------------------------- | --------------- | ----------------------------------------- |
| [ingestion/pdf_parser.py](ingestion/pdf_parser.py)             |  Working      | Multi-page PDF parsing with model linking |
| [ingestion/graph_builder.py](ingestion/graph_builder.py)       |  Working      | Graph construction with relationships     |
| [graph/connect.py](graph/connect.py)                           |  Working      | Neo4j connection                          |
| [graph/queries.py](graph/queries.py)                           |  **Enhanced** | Schema retrieval with field types         |
| [pipeline/generate_api_call.py](pipeline/generate_api_call.py) |  **Enhanced** | Improved prompt with formatted schema     |
| [llm/gemini_client.py](llm/gemini_client.py)                   |  Working      | Gemini API client with JSON mode          |
| [main.py](main.py)                                             |  Working      | Entry point                               |
| [test_system.py](test_system.py)                               |  **New**      | System tests                              |
| [validate_requirements.py](validate_requirements.py)           |  **New**      | Comprehensive validation                  |
| [test_edge_cases.py](test_edge_cases.py)                       |  **New**      | Edge case testing                         |



1.  Multi-page PDF context handling
2.  Explicit graph relationships (not vector store dumps)
3.  Proper model linking across pages
4.  No hallucinations (grounded in PDF)
5.  Nested dest_address object in output
6.  Correct authentication format
7.  Complete GraphRAG pipeline




## 1. PROJECT STRUCTURE

```
InureAI/
├── data/
│   └── nexus_logistics_api_v2.pdf    # Source API documentation
├── graph/
│   ├── connect.py                     # Neo4j connection
│   └── queries.py                     # Graph queries (ENHANCED)
├── ingestion/
│   ├── pdf_parser.py                  # Multi-page PDF parsing
│   └── graph_builder.py               # Graph construction
├── llm/
│   └── gemini_client.py               # Gemini LLM client
├── pipeline/
│   └── generate_api_call.py           # Main API generation (ENHANCED)
├── main.py                            # Entry point
├── test_system.py                     # System tests
└── validate_requirements.py           # Comprehensive validation
```

---

## 2. RUNNING THE SYSTEM

### Basic Execution

```bash
python main.py
```