from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import QUrl, QTimer, Qt
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView
import requests
import os

class RadarWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather Radar")
        self.setMinimumSize(200, 150)
        self.resize(1024, 768)
        
        # Enable window flags for resizing
        self.setWindowFlags(
            Qt.WindowType.Window |  # Basic window flags
            Qt.WindowType.WindowMinimizeButtonHint |
            Qt.WindowType.WindowMaximizeButtonHint |
            Qt.WindowType.WindowCloseButtonHint
        )
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, True)
        
        # Create web view
        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)
        
        # Enable required settings
        settings = self.web_view.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        
        # Initial update
        self.update_radar()
        
        # Set up auto-update timer (every 5 minutes)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_radar)
        self.timer.start(5 * 60 * 1000)  # 5 minutes in milliseconds
    
    def update_radar(self):
        try:
            print("Updating radar data...")
            response = requests.get("https://api.rainviewer.com/public/weather-maps.json")
            data = response.json()
            radar_time = data['radar']['past'][-1]['time']
            radar_url = f"https://tilecache.rainviewer.com/v2/radar/{radar_time}/256/{{z}}/{{x}}/{{y}}/2/1_1.png"
            
            html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
                    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
                    <style>
                        body {{ margin: 0; padding: 0; }}
                        #map {{ height: 100vh; width: 100%; }}
                        #timestamp {{ 
                            position: absolute; 
                            bottom: 10px; 
                            right: 10px; 
                            background: white; 
                            padding: 5px; 
                            border-radius: 5px;
                            z-index: 1000;
                        }}
                    </style>
                </head>
                <body>
                    <div id="map"></div>
                    <div id="timestamp">Last Updated: {self.get_formatted_time()}</div>
                    <script>
                        var map = L.map('map', {{
                            center: [39.8283, -98.5795],
                            zoom: 4
                        }});
                        
                        // Add base map
                        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                            attribution: '© OpenStreetMap contributors'
                        }}).addTo(map);
                        
                        // Add radar layer
                        if ('{radar_url}') {{
                            L.tileLayer('{radar_url}', {{
                                opacity: 0.7
                            }}).addTo(map);
                        }}
                    </script>
                </body>
                </html>
            """
            
            temp_map_path = os.path.abspath("temp_map.html")
            with open(temp_map_path, "w", encoding='utf-8') as f:
                f.write(html_content)
            
            self.web_view.setUrl(QUrl.fromLocalFile(temp_map_path))
            print("Radar update complete!")
            
        except Exception as e:
            print(f"Error updating radar: {e}")
    
    def get_formatted_time(self):
        from datetime import datetime
        return datetime.now().strftime("%I:%M %p")
