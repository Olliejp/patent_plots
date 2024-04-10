import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.io as pio
pio.templates.default = "plotly"

st.title("Patent plots")

df = pd.read_csv("molded_fiber_packaging.csv", index_col=0)

def standardise_name(applicant):
    try:
        applicant_lower = applicant.lower()
        if "wing fat" in applicant_lower:
            return "WING FAT MOLDED FIBER PACKAGING TECHNOLOGY CO. LTD"
        elif "huhtamaki" in applicant_lower:
            return "HUHTAMAKI MOLDED FIBER TECH BV"
        else:
            return applicant
    except Exception:
        return applicant

df['Applicant'] = df['Applicant'].apply(standardise_name)

applicant_counts = df['Applicant'].value_counts().reset_index()
applicant_counts.columns = ['Applicant', 'Count']

df['Filing Date'] = pd.to_datetime(df['Filing Date'])
df = df.sort_values('Filing Date')
df['Year'] = df['Filing Date'].dt.year
patents_per_year = df.groupby('Year').size().cumsum()

cumulative_patents_df = patents_per_year.reset_index()
cumulative_patents_df.columns = ['Year', 'Cumulative Patents']

st.header("Patent applications for Molded Fiber Packaging")

fig = px.pie(applicant_counts[applicant_counts['Count']>=3], names='Applicant', values='Count', hole=0.4,
             title='Proportion of patents. Applicants with greater than 3 patents')
st.plotly_chart(fig)

fig_1 = px.line(cumulative_patents_df[cumulative_patents_df['Year']>=2000], x='Year', y='Cumulative Patents', title='Cumulative Number of Patents Filed Per Year')
st.plotly_chart(fig_1)

applicant_counts = df['Applicant'].value_counts()
applicants_with_3_or_more_filings = applicant_counts[applicant_counts >= 3].index
filtered_df = df[df['Applicant'].isin(applicants_with_3_or_more_filings)]
cumulative_patents = filtered_df.groupby(['Applicant', 'Year']).size().groupby(level=0).cumsum().reset_index(name='Cumulative Patents')

years = range(cumulative_patents['Year'].min(), cumulative_patents['Year'].max() + 1)
all_applicants = cumulative_patents['Applicant'].unique()

new_rows = []
for applicant in all_applicants:
    applicant_years = cumulative_patents[cumulative_patents['Applicant'] == applicant]['Year']
    missing_years = set(years) - set(applicant_years)
    for year in missing_years:
        new_rows.append({'Applicant': applicant, 'Year': year, 'Cumulative Patents': 0})


missing_years_df = pd.DataFrame(new_rows)
cumulative_patents = pd.concat([cumulative_patents, missing_years_df], ignore_index=True)


cumulative_patents = cumulative_patents.sort_values(by=['Applicant', 'Year'])
cumulative_patents['Cumulative Patents'] = cumulative_patents.groupby('Applicant')['Cumulative Patents'].cummax()

fig_2 = px.line(cumulative_patents, x='Year', y='Cumulative Patents', color='Applicant', title='Cumulative number of patents filed per year by applicant (more than 3 patents)')
st.plotly_chart(fig_2)

st.header("Patent applications for dry-forming and cellulose")

df_2 = pd.read_csv("dry-forming-cellulose.csv", index_col=0)

def standardise_name_2(applicant):
    try:
        applicant_lower = applicant.lower()
        if "scan" in applicant_lower:
            return "SCAN-WEB I/S"
        elif "pulpac" in applicant_lower:
            return "PULPAC"
        elif "pupac" in applicant_lower:
            return "PULPAC"
        elif "kimberly" in applicant_lower:
            return "KIMBERLY CLARK CO"
        elif "ekonomisk" in applicant_lower:
            return "SÖDRA SKOGSÄGARNA EKONOMISK FÖRENING"
        elif "oerlikon" in applicant_lower:
            return "OERLIKON TEXTILE GMBH & CO KG"
        elif "nauchno" in applicant_lower:
            return "VSESOYUZNYJ NAUCHNO-ISSLEDOVATELSKIJ"
        else:
            return applicant
    except Exception:
        return applicant

df_2['Applicant'] = df_2['Applicant'].apply(standardise_name_2)
names_to_exclude = ['VSESOYUZNYJ NAUCHNO-ISSLEDOVATELSKIJ', 'พูลแพค เอบี', '欧瑞康纺织有限及两合公司']
df_2 = df_2[~df_2['Applicant'].isin(names_to_exclude)]

applicant_counts = df_2['Applicant'].value_counts().reset_index()
applicant_counts.columns = ['Applicant', 'Count']

fig_3 = px.pie(applicant_counts, names='Applicant', values='Count', hole=0.4,
             title='Proportion of patents')
st.plotly_chart(fig_3)

df_2['Filing Date'] = pd.to_datetime(df_2['Filing Date'], format="%d.%m.%Y")

df_2 = df_2.sort_values('Filing Date')
df_2['Year'] = df_2['Filing Date'].dt.year
patents_per_year = df_2.groupby('Year').size().cumsum()

cumulative_patents_df = patents_per_year.reset_index()
cumulative_patents_df.columns = ['Year', 'Cumulative Patents']

fig_4 = px.line(cumulative_patents_df[cumulative_patents_df['Year']>=2000], x='Year', y='Cumulative Patents', title='Cumulative Number of Patents Filed Per Year')
st.plotly_chart(fig_4)

applicant_counts = df_2['Applicant'].value_counts()
applicants_with_3_or_more_filings = applicant_counts[applicant_counts >= 2].index
filtered_df = df_2[df_2['Applicant'].isin(applicants_with_3_or_more_filings)]
cumulative_patents = filtered_df.groupby(['Applicant', 'Year']).size().groupby(level=0).cumsum().reset_index(name='Cumulative Patents')


years = range(cumulative_patents['Year'].min(), cumulative_patents['Year'].max() + 1)
all_applicants = cumulative_patents['Applicant'].unique()

new_rows = []
for applicant in all_applicants:
    applicant_years = cumulative_patents[cumulative_patents['Applicant'] == applicant]['Year']
    missing_years = set(years) - set(applicant_years)
    for year in missing_years:
        new_rows.append({'Applicant': applicant, 'Year': year, 'Cumulative Patents': 0})


missing_years_df = pd.DataFrame(new_rows)
cumulative_patents = pd.concat([cumulative_patents, missing_years_df], ignore_index=True)


cumulative_patents = cumulative_patents.sort_values(by=['Applicant', 'Year'])
cumulative_patents['Cumulative Patents'] = cumulative_patents.groupby('Applicant')['Cumulative Patents'].cummax()

fig_5 = px.line(cumulative_patents, x='Year', y='Cumulative Patents', color='Applicant', title='Cumulative number of patents filed per year by applicant (more than 2 patents)')
st.plotly_chart(fig_5)
