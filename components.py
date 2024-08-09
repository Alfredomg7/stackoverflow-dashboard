from dash import html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px

def create_tabs(options, id='tabs'):
    """
    Create tabs using Dash Bootstrap Components.
    
    Parameters
    ----------
    options : list
        A list of options for the tabs.
    id : str
        The ID of the tabs.

    Returns
    -------
    dbc.Col
        The tabs component. 
    """
    tabs = dbc.Col(dbc.Tabs(
        id=id,
        active_tab=options[0],
        class_name='nav nav-pills nav-fill d-flex justify-content-center w-100 bg-primary',
        children=[
            dbc.Tab(label=option, tab_id=option, class_name='nav-item fw-bold') for option in options
        ]
        ), width=12, className='my-2')
    return tabs

def create_checklist(options, id='checklist', title='Age Filter'):
    """
    Create a checklist using Dash Bootstrap Components with a title.
    
    Parameters
    ----------
    options : list
        A list of options for the checklist.
    id : str
        The ID of the checklist.
    title : str
        The title text to be displayed on the left side.

    Returns
    -------
    dbc.Row
        A Dash Bootstrap Components row containing the title and the checklist.
    """
    checklist = dbc.Checklist(
        id=id,
        options=options,
        inline=True,
        switch=True,
        className='d-flex justify-content-start w-100 text-white'
    )
    
    layout = dbc.Row(
        [
            dbc.Col(html.Div(title, 
                             className='text-light text-center fs-4'),
                             width=2),
            dbc.Col(checklist, width=10)
        ],
        className='my-3',
    )
    
    return layout

def create_top_by_category_chart(df, category):
    """
    Create a bar chart showing the top 'HaveWorkedWith' and 'WantToWorkWith' for the selected category.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the survey data.
    category : str
        The selected category.
    
    Returns
    -------
    go.Figure
        The bar chart figure.
    """
    n_top = 20

    # Prepare 'HaveWorkedWith' data
    have_worked_with_column = category + 'HaveWorkedWith'
    have_worked_with_votes = df[have_worked_with_column].str.split(';', expand=True).stack()
    top_have_worked_with = have_worked_with_votes.value_counts().head(n_top).sort_values(ascending=True)
    
    # Prepare 'WantWorkWith' data
    want_to_work_with_column = category + 'WantToWorkWith'
    want_to_work_with_votes = df[want_to_work_with_column].str.split(';', expand=True).stack()
    top_want_to_work_with = want_to_work_with_votes.value_counts().head(n_top).sort_values(ascending=True)

    # Create the bar chart
    fig = go.Figure()

    # Add 'HaveWorkedWith' data (plot to the left)
    fig.add_trace(go.Bar(
        x=-top_have_worked_with.values,
        y=top_have_worked_with.index,
        name='Have Worked With',
        orientation='h',
        xaxis='x',
        yaxis='y'
    ))
    
    # Add 'WantToWorkWith' data (plot to the right)
    fig.add_trace(go.Bar(
        x=top_want_to_work_with.values,
        y=top_want_to_work_with.index,
        name='Want to Work With',
        orientation='h',
        xaxis='x2',
        yaxis='y2'
    ))

    # Update the layout
    fig.update_layout(
        title=f'Top {n_top} {category} Want to Work With vs. Have Worked With',
        title_font_size=20,
        title_x=0.5,
        xaxis=dict(
            title='Number of Votes',
            title_font_size=18,
            side='left',
            showgrid=False,
            range=[-top_have_worked_with.values.max() * 2, 0]
        ),
        xaxis2=dict(
            title='',
            title_font_size=18,
            overlaying='x',
            side='right',
            showgrid=False,
            range=[0, top_have_worked_with.values.max() * 2]
        ),
        yaxis=dict(
            tickfont_size=16,
        ),
        yaxis2=dict(
            tickfont_size=16,
            overlaying='y',
            side='right',
        ),
        legend=dict(
            x=0.4,
            y=0,
            traceorder='normal',
            orientation='v',
            font=dict(size=14),
            bgcolor='rgba(34, 34, 34,0.7)'
        ),
        barmode='overlay',
        bargap=0.2
    )
    
    return fig

def create_choropleth_map(df, country_column):
    """
    Create a choropleth map showing the distribution of the selected column.
    
    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the survey data.
    country_column : str
        The column containing the country name
    
    Returns
    -------
    go.Figure
        The choropleth map figure.
    """

    df_count = df.groupby(country_column).size().reset_index(name='Respondents')

    fig = px.choropleth(
        df_count,
        locations=country_column,
        locationmode='country names',
        color='Respondents',
        hover_name=country_column,
        color_continuous_scale=px.colors.sequential.Tealgrn,
        title=f'Distribution of Survey Respondents by {country_column}',
    )

    fig.update_layout(
        title_font_size=20,
        title_x=0.5,
    )

    return fig