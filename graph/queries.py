from graph.connect import get_session

def find_endpoint(user_intent: str):
    """Find endpoint path based on user intent"""
    keywords = ["ship", "shipping", "deliver"]
    if any(k in user_intent.lower() for k in keywords):
        return "/shipments/create"
    return None


def get_endpoint_details(path: str):
    """Get complete endpoint details including URL, method, and authentication"""
    with get_session() as session:
        result = session.run("""
        MATCH (api:API)
        MATCH (e:Endpoint {path: $path})
        RETURN api.base_url AS base_url,
               api.auth_header AS auth_header,
               api.auth_format AS auth_format,
               e.path AS path,
               e.method AS method,
               e.description AS description
        """, path=path).single()
        
        if result:
            return {
                "url": result["base_url"] + result["path"],
                "method": result["method"],
                "auth_header": result["auth_header"],
                "auth_format": result["auth_format"],
                "description": result["description"]
            }
        return None


def get_endpoint_schema(path: str):
    with get_session() as session:
        result = session.run("""
        MATCH (e:Endpoint {path:$path})
        MATCH (e)-[:ACCEPTS]->(p:Parameter)
        OPTIONAL MATCH (p)-[:IS_TYPE]->(m:Model)-[:HAS_FIELD]->(f:Field)
        RETURN p.name AS param,
               p.type AS param_type,
               p.required AS required,
               m.name AS model_name,
               collect({name: f.name, type: f.type}) AS fields
        """, path=path)

        schema = {}
        for r in result:
            param_info = {
                "type": r["param_type"],
                "required": r["required"]
            }
            
            # If parameter references a model with fields
            if r["fields"] and r["fields"][0]['name'] is not None:
                param_info["model"] = r["model_name"]
                param_info["fields"] = {
                    field["name"]: field["type"] 
                    for field in r["fields"]
                }
            
            schema[r["param"]] = param_info

        return schema
