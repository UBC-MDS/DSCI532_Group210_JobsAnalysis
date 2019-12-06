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
            We are exploring a dataset of 255 jobs with both genders' hiring
            numbers from 1850 to 2000 for each decade. We will look at how
            the gender compositions in these jobs have evolved and how each
            job gender dominant group, such as only female and male jobs,
            has changed in its prevalence over the decades.
        ''', className='lead my-3'),

        html.H4('''
            We classify the jobs into gender groups based on their
            male-to-female employment ratios. If it is more than 2, we
            classify the job as being male dominant. If it is less than 0.5,
            we classify the job as being female dominant. Male-only and
            female-only categories are self-explanatory. We group the rest
            as being gender balanced.
        ''', className='lead my-3')
    ], className='col-md-9 px-0')
], className="jumbotron p-4 p-md-5 text-white rounded bg-dark")

first_row = html.Div([
    html.Div([
        html.Div([
            html.Label(
                'Select a job to see its male and female employment trends'
            ),
            dcc.Dropdown(
                id='job_name',
                options=[{'label': i, 'value': i}
                         for i in data_wrangling.get_unique_job_names()],
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

second_row = html.Div([
    html.Div([
        html.Div([
            html.Label('Toggle groups to compare their trends.'),
            dbc.Checklist(
                id='dominancy_groups',
                className='checklist',
                options=[
                    {
                        'label': i, 'value': i
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
            html.Label(
                'Based on total aggregated proportion over the time range'
            ),
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
    first_row,
    divider,
    second_row,
    divider,
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
