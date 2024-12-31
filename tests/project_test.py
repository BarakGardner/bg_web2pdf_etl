from pathlib import Path
import datetime

pdf_path = Path("/home/barak/Desktop/web2pdf-etl_output's/PDFs")
print(pdf_path)

for file in pdf_path.iterdir():
    metadata = file.stat().st_ctime
    c_time = datetime.datetime.fromtimestamp(metadata)
    print(metadata)
    print(c_time)