# Geoscripting 2021
# Spatial map function
# Baguette team
# Hugo POUPARD & Jochem T'Hart

#Create the desired folders
CreateDirs <- function()
{
  dir.create("data", showWarnings=FALSE)
  dir.create("output", showWarnings=FALSE)
}

#create get data to download desired files etcetc
GetData <- function(url)
{
  zip_file = "./data/data.zip"
  if (!file.exists(zip_file))
    download.file(url, zip_file)
  unzip(zip_file, exdir="./data")
}

GetBoundaries <- function(region, lvl)
{
  return(raster::getData('GADM',country=region, level=lvl, path="./data"))
}
