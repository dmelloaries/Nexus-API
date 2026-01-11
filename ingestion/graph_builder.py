from graph.connect import get_session

def build_graph(api_data: dict):
    with get_session() as session:
        session.run("MATCH (n) DETACH DELETE n")

        # Store API metadata (base_url and authentication)
        session.run("""
        CREATE (api:API {
            base_url: $base_url,
            auth_header: $auth_header,
            auth_format: $auth_format
        })
        """,
        base_url=api_data["base_url"],
        auth_header=api_data["authentication"]["header"],
        auth_format=api_data["authentication"]["format"])

        # Endpoints
        for ep in api_data["endpoints"]:
            session.run("""
            CREATE (e:Endpoint {
                name:$name,
                path:$path,
                method:$method,
                description:$desc
            })
            """, name=ep["name"],
                 path=ep["path"],
                 method=ep["method"],
                 desc=ep["description"])

            for p in ep["parameters"]:
                session.run("""
                MATCH (e:Endpoint {path:$path})
                CREATE (p:Parameter {
                    name:$name,
                    type:$type,
                    required:$required
                })
                CREATE (e)-[:ACCEPTS]->(p)
                """,
                path=ep["path"],
                name=p["name"],
                type=p["type"],
                required=p["required"])

                if "model_reference" in p:
                    session.run("""
                    MATCH (p:Parameter {name:$pname})
                    MERGE (m:Model {name:$mname})
                    CREATE (p)-[:IS_TYPE]->(m)
                    """,
                    pname=p["name"],
                    mname=p["model_reference"])

        # Models
        for model in api_data["models"].values():
            for field in model["fields"]:
                session.run("""
                MATCH (m:Model {name:$mname})
                CREATE (f:Field {
                    name:$fname,
                    type:$ftype
                })
                CREATE (m)-[:HAS_FIELD]->(f)
                """,
                mname=model["name"],
                fname=field["name"],
                ftype=field["type"])
