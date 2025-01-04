## Plotting Grow Dataset(GrowLocations.csv) on UK Map

### Introduction
The script effectively processes and visualises GrowLocations data by addressing key challenges in data cleaning and representation. The cleaned dataset ensures concise serial numbers and valid locations, and the interactive visualisation provides a user-friendly interface for analysing sensor locations across the UK.

## Features

#### Data Loading and Cleaning
1. **Data Loading**: Reads the dataset into a Pandas DataFrame.
2. **Column Verification**: Ensures the dataset contains `Latitude`, `Longitude`, and `Serial` columns.
3. **Swapped Column Correction**: Corrects cases where `Latitude` and `Longitude` columns might have been inadvertently swapped.
4. **Validity Filtering**: Filters out entries with latitude and longitude values outside the UK geographical bounds:
   - Longitude range: \[-10.592, 1.6848\]
   - Latitude range: \[50.681, 57.985\]
5. **Serial Number Cleaning**: Extracts the core part of the sensor serial numbers, removing unnecessary trailing data. For example:
   - Original: `PI040298AD5I211590. FuturePractice:,Id:861,...`
   - Cleaned: `PI040298AD5I211590`

#### Interactive Visualisation
1. **Map Integration**:
  - Displays sensor locations on a UK map image (`map7.png`).
2. **Sensor Location Plotting**:
  - Marks sensor positions as red dots, mapped to their geographic coordinates.
3. **Interactive Tooltips**:
  - Displays detailed sensor information when hovering over a location.

