# install.packages(c("DBI", "RSQLite", "tidyverse", "zoo", "lubridate"))

library(DBI)
library(RSQLite)
library(tidyverse)
library(zoo)
library(lubridate)

con <- dbConnect(SQLite(), "C:/Users/Mobley/Desktop/etf-sql-analysis/etf_analysis.db")
prices <- dbGetQuery(con, "SELECT * FROM prices")
prices$date <- as.Date(prices$date)

glimpse(prices)
