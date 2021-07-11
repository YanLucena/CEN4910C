 # Magnificent 7
 #!/usr/bin/python3

import geopandas as gp
import geojson
import re

# Read the readme.txt file for further instructions.

orlando_neighborhoods_zip_file = "assets\\OrlandoNeighborhoods.zip"
fixed_tiles_zip_file = "assets\\2019-01-01_performance_fixed_tiles.zip"

fixed_tiles_zip_file_date = re.search("(([0-9]{4}\-[0-9]{2}\-[0-9]{2}))", fixed_tiles_zip_file).group(0)

# Creates a geojson file based on the Orlando coordinates.
print("Creating a geojson file based on the Orlando coordinates...")
orlando_neighborhoods_coordinates = gp.read_file(orlando_neighborhoods_zip_file)
orlando_neighborhoods_coordinates = orlando_neighborhoods_coordinates.to_crs(4326)
orlando_neighborhoods_coordinates.to_file("assets\\orlando_neighborhoods.geojson", driver="GeoJSON")

# Creates a geojson file based on the fixed internet speed coordinates.
print("Creating a geojson file based on the fixed internet speed coordinates of quarter " + fixed_tiles_zip_file_date + "...")
internet_speed_tiles_by_location = gp.read_file(fixed_tiles_zip_file)
internet_speed_tiles_by_location = internet_speed_tiles_by_location.to_crs(4326)
internet_speed_tiles_by_location = internet_speed_tiles_by_location.to_file("assets\\internet_speed_tiles_" + fixed_tiles_zip_file_date + ".geojson", driver="GeoJSON")

# Reading Orlando data.
print("Reading Orlando data...")
orlando_neighborhoods_coordinates = gp.read_file("assets\\orlando_neighborhoods.geojson")

# Reading internet speed data.
print("Reading internet speed data...")
internet_speed_tiles_by_location = gp.read_file("assets\\internet_speed_tiles_" + fixed_tiles_zip_file_date + ".geojson")

# Joining data.
print("Joining data...")
tiles_in_orlando_neighborhoods = gp.sjoin(
    internet_speed_tiles_by_location,
    orlando_neighborhoods_coordinates,
    how="inner",
    op="intersects",
)

# Converting to Mbps for easier reading.
print("Converting to Mbps for easier reading...")
tiles_in_orlando_neighborhoods["avg_d_mbps"] = (
    tiles_in_orlando_neighborhoods["avg_d_kbps"] / 1024
)
tiles_in_orlando_neighborhoods["avg_u_mbps"] = (
    tiles_in_orlando_neighborhoods["avg_u_kbps"] / 1024
)

# Writing to file.
print("Writing to file...")
with open("results\\filtered_orlando_data_" + fixed_tiles_zip_file_date + ".geojson", "w") as output_file:
    geojson.dump(tiles_in_orlando_neighborhoods, output_file, ensure_ascii=False)