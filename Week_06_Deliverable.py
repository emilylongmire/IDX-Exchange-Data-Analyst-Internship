# Week 6 Deliverable
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# read in data
listings = pd.read_csv("Listings_Cleaned.csv", low_memory=False)
sold = pd.read_csv("Sold_Cleaned.csv", low_memory=False)


# create key metrics ---------------------------------------------------------------------------------------------------
sold["Price Ratio"] = sold["ClosePrice"] / sold["OriginalListPrice"]
sold["Price Per Sq Ft"] = sold["ClosePrice"] / sold["LivingArea"]
sold = sold.rename(columns={"DaysOnMarket": "Days on Market"})
listings = listings.rename(columns={"DaysOnMarket": "Days on Market"})

# make sure date related colummns are in date time format
date_cols = ["CloseDate", "ListingContractDate", "PurchaseContractDate"]
for col in date_cols:
    sold[col] = pd.to_datetime(sold[col], errors="coerce")

# extract year, month, and year/month from close date
sold["Year"] = sold["CloseDate"].dt.year
sold["Month"] = sold["CloseDate"].dt.month
sold["YrMo"] = sold["CloseDate"].dt.to_period("M").astype(str)

sold["Close to Original List Ratio"] = sold["ClosePrice"] / sold["OriginalListPrice"]
sold["Listing to Contract Days"] = (sold["PurchaseContractDate"] - sold["ListingContractDate"]).dt.days
sold["Contract to Close Days"] = (sold["CloseDate"] - sold["PurchaseContractDate"]).dt.days

# add school districts using latitude and longitude --------------------------------------------------------------------
school_districts = gpd.read_file("California_School_District_Areas_2024-25.geojson")
school_districts = school_districts.to_crs("EPSG:4326")

sold_GeoDataFrame = gpd.GeoDataFrame(sold, geometry=[Point(xy) for xy in zip(sold["Longitude"], sold["Latitude"])],crs="EPSG:4326")

sold = gpd.sjoin(sold_GeoDataFrame, school_districts[["geometry", "DistrictName"]], how="left", predicate="within")
sold = sold.drop(columns=["index_right", "geometry"])
sold = sold.rename(columns={"DistrictName": "School District"})


# segment analysis -----------------------------------------------------------------------------------------------------
property_type = sold.groupby(["PropertyType", "PropertySubType"]).agg(Count=("ClosePrice", "count"),
    Avg_Close_Price=("ClosePrice", "mean"), Median_Close_Price=("ClosePrice", "median"),
    Avg_Price_Ratio=("Price Ratio", "mean"), Avg_Days_on_Market=("Days on Market", "mean"),
    Avg_PPSF=("Price Per Sq Ft", "mean")).reset_index().round(3)

county = sold.groupby(["CountyOrParish", "MLSAreaMajor"]).agg(Count=("ClosePrice", "count"),
    Avg_Close_Price=("ClosePrice", "mean"), Avg_Price_Ratio=("Price Ratio", "mean"),
    Avg_Days_on_Market=("Days on Market", "mean")).reset_index().round(3)

office = sold.groupby(["ListOfficeName", "BuyerOfficeName"]).agg(Count=("ClosePrice", "count"),
    Avg_Close_Price=("ClosePrice", "mean"),Avg_Price_Ratio=("Price Ratio", "mean")).reset_index().round(3)

# sample output
sample_output = sold[["ClosePrice", "OriginalListPrice", "Price Ratio", "Price Per Sq Ft", "Days on Market",
        "YrMo", "Listing to Contract Days", "Contract to Close Days", "School District"]]

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)

print("\nSample Output: \n", sample_output.head(10))

# print segment analysis data frames
print("\nSegment Analysis Property Type: \n", property_type.head(10))
print("\nSegment Analysis County: \n", county.head(10))
print("\nSegment Analysis Office: \n", office.head(10))

# save segment analysis to csv's
property_type.to_csv("Segment_Analysis_Property_Type.csv", index=False)
county.to_csv("Segment_Analysis_County.csv", index=False)
office.to_csv("Segment_Analysis_Office.csv", index=False)

sold.to_csv("Sold_Cleaned.csv", index=False)