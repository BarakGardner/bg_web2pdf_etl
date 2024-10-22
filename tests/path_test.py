import pathlib

dir = pathlib.Path('~/web2pdf_output')
home_dir = dir.expanduser()
if not home_dir.exists():
    home_dir.mkdir(exist_ok=True)

print(home_dir)