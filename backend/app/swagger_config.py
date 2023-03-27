from flasgger import Swagger

def get_swagger_config():
    swagger_config = Swagger.DEFAULT_CONFIG.copy()
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "version": "1.0.1",
                "title": "My API",
                "description": "My API description",
                "endpoint": "spec",
                "route": "/spec",
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/swagger-ui",
        "swagger_ui": True,
        # "specs_route": "/app/docs/",
    }
    return swagger_config