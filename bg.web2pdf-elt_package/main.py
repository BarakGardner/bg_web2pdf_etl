import pdf_etl as etl
import pdf_scraper as scraper

if __name__ == "__main__":
    print("initializing scraper")
    scraper.main()
    print("scraper finished")
    print("initializing etl system")
    etl.main()
    print("etl system finished")