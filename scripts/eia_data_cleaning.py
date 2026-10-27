import pandas as pd

try:
    # Requesting file path
    file = input("Enter file path: ")
    # file = 'Table_1.3_Primary_Energy_Consumption_by_Source.xlsx'
    
    # Reading the "Monthly Data" tab in the Excel file while skipping rows 1-10
    eia_monthly = pd.read_excel(file, sheet_name='Monthly Data', skiprows=10)
    eia_yearly = pd.read_excel(file, sheet_name='Annual Data', skiprows=10)
    
    # Concatenating headers with respective units and overwriting the current headers with new headers
    new_monthly_headers = []
    for col, unit in zip(eia_monthly.columns, eia_monthly.iloc[0]):
        if pd.isna(unit):
            new_monthly_headers.append(col)
        else:
            new_monthly_headers.append(f"{col} {unit}")
    eia_monthly.columns = new_monthly_headers
    
    new_yearly_headers = []
    for col, unit in zip(eia_yearly.columns, eia_yearly.iloc[0]):
        if pd.isna(unit):
            new_yearly_headers.append(col)
        else:
            new_yearly_headers.append(f"{col} {unit}")
    new_yearly_headers[0] = "Year"
    eia_yearly.columns = new_yearly_headers
    
    # Dropping the units row and reseting the index
    eia_monthly = eia_monthly.drop(index=0).reset_index(drop=True)
    eia_yearly = eia_yearly.drop(index=0).reset_index(drop=True)
    
    # Creating a filter for the desired period and specifying target columns
    monthly_mask = (eia_monthly['Month'].dt.year >= 1973) & (eia_monthly['Month'].dt.year <= 1983)
    target_columns = ['Solar Energy Consumption (Quadrillion Btu)', 'Wind Energy Consumption (Quadrillion Btu)']
    # Replacing missing Solar and Wind values in the specified time period with zero
    eia_monthly.loc[monthly_mask, target_columns] = eia_monthly.loc[monthly_mask, target_columns].replace("Not Available", 0.0)
    
    yearly_mask = (eia_yearly['Year'] >= 1949) & (eia_yearly['Year'] <= 1983)
    target_columns = ['Geothermal Energy Consumption (Quadrillion Btu)', 'Solar Energy Consumption (Quadrillion Btu)', 'Wind Energy Consumption (Quadrillion Btu)']
    # Replacing missing Geothermal, Solar and Wind values in the specified time period with zero
    eia_yearly.loc[yearly_mask, target_columns] = eia_yearly.loc[yearly_mask, target_columns].replace("Not Available", 0.0)

    # Convert the integer year into a proper datetime object (defaults to Jan 1st of that year)
    eia_monthly['Month'] = pd.to_datetime(eia_monthly['Month'], format='%b %Y')
    eia_yearly['Year'] = pd.to_datetime(eia_yearly['Year'], format='%Y')
    
    # Enforcing appropriate data type for all energy consumption columns
    eia_monthly[new_monthly_headers[1:]] = eia_monthly[new_monthly_headers[1:]].apply(pd.to_numeric)
    eia_yearly[new_yearly_headers[1:]] = eia_yearly[new_yearly_headers[1:]].apply(pd.to_numeric)
    
    # Displaying data summary and other metrics to evaluate data cleanliness
    print("Monthly Data Info:")
    print(eia_monthly.info())
    for i in new_monthly_headers:
        print(f"{i}: Max = {max(eia_monthly[i])} | Min = {min(eia_monthly[i])}")
    print()
    print("Annual Data Info:")
    print(eia_yearly.info())
    for i in new_yearly_headers:
        print(f"{i}: Max = {max(eia_yearly[i])} | Min = {min(eia_yearly[i])}")    
    
    # Displaying final, cleaned data
    print()
    print("Monthly Data:")
    print(eia_monthly)
    print()
    print("Annual Data:")
    print(eia_yearly)
    
    try:
        # Writing the cleaned data to an Excel file
        with pd.ExcelWriter(file.split(".x")[0] + "_Python_Cleaned.xlsx", engine="openpyxl") as f:
            eia_monthly.to_excel(f, sheet_name="Monthly Data", index=False)
            eia_yearly.to_excel(f, sheet_name="Annual Data", index=False)
            
        print("Writing...")
        print("Both sheets successfully written to the cleaned workbook.")
    except PermissionError:
        print("Error: File is open. Close to file to write updates.")
    
except FileNotFoundError:
    print("File not found.")    
