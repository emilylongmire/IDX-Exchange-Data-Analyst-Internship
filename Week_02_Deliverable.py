# Week 2 Deliverable - inspect data, identify outliers and columns with lots of missing values

import pandas as pd
import matplotlib.pyplot as plt

# read in data
listing_data = pd.read_csv("CRMLSListing.csv", low_memory=False)
sold_data = pd.read_csv("CRMLSSold.csv", low_memory=False)

# identify number of rows and columns
print("Listing data rows:" ,listing_data.shape[0], "\nListing data columns:" ,listing_data.shape[1])
print("\nSold data rows:" ,sold_data.shape[0], "\nSold data columns:" ,sold_data.shape[1])

# Listing : 591818 rows, 84 columns
# Sold : 430438 rows, 82 columns

# ensure only residential properties are included
print(sold_data["PropertyType"].unique())
print(listing_data["PropertyType"].unique())

# only residential included

# review column data types
print("\n")
print(listing_data.info())
print(sold_data.info())

# combination of strings, floats, ints, and objects

# listing data has some duplicate columns with ".1" at the end -> drop
listing_data = listing_data.drop(columns={"PropertyType.1","ListAgentFirstName.1","DaysOnMarket.1","LivingArea.1",
                                 "Longitude.1","Latitude.1","ListPrice.1","ListAgentLastName.1","CloseDate.1",
                                 "BuyerOfficeName.1","UnparsedAddress.1"})

# ----------------------------------------------------------------------------------------------------------------------
# check for null values
listing_nulls = listing_data.isnull().sum()/len(listing_data)*100
sold_nulls = sold_data.isnull().sum()/len(sold_data)*100

listing_nulls_over_90 = listing_nulls[listing_nulls >= 90]
sold_nulls_over_90 = sold_nulls[sold_nulls >= 90]

print("\nListing columns with over 90% missing values\n", listing_nulls_over_90)
print("\nSold columns with over 90% missing values\n", sold_nulls_over_90)

# Listing columns: FireplacesTotal, AboveGradeFinishedArea, TaxAnnualAmount, BuilderName, TaxYear, BuildingAreaTotal,
# ElementarySchoolDistrict, CoBuyerAgentFirstName, BelowGradeFinishedArea, BusinessType, CoveredSpaces,
# LotSizeDimensions, MiddleOrJuniorSchoolDistrict

# Sold columns : WaterfrontYN, BasementYN, FireplacesTotal, AboveGradeFinishedArea, TaxAnnualAmount, BuilderName,
# TaxYear, BuildingAreaTotal, ElementarySchoolDistrict, CoBuyerAgentFirstName, BelowGradeFinishedArea, BusinessType,
# CoveredSpaces, LotSizeDimensions, MiddleOrJuniorSchoolDistrict

# create null-summary tables
null_summary_listing = pd.DataFrame({"null_count": listing_data.isnull().sum(), "null_pct": listing_nulls
                                     }).sort_values("null_pct", ascending=False)

null_summary_sold = pd.DataFrame({"null_count": sold_data.isnull().sum(),"null_pct": sold_nulls
                                  }).sort_values("null_pct", ascending=False)

print("\nListing data null-count summary:\n", null_summary_listing)
print("\nSold data null-count summary:\n", null_summary_sold)

# drop columns with >90% missing values
listing_data_cleaned = listing_data.drop(columns = listing_nulls_over_90.index)
sold_data_cleaned = sold_data.drop(columns = sold_nulls_over_90.index)

# ----------------------------------------------------------------------------------------------------------------------
# check distribution for the following columns
distribution_columns = ["ClosePrice", "ListPrice", "OriginalListPrice", "LivingArea", "LotSizeAcres", "BedroomsTotal",
"BathroomsTotalInteger", "DaysOnMarket", "YearBuilt"]

data_sets = {"listing": listing_data_cleaned, "sold": sold_data_cleaned}

# loop through both data sets and all the columns
for name, d in data_sets.items():
    for col in distribution_columns:
        data = d[col]

        # print column name, mix, max, mean, median, and percentiles for each column
        print(f"\n[{name}] {col} - Min: {data.min()} - Max: {data.max()} - Mean: {data.mean()} - Median: {data.median()}")
        print("Percentiles:\n", data.quantile([0.05, 0.25, 0.5, 0.75, 0.95, 0.99]))

        # outlier summary - IQR
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = data[(data < lower_bound) | (data > upper_bound)]
        print(f"Outliers: {len(outliers)} ({len(outliers) / len(data) * 100:.2f}%)")

        # large % of outliers : LotSizeAcres

        # histogram
        data.hist(bins=50)
        plt.title(f"{name} - {col} Histogram")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.savefig(f"{name}_{col}_histogram.png")
        plt.close()

        # boxplot
        d.boxplot(column=col)
        plt.title(f"{name} - {col} Boxplot")
        plt.savefig(f"{name}_{col}_boxplot.png")
        plt.close()

# ----------------------------------------------------------------------------------------------------------------------
# print median and average close prices
print("\nMedian sold data close price:", sold_data_cleaned["ClosePrice"].median())
print("Average sold data close price:", sold_data_cleaned["ClosePrice"].mean())
# Median : $825000
# Average : $1193100.82

# percentage sold above vs. below list price
above_list_price = (sold_data_cleaned["ClosePrice"] > sold_data_cleaned["ListPrice"]).mean() * 100
# 40.1%
below_list_price = (sold_data_cleaned["ClosePrice"] < sold_data_cleaned["ListPrice"]).mean() * 100
# 42.54%
at_list = (sold_data_cleaned["ClosePrice"] == sold_data_cleaned["ListPrice"]).mean() * 100
# 17.36%
print(f"\nSold above list price: {above_list_price:.2f}%")
print(f"Sold below list price: {below_list_price:.2f}%")
print(f"Sold at list price: {at_list:.2f}%")

# ensure dates are in datetime format
sold_data_cleaned["ListingContractDate"] = pd.to_datetime(sold_data_cleaned["ListingContractDate"], errors="coerce")
sold_data_cleaned["CloseDate"] = pd.to_datetime(sold_data_cleaned["CloseDate"], errors="coerce")

# check if any listing dates come after sold dates
date_issues = sold_data_cleaned[sold_data_cleaned["CloseDate"] < sold_data_cleaned["ListingContractDate"]]
print(f"\nRows with date consistency issues: {len(date_issues)}")
# 64 rows with consistency issues

# counties with the highest median prices
county_median = sold_data_cleaned.groupby("CountyOrParish")["ClosePrice"].median().sort_values(ascending=False)
print("\nCounties with highest median close price:\n", county_median.head(10))

# ----------------------------------------------------------------------------------------------------------------------
# save to csv
listing_data_cleaned.to_csv("CRMLSListing_cleaned.csv", index=False)
sold_data_cleaned.to_csv("CRMLSSold_cleaned.csv", index=False)