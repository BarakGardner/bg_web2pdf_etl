import pathlib

class OutputDir():
    def __init__(self):
        self.main_dir = pathlib.Path("~/Desktop/web2pdf-etl_output's")
        self.full_dir = self.main_dir.expanduser()
        self.pdf_dir = pathlib.Path(f"{self.full_dir}/PDFs")
        self.report_dir = pathlib.Path(f"{self.full_dir}/Reports")
        self.html_dir = pathlib.Path(f"{self.full_dir}/html")
        self.log_dir = pathlib.Path(f"{self.full_dir}/logs")


    def check_pathing(self):
        if not self.full_dir.exists():
            self.full_dir.mkdir(exist_ok=True)
        else:
            print(f"{self.full_dir} Already exists, continuing on to next check")

        if not self.pdf_dir.exists():
            self.pdf_dir.mkdir(exist_ok=True)
        else:
            print(f"{self.pdf_dir} Already exists, continuing on to next check")

        if not self.report_dir.exists():
            self.report_dir.mkdir(exist_ok=True)
        else:
            print(f"{self.report_dir} Already exists, continuing on to next check")

        if not self.html_dir.exists():
            self.html_dir.mkdir(exist_ok=True)
        else:
            print(f"{self.html_dir} Already exists, continuing on to next check")

        if not self.log_dir.exists():
            self.log_dir.mkdir(exist_ok=True)
        else:
            print(f"{self.log_dir} Already exists, all directories accounted for.")


output = OutputDir()

def main():
    output.check_pathing()

if __name__ == "__main__":
    main()