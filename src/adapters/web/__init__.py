from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)

    from src.adapters.yaml.necron_yaml_army_repository import NecronYamlArmyRepository

    app.army_repository = NecronYamlArmyRepository()  # type: ignore[attr-defined]

    from src.adapters.web.routes import main

    app.register_blueprint(main.bp)

    return app
