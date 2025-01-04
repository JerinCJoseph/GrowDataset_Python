import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# bounding box with valid coordinates
longitude_min, longitude_max = -10.592, 1.6848
latitude_min, latitude_max = 50.681, 57.985

"""Loading and cleaning the GrowLocations dataset.
    - Removing any invalid latitude and longitude values.
    - Correct swapped latitude and longitude .
    - Cleaning up the Serial column to retain only the main serial number."""
def load_and_clean_dataset(file_path):    
    data = pd.read_csv(file_path)
    
    # Verifying column names 
    if 'Latitude' not in data.columns or 'Longitude' not in data.columns or 'Serial' not in data.columns:
        raise ValueError("Dataset is missing required Latitude, Longitude, or Serial columns.")

    # Correcting column labels
    data.rename(columns={'Latitude': 'Longitude', 'Longitude': 'Latitude'}, inplace=True)

    # Cleaning the Serial col
    if 'Serial' in data.columns:
        data['Serial'] = data['Serial'].str.extract(r'(\bPI[0-9A-Z]+\b)')
        data['Serial'] = data['Serial'].fillna("Unknown Serial")

    # Removing rows with invalid latitude and longitude (values outside the bound box coordinates)
    valid_data = data[
        (data['Latitude'].between(latitude_min, latitude_max)) &
        (data['Longitude'].between(longitude_min, longitude_max))
    ]

    return valid_data

"""Plotting the cleaned data on the UK map image with tooltips"""
def plot_data_on_image_with_tooltips(data, map_image_path):
    # Loading the map image
    map_image = Image.open(map_image_path)

    # Plotting the map image as the background
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(map_image, extent=[longitude_min, longitude_max, latitude_min, latitude_max], aspect='auto')

    # Plotting the sensor locations
    scatter = ax.scatter(
        data['Longitude'], data['Latitude'], color='red', s=10, label='Sensor Locations'
    )

    # Adding labels and legend
    plt.title('Growdata Sensor Locations on UK Map', fontsize=16)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()

    """Updates the tooltip content and position based on 
       the hovered data point."""
    sensor_tooltip = ax.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"), arrowprops=dict(arrowstyle="->"))
    sensor_tooltip.set_visible(False)

    def update_tooltip(ind):
        pos = scatter.get_offsets()[ind[0]]
        sensor_tooltip.xy = pos
        columns_to_display = [col for col in data.columns if col not in ['Type', 'Code']]
        text = "{}".format(
            "\n".join([f"{col}: {data.iloc[ind[0]][col]}" for col in columns_to_display]) 
        )
        sensor_tooltip.set_text(text)
        sensor_tooltip.get_bbox_patch().set_alpha(0.9)

    def on_hover(event):
        vis = sensor_tooltip.get_visible()
        if event.inaxes == ax:
            cont, ind = scatter.contains(event)
            if cont:
                update_tooltip(ind["ind"])
                sensor_tooltip.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    sensor_tooltip.set_visible(False)
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", on_hover)

    plt.show()

if __name__ == "__main__":
    file_path = "GrowLocations.csv"  
    map_image_path = "map7.png"  

    try:
        # Loading and cleaning the dataset
        cleaned_data = load_and_clean_dataset(file_path)

        # Plotting the cleaned data on the UK map image with tooltips
        plot_data_on_image_with_tooltips(cleaned_data, map_image_path)

    except Exception as e:
        print(f"An error occurred: {e}")
