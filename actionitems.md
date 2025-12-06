# Project Action Items — Data Mining Premier League

## Phase 0 — Framing (Current)
- [x] Finalize abstract (use revised version)
- [x] Lock season: Premier League 2015–2016
- [x] Define target variables  
  - [x] Option A: Goals + Assists per 90  
  - [x] Option B: xG + xA per 90  
  - [ ] Decide one primary, one optional secondary
- [x] Define population  
  - [x] Minimum minutes (e.g., > 900)  
  - [x] Positions included (e.g., FW, AM, WM)

---

## Phase 1 — Build Modeling Table (Critical Path)
- [x] Load cleaned StatsBomb data
- [x] Load xThreat parquet (already computed)
- [x] Aggregate xThreat to player-season level
- [x] Aggregate StatsBomb metrics to player-season level:
  - [x] xG, xA
  - [x] Shots/90
  - [x] Progressive passes/carries
  - [ ] Touches in final third/box (optional)
- [x] Merge features into one DataFrame
- [x] Filter by minutes & positions
- [x] Remove or impute missing values
- [x] Select ~25–35 features for modeling
- [x] Save modeling table

---

## Phase 2 — Exploratory Data Analysis
- [ ] Histogram of target variable(s)
- [ ] Scatterplots of xT vs output metrics
- [ ] Correlation heatmap (reduced feature set)
- [ ] Boxplots by position
- [ ] Save all visuals in `reports/figures/`

---

## Phase 3 — PCA & Archetypes
- [ ] Standardize selected features
- [ ] Fit PCA on 15–25 attacking features
- [ ] Examine explained variance
- [ ] Interpret component loadings
- [ ] Produce PCA scatterplot (PC1 vs PC2)
- [ ] Add PCA components to modeling table

---

## Phase 4 — Regression Models
- [ ] Build baseline linear regression predicting target variable
- [ ] Compare models with and without xThreat
- [ ] Evaluate R², RMSE, residual plots
- [ ] Interpret coefficients
- [ ] Save results

---

## Phase 5 — Classification Models (KNN + Decision Tree)
- [ ] Create binary label (top 20–25% attackers)
- [ ] Fit KNN classifier
  - [ ] Tune k (quick CV)
  - [ ] Evaluate accuracy, precision, recall
- [ ] Fit decision tree classifier
  - [ ] Limit depth to ensure interpretability
  - [ ] Plot feature importances
- [ ] Compare models with and without xThreat features

---

## Phase 6 — Final Deliverables
- [ ] Notebook: Feature Engineering
- [ ] Notebook: EDA
- [ ] Notebook: PCA + Archetypes
- [ ] Notebook: Regression + Classification Models
- [ ] Final report summarizing:
  - [ ] Methods
  - [ ] Key findings
  - [ ] Visuals
  - [ ] Limitations
  - [ ] Future work
- [ ] Push everything to GitHub repo

---

## Optional Bells & Whistles (Only If Time Allows)
- [ ] KMeans clustering in PCA space
- [ ] Comparison of xThreat vs xG as predictors
- [ ] Per-player mini profiles (2–3 examples)
- [ ] Team-level aggregates (xT vs points)
