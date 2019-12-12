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

external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets
)
app.title = 'Job Analysis'
server = app.server

divider = html.Div(className='border-bottom mb-5')

header = html.Div([
    html.Div([
        html.H1([
            html.Img(src='/assets/job.png', className='logo'),
            'Job Analysis'
        ]),

        html.P('''
            We are exploring a dataset of 255 jobs with both genders' employment
            numbers from 1850 to 2000 for each decade. We will focus on how
            the gender compositions in these jobs have evolved. An user might
            use this dashboard to gain insights with these trends and
            investigate how to improve gender balance in certain industries
            or jobs.
        ''', className='lead my-3'),
    ], className='col-md-9 px-0')
], className="jumbotron p-4 p-md-5 text-white rounded bg-dark")

first_row = html.Div([
    html.Div([
        html.Div([
            html.Label(
                'Select a job'
            ),
            dcc.Dropdown(
                id='job_name',
                options=[{
                    'label': i, 'value': i
                } for i in data_wrangling.get_unique_job_names()],
                value=data_wrangling.get_unique_job_names()[0],
                placeholder="Select a job name...",
                className="dropdown-content"
            )
        ], className="dropdown")
    ], className="column side"),
    html.Div(
        children=[
            html.Iframe(
                id='single-job-plot',
                height='400',
                width='700',
                sandbox='allow-scripts',

                # This is where we will pass the html
                # srcDoc= ... ,
                className="chartframe"
            )
        ],
        className="column middle"
    ),
], className="row")

gender_group_label_map = {
    'male dominant': 'male dominant(more than two male to one female)',
    'female dominant': 'female dominant(more than two females to one male)',
    'balanced': 'balanced',
    'only male': 'only male',
    'only female': 'only female'
}

second_row = html.Div([
    html.Div([
        html.Div([
            html.Label('Toggle groups'),
            dbc.Checklist(
                id='dominancy_groups',
                className='checklist',
                options=[
                    {
                        'label': gender_group_label_map[i], 'value': i
                    } for i in data_wrangling.get_gender_dominancy_groups()
                ],
                value=data_wrangling.get_gender_dominancy_groups()
            )
        ])
    ], className="column side"),
    html.Div([
            html.Iframe(
                id='job-dominancy-plot',
                height='400',
                width='820',
                sandbox='allow-scripts',

                # This is where we will pass the html
                # srcDoc= ... ,
                className="chartframe"
            )
    ], className="column middle")
], className="row")

third_row = html.Div([
    html.Div([
        html.Div([
            html.Label('Select a gender balance'),
            html.Br(),
            dcc.Dropdown(
                id='gender_balance',
                clearable= False,
                className='dropdown-content',
                options=[
                    {'label': 'Female Dominated', 'value': 'female dominated'},
                    {'label': 'Balanced', 'value': 'balanced'},
                    {'label': 'Male Dominated', 'value': 'male dominated'}
                ],
                value='female dominated',
                placeholder="Select a gender balance..."
            )
        ], className="dropdown")
    ], className="column side"),
    html.Div([
        html.P('''
            Click on a bar to see data for an individual job,
            and use shift+click to toggle additional jobs.
            Double-click to cancel selections.
        '''),
        html.Iframe(
            id='job-proportions-plot',
            height='800',
            width='1150',
            sandbox='allow-scripts',

            # This is where we will pass the html
            # srcDoc= ... ,
            className="chartframe"
        )
    ], className="column middle")
], className="row")

main_app = html.Div([
    header,
    html.P('''
        Let's first look at the male and female employment trends of
        individual jobs!
    ''', className='lead mb-2 font-weight-bold'),
    first_row,
    divider,
    html.P('''
        Here, we will categorize the jobs into different gender dominant
        groups, based on their male-to-female ratios, and look at their trends
        over the decades.
    ''', className='lead mb-2 font-weight-bold'),
    second_row,
    divider,
    html.P('''
        For the final graph, we will look at different top 10 jobs in terms of
        their historical female employment proportion and investigate how their
        gender balance has changed over time.
    ''', className='lead mb-2 font-weight-bold'),
    third_row
], className="container main")

footer = html.Footer([
    html.A(
        'Data source',
        href='https://github.com/vega/vega-datasets/blob/master/sources.md#jobsjson',
        target='_blank'
    ),
    html.P('''
        The data is provided by Vega. Unfortunately, the source of this data is
        unkown, so we do not have any background information about it.
    '''),
], className='footer')

app.layout = html.Div([
    main_app,
    footer
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

@app.callback(
    dash.dependencies.Output('job-proportions-plot', 'srcDoc'),
    [dash.dependencies.Input('gender_balance', 'value')]
)
def update_interactive_proportions_plot(gender_balance):
    return callback_functions.get_interactive_proportions_plot(gender_balance)

if __name__ == "__main__":
    app.run_server(debug=True, port=5001)
