# Week 4 Deliverable
import pandas as pd
import matplotlib.pyplot as plt


# read in sold/listing with rates data
listing_data = pd.read_csv("Sold_With_Rates.csv", low_memory=False)
sold_data = pd.read_csv("Listings_With_Rates.csv", low_memory=False)


# convert to datetime --------------------------------------------------------------------------------------------------
to_datetime_cols = ["CloseDate", "PurchaseContractDate", "ListingContractDate", "ContractStatusChangeDate"]

for col in to_datetime_cols:
   listing_data[col] = pd.to_datetime(listing_data[col])
   sold_data[col] = pd.to_datetime(sold_data[col])


# drop redundant columns -----------------------------------------------------------------------------------------------
# BuyerAgencyCompensation and BuerAgencyCompensationType = all NA values for sold data
# LotSizeArea = same as LotSizeSquareFeet
# Note -> Levels and Stories slightly redundant, but Stories includes extra information + may need to be cleaned
columns_to_drop_sold = ["BuyerAgencyCompensation","BuyerAgencyCompensationType","LotSizeArea"]
columns_to_drop_listing = ["LotSizeArea"]

sold_data.drop(columns=columns_to_drop_sold, inplace=True)
listing_data.drop(columns=columns_to_drop_listing, inplace=True)


# missing values -------------------------------------------------------------------------------------------------------
# first, analyze the distributions/outliers of the numeric columns from week 2
# impute LotSizeAcres with the median due to the large amount of outliers
sold_data["LotSizeAcres"] = sold_data["LotSizeAcres"].fillna(sold_data["LotSizeAcres"].median())
listing_data["LotSizeAcres"] = listing_data["LotSizeAcres"].fillna(listing_data["LotSizeAcres"].median())


# remove invalid numeric values ----------------------------------------------------------------------------------------
sold_mask = ((sold_data["ClosePrice"] > 0) & (sold_data["LivingArea"] > 0) & (sold_data["DaysOnMarket"] >= 0) &
    (sold_data["BedroomsTotal"] >= 0) & (sold_data["BathroomsTotalInteger"] >= 0))

listing_mask = ((listing_data["LivingArea"] > 0) & (listing_data["DaysOnMarket"] >= 0) &
    (listing_data["BedroomsTotal"] >= 0) & (listing_data["BathroomsTotalInteger"] >= 0))

listing_data = listing_data[listing_mask].copy()
sold_data = sold_data[sold_mask].copy()

# date consistency checks ----------------------------------------------------------------------------------------------
sold_data["listing_after_close_flag"] = sold_data["ListingContractDate"] > sold_data["CloseDate"]
sold_data["purchase_after_close_flag"] = sold_data["PurchaseContractDate"] > sold_data["CloseDate"]
sold_data["negative_timeline_flag"] = ((sold_data["PurchaseContractDate"] < sold_data["ListingContractDate"]) |
    (sold_data["CloseDate"] < sold_data["PurchaseContractDate"]))

# geographic data checks -----------------------------------------------------------------------------------------------
sold_data["missing"] = sold_data["Latitude"].isna() | sold_data["Longitude"].isna()
sold_data["sentinel"] = (sold_data["Latitude"] == 0) | (sold_data["Longitude"] == 0)
sold_data["positive_longitude"] = sold_data["Longitude"] > 0
sold_data["out_of_state"] = (~sold_data["missing"] & ~sold_data["sentinel"] & ((sold_data["Latitude"]
     < 32) | (sold_data["Latitude"] > 42) | (sold_data["Longitude"] < -124) | (sold_data["Longitude"] > -114)))