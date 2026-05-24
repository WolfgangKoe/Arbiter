from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)

    from src.adapters.web.routes import main

    app.register_blueprint(main.bp)

    return app
