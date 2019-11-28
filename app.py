# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import sys
sys.path.append('src')
from src import callback_functions
from src import data_wrangling

app = dash.Dash(__name__)
app.css.append_css({
    'external_url':
        'https://cdn.rawgit.com/gschivley/8040fc3c7e11d2a4e7f0589ffc829a02/raw/fe763af6be3fc79eca341b04cd641124de6f6f0d/dash.css'
})
app.title = 'Job Analysis'
server = app.server

app.layout = html.Div([

    html.H2([
        html.Img(src='/assets/job.png'),
        html.Span("Job Analysis App")
    ], className="banner"),

    html.Div([

        html.Div([
            html.Label('Jobs'),
            dcc.Dropdown(
                id='job_name',
                options=[{
                    'label': i, 'value': i
                } for i in data_wrangling.get_unique_job_names()],
                value=data_wrangling.get_unique_job_names()[0],
                placeholder="Select a job name...")
        ]),

        html.Iframe(
            id='single-job-plot',
            height='400',
            width='800',
            sandbox='allow-scripts',

            # This is where we will pass the html
            # srcDoc= ... ,
            className="chartframe"
        )
    ]),

    html.Div([
        dcc.Checklist(
                id='dominancy_groups',
                options=[
                    {
                        'label': i, 'value': i
                    } for i in data_wrangling.get_gender_dominancy_groups()
                ],
                value=data_wrangling.get_gender_dominancy_groups()
        ),

        html.Iframe(
            id='job-dominancy-plot',
            height='400',
            width='800',
            sandbox='allow-scripts',
            className="chartframe"
        )
    ])
])


@app.callback(
    dash.dependencies.Output('single-job-plot', 'srcDoc'),
    [dash.dependencies.Input('job_name', 'value')]
)
def update_single_job_plot(job_name):
    return callback_functions.update_job_name_by_gender(job_name)


@app.callback(
    dash.dependencies.Output('job-dominancy-plot', 'srcDoc'),
    [dash.dependencies.Input('dominancy_groups', 'value')]
)
def update_job_dominancy_plot(selected_groups):
    return callback_functions.get_gender_dominancy_graph(selected_groups)


if __name__ == "__main__":
    app.run_server(debug=True, port=5001)
