# data-mine-mposadas
Project for Data Mining

## How to run virtual environment:
    To Activate: conda activate data-mining
    Only done once: pip install -r requirements.txt
    To deactivate: conda deactivate


This repo is being used to create, develop, test and refine different data models for my data mining class. The data I am currently working with is Premier League data from the 2024-2025 season. 3rd party api is listed below for your own viewing and documentation. 
Current work is under apis folder. Further implementation will be turning this into a working web app with different features working with current ongoing season. 

## [**FootyStats**] (https://footystats.org/api/ ) 
    - NOTES: Free tier only includes a Premier League


## Repo Structure
- data_pipeline contains our script we used to get our data source. We saved it as a parquet so we can access all across our repo. Data_utils are our helper functions for our data_pipeline
- models contains our jupyter notebook model scripts for our data mining class. 


# Scope of this Project
I use the StatsBomb Open Data Repository to derive advanced attacking metrics for Premier League players in the 2018–2019 season, with a focus on Expected Threat (xT) and complementary event-based metrics such as xG, xA, progressive actions, and possession value contributions. The goal of this project is to understand the underlying dimensions of attacking play, evaluate how well advanced metrics explain attacking output, and identify distinct attacking player archetypes. To accomplish this, I build a unified player-season dataset and apply Principal Component Analysis, linear regression, K-Nearest Neighbors, and decision tree models. Deliverables include structured Jupyter notebooks for feature engineering, modeling, and visualization, as well as a concise written report summarizing insights, model interpretations, and areas for future expansion.

This project includes a vast amount of work in the data preparation phase in order to compute and match the data within the StatsBomb Open Data Repository
