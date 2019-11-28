# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import sqlalchemy
import altair as alt
import io
import base64
import os

from vega_datasets import data

# Don't need this with the cars dataset
alt.data_transformers.enable('default', max_rows=10000)

def modify_a():
    """
    Placeholder for all data wrangling
    """
    return data.jobs()

def modify_b():
    """
    Placeholder for all data wrangling
    """
    return data.jobs()

jobs = data.jobs()
jobs_modified_a = modify_a()
jobs_modified_b = modify_b()

app = dash.Dash(__name__)
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
                options=[{'label': i, 'value': i} for i in jobs.job.unique()],
                value=jobs.job.unique()[0],
                placeholder="Select a job name..."
            )
        ], className='jobdropdown')
    ]),

    html.Iframe(
        id='plot',
        height='500',
        width='1000',
        sandbox='allow-scripts',

        # This is where we will pass the html
        # srcDoc= ... ,
        className="chartframe"
    )
])

@app.callback(
    dash.dependencies.Output('plot', 'srcDoc'),
    [
        dash.dependencies.Input('job_name', 'value')
    ]
)
def update_job_name_by_gender(job_name):
    job_counts_by_gender = alt.Chart(jobs).mark_line().encode(
        alt.X('year:O', title='Year'),
        alt.Y('count:Q', title='Count'),
        color='sex:N'
    ).transform_filter(
        alt.datum.job == job_name
    ).properties(
        width=250,
        height=250,
        title='Employment number by year'
    )

    job_percentages_by_gender = alt.Chart(jobs).mark_line().encode(
        alt.X('year:O', title='Year'),
        alt.Y(
            'perc:Q',
            axis=alt.Axis(format='%'),
            title='Percentage'
        ),
        color='sex:N'
    ).transform_filter(
        alt.datum.job == job_name
    ).properties(
        width=250,
        height=250,
        title='Percentage employed on the job market'
    )

    chart = job_counts_by_gender | job_percentages_by_gender

    # Save html as a StringIO object in memory
    jobs_by_gender_html = io.StringIO()
    chart.save(jobs_by_gender_html, 'html')

    # Return the html from StringIO object
    return jobs_by_gender_html.getvalue()

if __name__ == "__main__":
    app.run_server(debug=True, port=5001)
