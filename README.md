Parkini
Parkini is a smart parking system that uses license plate recognition to detect cars in a parking lot and check if they have a valid parking ticket. If a car has a valid ticket, it is allowed to park. If not, the driver is prompted to buy a ticket or leave the parking lot.

Dependencies
Before running the Smart Park System, you will need to make sure the following dependencies are installed:

cv2
pytesseract
datetime
logging
mysql.connector
string
random
You will also need to install Tesseract-OCR.exe software on your machine. You can download it from the official website: https://github.com/UB-Mannheim/tesseract/wiki.

Once you have installed Tesseract-OCR.exe, you will need to add it to your system path so that the program can find it.
The system works as follows:

The LicensePlateDetector class is used to detect the license plate in an image. It performs the following steps:
Reads the input image
Converts the image to grayscale
Performs Canny edge detection on the grayscale image
Finds the contours in the edge-detected image
Finds the license plate in the contours
Preprocesses the license plate image
Recognizes the text on the license plate
Draws a bounding box around the license plate and displays the image
If the license plate is detected, the system checks the car's information in the database. It performs the following steps:
Connects to the MySQL database
Checks if the license plate exists in the car table and has a valid parking ticket
If the car is not in the car table, prompts the user to buy a ticket or leave the parking lot
If the car is a daily car, generates a ticket number and inserts the car information into the daily_cars table in the database.
Usage
To use the Parkini system, run the main.py file. The program will prompt you to enter the path of the input image. You can also customize the path to the Tesseract OCR configuration file by modifying the tesseract_config_path parameter in the LicensePlateDetector constructor.

Contributors
This project was developed by @ZakArfaoui / Yassin Moumni / Zied Ktata. Feel free to contribute to this project by submitting pull requests or reporting issues.
