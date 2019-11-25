# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import sqlalchemy
import altair as alt
import io
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
app.css.append_css({'external_url':
                    'https://cdn.rawgit.com/gschivley/8040fc3c7e11d2a4e7f0589ffc829a02/raw/fe763af6be3fc79eca341b04cd641124de6f6f0d/dash.css'
                    })
app.title = 'Test dash and altair'
server = app.server


app.layout = html.Div([

    html.Div([
        html.H2("Job Analysis App"),
        html.Img(src="/assets/icons.png")
    ], className="banner"),

    html.Div([

        html.Div([
            html.Label('Jobs'),
            # dcc.Input(id='mother_birth', value=1952, type='number'),
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
        alt.X('year:O'),
        alt.Y('count:Q'),
        color='sex:N'
    ).transform_filter(
        alt.datum.job == job_name
    ).properties(
        width=250,
        height=250
    )

    job_percentages_by_gender = alt.Chart(jobs).mark_line().encode(
        alt.X('year:O'),
        alt.Y('perc:Q', axis=alt.Axis(format='%')),
        color='sex:N'
    ).transform_filter(
        alt.datum.job == job_name
    ).properties(
        width=250,
        height=250
    )

    chart = job_counts_by_gender | job_percentages_by_gender

    # Save html as a StringIO object in memory
    jobs_by_gender_html = io.StringIO()
    chart.save(jobs_by_gender_html, 'html')

    # Return the html from StringIO object
    return jobs_by_gender_html.getvalue()

if __name__ == "__main__":
    app.run_server(debug=True, port=5001)
