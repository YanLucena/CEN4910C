Data for the scripts can be found in the links below:

# https://ookla-open-data.s3-us-west-2.amazonaws.com
   look for shapefiles, example: shapefiles/performance/type=fixed/year=2021/quarter=1/2021-01-01_performance_fixed_tiles.zip
# https://gis.orlando.gov/PDF_Docs/Data4Web/ZipFiles/OrlandoNeighborhoods.zip

Instructions for running the scripts:

To create the final geojson files one must run the merger.py first, wait for the filtered file to be created, then run the normalizer.py passing the just created filtered file as the input. The merger.py file merges the Ookla dataset with the Orlando neighborhoods data. The normalizer.py turns the tiles geojson into averaged geojson.

In easy steps, to create the files follow the below:

	- Download the most recent dataset from the Ookla endpoint above into the assets folder of this project.
	- Edit line 11 of merger.py to reference the Ookla file downloaded in the step above.
	- Run merger.py. It may take a long time to complete depending of the machine resources.
	- Once merger.py finished running, check wether the filtered file was created under the results folder.
	- Change line 9 of normalizer.py to reference the filetered file.
	- Run normalizer.py
	- Check if the final file has been generated within the results folder.

Observations:

	- Boths scripts are not combined as per the short due date of this project. But they can certainly be.
	- Heavy residual files will be generated under the assets folder after each run of the merger.py. We decided to keep them there as they can be of use for future development and so that less memory is consumed during each run. However, that can be changed by modifying the script.

