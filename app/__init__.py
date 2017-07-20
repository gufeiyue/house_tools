
from flask import Flask




def create_app():
    app = Flask(__name__)

    app.secret_key = "gufy"


    from .tax import tax as tax_buleprint
    app.register_blueprint(tax_buleprint, url_prefix='/tax')

    return app
