from flask import Flask, request
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly
import json
import requests
import datetime


url = 'https://app-test-vg50.onrender.com'

def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/'
        )

    dash_app.layout = html.Div([
    html.H1("Dashboard Title" ,style ={"text-align": "center","font-family":"Lato"}),
    html.Br(),
    html.Br(),
    html.Div([
        dcc.Input(
            id='my_txt_input',
            type='text',
            debounce=True,           # changes to input are sent to Dash server only on enter or losing focus
            pattern=r"^[A-Za-z].*",  # Regex: string must start with letters only
            spellCheck=True,
            inputMode='latin',       # provides a hint to browser on type of data that might be entered by the user.
            name='text',             # the name of the control, which is submitted with the form data
            list='browser',          # identifies a list of pre-defined options to suggest to the user
            n_submit=0,               # number of times the Enter key was pressed while the input had focus
            n_submit_timestamp=-1,   # last time that Enter was pressed
            autoFocus=True,          # the element should be automatically focused after the page loaded
            n_blur=0,                # number of times the input lost focus
            n_blur_timestamp=-1,     # last time the input lost focus.
            # selectionDirection='', # the direction in which selection occurred
            # selectionStart='',     # the offset into the element's text content of the first selected character
            # selectionEnd='',       # the offset into the element's text content of the last selected character
            ),
        ]),
    html.Br(),
    #html.Datalist(id='browser', children=[
    #    html.Option(value="blue"),
    #    html.Option(value="yellow"),
     #   html.Option(value="green")
   # ]),

    html.Br(),
    html.Br(),

    html.Div(id='inp'),

    html.P(['------------------------']),

    html.Br(),
    html.Br(),

    html.Div(id='result'),

    html.P(['------------------------'])

    ])

    @dash_app.callback([Output(component_id='result', component_property='children'),
                    Output(component_id='inp', component_property='children')],
                    Input(component_id='my_txt_input', component_property='value'),
                    prevent_initial_call=True)
    def call_api(text):

        msg = {'input': text}
        response = requests.get(url,params=msg)
        result = response.json()
        result = result['chars']

        return [result, text]



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
