# app.py
from dash import Dash
import dash

from ui.style_shell import SPECTRE_INDEX_STRING
from ui.layout import build_layout
from ui.callbacks import register_callbacks

app = Dash(__name__)
server = app.server

app.title = "Spectre Neural Search Policy Engine"
app.index_string = SPECTRE_INDEX_STRING
app.layout = build_layout()

# Register all callbacks against this app instance
register_callbacks(app)


if __name__ == "__main__":
    app.run(debug=True)
