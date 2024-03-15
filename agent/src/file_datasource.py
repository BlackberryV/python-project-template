from csv import DictReader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
from domain.parking import Parking
import config

class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str, parking_filename: str) -> None:
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename
        self.accelerometer_filename = accelerometer_filename

    def read(self, accelerometr_file_data, gps_file_data, parking_file_data):
        gps_reader = DictReader(gps_file_data, delimiter=",")
        parking_reader = DictReader(parking_file_data, delimiter=",")
        accelerometer_reader = DictReader(accelerometr_file_data, delimiter=",")

        gps_data = [Gps(float(row["latitude"]), float(row["longitude"])) for row in gps_reader]
        parking_data = [Parking(int(row["empty_count"]), Gps(float(row["latitude"]), float(row["longitude"]))) for row in parking_reader]
        accelerometer_data = [Accelerometer(int(row["x"]), int(row["y"]), int(row["z"])) for row in accelerometer_reader]

        longest_array_len = max(len(accelerometer_data), len(gps_data), len(parking_data))
        correct_items_array = []

        for i in range(longest_array_len):
            accelerometer = accelerometer_data[i] if i < len(accelerometer_data) else Accelerometer(1.0,1.0,1.0)
            gps = gps_data[i] if i < len(gps_data) else Gps(1.0, 1.0)
            parking = parking_data[i] if i < len(parking_data) else Parking(0, Gps(1.0, 1.0))

            correct_items_array.append(AggregatedData(accelerometer, gps, parking, datetime.now(), config.USER_ID))

        return correct_items_array
    
    def startReading(self):
        """Метод повинен викликатись перед початком читання даних"""
        accelometerData = open(self.accelerometer_filename, "r")
        gpsData = open(self.gps_filename, "r")
        parkingData = open(self.parking_filename, "r")
        return accelometerData, gpsData, parkingData

    def stopReading(self, accelerometer, gps, parking):
        """Метод повинен викликатись для закінчення читання даних"""
        accelerometer.close()
        gps.close()
        parking.close()
