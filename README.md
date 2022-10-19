# Predicting Internet Traffic Across Websites Categories

## Repository Contents

This repository contains code, data and figures for a data science project investigating internet traffic across different website categories including e-commerce, news and sports websites. This project was created as part of the Data Science Project Course (DS 4002) at the University of Virginia in the Fall of 2022.

## Source Code

Source code for this project can be found in the `src` directory of this repository.

### Installing/Building Code in this Repository

After cloning or forking this repository, its contents can be used to recreate different parts of this project. The required modules and packages used in Python and R for this project are listed below.

### Modules and Packages Used in this Project

#### Python Modules

This project makes use of the following Python modules:

- numpy
- pandas
- matplotlib.pyploy
- datetime
- sklearn
-- preprocessing
-- svm
- statsmodels.tsa.api
- statsmodel.api
- pmdarima

#### R Packages

This project makes use of the following R packages:

### Usage of Code in this Repository

## Data

### Data Dictionary

| Variable | Data Type | Description | Example |
|----------|-----------|-------------|---------|
| Site | String | Whe website of interest | 'Amazon' |
| MonthYear | Date | The month and year corresponding to the page views | 2017-01-01 |
| Year | Numeric | The year the website was visited | 2017 |
| AllDevices | Numeric | The number of page devices for the month and year across all devices | 2571858 |
| Desktop | Numeric | The number of page devices for the month and year across desktop devices | 6565 |
| Mobile | Numeric | The number of page devices for the month and year across mobile devices | 233 |
| Category | String | The category/industry that the website falls into. One of: 'E-commerce', 'News', 'Sports' | 'E-commerce'

## Figures

Figures for this project can be found in the `figures` directory of this repository.

### Table of Contents

| Figure Name | Variables | Summary |
|-------------|-----------|---------|
| Amazon Page Visits Over Time | x = date, y = page visits (in billions) | The line graph shows the trend and moving average of page visits on Amazon since 2017. The overall trend we see is that page visits are increasing. There also appears to roughly be patterns of seasonality, with higher page visits towards the ends and beginnings of the year, with lower numbers in the middle of the year |
| Outlier Detection | x = date, y = page visits | This plot shows the same line graph as the prior graph, but points out the outliers that were calculated in the time series. From this, we know May 2017, September 2017, August 2022, and October 2022 are all outliers to be removed for further analysis |
| SARIMA (1,1,1) x (1,1,1,12) | x and y are different variables relevant to each plot | The series of plot found in this figure summarize the time series forecasting model and its evaluated metrics. From the "Forecast" model, we see our predictions are working relatively well, following the general pattern from the observed data. From the "Residuals" plot, we see that the residuals appear to be stationary with no changing patterns, which is a good sign. From the "Residual Distribution" plot, we see the residuals are roughly normally distributed, which is appropriate. |

## References

[1] R. Jogi, “How to Handle Heavy Internet Traffic on Your Website?,” Cloud Minister Technologies. Sept. 28, 2021. [Online]. Available: https://cloudminister.com. [Accessed Oct. 5, 2022].

[2] A. Coghlan, “Using R for Time Series Analysis,” Little Book of R for Time Series. 2010. [Online]. Available: https://a-little-book-of-r-for-time-series.readthedocs.io. [Accessed Oct. 12, 2022].

Files documenting the previous 2 milestones of this project can be found in the `milestones` directory of this repository in `M1Hypothesis.pdf` ([src](milestones/MI1Hypothesis.pdf)) and `MI2EstablishDataAndAnalysisPlan.pdf` ([src](milestones/MI2EstablishDataAndAnalysisPlan.pdf)).
