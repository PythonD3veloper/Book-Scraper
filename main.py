from bs4 import BeautifulSoup
from requests import get
from openpyxl import Workbook

from json import load
from pathlib import Path
from datetime import datetime

class Logger:
    log_file_name = None

    def __init__(self, log_file_name):
        self.log_file_name = Path(log_file_name)

        self.log_file_name.touch(exist_ok=True)
    
    def write_to(self, message):
        with self.log_file_name.open("a") as file:
            now = datetime.now()

            formatted = now.strftime("%m/%d/%y %I:%M:%S %p")

            file.write(f"[{formatted}] {message}\n")

def set_dimensions(ws):
    ws.column_dimensions["A"].width = 83
    ws.column_dimensions["E"].width = 78

def init(ws, save_images):
    try:
        if save_images:
            ws.append(["Title", "Price", "In Stock", "Rating", "Image URL"])
        else:
            ws.append(["Title", "Price", "In Stock", "Rating"])
    except Exception as e:
        print(f"Failed to append to excel file: {e}")

def download_image(logger, url, image_name, image_folder):
    folder = Path(image_folder)
    folder.mkdir(exist_ok=True)

    safe_name = "".join(c for c in image_name if c.isalnum() or c in (" ", "_", "-"))
    file_name = folder / f"{safe_name}.jpg"

    logger.write_to(f"Downloading {file_name}...")

    try:
        response = get(url, timeout=10)
        response.raise_for_status()
        
        with file_name.open("wb") as file:
            file.write(response.content)
        
        logger.write_to("Downloaded!")
    except Exception as e:
        print(f"Failed to get response: {e}")


def scrape(logger, ws, pages_to_scrape, save_images, download_images, image_folder):
    if download_images:
        logger.write_to(f"Downloading images to {image_folder}")

    for i in range(1, pages_to_scrape + 1):
        url = f"https://books.toscrape.com/catalogue/page-{i}.html"

        logger.write_to(f"Scraping URL: {url}")

        try:
            response = get(url, timeout=10)
            response.raise_for_status()
            html = response.text

        except Exception as e:
            print(f"Failed to get website {url}: {e}")
            logger.write_to(f"Failed to get website {url}: {e}")
            continue

        soup = BeautifulSoup(html, "html.parser")

        books = soup.find_all("article", class_="product_pod")

        for book in books:
            book_title = book.find("h3").find("a")["title"]

            price_container = book.find("div", "product_price")

            price = price_container.find("p", "price_color").get_text()

            price = price[2:]

            in_stock = "in stock" in price_container.find("p", class_="instock availability").get_text(strip=True).lower()
    
            ratings_tag = book.find("p", class_="star-rating")
            ratings = ratings_tag["class"][1]

            if save_images:
                img_tag = book.find("img")
                img_src = img_tag["src"]

                img_url = "https://books.toscrape.com/" + img_src.replace("../", "")

                if download_images:
                    download_image(logger, img_url, book_title, image_folder)

                ws.append([book_title, price, in_stock, ratings, img_url])
            else:
                ws.append([book_title, price, in_stock, ratings])

# This is the main function, handles
def main():
    excel_title = None
    pages_to_scrape = None
    save_images = None
    logs_enabled = None
    log_file_name = None
    download_images = None
    images_folder = None

    with open("config.json", 'r') as file:
        data = load(file)
        excel_title = data["excel_output_name"]
        pages_to_scrape = data["pages_to_scrape"]
        save_images = data["save_images"]
        logs_enabled = data["logs_enabled"]
        log_file_name = Logger(data["log_file_name"])
        download_images = data["download_images"]
        images_folder = data["images_folder"]

    wb = Workbook()
    ws = wb.active

    ws.title = "Book Data"
    if logs_enabled:
        log_file_name.write_to("Created excel sheet with title 'Book Data'")

    set_dimensions(ws)
    init(ws, save_images)
    if logs_enabled:
        log_file_name.write_to("Initialised")

    scrape(log_file_name, ws, pages_to_scrape, save_images, download_images, images_folder)

    log_file_name.write_to("Saving excel file")

    try:
        wb.save(excel_title)
    except Exception as e:
        print(f"Failed to save to excel file: {e}")
        log_file_name.write_to(f"Failed to save to excel file: {e}")

if __name__ == "__main__":
    main()