# Magnificent 7
# !/usr/bin/python3

from pprint import pprint
import geopandas as gp
import geojson
import re

file = "filtered_orlando_data_2019-01-01.geojson"
date = re.search("(([0-9]{4}\-[0-9]{2}\-[0-9]{2}))", file).group(0)

def main():
    neigh_df = gp.read_file("assets\\orlando_neighborhoods.geojson")
    tiles_df = gp.read_file("results\\" + file)

    del tiles_df["avg_d_kbps"]
    del tiles_df["avg_u_kbps"]

    mean_d = tiles_df.groupby("NeighID")["avg_d_mbps"].mean()
    mean_u = tiles_df.groupby("NeighID")["avg_u_mbps"].mean()

    means = tiles_df[["NeighID", "avg_d_mbps", "avg_u_mbps"]].groupby("NeighID").mean()

    means = means.reset_index()

    avg_d_mbps = []
    avg_u_mbps = []

    for i, row in neigh_df.iterrows():
        neigh_id = row["NeighID"]

        try:
            d = list(
                means[means["NeighID"] == neigh_id].to_dict().get("avg_d_mbps").values()
            )[0]
            u = list(
                means[means["NeighID"] == neigh_id].to_dict().get("avg_u_mbps").values()
            )[0]
        except:
            d = None
            u = None

        avg_d_mbps.append(d)
        avg_u_mbps.append(u)

    neigh_df["avg_d_mbps"] = avg_d_mbps
    neigh_df["avg_u_mbps"] = avg_u_mbps

    out_f = open("results\\orlando_averaged_" + date + ".geojson", "w", encoding="utf-8")
    geojson.dump(neigh_df, out_f)
    out_f.close()

if __name__ == "__main__":
    main()
