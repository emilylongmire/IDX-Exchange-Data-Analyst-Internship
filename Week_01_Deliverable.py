# Week 1 Deliverable : concatenate sold and listing csv files into 2 csv's
# filter only residential properties
import pandas as pd

# set data types for certain columns to avoid error message
data_types = {"WaterfrontYN": "string", "ElementarySchool": "string", "BuilderName": "string","CoBuyerAgentFirstName": "string",
              "PostalCode": "string", "BusinessType": "string", "MiddleOrJuniorSchool": "string", "HighSchool": "string",}

# read in listing data
sold1 = pd.read_csv("csv/CRMLSSold202401.csv")
sold2 = pd.read_csv("csv/CRMLSSold202402.csv")
sold3 = pd.read_csv("csv/CRMLSSold202403.csv")
sold4 = pd.read_csv("csv/CRMLSSold202404.csv", dtype=data_types)
sold5 = pd.read_csv("csv/CRMLSSold202405_filled.csv")
sold6 = pd.read_csv("csv/CRMLSSold202406_filled.csv")
sold7 = pd.read_csv("csv/CRMLSSold202407_filled.csv")
sold8 = pd.read_csv("csv/CRMLSSold202408.csv")
sold9 = pd.read_csv("csv/CRMLSSold202409.csv")
sold10 = pd.read_csv("csv/CRMLSSold202410.csv")
sold11 = pd.read_csv("csv/CRMLSSold202411.csv")
sold12 = pd.read_csv("csv/CRMLSSold202412.csv")
sold13 = pd.read_csv("csv/CRMLSSold202501_filled.csv")
sold14 = pd.read_csv("csv/CRMLSSold202502.csv")
sold15 = pd.read_csv("csv/CRMLSSold202503.csv")
sold16 = pd.read_csv("csv/CRMLSSold202504.csv")
sold17 = pd.read_csv("csv/CRMLSSold202505.csv")
sold18 = pd.read_csv("csv/CRMLSSold202506.csv", dtype=data_types)
sold19 = pd.read_csv("csv/CRMLSSold202507.csv")
sold20 = pd.read_csv("csv/CRMLSSold202508.csv")
sold21 = pd.read_csv("csv/CRMLSSold202509.csv")
sold22 = pd.read_csv("csv/CRMLSSold202510.csv")
sold23 = pd.read_csv("csv/CRMLSSold202511.csv")
sold24 = pd.read_csv("csv/CRMLSSold202512.csv")
sold25 = pd.read_csv("csv/CRMLSSold202601.csv", dtype=data_types)
sold26 = pd.read_csv("csv/CRMLSSold202602.csv")
sold27 = pd.read_csv("csv/CRMLSSold202603.csv")
sold28 = pd.read_csv("csv/CRMLSSold202604.csv")
sold29 = pd.read_csv("csv/CRMLSSold202605.csv")

# concatenate sold data
sold = pd.concat([sold1, sold2, sold3, sold4, sold5, sold6, sold7, sold8,
                  sold9, sold10, sold11, sold12, sold13, sold14, sold15,
                  sold16, sold17, sold18, sold19, sold20, sold21, sold22,
                  sold23, sold24, sold25, sold26, sold27, sold28, sold29])

# read in listing data
list1= pd.read_csv("csv/CRMLSListing202401.csv")
list2 = pd.read_csv("csv/CRMLSListing202402.csv")
list3 = pd.read_csv("csv/CRMLSListing202403.csv")
list4 = pd.read_csv("csv/CRMLSListing202404.csv")
list5 = pd.read_csv("csv/CRMLSListing202405.csv")
list6 = pd.read_csv("csv/CRMLSListing202406.csv")
list7 = pd.read_csv("csv/CRMLSListing202407.csv")
list8 = pd.read_csv("csv/CRMLSListing202408.csv")
list9 = pd.read_csv("csv/CRMLSListing202409.csv")
list10 = pd.read_csv("csv/CRMLSListing202410.csv")
list11 = pd.read_csv("csv/CRMLSListing202411.csv")
list12 = pd.read_csv("csv/CRMLSListing202412.csv")
list13 = pd.read_csv("csv/CRMLSListing202501.csv")
list14 = pd.read_csv("csv/CRMLSListing202502.csv")
list15 = pd.read_csv("csv/CRMLSListing202503.csv")
list16 = pd.read_csv("csv/CRMLSListing202504.csv")
list17 = pd.read_csv("csv/CRMLSListing202505.csv")
list18 = pd.read_csv("csv/CRMLSListing202506.csv")
list19 = pd.read_csv("csv/CRMLSListing202507.csv")
list20 = pd.read_csv("csv/CRMLSListing202508.csv")
list21 = pd.read_csv("csv/CRMLSListing202509.csv")
list22 = pd.read_csv("csv/CRMLSListing202510.csv")
list23 = pd.read_csv("csv/CRMLSListing202511.csv")
list24 = pd.read_csv("csv/CRMLSListing202512.csv")
list25 = pd.read_csv("csv/CRMLSListing202601.csv")
list26 = pd.read_csv("csv/CRMLSListing202602.csv", dtype=data_types)
list27 = pd.read_csv("csv/CRMLSListing202603.csv")
list28 = pd.read_csv("csv/CRMLSListing202604.csv")
list29 = pd.read_csv("csv/CRMLSListing202605.csv")

# concatenate listing data
list = pd.concat([list1, list2, list3, list4, list5, list6, list7, list8,
                  list9, list10, list11, list12, list13, list14, list15,
                  list16, list17, list18, list19, list20, list21, list22,
                  list23, list24, list25, list26, list27, list28, list29])

# drop extra columns
sold.drop(columns={"lonfilled","latfilled"}, inplace=True)

# print rows for each data frame
print("Sold Rows: ", sold.shape[0])
print("List Rows: ", list.shape[0])
# Sold : 615725 rows
# Listing : 876594 rows

# filter to only residential properties
sold_residential = sold[sold["PropertyType"]=="Residential"]
list_residential = list[list["PropertyType"]=="Residential"]

# print rows for each filtered data frame
print("Sold Rows - Residential Only: ", sold_residential.shape[0])
print("List Rows - Residential Only: ", list_residential.shape[0] )
# Sold : 414063 rows
# Listing : 557318

# output sold and listing data to csv's
sold_residential.to_csv("CRMLSSold.csv", index=False)
list_residential.to_csv("CRMLSListing.csv", index=False)