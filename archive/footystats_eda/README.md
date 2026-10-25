# Guidelines we are taking for the process of EDA
### 1. Understand the Context and Data Source

Before touching the data:

Define your goal or question: what are you trying to learn or predict?

Understand how the data was collected and what each feature represents.

Identify data types (numerical, categorical, time-series, text, etc.).

Check for granularity — is each row an individual, a transaction, an event?

📘 Example: In a Premier League dataset, determine whether rows represent matches, players, or events (shots, passes, goals, etc.).

### 2. Data Cleaning and Quality Checks

You can’t analyze dirty data. Inspect for:

Missing values → quantify, visualize (df.isnull().sum()), decide to impute or drop.

Duplicate rows → remove or consolidate.

Inconsistent types or formats (e.g., strings vs. floats).

Outliers → detect via z-scores, IQR, or visualization (boxplots, scatterplots).

Invalid or impossible values (e.g., negative ages, percentages > 100).

📘 Goal: Make sure the dataset is consistent and analysis-ready.

### 3. Univariate Analysis (Single Variable)

Understand the distribution and characteristics of individual features:

Numerical variables: histograms, boxplots, mean/median/std, skewness, kurtosis.

Categorical variables: bar charts, frequency tables, mode, proportions.

Identify potential transformations (e.g., log-scale for skewed data).

📘 Example: Distribution of goals scored per match or yellow cards per team.

### 4. Bivariate / Multivariate Analysis (Left of here, need to make groups to visualize/ extract further data)

Examine relationships between variables:

Numerical–Numerical: scatter plots, correlation matrix, pairplots.

Numerical–Categorical: boxplots, ANOVA tests.

Categorical–Categorical: contingency tables, chi-square tests, stacked bar charts.

Look for patterns, clusters, or linear/nonlinear relationships.

📘 Example: Do teams with higher possession rates score more goals?

### 5. Feature Relationships and Redundancy

Detect multicollinearity using correlation heatmaps or VIF (Variance Inflation Factor).

Identify redundant variables that provide overlapping information.

Group variables into thematic categories (e.g., goals, passes, defense metrics).

📘 Example: In your Premier League dataset, you grouped features into “goals,” “corners,” “cards,” etc.

### 6. Time-Series or Grouped Patterns (if applicable)

If data is temporal or hierarchical:

Plot trends over time (rolling averages, seasonality, cycles).

Examine group differences (e.g., by team, player, season).

Aggregate metrics (mean goals per month, cumulative xG, etc.).

### 7. Visualization

EDA is visual-heavy because patterns are often clearest visually:

Use histograms, scatterplots, boxplots, heatmaps, pairplots.

Combine plots and summary stats for insights.

Identify outliers, clusters, or unexpected relationships visually.

📘 Libraries: matplotlib, seaborn, plotly, or pandas_profiling for quick reports.

### 8. Summarize Key Insights

End with a concise summary:

Major patterns and correlations

Outliers and potential data issues

Relationships worth modeling

Hypotheses to test later

📘 Deliverable: a short narrative with visuals that connects data behavior to your research question.



# Food for tought from MacEvoy
What are we trying to model here? What are variables that contribute to scoring? 
Do some PCA and look at the eigen values to get a feel for relationships. He's not sure how that will turn out. 


# Food for thought from King
95th percentile w/ 18 degrees of freedom. Plyer packages. Tidyverse. Below -0.5 and above 0.5 for correlation values and p values below 0.05
pairwise approach. Check email from King for further instructions. 


# food for thought
    Different models and power scores for teams offense and defense. Power of the team is the aggregate sum of the scores of the players of the teams. 
    As people get pulled off or subbed off, the team power score changes

    Ignore everything and make a machine learning model. Let the machine find the pattern/ predictor. What is it looking at to get those predictors?
    [https://baselight.app/u/blt/dataset/ultimate_soccer_dataset] (need to use a new dataset since our dataset is much too small for ML models)

    Principle Component Analysis and ML might help us find something since they purely look at the numbers without the context. 
    Modeling power. No values for power.

    