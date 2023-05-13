import cv2
import pytesseract
import datetime
import logging
import mysql.connector
import string
import random

logging.basicConfig(level=logging.INFO)

class LicensePlateDetector:
    def __init__(self, image_path, tesseract_config_path):
        self.image_path = image_path
        self.tesseract_config_path = tesseract_config_path
        self.image = None
        self.gray_image = None
        self.canny_edge = None
        self.contours = None
        self.contour_with_license_plate = None
        self.license_plate = None
        self.x = None
        self.y = None
        self.w = None
        self.h = None
        self.date_in = datetime.date.today()
        self.date_out = self.date_in + datetime.timedelta(days=30)

    def read_image(self):
        try:
            self.image = cv2.imread(self.image_path)
        except:
            raise Exception('Failed to read image file')

    def convert_to_gray(self):
        self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Grayscale Image', self.gray_image)
        cv2.waitKey(0)

        

    def canny_edge_detection(self):
        self.canny_edge = cv2.Canny(self.gray_image, 170, 200)
        cv2.imshow('Canny Edge Detection', self.canny_edge)
        cv2.waitKey(0)


    def find_contours(self):
        contours, new = cv2.findContours(self.canny_edge.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        self.contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]
        cv2.drawContours(self.image, self.contours, -1, (0, 255, 0), 2)
        cv2.imshow('License Plate Detection', self.image)
        cv2.waitKey(0)


    def find_license_plate(self):
        for contour in self.contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)
            if len(approx) == 4:
                self.contour_with_license_plate = approx
                self.x, self.y, self.w, self.h = cv2.boundingRect(contour)
                self.license_plate = self.gray_image[self.y:self.y + self.h, self.x:self.x + self.w]
                cv2.imshow('License Plate Detection', self.license_plate)
                cv2.waitKey(0)
                break


    def preprocess_license_plate(self):
        self.license_plate = cv2.bilateralFilter(self.license_plate, 11, 17, 17)
        (thresh, self.license_plate) = cv2.threshold(self.license_plate, 150, 180, cv2.THRESH_BINARY)
        


    def recognize_text(self):
        custom_config = r"--oem 3 --psm 6 -l eng+ara --tessdata-dir 'C:/Program Files/Tesseract-OCR/tessdata'"
        text = pytesseract.image_to_string(self.license_plate, config=custom_config)
        return text.strip()


    def draw_license_plate(self, text):
        self.image = cv2.rectangle(self.image, (self.x, self.y), (self.x + self.w, self.y + self.h), (0, 0, 255), 2)
        cv2.putText(self.image, text, (self.x, self.y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.imshow('License Plate Detection', self.image)
        cv2.waitKey(0)

    def run(self):
        self.read_image()
        self.convert_to_gray()
        self.canny_edge_detection()
        self.find_contours()
        self.find_license_plate()
        self.preprocess_license_plate()
        text = self.recognize_text()
        self.draw_license_plate(text)
        return text


def connect_to_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="smart_park_db"
    )
    return conn
def generate_code():
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
    return code



def check_license_plate(conn, license_plate, date_in, date_out):
    cursor = conn.cursor()
    query = "SELECT * FROM car WHERE plate_number = %s AND date_in <= %s AND date_out >= %s"
    values = (license_plate, date_out, date_in)
    cursor.execute(query, values)
    result = cursor.fetchone()
    if result:
        logging.info("License plate found in database")
    else:
        # ask the user if the car is a daily car
        is_daily_car = input("Welcome! Is this a daily car? (yes/no): ")
        if is_daily_car.lower() == "yes":
            # generate a ticket number
            ticket_number = generate_code()
            name = input("Please enter the name of the driver: ")
            # insert the car information into the daily_cars table
            insert_query = "INSERT INTO daily_cars (ticket_number, name, plate_number, date_in, date_out) VALUES (%s, %s, %s, %s, %s)"
            insert_values = (ticket_number, name, license_plate, date_in, date_out)
            cursor.execute(insert_query, insert_values)
            conn.commit()
            logging.info(f"Car with license plate {license_plate} has been added to the daily cars list. Your ticket number is {ticket_number}.")
        else:
            # insert the car information into the car table
            insert_query = "INSERT INTO car (plate_number, date_in, date_out) VALUES (%s, %s, %s)"
            insert_values = (license_plate, date_in, date_out)
            cursor.execute(insert_query, insert_values)
            conn.commit()
            logging.info(f"Car with license plate {license_plate} has been added to the regular cars list.")

   



def main():
    image_path = './img/tn3.png'
    tesseract_config_path = 'config_file_path'
    
    try:
        detector = LicensePlateDetector(image_path, tesseract_config_path)
        license_plate = detector.run()
    except Exception as e:
        logging.error(f"Error: {e}")
        return

    conn = connect_to_database()
    check_license_plate(conn, license_plate, detector.date_in, detector.date_out)
    conn.close()


if __name__ == '__main__':
    main()