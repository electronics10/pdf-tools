from pypdf import PdfReader, PdfWriter

reader = PdfReader("textbook.pdf")
writer = PdfWriter()

start_page = 903
end_page = 905
for page in reader.pages[start_page-1:end_page]:
    writer.add_page(page)

with open("splitted.pdf", "wb") as f:
    writer.write(f)
