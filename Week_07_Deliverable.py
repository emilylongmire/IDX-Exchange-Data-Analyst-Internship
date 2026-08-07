# Week 7 Deliverable - outlier detection + filtering
import pandas as pd

# read in data
listings = pd.read_csv("Listings_Cleaned.csv", low_memory=False)
sold = pd.read_csv("Sold_Cleaned.csv", low_memory=False)

# flag ClosePrice as invalid if the value is less than 0
sold["ClosePrice_invalid"] = sold["ClosePrice"] <= 0

# flag outliers for ClosePrice based on IQR
Q1 = sold["ClosePrice"].quantile(0.25)
Q3 = sold["ClosePrice"].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
sold["ClosePrice_outliers"] = (sold["ClosePrice"] < lower) | (sold["ClosePrice"] > upper)
sold.loc[sold["ClosePrice"].isna(), "ClosePrice_outliers"] = False

# flag outliers for DaysOnMarket based on IQR
Q1 = sold["DaysOnMarket"].quantile(0.25)
Q3 = sold["DaysOnMarket"].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
sold["DaysOnMarket_outliers"] = (sold["DaysOnMarket"] < lower) | (sold["DaysOnMarket"] > upper)
sold.loc[sold["DaysOnMarket"].isna(), "DaysOnMarket_outliers"] = False

# flag outliers for LivingArea based on IQR
Q1 = sold["LivingArea"].quantile(0.25)
Q3 = sold["LivingArea"].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
sold["LivingArea_outliers"] = (sold["LivingArea"] < lower) | (sold["LivingArea"] > upper)
sold.loc[sold["LivingArea"].isna(), "LivingArea_outliers"] = False

# flag sold data entries as outliers if the values for ClosePrice, DaysOnMarket, or Living Area are outliers
sold["is_outlier"] = (sold["ClosePrice_invalid"] | sold["ClosePrice_outliers"] | sold["DaysOnMarket_outliers"]
                      | sold["LivingArea_outliers"])

# save data set with outlier flag to csv
sold.to_csv("Sold_Flagged_Full.csv", index=False)

# filter out outliers and save to csv
sold_filtered = sold[~sold["is_outlier"]].copy()
sold_filtered.to_csv("Sold_Filtered_Clean.csv", index=False)

# compare shape and medians before and after outlier filtering
print("\nNumber of rows before filtering:", sold.shape[0])
print("Number of rows after filtering:", sold_filtered.shape[0])
print("Number of rows flagged as outliers:", sold["is_outlier"].sum())
print("\nClosePrice median before filtering:", sold["ClosePrice"].median())
print("ClosePrice median after filtering:", sold_filtered["ClosePrice"].median())
print("\nDaysOnMarket median before filtering:", sold["DaysOnMarket"].median())
print("DaysOnMarket median after filtering:", sold_filtered["DaysOnMarket"].median())
print("\nLivingArea median before filtering:", sold["LivingArea"].median())
print("LivingArea median after filtering:", sold_filtered["LivingArea"].median())