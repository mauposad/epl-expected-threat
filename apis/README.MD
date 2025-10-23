####  Dealing with Nested Json packages
    pandas.normalize to flatten json package the entire way through.

The different json packages represent the different years. It gives the stats for each year. Only need the first two packages. Could display based each one based on format/ season type. 
    Formats 
        Cup
        Domestic League
        International

####  Dealing with Nested Json packages
    pandas.normalize to flatten json package the entire way through.


# Data Pipeline for 2025 - 2026 Season (deciding which api calls to make and how)
This is how we are going to work around the limited API access. We are going to make calls to the several seasons and attempt to gather a dataframe of relegated/promoted teams. This we have access to all a large variety of team ids both in the prem and not in the prem. (we might be able to get some interesting information out of analyzing relegated and promoted teams)

# Plan of approach for collecting team ID's
We can use a variety of approaches. First off we will use the previous year league list since it works for us. We can collect the id's and input them into a dataframe.We will have to use several years worth of league teams. SO we can try to estimate as best as possible on how to get the current league table. We cannot get current match day details. I believe all we can get are the current team stats. Outside of that, how else can we get the current details? Use more than one API Service?

An obvious catch for teams that are not in the prem is that we will not be able to access team stats if they are not in the prem? Correct?


# Design functions for the appriopriate API endpoints.Then extract the relevant information from each call and input into dataframe
For this to work we will have to save our data frame and database to memory. So that we have persistence through sessions. 
One thing we can do is run our platform on matchdays so we can get access to the full list of teams. 

# Current Status and POA (10/22)
We currently have a clean working dataframe ready for analysis. This consists of last years data. We can use this to train models. Our next steps would be to create a working pipeline for this years data, and work with the data models. POA for this seasons data pipeline is discussed above 