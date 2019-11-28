import altair as alt
from vega_datasets import data


def get_jobs_df():
    return data.jobs()

def get_unique_job_names():
    return data.jobs().job.unique()


# Categorize each row into a gender dominant group 
# based on its male to female ratio of that year
def categorize_gender_dominant_group(row):  
  male_count = row['count']['men']
  female_count = row['count']['women']
  
  if male_count == 0 and female_count == 0:
    return 'no job'
  elif row['count']['women'] == 0:
    return 'only male'
  elif row['count']['men'] == 0:
    return 'only female'
  elif (male_count/female_count) >= 2:
    return 'male dominant'
  elif (male_count/female_count) <= 0.5:
    return 'female dominant'
  else:
    return 'balanced'

def sort_order(col_val):
    if col_val == 'only male':
        return 1
    elif col_val == 'male dominant':
        return 2
    elif col_val == 'balanced':
        return 3
    elif col_val == 'female dominant':
        return 4
    else:
        return 5

def get_gender_dominant_group_count_df():
    jobs = get_jobs_df()

    grouped_jobs = jobs.pivot_table(
        columns=['sex'], 
        values=['count', 'perc'], 
        index=['year', 'job']
    )
    grouped_jobs['gender_dominant_group'] = grouped_jobs.apply(categorize_gender_dominant_group, axis=1)
    grouped_jobs = grouped_jobs[grouped_jobs['gender_dominant_group'] != 'no job']
    gender_dominant_group_count_df = (
        grouped_jobs.groupby(['year', 'gender_dominant_group']).size().unstack(fill_value = 0)
    )
    gender_dominant_group_count_df = gender_dominant_group_count_df.reset_index()
    gender_dominant_group_count_df.columns.name = ''

    # Set the total column
    gender_dominant_group_count_df['total'] = gender_dominant_group_count_df.loc[:, gender_dominant_group_count_df.columns != 'year'].apply(sum, axis = 1)

    gender_dominant_group_count_df = gender_dominant_group_count_df[['year','only male','male dominant','balanced', 'female dominant', 'only female', 'total']]

    gender_dominant_group_count_df = gender_dominant_group_count_df.drop('total', axis=1)

    gender_dominant_group_count_df = gender_dominant_group_count_df.melt(
        id_vars=['year'],
        var_name='job_gender_dominant_group', 
        value_name='total'
    )

    gender_dominant_group_count_df['sort_order'] = gender_dominant_group_count_df['job_gender_dominant_group'].apply(sort_order)
    return gender_dominant_group_count_df

def get_gender_dominancy_groups():
    return ['only male','male dominant','balanced', 'female dominant', 'only female']