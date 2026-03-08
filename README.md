# LinkScan

A fast and modern web-based tool to scan any webpage for broken links and images. LinkScan provides a detailed report, a health score, and filtering options in a clean, responsive interface with both light and dark themes.

![LinkScan Screenshot](https://raw.githubusercontent.com/JaivPatel07/LINK-CHECKER/main/screenshot.png)

## Features

- **Comprehensive Scanning**: Checks all `<a>` (links) and `<img>` (images) tags on a given URL.
- **Detailed Reports**: Shows status codes (e.g., 200, 404), status labels (OK, Broken), and response times for each resource.
- **Health Score**: Calculates an overall site health percentage based on the number of working links.
- **Image Auditing**: Provides a separate breakdown for total, working, and broken images.
- **Interactive UI**:
    - Separate tabs for Links and Images.
    - Filter results by status: All, Working, or Broken.
- **Export to CSV**: Download the list of links or images as a CSV file for further analysis.
- **Modern Theming**: Includes a sleek, professional UI with a user-selectable light or dark theme that respects system preference.
- **Responsive Design**: Works great on both desktop and mobile devices.

## 🛠️ Tech Stack

- **Backend**: **Python** with **Flask**, using `requests` for HTTP calls and `BeautifulSoup4` for HTML parsing.
- **Frontend**: Vanilla **HTML**, **CSS**, and **JavaScript** (no frameworks).
- **Fonts**: Inter and DM Mono from Google Fonts.

## 🚀 Getting Started

Follow these instructions to get a local copy up and running.

### Prerequisites

- Python 3.x
- `pip` for package management

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/JaivPatel07/LINK-CHECKER.git
    cd LINK-CHECKER
    ```

2.  **Set up the Python backend:**
    - Create and activate a virtual environment:
      ```sh
      # For Windows
      python -m venv venv
      .\venv\Scripts\activate

      # For macOS/Linux
      python3 -m venv venv
      source venv/bin/activate
      ```
    - Install the required packages from `requirements.txt`:
      ```sh
      pip install -r requirements.txt
      ```
      *(If `requirements.txt` does not exist, create it with `Flask`, `Flask-Cors`, `requests`, and `beautifulsoup4`)*

### Running the Application

1.  **Start the Flask API:**
    Run the `api.py` file to start the backend server. It will run on `http://localhost:5000`.
    ```sh
    python api.py
    ```

2.  **Launch the Frontend:**
    Open the `index.html` file directly in your web browser.

3.  **Scan a URL:**
    Enter a URL in the input field (e.g., `google.com`) and click "Scan".

## API Endpoint

The application uses a single API endpoint to perform the scan.

- **URL**: `http://localhost:5000/check`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Request Body**:
  ```json
  {
    "url": "https://example.com"
  }
  ```
