import os
import json
from ingestion.pdf_parser import PDFParser
from ingestion.graph_builder import build_graph
from pipeline.generate_api_call import generate_api_call

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

pdf_path = os.path.join(BASE_DIR, "data", "nexus_logistics_api_v2.pdf")

# 1. Parse PDF
parser = PDFParser(pdf_path)
api_data = parser.extract_structured_data()

# 2. Build Graph
build_graph(api_data)

# 3. User Intent
user_intent = (
    "I need to ship a 50kg package from Warehouse A "
    "to 123 Main St, New York, US using Express shipping."
)

# 4. Generate API call
result = generate_api_call(user_intent)
print(json.dumps(result, indent=2))
