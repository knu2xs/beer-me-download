# Beer Me

This repository is pretty simple, one file doing one thing, downloading an xml file of breweries from CraftBeer.com and saving it as an ArcGIS feature class in the default user file geodatabase. It is the script I wrote to get and convert the data eventually used to create the [Brewery Finder](http://arcg.is/1jRDXtK). 

## Use

Provided you have the requirements detailed below (ArcGIS Desktop installed), just double click `beer_me.py` and you will soon discover a new feature class in your default geodatabase.

## Requirements

### ArcGIS Desktop

This means you need to have ArcGIS Desktop installed so the default geodatabase will be present and so the Python functions specific to ArcGIS accessed through the arcpy module will be available.

### Python Path

You may need to add the location of your Python executable to your system path to be able to simply double click on the `beer_me.py` file. Instructions for [adding Python to the environment variable this can be found in the Python documentation](https://docs.python.org/2/using/windows.html#excursus-setting-environment-variables).