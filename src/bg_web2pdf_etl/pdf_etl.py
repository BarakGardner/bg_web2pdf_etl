# imports
import pymupdf # used to convert pdf to text so python can read the data
from pathlib import Path # used to find the path of the files needed
import json # used to write data to json file when parsing and calculations are complete
import logging # used to create log file, and send logs to it for future viewing and use
from pathing import output



paths = [] # file paths are saved here
data_list = []
# sets up the file paths by searching the root provided for the pdf's, saves their paths to a list
root = output.pdf_dir # the root path for Path() to search
for path in Path(root).glob("**/*.pdf"): # for loop using Path().glob to search for pdf's only in set root
    paths.append(path) # saving filepaths to list

# takes filepath, opens pdf, gets all text from pdf, cleans it, parses the wanted data and saves that to dict, takes some data and does necessary calculations and saves results to dict.
class GetFileData():
    def __init__(self,path): # taking file path on initialization
        self.path = path # setting self.path as document input
        self.filedate = Path(self.path).stem.lstrip("Statistical_Report_Beer_") # file date saved here (date only no file identifier included)
        self.infile = pymupdf.open(self.path) # using pymupdf to open the file
        self.cleaned_text = [] # used to save cleaned text
        # used to save finished data, has a key for each piece I need, value will be populated as data is found or calculated
        self.data = {
            "Name": self.filedate,
            "Period": None,
            "Date": None,
            "CMProd": None,
            "PYCMProd": None,
            "CYCTDProd": None,
            "PYCTDProd": None,
            "PYCMEoMStock": None,
            "CMEoMStock": None,
            "CMSales": None,
            "PYCMSales": None,
            "YearProdDif": None
            }

    # extracts the table's as text from the pdf, creating a list of lists. with each list inside the main list being an extracted table from the pdf
    def get_text(self):
        page = self.infile[0]
        findtables = page.find_tables()
        self.tables = findtables[0].extract()

    # cleans table's to make data more readable and takes first table out so I can extract data needed from it   
    def clean_text(self):
        self.date = self.tables[0].pop(0).split('\n')
        for table in self.tables:
            for i in table:
                if i is not None:
                    self.cleaned_text.append(i.replace('\n', ' '))
            

    # takes cleaned text and parses the data from it that we need
    def get_data(self):
        try:
            # logging the start of data extraction
            logging.info(f"Data extraction has started for filedate: {self.filedate}")

            # validating self.date list is not empty
            if not isinstance(self.date, list) or len(self.date) == 0:
                logging.warning(f"Malformed 'date' data: Expected non-empty list, got {self.date}")
                return
            
            # validating self.cleaned_text is not empty
            if not isinstance(self.cleaned_text, list) or len(self.cleaned_text) == 0:
                logging.warning(f"Malformed 'cleaned text' data: Expected non-empty list, got {self.cleaned_text}")
                return
            
            found_report_date = False
            for i in self.date: # uses for loop to search for reporting period and report date, then saves it to the data dict
                if "Reporting Period" in i:
                    logging.debug(f"Found 'Reporting Period': {i}")
                    self.data["Period"] = i
                if "Report Date" in i:
                    logging.debug(f"Found 'Report Date': {i}")
                    self.data["Date"] = i
                    found_report_date = True
                    break

            if not found_report_date:
                logging.warning(f"Report Dates not found in 'self.date' list: {self.date}")

            found_production = False
            found_stocks = False

            # uses for loop to check index item is in the right place, if yes then it takes the data we want and saves it to the data dict
            for index, item in enumerate(self.cleaned_text):
                logging.debug(f"Processing index {index}: {item}")
                # checks index for production numbers
                if index == 8 and "Production" in item:
                    try:
                        self.data["CMProd"] = self.cleaned_text[9]
                        self.data["PYCMProd"] = self.cleaned_text[10]
                        self.data["CYCTDProd"] = self.cleaned_text[11]
                        self.data["PYCTDProd"] = self.cleaned_text[12]
                        logging.debug(f"Succcessfully extracted production data below index 8")
                        found_production = True
                    except IndexError as e:
                        logging.error(f"Malformed 'cleaned text': Production data incomplete below index 8 for filedate: {self.filedate}")
                        return
                    

                # checks index for end of month on hand in revised files
                if index == 70 and "S t o c k s On Hand End-of-Month" in item:
                    try:
                        self.data["CMEoMStock"] = self.cleaned_text[71]
                        self.data["PYCMEoMStock"] = self.cleaned_text[72]
                        logging.debug(f"Successfully extracted stock data below index 70")
                        found_stocks = True
                        break
                    except IndexError as e:
                        logging.error(f"Malformed 'cleaned text': Stock data incomplete below index 70 for filedate: {self.filedate}")
                        return
                    

                # checks index for end of month on hand in normal files
                if index == 75 and "S t o c k s On Hand End-of-Month" in item:
                    try:
                        self.data["CMEoMStock"] = self.cleaned_text[76]
                        self.data["PYCMEoMStock"] = self.cleaned_text[77]
                        logging.debug(f"Successfully extracted stock data below index 75")
                        found_stocks = True
                        break
                    except IndexError as e:
                        logging.error(f"Malformed 'cleaned text': Stock data incomplete below index 75 for filedate: {self.filedate}")
                        return
                    
                    
            if not found_production:
                logging.warning(f"Production data not found at expected index (8) in 'cleaned text' for filedate: {self.filedate}")

            if not found_stocks:
                logging.warning(f"Stock data not found at expected index (75 or 70) in 'cleaned text' for filedate: {self.filedate}")

            logging.info(f"Data extraction successfull for filedate: {self.filedate}")

        except Exception as e:
            logging.exception(f"An error occurred during data extraction for filedate: {self.filedate}")
 

    # takes necessary data from dict, removes the commas, converts to dict, subtracts, then formats back to readable str and assigns to dict
    def calculate_and_save(self):
        self.data["CMSales"] = format(int(self.data["CMProd"].replace(',','')) - int(self.data["CMEoMStock"].replace(',','')),',d')
        self.data["PYCMSales"] = format(int(self.data["PYCMProd"].replace(',','')) - int(self.data["PYCMEoMStock"].replace(',','')),',d')
        self.data["YearProdDif"] = format(int(self.data["CYCTDProd"].replace(',','')) - int(self.data["PYCTDProd"].replace(',','')),',d')
        data_list.append(self.data)

    # takes data_list and saves it to json file that uses


def main():
    logging.basicConfig(level=logging.DEBUG, filename=f"{output.log_dir}/pdf_etl.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")
    for p in paths:
        call = GetFileData(p)
        call.get_text()
        call.clean_text()
        call.get_data()
        call.calculate_and_save()
    prefered_path = output.report_dir
    with open(f'{prefered_path}/ttb_stats.json', 'w') as datadump:
        json.dump(data_list, datadump, indent=1)

if __name__ == "__main__":
    main()

        