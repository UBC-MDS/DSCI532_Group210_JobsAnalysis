import pandas as pd
import altair as alt
import data_wrangling
import io

jobs = data_wrangling.get_jobs_df()
gender_dominancy_df = data_wrangling.get_gender_dominant_group_count_df()

data_frames = {'balanced': pd.read_csv('data/top_10_balanced_jobs.csv'),
               'female dominated': pd.read_csv('data/top_10_female_jobs.csv'),
               'male dominated': pd.read_csv('data/top_10_male_jobs.csv')}


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

def get_interactive_proportions_plot(gender_balance):
    source = data_frames[gender_balance]
    pts = alt.selection(type="multi", encodings=['x'])

    lin = alt.Chart(source).mark_line().encode(
    alt.X('year:O', title='Year'),
    alt.Y('female_prop:Q',
          title="Proportion of Women",
          axis=alt.Axis(format='%'), 
          scale=alt.Scale(domain=[0,1])),
    alt.Color('job:N', title= "Job")
    ).transform_filter(
        pts
    ).properties(
        width=550,
        height=200,
        title="Proportion of women by decade"
    )

    label = alt.selection_single(
    encodings=['x'], # limit selection to x-axis value
    on='mouseover',  # select on mouseover events
    nearest=True,    # select data point nearest the cursor
    empty='none'     # empty selection includes no data points
    )

    lin_w_interaction = alt.layer(
    lin, # base line chart
        alt.Chart().mark_rule(color='#aaa').encode(
        x='year:O'
    ).transform_filter(label),
    lin.mark_circle().encode(
        opacity=alt.condition(label, alt.value(1), alt.value(0))
    ).add_selection(label),
    lin.mark_text(align='left', dx=5, dy=-5, stroke='white', strokeWidth=2).encode(
        text=alt.Text('female_prop:Q',format='.2%')
    ).transform_filter(label),
     lin.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.Text('female_prop:Q',format='.2%')
    ).transform_filter(label),
    data = source
    )

    bar = alt.Chart(source).mark_bar(size=25).encode(
    y=alt.Y('job:N',
            title='',
            sort=alt.EncodingSortField(field="total_prop_female",op="sum",order="descending" )),
    x=alt.X('total_prop_female:Q',
            title="Total Proportion of Women",
            axis=alt.Axis(format='%')),
    color=alt.condition(pts, alt.Color('job:N', legend=None), alt.ColorValue("grey"))
    ).properties(
        width=200,
        height=300,
        title= "Top 10 " + gender_balance + " jobs (Shift+click on bars to see individual data for selected jobs)"
    ).add_selection(pts)

    interactive_job_chart = alt.hconcat(
        bar,
        lin_w_interaction
    ).resolve_legend(
        color="independent",
        size="independent"
    )
    # Save html as a StringIO object in memory
    job_gender_proportions_html = io.StringIO()
    interactive_job_chart.save(job_gender_proportions_html, 'html')

    # Return the html from StringIO object
    return job_gender_proportions_html.getvalue()

    
    
