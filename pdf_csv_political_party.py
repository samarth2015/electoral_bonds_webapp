import PyPDF2
import csv

# Path to the PDF file
pdf_path = "E:\\Assignment 4\\political_party.pdf"

# Output CSV file path
csv_path = "E:\\Assignment 4\\political_party.csv"

# Open the PDF file
with open(pdf_path, 'rb') as pdf_file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Create a CSV file and write the lines as rows
    with open(csv_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Iterate over each page of the PDF
        for page in pdf_reader.pages:
            # Extract the text from the page
            page_text = page.extract_text()

            # Split the text into lines
            lines = page_text.split('\n')
            # print(lines)
            lines = lines[5:-1]

            # Write each line as a row in the CSV file
            for line in lines:
                row = line.split(' ')
                row = row[:2] + [' '.join(row[2:-6])] + row[-6:]
                csv_writer.writerow(row)  # Adjust the delimiter as per your PDF format

