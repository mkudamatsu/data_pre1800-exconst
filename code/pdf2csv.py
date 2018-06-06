print "Setting the working directory"
import os
work_dir = os.path.dirname(os.path.realpath(__file__)) # This method returns the directry path of this script.
os.chdir(work_dir)

if not os.path.isdir("../temp/"): # Create the temporary file directory if it doesn't exist
    os.makedirs("../temp/")

print "Import PDFMiner.six modules"                         # Comment source: https://gist.github.com/vinovator/c78c2cb63d62fdd9fb67
from pdfminer.pdfparser import PDFParser                    # fetches data from pdf file
from pdfminer.pdfdocument import PDFDocument                # stores data parsed by PDFParser
from pdfminer.pdfinterp import PDFPageInterpreter           # processes page contents from PDFDocument
from pdfminer.pdfdevice import PDFDevice                    # translates processed information from PDFPageInterpreter to whatever you need
from pdfminer.pdfinterp import PDFResourceManager           # stores shared resources such as fonts or images used by both PDFPageInterpreter and PDFDevice
from pdfminer.pdfpage import PDFPage                        # make the PDF document into the list of pages
from pdfminer.pdfpage import PDFTextExtractionNotAllowed    # raise exception whenever text extraction from PDF is not allowed

from pdfminer.layout import LAParams                        # analyze the layout and return a LTPage object for each page in the PDF document
from pdfminer.layout import LTTextBox                       # extract text from text boxes
from pdfminer.layout import LTTextLine                      # extract text from text lines
from pdfminer.converter import PDFPageAggregator            # Extract the decive to page aggregator to get LT object elements

### Define the main function ###
def main():
    try:
        print "Set inputs..."
        in_pdf = "../orig/w9378.pdf"
        password = ""               # Insert the password if the PDF file is locked

        print "Open the PDF"
        with open(in_pdf, "rb") as fp:
            print "Transfer information (i.e. parse) from PDF file to PDF document object"
            parser = PDFParser(fp)
            print "Store the parsed information"
            document = PDFDocument(parser, password)
            print  "Check if the document allows text extraction. If not, abort."
            if not document.is_extractable:
                raise PDFTextExtractionNotAllowed
            print "Create PDFResourceManager object that stores shared resources such as fonts or images"
            rsrcmgr = PDFResourceManager()
            print "Set parameters for layout analysis"
            laparams = LAParams()
            print "Create a PDF device object"
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            print "Create a PDF interpreter object"
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            print "We have everythiing to process a PDF file."
            print "Create an empty Python list to which we store extracted texts"
            text_content = []
            print "Start the loop over pages"
            for page in PDFPage.create_pages(document):
                print "...processing a PDF page"
                interpreter.process_page(page)
                print "...rendering the layout"
                layout = device.get_result()
                print "...extracting texts as a Python list"
                print "...starting the loop over LT* objects"
                for lt_obj in layout:
                    print "...checking if it's a line of text or a text box"
                    if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                        print lt_obj.get_text()
                        print "...saving texts if so"
                        text_content.append(lt_obj.get_text())
                text_content.append('\n') # So each line corresponds to each page

        print "Set outputs..."
        out_csv = "../temp/test.csv"
        print "Writing out texts in the output file"
        with open(out_csv, "w") as csv:
            print "Looping over list items"
            for entries in text_content:
                print "Writing extractec texts"
                # csv.write(entries)
                csv.write(entries.encode("utf-8"))
        print "Done."

    # Return any other type of error
    except:
        print "There is an error."

### Define the subfunctions ###
def download_data(filename, indir, outdir):
    print "...launching urllib"
    import urllib
    print "...downloading data"
    urllib.urlretrieve(indir + filename, outdir + filename)

### Execute the main function ###
if __name__ == "__main__":
    main()
