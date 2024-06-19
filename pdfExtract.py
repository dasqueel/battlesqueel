import PyPDF2

def extract_pages(input_pdf_path, output_pdf_path, start_page, end_page):
    """
    Extract multiple consecutive pages from a PDF file and save them as a new PDF file.

    :param input_pdf_path: Path to the input PDF file.
    :param output_pdf_path: Path to the output PDF file where the pages will be saved.
    :param start_page: The starting page number to extract (0-based index).
    :param end_page: The ending page number to extract (0-based index).
    """
    try:
        # Open the input PDF file
        with open(input_pdf_path, 'rb') as input_pdf:
            reader = PyPDF2.PdfReader(input_pdf)
            num_pages = len(reader.pages)
            if start_page < 0 or end_page >= num_pages or start_page > end_page:
                raise ValueError(f"Invalid page range. The document has {num_pages} pages.")

            # Create a PdfWriter object to hold the pages
            writer = PyPDF2.PdfWriter()

            # Add the specified pages to the writer object
            for page_number in range(start_page, end_page + 1):
                writer.add_page(reader.pages[page_number])

            # Write the pages to the output PDF file
            with open(output_pdf_path, 'wb') as output_pdf:
                writer.write(output_pdf)

        print(f"Pages {start_page + 1} to {end_page + 1} extracted and saved as {output_pdf_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")

teamAbbr = "nmst"
end_page = 330
start_page = end_page - 1
input_pdf_path = r'/mnt/c/Users/neilb/Downloads/2024 Phil Steele Digital Magazine.pdf'
output_pdf_path = f'./steele/{teamAbbr}.pdf'

extract_pages(input_pdf_path, output_pdf_path, start_page, end_page)
