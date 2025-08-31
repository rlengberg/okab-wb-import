  # A python tool born out of convenience  
  **Created by Robert Lengberg to process OKAB waybills for externally converted products.**<br/>

  It will currently NOT handle scanned waybills (a.k.a OCR read)<br/>
  OKAB can supply us with PDF files directly from their system<br/>
  and this tool relies on them doing that.<br/>

  Verify that the OKAB waybill is correct before relying on this tool<br/>
  Verify the results of the CSV file before importing it in MEXIEC<br/>

### Setup guide:
>  1. Put the executable in its own folder on your PC<br/>
>  2. Create a directory named "pdf"<br/>
>  3. Create a directory named "csv"<br/>
>  4. Remove old PDF files (the app will process all files in "pdf" folder)<br/>
>  5. Place the PDF files you want to process in "pdf" folder.<br/>
>   6. Run the executable, results will be output to "csv" folder.<br/>

### Folder structure (top folder can be named anything)
- OKAB Waybill Extractor
  - /pdf
  - /csv
  - process_okab_waybills.exe

 ### Stand-alone Executable
> Install pyInstaller with pip in your virtual environment
> run pyinstaller "./process_okab_waybills.py" -F
