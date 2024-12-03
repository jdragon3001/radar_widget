from PyQt6.QtWidgets import QApplication
from PyQt6.QtQml import QQmlApplicationEngine
from radar_widget import RadarWidget
import sys

def main():
    # Create QApplication instance
    app = QApplication(sys.argv)
    app.setApplicationName("Weather Radar")
    
    # Create and show radar widget
    radar = RadarWidget()
    radar.show()
    
    # Start the application event loop
    return app.exec()

if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        print("Closing Weather Radar application...") 