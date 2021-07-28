
import os.path
import comtypes.client

wdFormatPDF = 17  # значение, соответствующее тому формату, который нужен на выходе

input_dir = 'input directory'
output_dir = 'output directory'

for subdir, dirs, files in os.walk(input_dir):
    for file in files:
        in_file = os.path.join(subdir, file)
        output_file = file.split('.')[0]
        out_file = output_dir+output_file+'.pdf'
        word = comtypes.client.CreateObject('Word.Application')

        doc = word.Documents.Open(in_file)
        doc.SaveAs(out_file, FileFormat=wdFormatPDF)
        doc.Close()
        word.Quit()

