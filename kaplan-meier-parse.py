import csv
import xlrd

def cleanCell(cell):
    cleaned = (str(cell).split(':')[-1])
    cleaned = cleaned.replace("'", "").replace('"', "")
    return cleaned

def parse_to_csv(path):
    # what sheet is the data on
    dataSheetIndex = 0

    # what row do the data set headers start in the file
    dataHeaderRowOffset = 1

    # what column does the data start on
    firstDataHeaderColumnOffset = 1

    # how many columns are between te data sets
    # determined below by taking number of empty cells between data set headers
    dataSetColumnOffset = 0

    # what row does the line headers in the data set start on
    lineHeaderRowOffset = 2

    # how many line headers (columns of data) are there
    numLineHeaders = 3

    # what row do data entries start on
    startDataEntryRow = 3

    # open excel file and get how many csv files we need to make
    book = xlrd.open_workbook(path)

    first_sheet = book.sheet_by_index(dataSheetIndex)

    numRows = first_sheet.nrows

    dataHeaderRow = first_sheet.row_values(dataHeaderRowOffset)

    numFiles = 0

    # if cell is not empty, increment number of files. 
    # else, increase column space offset between data sets
    for r in dataHeaderRow:
        if (r != ''): 
            numFiles += 1
        else:
            dataSetColumnOffset += 1

    # the data set column offset will also count empty columns at the end, 
    # but this shouldn't count toward the offset, as these columns are data entry columns
    # and the data set header is only in the first column
    # so subtract number of line headers minus 1
    dataSetColumnOffset -= numLineHeaders - 1

    for index in range(numFiles):
        # perpare each csv file for writing
        filename = 'test' + str(index) + '.csv'

        ofile = open(filename, 'w+', newline='')

        # get the row headers
        rowX = lineHeaderRowOffset
        start_colX = firstDataHeaderColumnOffset + (index*dataSetColumnOffset)
        end_colX = start_colX + numLineHeaders

        cells = first_sheet.row_slice(rowx = rowX,
                              start_colx = start_colX,
                              end_colx = end_colX)

        headerCells = [cleanCell(x) for x in cells]

        # get rows of data
        dataRows = []

        for rownum in range(startDataEntryRow, numRows):
            cells = first_sheet.row_slice(rowx = rownum,
                                 start_colx = start_colX,
                                 end_colx = end_colX)

            dataRows.append([cleanCell(x) for x in cells])

        try:
            writer = csv.writer(ofile)

            writer.writerow(headerCells)

            for row in dataRows:
                # don't write empty row
                if row[0]:
                    writer.writerow(row)

        finally:
            ofile.close()


if __name__ == "__main__":
    path = "Survival plot data.xlsx"
    parse_to_csv(path)