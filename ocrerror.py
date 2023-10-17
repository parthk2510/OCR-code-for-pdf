import pdfplumber

# Open the PDF file.
with pdfplumber.open("my_pdf.pdf") as pdf:

  # Get the first page.
  first_page = pdf.pages[0]

  # Extract the text from the page.
  page_text = first_page.extract_text()

  # Find the text "Title:" on the page.
  title_index = page_text.find("Title:")

  # Extract the title of the PDF file.
  title = page_text[title_index + 6:]

  # Print the title of the PDF file to the console.
  print(title)