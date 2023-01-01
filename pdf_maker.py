import os
import shutil
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger

import excel_merge as em
import excel2PDF as e2p
import img2PDF as i2p


def mergePdf(inFileList, outFile):
    '''
    合并文档
    :param inFileList: 要合并的文档的 list
    :param outFile:    合并后的输出文件
    :return:
    '''
    pdfFileWriter = PdfFileWriter()
    for inFile in inFileList:
        # 依次循环打开要合并文件
        pdfReader = PdfFileReader(open(inFile, 'rb'))
        numPages = pdfReader.getNumPages()
        for index in range(0, numPages):
            pageObj = pdfReader.getPage(index)
            pdfFileWriter.addPage(pageObj)

        # 最后,统一写入到输出文件中
        pdfFileWriter.write(open(outFile, 'wb'))


def main():
    tmp_path = './tmp'
    if not os.path.isdir(tmp_path):
        os.mkdir(tmp_path)

    em.func()
    e2p.func()
    i2p.func()

    writer = PdfFileWriter()
    excels = PdfFileReader("tmp/tmp.pdf")
    imgs = PdfFileReader("tmp/imgs.pdf")
    excelsPages = excels.getNumPages()
    imgsPages = imgs.getNumPages()
    numPages = min(excelsPages, imgsPages)
    for index in range(numPages):
        page = excels.getPage(index)
        writer.addPage(page)
        page = imgs.getPage(index)
        writer.addPage(page)

    writer.write(open("output.pdf", 'wb'))
    shutil.rmtree('./tmp')


if __name__ == '__main__':
    main()
