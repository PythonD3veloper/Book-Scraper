# 📚 Book Scraper (Books to Scrape)

A Python web‑scraping project that extracts book data from **Books to Scrape** and saves it into an Excel file.  
The scraper supports configurable settings through `config.json`, optional image URL extraction, and basic error handling.

---

## 🚀 Features

- Scrapes:
  - Book title  
  - Price  
  - Stock availability  
  - Rating  
  - Image URL (optional)
  - Download Images (optional)
- Saves results to an Excel file (`.xlsx`)
- Configurable settings via `config.json`
- Graceful error handling for network issues
- Clean, modular code structure

---

## 📁 Project Structure

project/
│── scraper.py
│── config.json
│── Book Data.xlsx   (output)
│── logs.txt   (output)
│── Images/   (output)
│── README.md

---

## ⚙️ Configuration (`config.json`)

The scraper reads settings from `config.json`:

```json
{
    "excel_output_name": "Book Data.xlsx",
    "pages_to_scrape": 5,
    "save_images": true,
    "logs_enabled": true,
    "log_file_name": "logs.txt",
    "download_images": true,
    "images_folder": "Images"
}

---

## 🥇 Requirements (Running Script)

Run the following command to download the requirements for the script.

"pip install -r requirements.txt"

And finally, to run the python script do the following

"python main.py"

If your still stuck, you may need to install python to run the script