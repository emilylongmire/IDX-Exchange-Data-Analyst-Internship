# Week 3 Deliverable
import pandas as pd

# read in sold/listing data
listing_data = pd.read_csv("CRMLSListing_cleaned.csv", low_memory=False)
sold_data = pd.read_csv("CRMLSSold_cleaned.csv", low_memory=False)

# fetch the mortgage rate data from FRED
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url, parse_dates=["observation_date"])
mortgage.columns = ["date", "rate_30yr_fixed"]

# resample weekly rates to monthly averages
mortgage["year_month"] = mortgage["date"].dt.to_period("M")
mortgage_monthly = (mortgage.groupby("year_month")["rate_30yr_fixed"].mean().reset_index())

# create a matching year_month key on the MLS datasets
# sold data — key off CloseDate
sold_data["year_month"] = pd.to_datetime(sold_data["CloseDate"]).dt.to_period("M")

# listing data — key off ListingContractDate
listing_data["year_month"] = pd.to_datetime(listing_data["ListingContractDate"]).dt.to_period('M')

# merge data
sold_with_rates = sold_data.merge(mortgage_monthly, on="year_month", how="left")
listings_with_rates = listing_data.merge(mortgage_monthly, on="year_month", how="left")

# validate the merge
# checking for any unmatched rows
print(sold_with_rates["rate_30yr_fixed"].isnull().sum())
print(listings_with_rates["rate_30yr_fixed"].isnull().sum())

# 0 null values for both sold and listing data

# preview
print(sold_with_rates[["CloseDate", "year_month", "ClosePrice", "rate_30yr_fixed"]].head())

sold_with_rates.to_csv("Sold_With_Rates.csv", index=False)
listings_with_rates.to_csv("Listings_With_Rates.csv", index=False)