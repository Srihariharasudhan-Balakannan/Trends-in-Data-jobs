# imports
from github import Github
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import plotly.graph_objs as gobj    
import requests
import json
# from geopy.geocoders import Nominatim
from mailer import EmailSender
from datetime import datetime
from geopy.geocoders import Photon


class TrendsInDataJobs:
    def __init__(self):
        pass


    def get_repository(self):
        """
        Get GitHub repository object.
        """
        access_token = st.secrets["access_token"]
        repo_str = 'Srihariharasudhan-Balakannan/Trends-in-Data-jobs'
        g = Github(access_token)
        repo = g.get_repo(repo_str)
        return repo


    def get_new_file(self, folder:str):
        """
        Iterate through the files and get the most recent one.
        """
        if folder not in ['source', 'consumption', 'target']:
            raise Exception("folder is either 'source' or 'consumption' or 'target'")
        repo = self.get_repository()
        contents = repo.get_contents(folder)
        path = ''
        for c in contents:
            if path < c.path:
                path = c.path
        return path


    def get_file_path(self, folder:str, path_type:str):
        """
        Get file path from GitHub repository.
        """
        github_url = 'https://github.com'
        repo = 'Srihariharasudhan-Balakannan/Trends-in-Data-jobs'
        branch = 'master'
        file_path = self.get_new_file(folder=folder)
        file_url = github_url + '/' + repo + '/blob/' + branch + '/' + file_path
        if path_type == 'url':
            return file_url
        elif path_type == 'raw':
            return file_url.replace('github', 'raw.githubusercontent').replace('blob/', '')
        else:
            raise Exception("path_type is either 'url' or 'raw'")


    def read_json(self, keys, path):
        """
        Read JSON file and extract specific keys.
        """
        try:
            if path.startswith("https://raw.githubusercontent.com"):
                # Fetch the JSON data from the GitHub raw URL
                response = requests.get(path)
                
                # Check if request was successful
                if response.status_code == 200:
                    # Load JSON data into a dictionary
                    data = json.loads(response.text)
                    return {key: data.get(key) for key in keys}
                else:
                    print("Failed to fetch JSON data:", response.status_code)
                    return None
            else:
                with open(path, 'r') as file:
                    data = json.load(file)
                    return {key: data.get(key) for key in keys}
        except FileNotFoundError:
            print("File not found:", path)
            return None
        
    def filename_to_sentence(self, url):
        """
        Convert a timestamp filename into a human-readable sentence.
        """
        # Extract filename from the URL
        filename = url.split('/')[-1]
        
        # Remove the file extension
        filename_without_ext = filename.split('.')[0]
        
        # Split the filename using hyphen as delimiter
        parts = filename_without_ext.split('-')
        
        # Extract date and time from the filename
        date_str = '-'.join(parts[:3])
        time_str = ':'.join(parts[3:])
        
        # Convert date and time strings to datetime objects
        dt_object = datetime.strptime(date_str + ' ' + time_str, '%Y-%m-%d %H:%M:%S')
        
        # Format the datetime object into a human-readable sentence
        sentence = dt_object.strftime("Last updated on %A, %B %d, %Y at %I:%M %p")
        
        return sentence


    def batch_geocode(self, locations):
        """
        Batch geocoding to get coordinates for multiple locations.
        """
        geolocator = Photon(user_agent="MyApp")
        geocoded_data = [geolocator.geocode(location) for location in locations]
        lst = [(data.latitude, data.longitude) if data else (-1, -1) for data in geocoded_data]
        return lst


    def add_coordinates(self, df, col_name):
        """
        Add coordinates to DataFrame based on location column.
        """
        locations = df[col_name].tolist()
        latitudes, longitudes = zip(*self.batch_geocode(locations))
        df['latitude'] = latitudes
        df['longitude'] = longitudes
        res_df = df[(df['latitude'] > 0) & (df['longitude'] > 0)]
        return res_df


    def get_target_data(self, job_role:str):
        """
        Get expected target data set for the specified job role.
        """
        raw_pth = self.get_file_path(folder='target', path_type='raw')
        json_data = self.read_json([job_role], raw_pth)
        return json_data.get(job_role)


    def get_dataframes(self, data):
        """
        Convert retrieved data dictionary into separate pandas DataFrames.
        Returns DataFrames for company, skill, location, job type, and experience data.
        """
        company_dict = data.get('company_dict', {})
        skill_dict = data.get('skill_dict', {})
        location_dict = data.get('location_dict', {})
        job_type_dict = data.get('job_type_dict', {})
        experience_dict = data.get('experience_dict', {})

        cmp_df = pd.DataFrame(list(company_dict.items()), columns=['company names', 'vacancy points'])
        skl_df = pd.DataFrame(list(skill_dict.items()), columns=['skills', 'demand points'])
        loc_df = pd.DataFrame(list(location_dict.items()), columns=['cities', 'job counts'])

        # Adding co-ordinates to cities for plotting
        # Adding an overall percentage to cities for plotting
        sum_counts = loc_df['job counts'].sum()
        loc_df['percent'] = (loc_df['job counts'] / sum_counts) * 100

        # Add co-ordinates to cities, for plotting
        loc_df = self.add_coordinates(loc_df, 'cities')

        jty_df = pd.DataFrame(list(job_type_dict.items()), columns=['job type', 'count'])
        exp_df = pd.DataFrame(list(experience_dict.items()), columns=['job level', 'count'])

        return cmp_df, skl_df, loc_df, jty_df, exp_df


    def plot_map(self, loc_df):
        """
        Plot map using location DataFrame.
        """
        # Create data for choropleth map
        data = dict(
            type='choropleth',
            locations=['india'],
            locationmode='country names',
            z=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
        )

        # Create the figure object
        map = gobj.Figure(data=[data])

        # Update the geographic information
        map.update_geos(fitbounds='locations', visible=False)

        # Update traces
        map.update_traces(showscale=False, hoverinfo="text")

        # Add scattergeo trace for cities
        map.add_trace(
            go.Scattergeo(
                lon=loc_df['longitude'],
                lat=loc_df['latitude'],
                text=loc_df['cities'],
                hoverinfo="text",
                marker=dict(
                    size=loc_df['percent'] + 5,
                    color='#0083B8'
                ),
                hoverlabel=dict(namelength=0)
            )
        )

        # Update layout
        map.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            dragmode=False
        )
        map['layout'].update(autosize=True)

        return map


    def plot_charts(self, cmp_df, skl_df, loc_df, jty_df, exp_df):
        """
        Plot various charts based on the provided DataFrames.
        Returns the generated chart objects.
        """
        cmp_fig = px.bar(cmp_df, x='vacancy points', y='company names', orientation='h', title='Top companies', 
                         color_discrete_sequence=["#0083B8"] * len(cmp_df), template="plotly_white")
        cmp_fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False)),
            yaxis=dict(autorange="reversed"),
            dragmode=False
        )

        skl_fig = px.bar(skl_df, x='skills', y='demand points', orientation='v', title='Top skills', 
                         color_discrete_sequence=["#0083B8"] * len(skl_df), template="plotly_white")
        skl_fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False)),
            yaxis=(dict(showgrid=False)),
            dragmode=False
        )

        loc_fig = px.bar(loc_df, x='cities', y='job counts', orientation='v', title='Top cities', 
                         color_discrete_sequence=["#0083B8"] * len(loc_df), template="plotly_white")
        loc_fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False)),
            yaxis=(dict(showgrid=False)),
            dragmode=False
        )

        jty_fig = px.pie(jty_df, values='count', names='job type', title='Job type - ratio')
        jty_fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            dragmode=False
        )

        exp_fig = px.pie(exp_df, values='count', names='job level', title='Job level - ratio')
        exp_fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            dragmode=False
        )

        return cmp_fig, skl_fig, loc_fig, jty_fig, exp_fig


    def load_data(self, option):
        """
        Load data based on the selected job role.
        """
        target_dict = self.get_target_data(option.lower())
        cmp_df, skl_df, loc_df, jty_df, exp_df = self.get_dataframes(target_dict)
        return cmp_df, skl_df, loc_df, jty_df, exp_df


    def visualize_data(self, option):
        """
        Visualize the data based on the selected job role.
        """
        with st.spinner('Please wait for few seconds ...'):
            cmp_df, skl_df, loc_df, jty_df, exp_df = self.load_data(option)
            cmp_fig, skl_fig, loc_fig, jty_fig, exp_fig = self.plot_charts(cmp_df, skl_df, loc_df, jty_df, exp_df)
            map_fig = self.plot_map(loc_df)

        # Plot the visualizations
        st.markdown("---")
        left_column, right_column = st.columns(2)
        config = {'displayModeBar': False}

        if cmp_df.empty:
            st.write("No company data available.")
        else:
            left_column.plotly_chart(cmp_fig, use_container_width=True, config=config)

        if skl_df.empty:
            st.write("No skill data available.")
        else:
            right_column.plotly_chart(skl_fig, use_container_width=True, config=config)

        if loc_df.empty:
            st.write("No location data available.")
        else:
            left_column.plotly_chart(loc_fig, use_container_width=True, config=config)
            right_column.plotly_chart(map_fig, use_container_width=True, config=config)

        if jty_df.empty:
            st.write("No job type data available.")
        else:
            left_column.plotly_chart(jty_fig, use_container_width=True, config=config)

        if exp_df.empty:
            st.write("No experience data available.")
        else:
            right_column.plotly_chart(exp_fig, use_container_width=True, config=config)

        hide_st_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    header {visibility: hidden;}
                    </style>
                    """
        st.markdown(hide_st_style, unsafe_allow_html=True)


    def run(self):
        """
        Execute the Streamlit application.
        """
        st.set_page_config(page_title="Trends in Data jobs (India)", page_icon=":bar_chart:", layout="wide")
        st.title('Trends in Data jobs')
        with st.form('Form'):
            job_roles = (
                "Data Engineer", 
                "Data Analyst", 
                "Data Architect", 
                "Data Scientist", 
                "Machine Learning Engineer"
                 )
            option = st.selectbox('Select a job role?', job_roles)
            submit = st.form_submit_button('Submit')

        if submit:  
            try:
                pth = self.get_new_file(folder='target')
                sentence = self.filename_to_sentence(pth)
                st.write('\n')
                st.write('\n')
                st.text(sentence)
                self.visualize_data(option=option)
            except Exception as e:
                print(e)
                emailsender = EmailSender()
                emailsender.send_mail(receiver_id=st.secrets["receiver_id"], exception=e) 
                st.markdown("---")
                st.write("Something went wrong. Please select another job role! We have notified the developer about this issue, and it will be fixed soon")
