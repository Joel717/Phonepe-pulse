#importing the required packages 
import streamlit as st
import pandas as pd
import psycopg2
import os 
import json
import plotly.express as px
from streamlit_option_menu import option_menu
from git.repo.base import Repo
from PIL import Image



#setting the page  configuration
st.set_page_config(page_title="Phonepe Pulse Visualization",
                   layout='wide',
                   
                   )

#configuring postgresSQL required for the calculations
mydb= psycopg2.connect(host="localhost",
            user="postgres",
            password="postgres",
            database= "phonepe",
            port = "5432"
            )
mycursor = mydb.cursor()

#creating a title for the page
st.title('_Phonepe Pulse Visualizations_')

#creating a topbar menu 
topbar=option_menu(
    menu_title=None,
    options=['Home','Top Charts','Data Exploration','About'],
    icons=['house','file-bar-graph','search','exclamation-circle'],
    orientation='horizontal',
    default_index=0,
    styles={
        "container": {"padding": "0!important", "background-color": "#f0f0f0"},
        "icon": {"color": "orange", "font-size": "16.5px"}, 
        "nav-link": {"font-size": "16.5px", "text-align": "left", "margin":"0px", "--hover-color": " #6739b7"},
        "nav-link-selected": {"background-color": " #6739b7"},
    }
    )
#creating topbar values
if topbar=='Home':
      st.header("Phonepe Visualizations")
      col1,col2=st.columns([1,1],gap='small')

      with col1:
         st.markdown('''<p style="font-size: 22px;">
                     The motive behind creating this interactive streamlit app is to visualize gather 
                    information from the 'Phonepe Pulse' data from Github.The data which was originally in 
                    json format is transformed into a pandas dataframe and then inserted into sql for 
                    effecient storage of the data. Then the data is queried using sql to creeate visualizations 
                    using plotly </p>
                     ''',unsafe_allow_html=True)
         with col2:
                    img=Image.open('C:\\Users\\devli\\Project_yt\\4.jpg')
                    st.image(img)
                    
      col1,col2=st.columns([1,1],gap='small')
      with col1:
                                            img2=Image.open('C:\\Users\\devli\\Project_yt\\5.png')
                                            st.image(img2)

                                            with col2:
                                                    st.markdown('''<p style="font-size: 22px;">
                                                                The image in the left is the official homepage of Phonepe pulse made by 
                                                                Phonepe themselves. The site provides extensive details on the 
                                                                amount of transactions and thetype of transactions done using the Phonepe app. 
                                                                The data is presented in a beautiful interactive geo viz making it easier for anyone to understand the location based insights </p>''', 
                                                                unsafe_allow_html=True)

        

#creating top10 visualizations for Transactions and users 
if topbar == "Top Charts":
    

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        Type = st.selectbox("**Type**", ("Transactions", "Users"))

    with col2:
        col2_1, col2_2 = st.columns(2)
        with col2_1:
            Years = st.slider("**Years**", min_value=2018, max_value=2022)
        with col2_2:
            Quarter = st.radio("Quarter", [1, 2, 3, 4], index=0, horizontal=True)

    
    if Type == "Transactions":
    
        
        col1, col2, = st.columns([1, 1], gap="small")

        with col1:
            st.markdown("### :violet[State]")
            mycursor.execute(f'''
                SELECT "States", 
                    SUM("Transaction_count") as Total_Transactions_Count, 
                    SUM("Transaction_amount") as Total 
                FROM aggt 
                WHERE "Years" = {int(Years)} AND "Quarter" = {int(Quarter)}  
                GROUP BY "States" 
                ORDER BY Total DESC 
                LIMIT 10
            ''')
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count', 'Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                        names='State',
                        title='Top 10',
                        color_discrete_sequence=px.colors.sequential.Agsunset,
                        hover_data=['Transactions_Count'],
                        labels={'Transactions_Count': 'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
                st.markdown("### :violet[District]")
                mycursor.execute(f'''
                    SELECT "District",
                        SUM("Transaction_count") as Total_Count,
                        SUM("Transaction_amount") as Total
                    FROM mapt
                    WHERE "Years" = {Years} AND "Quarter" = {Quarter}
                    GROUP BY "District"
                    ORDER BY Total DESC
                    LIMIT 10
                        ''')
                df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

                fig = px.pie(df, values='Total_Amount',
                                names='District',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
                
                #insights about the pie chart
        with st.container():
                    st.markdown(
                '''
                <div style="background-color: #f0f0f0; padding: 15px; border-radius: 10px;">
                    <p style="font-size: 18px;">The pie-charts provide valuable insights on the Transaction data</p>
                    <p style="font-size: 18px;">The state pie-chart gives insights on top 10 states that have done transactions using PhonePe</p>
                    <p style="font-size: 18px;">The District pie-chart provides info on the top 10 districts based on the number of transactions</p>
                    <p style="font-size: 18px;">The required parameters can be set using the slider and radio at the top</p>
                </div>
                ''',
                unsafe_allow_html=True
            )
        
                
               
                

    if Type == "Users":
                    
            col1,col2 = st.columns([1,1],gap="small")
                
            with col1:
                          
                          st.markdown("### :violet[Brands]")
                          if Years == 2022 and Quarter in [2,3,4]:
                            st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")

                          else:
                                 mycursor.execute(f'''
                                                SELECT "Brands",
                                                    SUM("Transaction_count") as Total_Count,
                                                    AVG("Percentage") * 100 as Avg_Percentage
                                                FROM aggu
                                                WHERE "Years" = {Years} AND "Quarter" = {Quarter}
                                                GROUP BY "Brands"
                                                ORDER BY Total_Count DESC
                                                LIMIT 10
                                                ''')
                                 
                                 df = pd.DataFrame(mycursor.fetchall(), columns=['Brands', 'TotalUsers','Avg_Percentage'])
                                 fig = px.bar(df,
                                            title='Top 10',
                                            x="TotalUsers",
                                            y="Brands",
                                            orientation='h',
                                            color='Avg_Percentage',
                                            color_continuous_scale=px.colors.sequential.Agsunset)
                                 st.plotly_chart(fig,use_container_width=True)   
            with col2:
                        st.markdown("### :violet[Districts]")
                        mycursor.execute( f'''
                                            SELECT "Districts",
                                                SUM("RegisteredUser") as Total_Users,
                                                SUM("AppOpens") as Total_Appopens
                                            FROM mapu
                                            WHERE "Years" = {Years} AND "Quarter" = {Quarter}
                                            GROUP BY "Districts"
                                            ORDER BY Total_Users DESC
                                            LIMIT 10
                                        ''')

                        df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
                        df.Total_Users = df.Total_Users.astype(float)
                        fig = px.bar(df,
                                    title='Top 10',
                                    x="Total_Users",
                                    y="District",
                                    orientation='h',
                                    color='Total_Users',
                                    color_continuous_scale=px.colors.sequential.Agsunset)
                        st.plotly_chart(fig,use_container_width=True)
            
            #insights about the pie chart
            with st.container():
                    st.markdown(
                '''
                <div style="background-color: #f0f0f0; padding: 15px; border-radius: 10px;">
                    <p style="font-size: 18px;">The bar charts provide valuable insights on the user data</p>
                    <p style="font-size: 18px;">The brand  bar chart gives insights on most used mobile brands on which the phonepe app is used</p>
                    <p style="font-size: 18px;">The District bar chart provides info on the top 10 districts based on the number of users in the district</p>
                    <p style="font-size: 18px;">The required parameters can be set using the slider and radio at the top</p>
                </div>
                ''',
                unsafe_allow_html=True
            )


#creating geo visualization for data exploration for transaction and users 

if topbar == 'Data Exploration':
        col1, col2 = st.columns([1, 1], gap="small")

        with col1:
            Type = st.selectbox("**Type**", ("Transactions", "Users"))

        with col2:
            col2_1, col2_2 = st.columns(2)

            with col2_1:
                Years = st.slider("**Years**", min_value=2018, max_value=2022)

            with col2_2:
                Quarter = st.radio("Quarter", [1, 2, 3, 4], index=0, horizontal=True)

        if Type == "Transactions":
        
                st.markdown("## :violet[Overall State Data - Transactions Amount]")
                mycursor.execute(f'''
                            SELECT "States",
                                SUM("Transaction_count") as Total_Transactions,
                                SUM("Transaction_amount") as Total_amount
                            FROM mapt
                            WHERE "Years" = {Years} AND "Quarter" = {Quarter}
                            GROUP BY "States"
                            ORDER BY "States"
                        ''')
                df1 = pd.DataFrame(mycursor.fetchall(),columns= ['States', 'Total_Transactions', 'Total_amount'])
                df2 = df1['States']
                df2=df2.drop_duplicates()

                fig = px.choropleth(df1,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='States',
                        color='Total_amount',
                        labels={'States'},
                        hover_data=['Total_amount', 'Total_Transactions', 'States'],
                        color_continuous_scale='sunset'
                    )

                fig.update_geos(fitbounds="locations", visible=False)
                fig.update_layout(geo=dict(
                                center=dict(lon=78, lat=23),
                                projection_scale=5
                            ))
                fig.update_geos(showsubunits=True, subunitcolor="Black")
                fig.update_layout(width=600, height=700)

                st.plotly_chart(fig,use_container_width=True)
            

        if Type=='Users':
                st.markdown("## :violet[Overall State Data - User App opening frequency]")
                mycursor.execute(f'''
                    SELECT "States",
                        SUM("RegisteredUser") as Total_Users,
                        SUM("AppOpens") as Total_Appopens
                    FROM mapu
                    WHERE "Years" = {Years} AND "Quarter" = {Quarter}
                    GROUP BY "States"
                    ORDER BY "States"
                ''')
                df1 = pd.DataFrame(mycursor.fetchall(), columns=['States', 'Total_Users','Total_Appopens'])
                df2 = df1['States']
                df1['Total_Appopens'] = df1['Total_Appopens'].astype(float)
                    
        
                fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                        featureidkey='properties.ST_NM',
                                        locations='States',
                                        labels={'States'},
                                        hover_data=['States'],
                                        color='Total_Appopens',
                                        color_continuous_scale='sunset'
                                        )
                                

                fig.update_geos(fitbounds="locations", visible=False)
                fig.update_layout(geo=dict(
                                center=dict(lon=78, lat=23),
                                projection_scale=5
                            ))
                fig.update_geos(showsubunits=True, subunitcolor="Black")
                fig.update_layout(width=600, height=700)

                st.plotly_chart(fig,use_container_width=True)
        
        #insights about the geo viz
        with st.container():
                            st.markdown(
                        '''
                        <div style="background-color: #f0f0f0; padding: 15px; border-radius: 10px;">
                            <p style="font-size: 18px;">The geo viz makes it easy to understand the data of the respective states</p>
                            <p style="font-size: 18px;">Selecting thr 'transaction' option from the dropdown gives insigth on the statewise transactions</p>
                            <p style="font-size: 18px;">Selecting the 'users' option from the dropdown provides insights on the statewise user data </p>
                            <p style="font-size: 18px;">The required parameters can be set using the slider and radio at the top</p>
                        </div>
                        ''',
                        unsafe_allow_html=True
                    )

#creating the About section
if topbar=='About':
       
              
            st.subheader('About the creator:')
            st.markdown('The app is created by: Joel Gracelin ')
            st.markdown('This app is created as a part of Guvi Master Data Science course')
            st.markdown('Domain: Fin-Tech')
            st.markdown("Inspired from [Phonepe Pulse](https://www.phonepe.com/pulse/)")
            st.markdown("[Ghithub](https://github.com/Joel717)")

            