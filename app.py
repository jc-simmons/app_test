from flask import Flask, request
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly
import json
import requests
import datetime


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/'
        )
    
    dash_app.layout = html.Div([
    html.H1("Dashboard Title" ,style ={"text-align": "center","font-family":"Lato"}),
    html.Br(),
    html.Br()
    ])


    return dash_app.server


def init_api(server):

    @server.route('/api/', methods=['POST', 'GET'])
    def handle_request():
        text = str(request.args.get('input'))
        characters = len(text)
        out_data = {'chars': characters}
        return json.dumps(out_data)


    return server


def init_app():
    app = Flask(__name__)

    with app.app_context():
        app = init_api(app)
        app = init_dashboard(app)
        return app

app = init_app()

if __name__ == "__main__":
    app.run()
