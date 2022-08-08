import dash
import pandas as pd
import dash_bootstrap_components as dbc
import json
from dash import dcc, html, ALL, MATCH
from dash.dependencies import Input, Output, State
from datetime import datetime
from flask import Flask
from ui.get_layout import get_layout
from common.merge_dictionary import merge_dictionary

################################################################################
# 00.  Parameter - 
#          Dash is Stateless and Global Variables Will Break Your App
#          Only create variables for static parameters
################################################################################

TITLE = "Resume"

################################################################################
# 01.   Data
################################################################################

# Load the resume data from JSON
# need to use absolute path on pythonAnywhere.com
# with open('/home/homerlee/mysite/assets/data.json') as f:
with open('.\\assets\\data.json') as f:
    data = json.load(f)

################################################################################
# 02.  Declare dash app
################################################################################
# A) using main.css instead of online resources

server = Flask(__name__)

app = dash.Dash(
    name = __name__,
    server = server,
    external_stylesheets = [
        dbc.themes.BOOTSTRAP,
        dbc.icons.BOOTSTRAP
    ],
    external_scripts = [
        "https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js",
        "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"
    ]
)

app.title = TITLE

################################################################################
# 03.  Backend
################################################################################

tech_stack = {}

for e in data["experience"]:
    tech_stack = merge_dictionary(
        tech_stack,
        data["experience"][e]["tech stack"]
    )

tech_stack_company_list = {}

for e in data["experience"]:
    for k, _ in data["experience"][e]["tech stack"].items():
        if k not in tech_stack_company_list:
            tech_stack_company_list[k] = []
        tech_stack_company_list[k].append(e)

################################################################################
# 04.  UI / UX
################################################################################
app.layout = get_layout(
    title = TITLE,
    data = data,
    tech_stack = tech_stack
)

################################################################################
# 05.  Callback / interactive actions
################################################################################

@app.callback(
    Output(component_id = 'dbc-cl-tech-stack',              component_property = 'value'),
    Input(component_id = 'dbc-bt-tech-stack-select-all',    component_property = 'n_clicks'),
    Input(component_id = 'dbc-bt-tech-stack-deselect-all',  component_property = 'n_clicks'),
    prevent_initial_call = True
)
def callback_click_select_all(n_clicks_s, n_clicks_d):
    ctx = dash.callback_context
    triggered_button_name = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_button_name == 'dbc-bt-tech-stack-select-all':
        return [k for k, _ in tech_stack.items()]
    if triggered_button_name == 'dbc-bt-tech-stack-deselect-all':
        return []


@app.callback(
    Output(component_id = "dbc-ad-main-deck",                   component_property = "active_item"),
    Input(component_id = "dbc-cl-tech-stack",                   component_property = "value"),
    prevent_initial_call = True
)
def callback_collapse_by_tech_stack(checkbox_value):

    # get the list of experience for selected tech stack
    expand_accordion_list = set()
    for v in checkbox_value:
        for e in tech_stack_company_list[v]:
            if e not in expand_accordion_list:
                expand_accordion_list.add(f"dbc-ad-main-deck-{e}")
    
    return list(expand_accordion_list)


################################################################################
# 99.  Run the app
################################################################################
if __name__ == '__main__':
    app.run_server(debug = True, use_reloader = False, port = 8721)
