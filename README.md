# Overview

This Dash application visualizes Stack Overflow survey data, providing insights into survey responses by different categories and age groups. It uses a Bootstrap theme and Plotly for interactive charts and maps.

## Features
- Category Tabs: Allows users to filter data by various categories (e.g., programming languages).
- Age Checklist: Filters data based on user-selected age groups.
- Top Bar Chart: Displays a bar chart of the top categories based on survey responses.
- Choropleth Map: Shows a geographical distribution of survey responses.

## Installation
### Clone the Repository
```bash
git clone https://github.com/Alfredomg7/StackOverFlowSurveyDashboard.git
cd StackOverFlowSurveyDashboard
```

### Install Dependencies
1. Ensure you have Python 3.7+ installed. 
2. Then install the required packages using pip:
```bash
pip install -r requirements.txt
```
3. Download the dataset
You can download the dataset by clicking [here](https://cdn.stackoverflow.co/files/jo7n4k8s/production/49915bfd46d0902c3564fd9a06b509d08a20488c.zip/stack-overflow-developer-survey-2023.zip). Save the file as `data.csv` in the data directory.

## Usage
### Run the Application
Navigate to the project directory and execute the following command:
```bash
python app.py
```

### Access the Dashboard
Open your web browser and go to [http://127.0.0.1:8050](http://127.0.0.1:8050) to view the dashboard.

## Code Explanation
### Initialization
- Dash app is initialized with a Vapor Bootstrap theme.
- Data is loaded from a CSV file.

### Components
- Tabs: Generated for filtering by different survey categories.
- Checklist: For filtering by age groups.

### Figures
- `top_by_category_figure`: A bar chart showing the top categories based on survey data.
- `choropleth_map`: A map visualizing the geographical distribution of survey responses.

### Callbacks
- `update_top_bar_chart`: Updates the top bar chart based on selected category and age filters.
- `update_choropleth_map`: Updates the choropleth map based on selected age filters.

## Contributing
Feel free to submit issues, pull requests, or suggest improvements. Contributions are welcome!
