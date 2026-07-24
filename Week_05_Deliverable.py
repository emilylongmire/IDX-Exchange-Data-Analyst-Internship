# Week 5 Deliverable
import pandas as pd

# read in sold/listing with rates data
sold_data = pd.read_csv("Sold_With_Rates.csv", low_memory=False)
listing_data = pd.read_csv("Listings_With_Rates.csv", low_memory=False)

# save # of rows before cleaning
before_rows_listing = len(listing_data)
before_rows_sold = len(sold_data)

# convert to datetime --------------------------------------------------------------------------------------------------
to_datetime_cols = ["CloseDate", "PurchaseContractDate", "ListingContractDate", "ContractStatusChangeDate"]

for col in to_datetime_cols:
    listing_data[col] = pd.to_datetime(listing_data[col])
    sold_data[col] = pd.to_datetime(sold_data[col])

# drop redundant columns -----------------------------------------------------------------------------------------------
# BuyerAgencyCompensation and BuyerAgencyCompensationType have a large percentage of missing values
# LotSizeArea and LotSizeFeet same values -> drop LotSizeArea
# ListingKeyNumeric and ListingKey same values -> drop ListingKeyNumeric
# OriginatingSystemName and OriginatingSystemSubName have many missing values for sold data -> drop
columns_to_drop_sold = ["BuyerAgencyCompensation", "BuyerAgencyCompensationType", "LotSizeArea", "ListingKeyNumeric",
                        "OriginatingSystemName", "OriginatingSystemSubName"]

columns_to_drop_listing = ["LotSizeArea", "ListingKeyNumeric"]

sold_data.drop(columns=columns_to_drop_sold, inplace=True)
listing_data.drop(columns=columns_to_drop_listing, inplace=True)

# remove duplicate records ---------------------------------------------------------------------------------------------
# non-unique ListingKey values
dupes_sold = sold_data["ListingKey"].duplicated().sum()
dupes_listing = listing_data["ListingKey"].duplicated().sum()
sold_data = sold_data.drop_duplicates(subset="ListingKey", keep="first").copy()
listing_data = listing_data.drop_duplicates(subset="ListingKey", keep="first").copy()

# missing values -------------------------------------------------------------------------------------------------------
# using distributions/outliers from week 2 deliverable
# LotSizeAcres has large amount of outliers -> impute with median
sold_data["LotSizeAcres"] = sold_data["LotSizeAcres"].fillna(sold_data["LotSizeAcres"].median())
listing_data["LotSizeAcres"] = listing_data["LotSizeAcres"].fillna(listing_data["LotSizeAcres"].median())

# remove invalid numeric values ----------------------------------------------------------------------------------------
sold_mask = ((sold_data["ClosePrice"] > 0) & (sold_data["LivingArea"] > 0) & (sold_data["DaysOnMarket"] >= 0) &
    (sold_data["BedroomsTotal"] >= 0) & (sold_data["BathroomsTotalInteger"] >= 0))

listing_mask = ((listing_data["LivingArea"] > 0) & (listing_data["DaysOnMarket"] >= 0) &
    (listing_data["BedroomsTotal"] >= 0) & (listing_data["BathroomsTotalInteger"] >= 0))

listing_data = listing_data[listing_mask].copy()
sold_data = sold_data[sold_mask].copy()

after_rows_listing = len(listing_data)
after_rows_sold = len(sold_data)

# flag unrealistic outliers
current_year = pd.Timestamp.now().year
for df in (sold_data, listing_data):
    df["bed_bath_flag"] = (df["BedroomsTotal"] > 20) | (df["BathroomsTotalInteger"] > 15)
    df["year_built_flag"] = df["YearBuilt"] > current_year

# date consistency checks ----------------------------------------------------------------------------------------------
def add_date_flags(df):
    df["listing_after_close_flag"] = df["ListingContractDate"] > df["CloseDate"]
    df["purchase_after_close_flag"] = df["PurchaseContractDate"] > df["CloseDate"]
    df["negative_timeline_flag"] = ((df["PurchaseContractDate"] < df["ListingContractDate"]) |
        (df["CloseDate"] < df["PurchaseContractDate"]))
    return df

sold_data = add_date_flags(sold_data)
listing_data = add_date_flags(listing_data)

# geographic data checks -----------------------------------------------------------------------------------------------
def add_geo_flags(df):
    df["missing"] = df["Latitude"].isna() | df["Longitude"].isna()
    df["sentinel"] = (df["Latitude"] == 0) | (df["Longitude"] == 0)
    df["positive_longitude"] = df["Longitude"] > 0
    df["out_of_state"] = (~df["missing"] & ~df["sentinel"] & ((df["Latitude"] < 32) | (df["Latitude"] > 42) |
        (df["Longitude"] < -124) | (df["Longitude"] > -114)))
    return df

sold_data = add_geo_flags(sold_data)
listing_data = add_geo_flags(listing_data)

# row counts -----------------------------------------------------------------------------------------------------------
print("Row counts before and after:")
print(f"Listing data before: {before_rows_listing}   after: {after_rows_listing}")
print(f"Sold data before: {before_rows_sold}   after: {after_rows_sold}")

# data type confirmation
print("\nData types:")
print("listing_data dtypes:\n", listing_data[to_datetime_cols].dtypes)
print("sold_data dtypes:\n", sold_data[to_datetime_cols].dtypes)

# date consistency flag counts
print("\nDate consistency flag counts:")
for name, df in [("listing_data", listing_data), ("sold_data", sold_data)]:
    print(f"{name}: listing_after_close={df["listing_after_close_flag"].sum()}, "
          f"purchase_after_close={df["purchase_after_close_flag"].sum()}, "
          f"negative_timeline={df["negative_timeline_flag"].sum()}")

# geographic data quality summary
print("\nGeographic data quality summary:")
for name, df in [("listing_data", listing_data), ("sold_data", sold_data)]:
    print(f"{name}: missing={df["missing"].sum()}, sentinel_zero={df["sentinel"].sum()}, "
          f"positive_longitude={df["positive_longitude"].sum()}, out_of_state={df["out_of_state"].sum()}")

# flagged data counts
print("\nUnrealistic value flags:")
for name, df in [("listing_data", listing_data), ("sold_data", sold_data)]:
    print(f"{name}: bed_bath_flagged={df["bed_bath_flag"].sum()}, "
          f"year_built_flagged={df["year_built_flag"].sum()}")

# save cleaned data sets to csvs
listing_data.to_csv("Listings_Cleaned.csv", index=False)
sold_data.to_csv("Sold_Cleaned.csv", index=False)