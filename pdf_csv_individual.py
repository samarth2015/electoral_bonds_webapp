# import fitz
# import csv

# # Path to the PDF file
# pdf_path = "E:\\Assignment 4\\individual.pdf"

# # Output CSV file path
# csv_path = "E:\\Assignment 4\\individual2.csv"

# # Open the PDF file
# with fitz.open(pdf_path) as pdf_file:
#     # Create a CSV file and write the lines as rows
#     with open(csv_path, 'w', newline='') as csv_file:
#         csv_writer = csv.writer(csv_file)

#         # Iterate over each page of the PDF
#         for page in pdf_file:
#             # Extract the text from the page
#             page_text = page.get_text()

#             # Split the text into lines
#             lines = page_text.split('\n')
#             print(lines)
#             lines = lines[3:-1]

#             # Write each line as a row in the CSV file
#             for line in lines:
#                 row = line.split(',')
#                 # row = row[:5] + [' '.join(row[5:-6])] + row[-6:]
#                 csv_writer.writerow(row)  # Adjust the delimiter as per your PDF format
import fitz
import csv

def pdf_to_csv(input_file, output_file):
    writer = csv.writer(open(output_file, 'w', newline=''))
    doc = fitz.open(input_file)
    i= 0
    for page in doc:
        tabs = page.find_tables()
        if tabs.tables:
            writer.writerows(tabs[0].extract())
            print("Page ", i, " done")
            i += 1


pdf_to_csv("E:\Assignment 4\individual.pdf", "E:\Assignment 4\individual.csv")
pdf_to_csv("E:\Assignment 4\political_party.pdf", "E:\Assignment 4\political_party.csv")


        
        