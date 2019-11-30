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

    html.H3('''
        We are exploring a dataset of 255 jobs with both genders' hiring numbers
        from 1850 to 2000 for each decade. We will look at how the gender
        compositions in these jobs have evolved and how each job gender dominant
        group, such as only female and male jobs, has changed in its prevalence
        over the decades.
    '''),

    # FIRST ROW
    html.Div(
        children = [
            html.Div(
                children=[
                    html.Div(
                        className="dropdown",
                        children=[
                            html.Label(
                                'Select a job to see its male and female employment trends'),
                            dcc.Dropdown(
                                id='job_name',
                                options=[{'label': i, 'value': i}
                                         for i in data_wrangling.get_unique_job_names()],
                                value=data_wrangling.get_unique_job_names()[0],
                                placeholder="Select a job name...",
                                className="dropdown-content"
                            )
                        ]
                    )
                ],
                className="column side"
            ),
            html.Div(
                children=[
                    html.Iframe(
                        id='single-job-plot',
                        height='400',
                        width='100%',
                        sandbox='allow-scripts',

                        # This is where we will pass the html
                        # srcDoc= ... ,
                        className="chartframe"
                    )
                ],
                className="column middle"
            ),
        ],
        className="row"
    ),

    # SECOND ROW
    html.Div(
        children = [
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Label('Toggle groups to compare their trends.'),
                            dbc.Checklist(
                                id='dominancy_groups',
                                className='checklist',
                                options=[{'label': i, 'value': i} for i in data_wrangling.get_gender_dominancy_groups()],
                                value=data_wrangling.get_gender_dominancy_groups()
                            )
                        ]
                    )
                ],
                className="column side"
            ),
            html.Div(
                children=[
                    html.Iframe(
                        id='job-dominancy-plot',
                        height='400',
                        width='100%',
                        sandbox='allow-scripts',

                        # This is where we will pass the html
                        # srcDoc= ... ,
                        className="chartframe"
                    )
                ],
                className="column middle"
            ),
        ],
        className="row"
    ),

    # THIRD ROW
    html.Div(
        children = [
            html.Div(
                children=[
                    html.Div(
                        className="dropdown",
                        children=[
                            html.Label('Select a gender balance.'),
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
                        ]
                    )
                ],
                className="column side"
            ),
            html.Div(
                children=[
                    html.P('Click on a bar to see data for an individual job, and use shift+click to toggle additional jobs. Double-click to cancel selections.'),
                    html.Iframe(
                        id='job-proportions-plot',
                        height='800',
                        width='100%',
                        sandbox='allow-scripts',

                        # This is where we will pass the html
                        # srcDoc= ... ,
                        className="chartframe"
                    )
                ],
                className="column middle"
            ),
        ],
        className="row"
    )
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
