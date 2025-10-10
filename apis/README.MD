JMES Path language to find an easier way to subset 

Structure of the current get_team API call
ID 
    data
        additional information (Figure out how to unpack this last nested json)

####  Dealing with Nested Json packages
    pandas.normalize to flatten json package the entire way through.

The different json packages represent the different years. It gives the stats for each year. Only need the first two packages. Could display based each one based on format/ season type. 
    Formats 
        Cup
        Domestic League
        International

####  Dealing with Nested Json packages
    pandas.normalize to flatten json package the entire way through.

# How to format our data frame? 
    Ideally we organize by team name in alphabetical order. That would mean we save a certain element to be the identifier for our data frame. Thats one problem all on its own. Aside from that we need to get all of the "team_id" for the current premier league teams. Where can we start looking? Inspecting the element? 

# How to get ALL of our data we need? (deciding which api calls to make and how)
This is how we are going to work around the limited API access. We are going to make calls to the several seasons and attempt to gather a dataframe of relegated/promoted teams. This we have access to all a large variety of team ids both in the prem and not in the prem. (we might be able to get some interesting information out of this as well)

# Plan of approach for collecting team ID's
We can use a variety of approaches. First off we will use the previous year league list since it works for us. We can collect the id's and input them into a dataframe. We also have to check teams that have never been promoted so we can use the current and ongoing matches and then check them against our current collected data. If not included we check, we must be careful to not add any teams that are not in the prem. 

An obvious catch for teams that are not in the prem is that we will not be able to access team stats if they are not in the prem? Correct? 


# Make functions for all the api endpoints we will constantly be calling so that we do not have to be copy pasting 
