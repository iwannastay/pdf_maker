import os

import xlrd  # 读取Excel文件的包
import xlsxwriter  # 将文件写入Excel的包

handle_postfix = ['xlsx', 'xls']


# 打开一个excel文件
def open_xls(file):
    f = xlrd.open_workbook(file)
    return f


# 获取excel中所有的sheet表
def get_sheet(f):
    return f.sheets()


# 读取文件内容并返回行内容
def read_sheet(xls, index):
    data = []
    table = get_sheet(xls)[index]
    num = table.nrows
    for row in range(num):
        rdata = table.row_values(row)
        data.append(rdata)
    return data


# 获取sheet表的个数
def get_sheet_num(f):
    return len(get_sheet(f))


def copy_data(ws, raw_data):
    for a in range(len(raw_data)):
        for b in range(len(raw_data[a])):
            c = raw_data[a][b]
            ws.write(a, b, c)


def merge_files(filename_list, target_file):
    # if os.path.isfile(target_file):
    #     os.remove(target_file)
    # fp = open(target_file, 'w')
    # fp.close()
    wb = xlsxwriter.Workbook(target_file)
    for file in filename_list:
        print("Reading excel file %s" % file)
        xls = open_xls(file)
        for index in range(get_sheet_num(xls)):
            print("copying sheet %d" % index)
            ws = wb.add_worksheet()
            raw_data = read_sheet(xls, index)
            copy_data(ws, raw_data)
    wb.close()


def collect_files(filepath):
    filename_list = []
    filepath_abs = os.path.abspath(filepath)
    if os.path.isfile(filepath_abs):
        if is_legal_postfix(filepath_abs):
            filename_list.append(filepath_abs)
        else:
            raise TypeError('文件 {} 后缀名不合法！仅支持如下文件类型：{}。'.format(filepath, ''.join(handle_postfix)))
    elif os.path.isdir(filepath_abs):
        for relative_path, _, files in os.walk(filepath_abs):
            for name in files:
                filename = os.path.join(filepath_abs, relative_path, name)
                if is_legal_postfix(filename):
                    filename_list.append(os.path.join(filename))
                else:
                    print("存在非法文件 {}，忽略。".format(filename))
    else:
        raise TypeError('文件/文件夹 {} 不存在或不合法！'.format(filepath))

    return filename_list


def is_legal_postfix(filename):
    return filename.split('.')[-1].lower() in handle_postfix and not os.path.basename(filename).startswith(
        '~')


def func():
    tmp_file = './tmp/tmp.xlsx'
    filename_list = collect_files("./excels")
    merge_files(filename_list, tmp_file)


# def main():
#     func()
#
#
# if __name__ == '__main__':
#     main()
