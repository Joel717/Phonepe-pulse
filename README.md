# Phonepe-pulse

## Overview

This repository contains a Streamlit app for visualizing data from the 'Phonepe Pulse' data. The app transforms the original JSON data into a Pandas DataFrame, inserts it into PostgreSQL for efficient storage, and then creates visualizations using Plotly and Plotly Express.

## Features

- **Top Charts:** Explore top charts for transactions and users.
- **Data Exploration:** Visualize transaction and user data on a geographical map.
- **About Section:** Learn more about the creator and the project.

## Problem statement 
- The driving factor behind the project is the Phonepe Pulse website and the GitHub data repository 
- The data should be cloned and made usable and stored in SQL for ease of use 
- Create insightful visualizations and geo viz to showcase the insights gathered from the data in a streamlit app

## Approach
- Mentioned below are the steps and tools used in the approach to create a streamlined solution 

## Data Extraction 
- The ipynb file has the code used to extract the data 
- The data is converted from a JSON file to a pandas data frame which is then uploaded to Postgres SQL for storage 
- SQL alchemy is used to insert the data into Postgres for ease of use and easy modularity

## Data Exploration 
- The data is queried using SQL queries to gather insights 
- The gathered insights are visualized using plotly 
- The visualisations are made interactive for better usability and understanding 

## Showcasing the Data 
- The visualizations are showcased using an interactive app built using streamlit 
- Streamlit app is inspired by the phonepe pulse site created by phonepe 
- The streamlit app helps in better navigation of the data 
