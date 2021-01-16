# Geoscripting 2021
# Project: Corona Locator
# Spatial map function
# Baguette team
# Hugo POUPARD & Jochem T'Hart
# 15 January 2021

# check for raster package and install if missing
if(!"raster" %in% rownames(installed.packages())){install.packages("raster")}

# check for sf package and install if missing
if(!"sf" %in% rownames(installed.packages())){install.packages("sf")}

# check for sf package and install if missing
if(!"randomForest" %in% rownames(installed.packages())){install.packages("randomForest")}

# check for sf package and install if missing
if(!"igraph" %in% rownames(installed.packages())){install.packages("igraph")}

# Libraries
library(raster)
library(sf)
library(randomForest)
library(igraph)
