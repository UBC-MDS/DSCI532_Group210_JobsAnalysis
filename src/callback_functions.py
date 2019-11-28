import pandas as pd
import altair as alt
import data_wrangling
import io

jobs = data_wrangling.get_jobs_df()
gender_dominancy_df = data_wrangling.get_gender_dominant_group_count_df()


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


def get_gender_dominancy_graph(dominancy_groups):

    df = gender_dominancy_df[gender_dominancy_df["job_gender_dominant_group"].isin(
        dominancy_groups)]
    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('year:O', axis=alt.Axis(title='Year')),
        y=alt.Y('total', axis=alt.Axis(title='Number of Jobs')),
        color=alt.Color('job_gender_dominant_group',
                        legend=alt.Legend(title="Job gender dominant group"),
                        sort=['male dominant', 'only male', 'balanced', 'female dominant', 'only female'])
    ).properties(
        title='Number of job gender dominant groups by year',
        height=250,
        width=400
    )

    label = alt.selection_single(
        encodings=['x'], # limit selection to x-axis value
        on='mouseover',  # select on mouseover events
        nearest=True,    # select data point nearest the cursor
        empty='none'     # empty selection includes no data points
    )

    interactive_chart = alt.layer(
        chart,
        alt.Chart().mark_rule(color='#aaa').encode(
            x='year:O'
        ).transform_filter(label),
        chart.mark_circle().encode(
            opacity=alt.condition(label, alt.value(1), alt.value(0))
        ).add_selection(label),
        chart.mark_text(align='left', dx=5, dy=-5, stroke='white', strokeWidth=2).encode(
            text='total:Q'
        ).transform_filter(label),
        chart.mark_text(align='left', dx=5, dy=-5).encode(
            text='total:Q'
        ).transform_filter(label),
        data=df
    )

    # Save html as a StringIO object in memory
    gender_dominancy_html = io.StringIO()
    interactive_chart.save(gender_dominancy_html, 'html')

    # Return the html from StringIO object
    return gender_dominancy_html.getvalue()
