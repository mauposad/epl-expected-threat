JMES Path language to find an easier way to subset 

load into a file and play with it in a webpage using javascript to pull out the important information
    pick any syntax but javascript might be the easiest way to pull out information


Structure of the current API call
ID 
    data
        additional information (Figure out how to unpack this last nested json)


- [ ] What if we did some preliminary trimming to the json package before normalizing and flattening
- [ ] How can we deal with nested jsons in our json packaages. Want to fully remove all of them and flatten json package
- [ ] How can we deal with all of the json packages we are being returned? First off what does each different package mean? 

The different json packages represent the different years. It gives the stats for each year. Only need the first two packages. Could display based each one based on format/ season type. 
    Formats 
        Cup
        Domestic League
        International

####  Dealing with Nested Json packages
    pandas.normalize to flatten json package the entire way through.

# How to format our data frame? 
    Ideally we organize by team name in alphabetical order. That would mean we save a certain element to be the identifier for our data frame. Thats one problem all on its own. Aside from that we need to get all of the "team_id" for the current premier league teams. Where can we start looking? Inspecting the element? 


Format for all the current premier league teams

0	{ id: 59, name: "Arsenal FC", cleanName: "Arsenal", … }
1	{ id: 92, name: "Tottenham Hotspur FC", cleanName: "Tottenham Hotspur", … }
2	{ id: 93, name: "Manchester City FC", cleanName: "Manchester City", … }
3	{ id: 108, name: "Leicester City FC", cleanName: "Leicester City", … }
4	{ id: 143, name: "Crystal Palace FC", cleanName: "Crystal Palace", … }
5	{ id: 144, name: "Everton FC", cleanName: "Everton", … }
6	{ id: 145, name: "Burnley FC", cleanName: "Burnley", … }
7	{ id: 146, name: "Southampton FC", cleanName: "Southampton", … }
8	{ id: 148, name: "AFC Bournemouth", cleanName: "AFC Bournemouth", … }
9	{ id: 149, name: "Manchester United FC", cleanName: "Manchester United", … }
10	{ id: 151, name: "Liverpool FC", cleanName: "Liverpool", … }
11	{ id: 152, name: "Chelsea FC", cleanName: "Chelsea", … }
12	{ id: 153, name: "West Ham United FC", cleanName: "West Ham United", … }
13	{ id: 155, name: "Watford FC", cleanName: "Watford", … }
14	{ id: 157, name: "Newcastle United FC", cleanName: "Newcastle United", … }
15	{ id: 158, name: "Aston Villa FC", cleanName: "Aston Villa", … }
16	{ id: 159, name: "Norwich City FC", cleanName: "Norwich City", … }
17	{ id: 209, name: "Brighton & Hove Albion FC", cleanName: "Brighton & Hove Albion", … }
18	{ id: 223, name: "Wolverhampton Wanderers FC", cleanName: "Wolverhampton Wanderers", … }
19	{ id: 251, name: "Sheffield United FC", cleanName: "Sheffield United", … }
