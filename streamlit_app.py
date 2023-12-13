# imports
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import plotly.graph_objs as gobj
from scrape_data import get_job_details
from functions import roll_up_data, add_coordinates

# run function 
def run():
    
    # set page configuration
    st.set_page_config(page_title="Trends in Data jobs (India)", page_icon=":bar_chart:", layout="wide")

    # title
    st.title('Trends in Data jobs')

    # drop-down option
    with st.form('Form'):
        option = st.selectbox('Select a job role?', ("Data Engineer", "Data Analyst", "Data Architect", "Data Scientist", "Machine Learning Engineer"))
        submit = st.form_submit_button('Submit')

    # once submit button is pressed
    if submit:
        
        # try except block to handle empty data returned post web scraping
        try:
            
            # display waiting text with in-build loading graphics until web-scraping and data processing is completed
            with st.spinner('Web-scraping in progress, please wait for few seconds ...'):
                
                # get job details as a list by web-scraping, and data cleansing
                job_lst = get_job_details(option)
                
                # roll up extracted data and get required information as individual dictionaries
                company_dict , skill_dict, location_dict, job_type_dict, experience_dict = roll_up_data(job_lst)
    
                # company data-frame
                cmp_df = pd.DataFrame(list(company_dict.items()))
                cmp_df.columns = ['company names', 'vacancy points']
    
                # skill data-frame
                skl_df = pd.DataFrame(list(skill_dict.items()))
                skl_df.columns = ['skills', 'demand points']
    
                # location data-frame
                loc_df = pd.DataFrame(list(location_dict.items()))
                loc_df.columns = ['cities', 'job counts']
                # add co-ordinates to cities, for plotting
                loc_df = add_coordinates(loc_df, 'cities')
                # add an overall percentage to cities, for plotting 
                sum = loc_df['job counts'].sum()
                loc_df['percent'] = (loc_df['job counts']/sum)*100
    
                # job-type data-frame
                jty_df = pd.DataFrame(list(job_type_dict.items()))
                jty_df.columns = ['job type', 'count']
    
                # experience data-frame
                exp_df = pd.DataFrame(list(experience_dict.items()))
                exp_df.columns = ['job level', 'count']
    
                # map object creation
                data = dict(type = 'choropleth', 
                            locations = ['india'], 
                            locationmode = 'country names', 
                            z=[1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0]) 
                map = gobj.Figure(
                    data = [data]
                )
                map.update_geos(
                    fitbounds='locations', 
                    visible=False
                )
                map.update_traces(
                    showscale=False, 
                    hoverinfo="text"
                )
                map.add_trace(
                    go.Scattergeo(
                            lon = loc_df['longitude'],
                            lat = loc_df['latitude'],
                            text = loc_df['cities'],
                            hoverinfo="text",
                            marker = dict(
                                size = loc_df['percent']+5,
                                color = '#0083B8'
                            ), 
                        hoverlabel=dict(namelength=0)
                    )
                )
                map.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)", 
                    dragmode=False
                )
                map['layout'].update(autosize = True)
    
                # company bar chart object 
                cmp_fig = px.bar(cmp_df, 
                                x='vacancy points', y='company names', 
                                orientation='h', title='Top companies',
                                color_discrete_sequence=["#0083B8"] * len(cmp_df),
                                template="plotly_white"
                )
                cmp_fig.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=(dict(showgrid=False)),
                    yaxis=dict(autorange="reversed"),
                    dragmode=False
                )
    
                # skills bar chart object
                skl_fig = px.bar(skl_df, 
                                x='skills', y='demand points', 
                                orientation='v', title='Top skills',
                                color_discrete_sequence=["#0083B8"] * len(skl_df),
                                template="plotly_white",
                )
                skl_fig.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=(dict(showgrid=False)),
                    yaxis=(dict(showgrid=False)),
                    dragmode=False
                )
    
                # location bar chart object
                loc_fig = px.bar(loc_df, 
                                x='cities', y='job counts', 
                                orientation='v', title='Top cities',
                                color_discrete_sequence=["#0083B8"] * len(loc_df),
                                template="plotly_white",
                )
                loc_fig.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=(dict(showgrid=False)),
                    yaxis=(dict(showgrid=False)),
                    dragmode=False
                )
    
                # experience level pie chart object
                names = exp_df['job level']
                values = exp_df['count']
                exp_fig = px.pie(exp_df, values=values, names=names, title='Job level - ratio')
                exp_fig.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    dragmode=False
                )
    
                # job-type pie chart object
                names = jty_df['job type']
                values = jty_df['count']
                jty_fig = px.pie(jty_df, values=values, names=names, title='Job type - ratio')
                jty_fig.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    dragmode=False
                )
    
            # plot chart and map objects
            st.markdown("---")
    
            # separating page into left and right columns
            left_column, right_column = st.columns(2)
    
            # plotting chart and map objects one by one
            config = {'displayModeBar': False}
            left_column.plotly_chart(cmp_fig, use_container_width=True, config=config)
            right_column.plotly_chart(skl_fig, use_container_width=True, config=config)
            left_column.plotly_chart(loc_fig, use_container_width=True, config=config)
            right_column.plotly_chart(map, use_container_width=True, config=config)
            left_column.plotly_chart(jty_fig, use_container_width=True, config=config)
            right_column.plotly_chart(exp_fig, use_container_width=True, config=config)
    
            hide_st_style = """
                        <style>
                        #MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}
                        header {visibility: hidden;}
                        </style>
                        """
            # hide the default styling
            st.markdown(hide_st_style, unsafe_allow_html=True)
    
            st.markdown("---")
            # plotting ends
        
        # catch and print error messages in logs and proceed further
        except Exception as e:
            print(e)
            st.markdown("---")
            st.write("Something went wrong, please select the job role again!")
            st.markdown("---")
