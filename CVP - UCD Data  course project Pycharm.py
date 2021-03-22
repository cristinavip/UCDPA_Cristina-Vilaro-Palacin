import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

country_vaccinations = pd.read_csv\
    (r"C:\Users\Lenovoi7Geforce\Desktop\CVP - UCD Data course project\country_vaccinations.csv")
covid_summary = pd.read_csv(
    r"C:\Users\Lenovoi7Geforce\Desktop\CVP - UCD Data course project\worldometer_coronavirus_summary_data.csv")
covid_daily = pd.read_csv\
    (r"C:\Users\Lenovoi7Geforce\Desktop\CVP - UCD Data course project\worldometer_coronavirus_daily_data.csv")

covid_summary_vaccinations = country_vaccinations.merge(covid_summary, on='country')
cosum = covid_summary_vaccinations.merge(covid_daily, on='country')

cosum.drop_duplicates

print(cosum.info())

cosum_inf_as_na = True

cosum.replace('', np.NaN)

#  plot Continents

EU_cosum_group_by = cosum.groupby(['continent'])['total_cases_per_1m_population',
                                                 'total_deaths_per_1m_population'].sum()
EU_group_sorted = EU_cosum_group_by.sort_values(by=["total_cases_per_1m_population"], axis=0, ascending=False,
                                                inplace=False, kind='quicksort', na_position='last')
cosum_fig = EU_group_sorted.plot(kind='bar', color=['forestgreen', 'orange'], edgecolor='black')
cosum_fig.legend(["Total cases per 1m population", "Total deaths per 1m population"])
plt.title("COVID19 cases and deaths per 1m population by continent", fontweight='bold', y=1.05)
plt.xlabel("Continents", fontweight='bold')
plt.ylabel("Cases and deaths per 1m population", fontweight='bold')
plt.tight_layout()

plt.show()


# EU COUNTRIES: total cases/ deaths

EU_countries = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia', 'Denmark', 'Estonia', 'Finland',
                'France', 'Germany', 'Greece', 'Hungary', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg',
                'Malta', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden']

EU_cosum = cosum[cosum['country'].isin(EU_countries)]

EU_cosum_total_conf = EU_cosum.sort_values(by=["total_confirmed"], axis=0, ascending=False, inplace=False,
                                           kind='quicksort', na_position='last')

x1 = EU_cosum_total_conf['country']
y1 = EU_cosum_total_conf['total_confirmed']
colors = EU_cosum_total_conf['total_deaths']
plt.scatter(x1, y1, c=colors, cmap='autumn_r')
plt.title("Total confirmed COVID19 cases and deaths in EU countries", fontweight='bold', y=1.08)
plt.xlabel("EU countries", fontweight='bold')
plt.tick_params(axis='x', labelrotation=90)
plt.ylabel("Total cases", fontweight='bold')
cbar = plt.colorbar()
cbar.set_label("Total deaths", fontweight='bold')
plt.grid()
plt.tight_layout()
plt.show()

# EU COUNTRIES: cases/deaths per 1m population


EU_cosum_cases_1m = EU_cosum.sort_values(by=["total_cases_per_1m_population"], axis=0, ascending=False, inplace=False,
                                         kind='quicksort', na_position='last')

x = EU_cosum_cases_1m['country']
y = EU_cosum_cases_1m['total_cases_per_1m_population']
colors = EU_cosum_cases_1m['total_deaths_per_1m_population']
plt.scatter(x, y, c=colors, cmap='autumn_r')
plt.title("COVID19 cases and deaths per 1m population in EU countries", fontweight='bold', y=1.05)
plt.xlabel("EU countries", fontweight='bold')
plt.tick_params(axis='x', labelrotation=90)
plt.ylabel("Cases per 1m population", fontweight='bold')
cbar = plt.colorbar()
cbar.set_label("Deaths per 1m population", fontweight='bold')
plt.grid()
plt.tight_layout()
plt.show()

# Ireland cumulative cases

cosum_country_ind = cosum.set_index("country")
Ire = cosum_country_ind.loc[['Ireland']]
Ire['date_y'] = pd.to_datetime(Ire['date_y'], format='%Y-%m-%d')

Ire_cumulative_plot = Ire.plot('date_y', 'cumulative_total_cases', markersize=12, color='forestgreen',
                                                linewidth=4, legend=None)
Ire_cumulative_plot.set_xlabel('Date', fontweight='bold')
Ire_cumulative_plot.set_ylabel('Ireland total cases ', fontweight='bold')
Ire_cumulative_plot.set_title('Cumulative COVID19 cases in Ireland overtime', fontweight='bold')
plt.tight_layout()
plt.show()


# Vaccines combinations

vaccines_data = cosum.drop_duplicates(subset=['country'], keep='first')
plt.rcParams.update({'font.size': 15})
vaccines_data_fig = vaccines_data['vaccines'].value_counts().plot(kind='barh', edgecolor='black',
                                                                  color=['limegreen', 'blueviolet', 'teal',
                                                                         'darkred', 'darkturquoise',
                                                                         'navajowhite', 'forestgreen', 'orange',
                                                                         'darkmagenta', 'olive'])

vaccines_data_fig.set_title('Approved COVID19 vaccines per number of countries', fontweight='bold')
vaccines_data_fig.set_xlabel('Number of countries', fontweight='bold')
vaccines_data_fig.set_ylabel('COVID19 Vaccines', fontweight='bold')
plt.tight_layout()
plt.show()

# Vaccines continents stacked

plt.rcParams.update({'font.size': 15})
vaccines_continents = (vaccines_data.groupby(['continent', 'vaccines'])['date_y'].count() / vaccines_data.groupby(
    ['continent'])['date_y'].count())
vaccines_continents_fig = vaccines_continents.unstack().plot.bar(stacked=True, cmap='gist_ncar', edgecolor='black')
vaccines_continents_fig.legend(title='Vaccines combinations', bbox_to_anchor=(1.05, 1), loc='upper left')

vaccines_continents_fig.set_title('Approved COVID19 vaccines combinations per continent', fontweight='bold')
vaccines_continents_fig.set_xlabel('Continent', fontweight='bold')
vaccines_continents_fig.set_ylabel('Frequency', fontweight='bold')
plt.tight_layout()
plt.show()

# Highest number of vaccinations per country (total)

plt.rcParams.update({'font.size': 20})
date_x_sorted = cosum.sort_values(by=["date_x"], ascending=False)
dupli_date_x = date_x_sorted.drop_duplicates(subset=['country'], keep='first')
total_x_ind = dupli_date_x.set_index("country")
total_x_ind_sorted = total_x_ind.sort_values(by=["total_vaccinations"], ascending=False)
total_index_vacc_iloc = total_x_ind_sorted.iloc[0:21]
date_index_vacc_fig = total_index_vacc_iloc.plot(y='total_vaccinations', kind='bar',
                                                 color=['limegreen', 'blueviolet', 'teal', 'darkred', 'darkturquoise',
                                                        'navajowhite', 'forestgreen', 'orange', 'darkmagenta', 'olive'],
                                                 edgecolor='black', legend=None)

date_index_vacc_fig.set_xlabel('Country', fontweight='bold')
date_index_vacc_fig.set_ylabel('Total COVID19 vaccinations', fontweight='bold')
date_index_vacc_fig.set_title('Number of total COVID19 vaccinations per country', fontweight='bold')
plt.tight_layout()
plt.show()


# Highest number of vaccinations per country (per hundred)

plt.rcParams.update({'font.size': 20})
date_x_sorted = cosum.sort_values(by=["date_x"], ascending=False)
dupli_date_x = date_x_sorted.drop_duplicates(subset=['country'], keep='first')
total_x_ind = dupli_date_x.set_index("country")
perhundred_x_ind_sorted = total_x_ind.sort_values(by=["people_vaccinated_per_hundred"], ascending=False)
perhundred_index_vacc_iloc = perhundred_x_ind_sorted.iloc[0:21]
date_index_vacc_fig = perhundred_index_vacc_iloc.plot(y='people_vaccinated_per_hundred', kind='bar', color=['limegreen',
                                                        'blueviolet', 'teal', 'darkred', 'darkturquoise', 'navajowhite',
                                                        'forestgreen', 'orange', 'darkmagenta', 'olive'],
                                                      edgecolor='black', legend=None)

date_index_vacc_fig.set_xlabel('Country', fontweight='bold')
date_index_vacc_fig.set_ylabel('Total COVID19 vaccinations', fontweight='bold')
date_index_vacc_fig.set_title('Number of total COVID19 vaccinations per hundred population per country',
                              fontweight='bold')
plt.tight_layout()
plt.show()


# Daily vaccinations per million in Ireland

cosum_country_ind = cosum.set_index("country")

Ire = cosum_country_ind.loc[['Ireland']]
Ire['date_x'] = pd.to_datetime(Ire['date_x'], format='%d/%m/%y')

x3 = Ire['date_x']
y3 = Ire['daily_vaccinations_per_million']

plt.plot(x3, y3, markersize=20, color='teal', linewidth=4)
plt.title("Daily Covid19 vaccinations per million people in Ireland", fontweight='bold')
plt.tick_params(axis='x', size=8)
plt.xlabel("Date", fontweight='bold')
plt.ylabel("Covid19 vaccinations", fontweight='bold')
plt.tight_layout()
plt.show()

