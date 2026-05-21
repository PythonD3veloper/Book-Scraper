# 📚 Book Scraper (Books to Scrape)

A Python web‑scraping project that extracts book data from **Books to Scrape** and saves it into an Excel file.  
The scraper supports configurable settings through `config.json`, optional image downloading, logging, and robust error handling.

---

## 🚀 Features

- Scrapes:
  - Book title  
  - Price  
  - Stock availability  
  - Rating  
  - Image URL (optional)
  - Downloads book cover images (optional)
- Saves results to an Excel file (`.xlsx`)
- Configurable settings via `config.json`
- Logging system with timestamps
- Organized image output folder
- Clean, modular code structure
- Graceful error handling for network issues

---

## 📁 Project Structure

project/
│── scraper.py
│── config.json
│── Book Data.xlsx       (output)
│── logs.txt             (output)
│── Images/              (output)
│── README.md


---

## ⚙️ Configuration (`config.json`)

The scraper reads all settings from `config.json`:

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