# 1. Import Dash
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px

# 2. Create a Dash app instance
app = dash.Dash(
    name='Data Science Job - Dashboard ',
    external_stylesheets=[dbc.themes.LUX]
)
app.title = 'Data Science Job - Dashboard'


## --- NAVBAR
navbar = dbc.NavbarSimple(
    brand="Data Science Job in US - Dashboard",
    color="#BC7196",
    dark=True,
    sticky='top',
    style={'textAlign':'center'}
)

## --- LOAD DATASET
data=pd.read_csv('salaries.csv')
data['experience_level'] = data['experience_level'].map({
    'SE':'Senior',
    'EN':'Entry',
    'MI':'Mid',
    'EX':'Expert'})
data['remote_ratio'] = data['remote_ratio'].map({0:'0% Remote',50:'50% Remote', 100:'100% Remote'})
data['company_size'] = data['company_size'].map({'L':'Large','M':'Medium','S':'Small'})
#card
total_job = [
    dbc.CardHeader('Total Unique Job Title'),
    dbc.CardBody([
        html.H5(data['job_title'].nunique())
    ])]
level_job = [
    dbc.CardHeader('Count of Experience Level'),
    dbc.CardBody([
        html.H5(data['experience_level'].nunique())
    ])]
remote = [
    dbc.CardHeader('Total Remote Job Type'),
    dbc.CardBody([
        html.H5(data['remote_ratio'].nunique())
    ])]

## ---PIE CHART---
job = pd.crosstab(
    index=data['experience_level'],
    columns='job_title'
).reset_index().sort_values('job_title', ascending=False)
job

# Visualization
job_pie=px.pie(job,
      names='experience_level',
      values='job_title',
      template='ggplot2',
      color_discrete_sequence=px.colors.sequential.Magenta,
      title='Experience Level among All Jobs',
      labels={'experience_level':'Level',
             'job_title':'Count'},
      hole=0.4)

ratio = pd.crosstab(
    index=data['remote_ratio'],
    columns='job_title'
).reset_index().sort_values('job_title', ascending=False)
job
ratio_viz = px.pie(ratio,
      names='remote_ratio',
      values='job_title',
      template='ggplot2',
      color_discrete_sequence=px.colors.sequential.Magenta,
      title='Count of Remote Possibility Among All Jobs',
      labels={'experience_level':'Level',
             'job_title':'Count'},
      hole=0.4)

# Aggregate data
top_sal=pd.pivot_table(data=data[data['experience_level']=='Entry'],
              index='job_title',
              values='salary',
              aggfunc='median').sort_values('salary',ascending=False).reset_index().head(10)
# top_sal
top_bar=px.bar(
    top_sal.sort_values('salary'),
    x = 'salary',
    y = 'job_title',
    labels = {
        'salary': 'Salary in U$D',
        'job_title':'Job Title'
    },
    color_discrete_sequence=px.colors.sequential.Magenta,
    template = 'ggplot2',
    title = 'Top 10 Job Title by Salary with Entry Level')
    

## --- BAR CHART ---
tail_sal=pd.pivot_table(data=data[data['experience_level']=='Entry'],
              index='job_title',
              values='salary',
              aggfunc='median').sort_values('salary',ascending=False).reset_index().tail(10)
# tail_sal
tail_bar=px.bar(
    tail_sal.sort_values('salary'),
    x = 'salary',
    y = 'job_title',
    labels = {
        'salary': 'Salary in U$D',
        'job_title':'Job Title'
    },
    template = 'ggplot2',
    color_discrete_sequence=px.colors.sequential.Magenta,
    title = 'Bottom 10 Job Title by Salary with Entry Level')

#agg company size
size = pd.pivot_table(data=data[data['experience_level']=='Entry'],
              index='job_title',
              values='salary',
               columns='company_size',
              aggfunc='mean').reset_index()
size = size.fillna(method='bfill')
size = size.fillna(method='ffill')
size['total'] = size['Large']+size['Medium']+size['Small']
#size company figure
rank_size = px.bar(size.sort_values('total').head(12), 
             y='job_title', 
             x=['Large','Medium','Small'], 
             template = 'ggplot2',
             color_discrete_sequence=px.colors.sequential.Magenta,
             labels={'job_title':'Job Title','value':'Salary'},
             title = 'The Average of Salary by Company Size in Entry Level')

## --- DASHBOARD LAYOUT
app.layout = html.Div([
        navbar,

        #main page
        html.Div([
                #Row 1
                dbc.Row([
                    dbc.Col([html.Br(),
                        dbc.Row([dbc.Card(total_job, color='#DA60CA', inverse=True)]),
                        html.Br(),
                        dbc.Row([dbc.Card(level_job, color='#DA60CA', inverse=True)]),
                        html.Br(),
                        dbc.Row([html.Br(),dbc.Card(remote, color='#DA60CA', inverse=True)]),
                    ],width=2),
                    dbc.Col([dcc.Graph(id='pie1', figure=job_pie)],width=5),
                    dbc.Col([dcc.Graph(id='pie2', figure=ratio_viz)],width=5)                    
                ],),
                html.Br(),

                #Row 2 
                dbc.Row([
                    dbc.Row([
                        html.Br(),
                        html.H3('Top & Bottom 10 Ranking Salary by Experience Level'),
                        dbc.Card([
                            dbc.CardHeader('Select Experience Level'),
                            dcc.Dropdown(id='dropdown1', options=data['experience_level'].unique(),value='Entry')])
                    ]),
                    dbc.Row([
                        dbc.Col([dcc.Graph(id='top', figure=top_bar),],width=6),
                        dbc.Col([dcc.Graph(id='bottom', figure=tail_bar),],width=6)
                    ])
                ],),
                html.Br(),

                #Row 4
                dbc.Row([
                    dbc.Row([
                        html.H3('The Average of Salary by Company Size'),
                        dbc.Card([
                            html.Br(),
                            dbc.CardHeader('Select Experience Level'),
                            dcc.Dropdown(id='dropdown2', options=data['experience_level'].unique(),value='Entry')])
                    ]),
                    dbc.Row([
                        dbc.Col([dcc.Graph(id='company_size', figure=rank_size),],width=12)
                    ])
                ],),

                html.Br(), 
                html.Br(),
                dbc.Row([
                    html.P(['By: Gilbert G P Tampubolon'], style={'textAlign':'center', 'color':'#222A2A'})
                    ]),
            ],
            style={
                'backgroundColor':'#E2E2E2',
                'paddingRight':'30px',
                'paddingLeft':'30px',
                'paddingBottom':'30px',
                'paddingTop':'30px'
                }
        ),

    ]
)
## PLOT3 Callback
@app.callback(
    Output(component_id='company_size', component_property='figure'),
    Input(component_id='dropdown2',component_property='value'))
def update_figure(som):
    size = pd.pivot_table(data=data[data['experience_level']==som],
              index='job_title',
              values='salary',
               columns='company_size',
              aggfunc='mean').reset_index()
    size = size.fillna(method='bfill')
    size = size.fillna(method='ffill')
    size['total'] = size['Large']+size['Medium']+size['Small']
    #size company figure
    rank_size = px.bar(size.sort_values('total').head(10), 
                y='job_title', 
                x=['Large','Medium','Small'], 
                template = 'ggplot2',
                color_discrete_sequence=px.colors.sequential.Magenta,
                labels={'job_title':'Job Title','value':'Salary'},
                title = f'The Average of Salary by Company Size in {som} Level')
    return(rank_size)

@app.callback(
    Output(component_id='bottom', component_property='figure'),
    Input(component_id='dropdown1',component_property='value'))
def update_figure(level):
    tail_sal=pd.pivot_table(data=data[data['experience_level']==level],
              index='job_title',
              values='salary',
              aggfunc='median').sort_values('salary',ascending=False).reset_index().tail(12)
# tail_sal
    tail_bar=px.bar(
        tail_sal.sort_values('salary'),
        x = 'salary',
        y = 'job_title',
        labels = {
            'salary': 'Salary in U$D',
            'job_title':'Job Title'
        },
        template = 'ggplot2',
        color_discrete_sequence=px.colors.sequential.Magenta,
        title = f'Bottom 10 Job Title by Salary with {level} Level')
    return(tail_bar)

@app.callback(
    Output(component_id='top', component_property='figure'),
    Input(component_id='dropdown1',component_property='value'))

def update_figure(top):
    top_sal=pd.pivot_table(data=data[data['experience_level']==top],
              index='job_title',
              values='salary',
              aggfunc='median').sort_values('salary',ascending=False).reset_index().head(10)
# top_sal
    top_bar=px.bar(
        top_sal.sort_values('salary'),
        x = 'salary',
        y = 'job_title',
        labels = {
            'salary': 'Salary in U$D',
            'job_title':'Job Title'
        },
        template = 'ggplot2',
        color_discrete_sequence=px.colors.sequential.Magenta,
        title = f'Top 10 Job Title by Salary with {top} Level')
    return(top_bar)


# 3. Start the Dash server
if __name__ == "__main__":
    app.run_server()
