# Learning Progress Tracker

The **Learning Progress Tracker** is a Python-based desktop application built using **Tkinter** and **Pandas**. It helps track users' learning progress over time, allowing them to log their learning hours, application hours, and certificates earned. The program calculates points based on various factors and provides real-time feedback through a progress bar, summarizing the user's performance each week.

---

## Features

- **User-Friendly Interface**: A GUI built with **Tkinter** to easily track learning progress.
- **Points Calculation**: Calculates learning points, application points, certificate points, and total evaluation points.
- **Progress Feedback**: Visual progress bar that updates as users log their data.
- **Bonus System**: Users can earn bonus points that affect their learning points in the following weeks.
- **Excel Data Integration**: Uses **Pandas** to read and write data to an Excel file, storing user data such as weekly progress.
- **Data Validation**: Checks for duplicate entries and ensures the integrity of the data entered by the user.
- **Performance Feedback**: Displays a message with performance feedback ("Excellent", "Good", etc.) based on total evaluation points.

---

## Installation

### Prerequisites

Make sure you have the following installed on your system:

- **Python 3.x**: The project runs on Python 3.
- **Tkinter**: The GUI toolkit used in the project. It’s typically included with Python by default.
- **Pandas**: Used for handling Excel file operations and storing data.
- **openpyxl**: For handling Excel file read/write operations.

To install the required Python packages, run:

```bash
pip install pandas openpyxl

```

## Running the Application
1. Clone or download the repository to your local machine:
   ```bash
   git clone https://github.com/Cinioluwa/tracker.git
   ```
2. Navigate to the project folder:
   ```bash
   cd tracker
   ```
3. Run the script:
   ```bash
   python tracker.py
   ```

The applicaiton window will appear, where you can enter your data for each week, calculate points, and view your progress.

## Usage
**Enter User Data**: Input your username, week number, learning hours, application hours, and number of certificates.
**Calculate Points**: Click on the "Calculate" button to calculate points for the given week.
**View History**: View historical progress for each user by clicking on "View History".
**Progress Bar**: The progress bar updates based on the total evaluation points you have accumulated.

## Technologies Used
**Python**: Programming language used for the application.
**Tkinter**: Used for creating the graphical user interface.
**Pandas**: Handles Excel file operations and data processing.
**openpyxl**: Library used by Pandas for reading and writing Excel files.
**Excel**: Stores and loads user data in an Excel file for persistence.
