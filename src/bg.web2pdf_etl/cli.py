from . import pdf_etl as etl
from . import pdf_scraper as scraper
from . import pathing

def main():
    print("initializing file path check/creation")
    pathing.main()
    print("pathing check/creation finished")
    print("initializing scraper")
    scraper.main()
    print("scraper finished")
    print("initializing etl system")
    etl.main()
    print("etl system finished")

    if __name__ == "__main__":
        main()