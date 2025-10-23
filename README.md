# data-mine-mposadas
Project for Data Mining

## How to run virtual environment:
    To Activate: conda activate data-mining
    Only done once: pip install -r requirements.txt
    To deactivate: conda deactivate


This repo is being used to create, develop, test and refine different data models for my data mining class. The dataI am currently working with is Premier League data from the 2024-2025 season. 3rd party api is listed below for your own viewing and documentation. 
Current work is under apis folder. Further implementation will be turning this into a working web app with different features working with current ongoing season. 

## [**FootyStats**] (https://footystats.org/api/ ) 
    - NOTES: Free tier only includes a Premier League


## Repo Structure
- data_pipeline contains our script we used to get our data source. We saved it as a parquet so we can access all across our repo. Data_utils are our helper functions for our data_pipeline
- models contains our jupyter notebook model scripts for our data mining class. 
