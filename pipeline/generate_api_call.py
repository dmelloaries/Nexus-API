import json
from graph.queries import find_endpoint, get_endpoint_schema, get_endpoint_details
from llm.gemini_client import generate_json

def generate_api_call(user_intent: str):
    # Step 1: Find the endpoint path based on user intent
    path = find_endpoint(user_intent)
    
    # Step 2: Retrieve endpoint details (URL, method, auth) from graph
    endpoint_details = get_endpoint_details(path)
    
    # Step 3: Retrieve parameter schema from graph
    schema = get_endpoint_schema(path)

    # Build a detailed schema description
    schema_description = []
    for param_name, param_info in schema.items():
        if isinstance(param_info, dict):
            if "fields" in param_info:
                # Parameter is a model/object
                fields_desc = ", ".join([f"{fname} ({ftype})" for fname, ftype in param_info["fields"].items()])
                schema_description.append(f"- {param_name} ({'required' if param_info['required'] else 'optional'}): object with fields [{fields_desc}]")
            else:
                # Regular parameter
                schema_description.append(f"- {param_name} ({'required' if param_info['required'] else 'optional'}): {param_info['type']}")
    
    schema_str = "\n".join(schema_description)

    prompt = f"""
You are given an API schema derived from a graph database.

Schema (STRICT):
{schema_str}

Rules (MANDATORY):
- dest_address MUST be an object with keys: street, city, country_code
- service_code MUST be one of: EXP, STD
- Do NOT return arrays for objects
- Do NOT invent new keys
- Return ONLY valid JSON, no markdown, no explanations

User request:
{user_intent}

Return only the JSON object for the request body.
"""

    try:
        body = json.loads(generate_json(prompt))
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON from LLM response: {e}")
        raise

    # Build response dynamically from graph data (not hardcoded!)
    return {
        "url": endpoint_details["url"],
        "method": endpoint_details["method"],
        "headers": {
            endpoint_details["auth_header"]: endpoint_details["auth_format"]
        },
        "body": body
    }
