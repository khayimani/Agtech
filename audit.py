import rasterio
import numpy as np

def calculate_ndvi(red_band_path, nir_band_path, output_path):
    # 1. Open the satellite image bands (Band 4 = Red, Band 8 = NIR for Sentinel-2)
    with rasterio.open(red_band_path) as red_src:
        red = red_src.read(1).astype('float32')
        profile = red_src.profile # Save metadata to write the new file later

    with rasterio.open(nir_band_path) as nir_src:
        nir = nir_src.read(1).astype('float32')

    # 2. The "Math" Advantage: Avoid division by zero errors
    np.seterr(divide='ignore', invalid='ignore')

    # 3. Calculate NDVI (The "Truth" Score)
    # Formula: (NIR - Red) / (NIR + Red)
    ndvi = (nir - red) / (nir + red)

    # 4. Filter the data (Astute Logic)
    # NDVI ranges from -1 to 1. 
    # > 0.4 means dense vegetation (Good work)
    # < 0.2 means bare soil (Bad work/Lazy)
    
    # 5. Save the "Truth Map"
    profile.update(dtype=rasterio.float32, count=1)
    with rasterio.open(output_path, 'w', **profile) as dst:
        dst.write(ndvi, 1)

    print(f"Audit Complete. Truth Map saved to {output_path}")
    
    # 6. Quick Analysis for the Client
    avg_health = np.nanmean(ndvi)
    if avg_health > 0.4:
        print("STATUS: Crops are healthy. Workers are doing their job.")
    elif avg_health > 0.2:
        print("STATUS: Warning. Growth is slow. Check irrigation.")
    else:
        print("STATUS: CRITICAL. It looks like bare soil. Did they even plant?")

# Usage: You download the Band 4 and Band 8 images from Copernicus (Free)
# calculate_ndvi('B04.jp2', 'B08.jp2', 'Farm_Audit_Week1.tif')