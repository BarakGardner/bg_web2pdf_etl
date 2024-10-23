import pdf_etl as etl
import pdf_scraper as scraper
import pathing

if __name__ == "__main__":
    print("initializing file path check/creation")
    pathing.main()
    print("pathing check/creation finished")
    print("initializing scraper")
    scraper.main()
    print("scraper finished")
    print("initializing etl system")
    etl.main()
    print("etl system finished")