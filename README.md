<img src="https://i.imgur.com/E9GJVaL.png" width=300>
<hr>

GeoPy is a Python script that generates a KML file based on network traffic data from a Wireshark pcap file. It uses IP geolocation to map the network connections and creates a KML file that can be uploaded to Google My Maps for visualization.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/p3rception/GeoPy.git
    ```

2. Navigate to the project directory:

    ```bash
    cd GeoPy
    ```
3. (Optional) Create and activate a virtual environment.

    ```bash
    # Creation
    python -m venv venv
    
    # Activation
    source venv/bin/activate    # Unix
    venv\Scripts\activate.bat   # Windows
    ```

4. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```
5. Download GeoLiteCity database to translate IP addresses into a Geo location(longitude & latitude). The database can be downloaded here: https://github.com/mbcc2006/GeoLiteCity-data

6. Save Wireshark captured data in .pcap format.

## Usage

1. ```python main.py <pcap_file> ```
2. Upload the generated KML file to [Google My Maps](https://www.google.com/mymaps).


## Author

Dimitris Pergelidis ([p3rception](https://github.com/p3rception))