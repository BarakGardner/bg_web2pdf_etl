"""
The Problem,

A python script that can download the PDF's for each month/year from the ttb.gov website.

Be nice to this website and limit your script to only 5 pdf's until it's working.

Use the disk to cache the pages and pdf's so you aren't hammering the website.
This also helps you work quicker since you aren't waiting for the internet.

Once you're able to reliable get all the PDF's, you should integrate
your statistics extraction from the previous exercise to produce full statistics.

It might be time to officially create a project and write automated tests for your code.
The next exercise will require you to wrewrite some of this, so having tests will make this quicker and easier.

To accomplis this problem you'll need some basics:

1. How to download a URL.
2. Saving it to disk so you don't have to rely on the network while you work.
3. Loading it with BeautifulSoup library.
4. How to use "with".
"""

#imports here
import requests
from bs4 import BeautifulSoup
import os

class GetPDFs():
    def __init__(self):
        self.ttb_url = 'https://learncodethehardway.com/setup/python/ttb/' # url for requests to open
        self.path = '/home/barak/lpthw/ex/ex52/ttb_page.html' # path and filename to save webpage to

    def scrape(self):
        if not os.path.exists('ttb_stats.json'): # checking for ttb_stats.json
            with open(self.path, 'w') as f: # using with to open/create file in write mode as f
                resp = requests.get(self.ttb_url) # using requests lib to access the url
                body = resp.text # variable set as output of the webpage code
                soup = BeautifulSoup(body, 'html5lib') # takes body (aka webpage html code) and uses html5lib parser on it
                f.write(soup.prettify()) # writing that code to html file using bs4 prettify to make it more readable (as this particular webpage is a oneliner so prettify formats it so it looks more normal)

        else: 
            with open(self.path) as f: # using with to open file
                body = f.read() # reading html file
                soup = BeautifulSoup(body, 'html5lib') # takes body (aka the written html file of the website code) and uses html5lib parser to read it

        for base in soup.find_all('a'): # loop over find_all results
            link = base.get('href') # get href items
            if link.endswith('.pdf'): # checks if href item endswith '.pdf'
                file_link = link[18:] # slices first part of link off (it isn't needed and if it is left there it will throw errors)
                file_name = link[47:] # slices last part of link off to be used as the filename when downloading
                if not os.path.exists(f'/home/barak/lpthw/ex/ex52/PDFs/{file_name}'):
                    pdf_url = self.ttb_url + file_link # combines the website link with the pdf link so it can be called
                    pdf_response = requests.get(pdf_url) # calling pdf url to get the pdf data from the webpage

                    if pdf_response.status_code == 200: # checks if the response code is good (200 == ok)
                        with open(f'/home/barak/lpthw/ex/ex52/PDFs/{file_name}', 'wb') as f: # uses with to create and open the file in the correct directory, using file name to make the name of the file. file is opened in write, binary mode as f
                            f.write(pdf_response.content) # writing response content to opened file
                        print('PDF downloaded successfully.') # letting the user know file was downloaded successfully
                    else: # this will run if above if statement returns false
                        print('Error:', pdf_response.status_code) # prints the request.get status code to let the user know why the above code didn't run
                else:
                    print('File already exists, continuing to next file')

def main():
    get_pdfs = GetPDFs()
    get_pdfs.scrape()

if __name__ == "__main__":
    main()