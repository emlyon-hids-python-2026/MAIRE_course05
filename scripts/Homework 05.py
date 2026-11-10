# %%
!uv add openpyxl
# %%
import pandas as pd
#Download the required libraries
# %%
df_Sales1 = pd.read_csv("../data/Sales_MedicStore_part1.csv", sep=";")
# %%
df_Sales2 = pd.read_csv("../data/Sales_MedicStore_part2.csv", sep=";")
# %%
df_Mapping1 = pd.read_excel("../data/Mapping.xlsx")
#Check the number of lines/ columns in each dataset
# %%
print("Sales Part 1:", df_Sales1.shape)
print("Sales Part 2:", df_Sales2.shape)
print("Mapping:", df_Mapping1.shape)

#add a value to the number of lines per dataset
#%%
lines_sales_part1 = df_Sales1.shape[0]
lines_sales_part2 = df_Sales2.shape[0]
lines_mapping = df_Mapping1.shape[0]
#check the data of each dataset
# %%
df_Sales1.head()
# %%
df_Sales2.head()
# %%
df_Mapping1.head()
#Combine Sales Part 1 and Sales Part 2 and check the result
#%%
# Combine Sales Part 1 and Sales Part 2
df_Sales = pd.concat([df_Sales1, df_Sales2], ignore_index=True)

# Show the resulting DataFrame
df_Sales.head()

#%%
# put the "Sub-Category" column as index in the mapping dataframe to prepare for the join
df_Mapping1 = df_Mapping1.set_index("Sub-Category")

# Launch the JOIN to add the mapping information to the sales dataframe as new columns
df_Final_sales = df_Sales.join(df_Mapping1, on="Sub-Category", how="left")
#%%
#Shape verification of the final dataset
print("Final_sales:", df_Final_sales.shape)
#verify the first lines of the final dataset
df_Final_sales.head()

# calculate the total sales for each order and add it as a new column in the final dataset
df_Final_sales["total_sales"] = df_Final_sales["Quantity"] * df_Final_sales["Unit Price"]
total = df_Final_sales["total_sales"].sum()
print(  f"Total des ventes: {total:,.2f} €")
# %%
#Export the final dataset to an Excel file
df_Final_sales.to_excel("../data/Final_Sales_Report.xlsx", index=False)


#Questions from the DATA TEAM:

#1. What is the number of lines and columns in our original datasets and in our final dataset ?

#%%
print("Sales Part 1:", df_Sales1.shape)
print("Sales Part 2:", df_Sales2.shape)
print("Mapping:", df_Mapping1.shape)
print("Final Sales:", df_Final_sales.shape)

#2. What are the column names in the final dataset ?
#%%
df_Final_sales.columns

#3. What are the top 5 lines of our dataset ?
#%%
df_Final_sales.head(5)
#4. What are the last 5 lines of our dataset ?
#%%
df_Final_sales.tail(5)

#5. Make a general statistical description of all the dataset
# %%
df_Final_sales.describe(include='all')

#Questions from the OPERATIONAL TEAM:

#1. How many orders do we have ?
#%%
nb_orders = df_Final_sales['Order ID'].nunique()
print(f"The number of orders is: {nb_orders}")

#2.What is the total sales amount ?
# %%
total_sales_amount = df_Final_sales['total_sales'].sum()
print(f"The total sales amount is: {total_sales_amount:,.2f} €")

#3. Who is the top 3 customers that makes the most purchases (order count)
# %%
order_count = (
    df_Final_sales["Customer Name"].value_counts().head(3)
)
print("the top 3 customers by order count are:")
print(order_count)
#4 What is the total Sales for France ?
# %%
sales_france = df_Final_sales.loc[df_Final_sales["Country"] == "France", "total_sales"]

print(f"The total sales for France are: {sales_france.sum():.2f} €")

#How much does the total Sales for France represent compare to the total global Sales
# %%
French_sales_pourcentage = (sales_france.sum() / total_sales_amount) * 100

print(f"The total sales for France represent {French_sales_pourcentage:.2f}% of the total global sales")

#%%
# Create a dictionary to store the analysis results
dict_analysis = {
"how many lines are in Sales_MedicStore_part1.csv": lines_sales_part1,
"how many lines are in Sales_MedicStore_part2.csv": lines_sales_part2,
"how many lines are in Mapping.xlsx": lines_mapping,
"how many orders do we have": nb_orders,
"what is the total sales amount": total_sales_amount,
"What is the total Sales for France": sales_france.sum(),
"How much does the total Sales for France represent compare to the total global Sales": French_sales_pourcentage
}

# Convert the dictionary to a DataFrame for better visualization
#%%
df_analysis = pd.DataFrame(list(dict_analysis.items()), columns=['Question', 'Answer'])
df_analysis.head()
# %%
