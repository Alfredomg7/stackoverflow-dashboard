import components as cmp
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd
import plotly.graph_objects as go

# Initialize the Dash app with bootstrap theme
load_figure_template("vapor")
app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])

# Load the data
df_path = 'data/lol.csv'
df = pd.read_csv(df_path)

# Create tabs for filter by category
category_options = [col.replace('HaveWorkedWith', '') for col in df.columns if 'HaveWorkedWith' in col]
category_tabs = cmp.create_tabs(category_options, id='category-tabs')

# Create checklist to filter by Age
age_options = [
    {'label': age.split(' years old')[0] if 'years old' in age else age, 'value': age}
    if age != '65 years or older' else {'label': '65+', 'value': '65+'}
    if age != 'Under 18' else {'label': '18-', 'value': '18-'}
    for age in df['Age'].unique()
]
age_checklist = cmp.create_checklist(age_options, id='age-checklist')

# Create the figures
fig_style = {'height': '80vh', 'width': '100%', 'margin': '0 auto', 'margin-bottom': '20px'}
top_by_category_figure = dcc.Graph(id='top_bar_chart', style=fig_style)
choropleth_map = dcc.Graph(id='choropleth_map', style=fig_style)

app.layout = html.Div([
    html.H1('Stack Overflow Survey Data', className='text-center my-4'),
    category_tabs,
    age_checklist,
    top_by_category_figure,
    choropleth_map
], className='m-4')

# Create the callback for the top have worked vs want to work with chart
@app.callback(
    Output('top_bar_chart', 'figure'),
    Input('category-tabs', 'active_tab'),
    Input('age-checklist', 'value')
)
def update_top_bar_chart(category, selected_ages):
    """
    Update the top have worked with chart based on the selected category and age filters.
    """
    if selected_ages:
        filtered_df = df[df['Age'].isin(selected_ages)]
    else:
        filtered_df = df.copy()

    if (category + 'HaveWorkedWith') not in filtered_df.columns:
        return go.Figure(data=[go.Bar()])
    
    fig = cmp.create_top_by_category_chart(filtered_df, category)
    
    return fig

# Create the callback for the choropleth map
@app.callback(
    Output('choropleth_map', 'figure'),
    Input('age-checklist', 'value')
)
def update_choropleth_map(selected_ages):
    """
    Update the choropleth map based on the selected age filters.
    """
    if selected_ages:
        filtered_df = df[df['Age'].isin(selected_ages)]
    else:
        filtered_df = df.copy()
    
    fig = cmp.create_choropleth_map(filtered_df, 'Country')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)