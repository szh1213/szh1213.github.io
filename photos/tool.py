# !/usr/bin/python3
# -*- coding: utf-8 -*-
from PIL import Image
import os
import sys
import json
from datetime import datetime
from ImageProcess import Graphics

# 定义压缩比，数值越大，压缩越小
SIZE_normal = 1.0
SIZE_small = 1.5
SIZE_more_small = 2.0
SIZE_more_small_small = 3.0


def make_directory(directory):
    """创建目录"""
    os.makedirs(directory)


def directory_exists(directory):
    """判断目录是否存在"""
    if os.path.exists(directory):
        return True
    else:
        return False


def list_img_file(directory):
    """列出目录下所有文件，并筛选出图片文件列表返回"""
    # old_list = os.listdir(directory)
    img_type = ["jpg", "jpeg", "png", "gif"]

    new_list = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)[len(directory):]
            # print(f'filename: => {file} | filepath: => {filepath}')
            name, fileformat = file.split(".")
            if fileformat.lower() in img_type:
                new_list.append(filepath)

    # for filename in old_list:
    #     print('filename: => ', filename)
    #     name, fileformat = filename.split(".")
    #     if fileformat.lower() in img_type:
    #         new_list.append(filename)

    return new_list


def print_help():
    print(
        """
    This program helps compress many image files
    you can choose which scale you want to compress your img(jpg/png/etc)
        1) normal compress(4M to 1M around)
        2) small compress(4M to 500K around)
        3) smaller compress(4M to 300K around)
        4) smallest compress(unkown)
        """
    )
    num = 4
    try:
        print('请输入压缩模式:')
        num = int(sys.stdin.readline().strip())
        print(f"你的选择是：{num}")
    except Exception as e:
        print(e)

    return num


def compress(choose, des_dir, src_dir, file_list):
    """
    压缩算法，img.thumbnail对图片进行压缩，

    参数
    -----------
    choose: str
        选择压缩的比例，有4个选项，越大压缩后的图片越小
    """
    if choose == 1:
        scale = SIZE_normal
    if choose == 2:
        scale = SIZE_small
    if choose == 3:
        scale = SIZE_more_small
    if choose == 4:
        scale = SIZE_more_small_small
    for infile in file_list:
        img = Image.open(src_dir+infile)
        # size_of_file = os.path.getsize(infile)
        w, h = img.size
        img.thumbnail((int(w/scale), int(h/scale)))
        tagPath = des_dir + infile
        fileDir = os.sep.join(tagPath.split(os.sep)[:-1])

        # 子目录创建
        if fileDir and not directory_exists(fileDir):
            make_directory(fileDir)
        print(f"infile: {infile} ===> tagPath: {tagPath}")

        img.save(tagPath)


def compress_photo():
    '''
    调用压缩图片的函数
    '''
    src_dir, des_dir = "photos/", "min_photos/"

    file_list_src, file_list_des = [], []

    # photos 目录判断
    if not directory_exists(src_dir):
        make_directory(src_dir)
    else:
        # business logic
        file_list_src = list_img_file(src_dir)

    # min_photos 目录判断
    if directory_exists(des_dir):
        file_list_des = list_img_file(des_dir)
    else:
        make_directory(des_dir)

    '''如果已经压缩了，就不再压缩'''
    for i in range(len(file_list_des)):
        if file_list_des[i] in file_list_src:
            file_list_src.remove(file_list_des[i])
    if len(file_list_src) == 0:
        print("=====没有新文件需要压缩=======")

    num = print_help()
    compress(num, des_dir, src_dir, file_list_src)


def handle_photo():
    '''
    根据图片的文件名处理成需要的json格式的数据
    -----------
    最后将data.json文件存到博客的source/photos文件夹下
    '''
    src_dir, des_dir = "photos/", "min_photos/"
    file_list = list_img_file(src_dir)
    list_info = []
    file_list.sort(key=lambda x: x.split(os.sep)[-1].split('_')[0])   # 按照日期排序

    for i in range(len(file_list)):
        filename = file_list[i]
        #date_info, info = filename.split("_")
        date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(os.stat('km.m').st_ctime))
        info = ""

        if len(date_info.split(os.sep)) == 2:
            _dir, date_str = date_info.split(os.sep)
        else:
            date_str = date_info

        info, _ = info.split(".")
        date = datetime.strptime(date_str, "%Y-%m-%d")
        year_month = date_str[0:7]
        if i == 0:  # 处理第一个文件
            new_dict = {
                "date": year_month,
                "arr": {
                    'year': date.year,
                    'month': date.month,
                    'link': [filename],
                    'text': [info],
                    'type': ['image']
                }
            }
            list_info.append(new_dict)
        elif year_month != list_info[-1]['date']:  # 不是最后的一个日期，就新建一个dict
            new_dict = {
                "date": year_month,
                "arr": {
                    'year': date.year,
                    'month': date.month,
                    'link': [filename],
                    'text': [info],
                    'type': ['image']
                }
            }
            list_info.append(new_dict)
        else:  # 同一个日期
            list_info[-1]['arr']['link'].append(filename)
            list_info[-1]['arr']['text'].append(info)
            list_info[-1]['arr']['type'].append('image')

    list_info.reverse()  # 翻转
    final_dict = {"list": list_info}
    with open("data.json", "w") as fp:
        json.dump(final_dict, fp)


def cut_photo() -> bool:
    """
    裁剪算法

    ----------
    调用Graphics类中的裁剪算法，将src_dir目录下的文件进行裁剪（裁剪成正方形）
    """
    flag = True
    src_dir = "photos/"
    if directory_exists(src_dir):
        # business logic
        file_list = list_img_file(src_dir)
        # print file_list
        if file_list:
            # num = print_help()
            for infile in file_list:
                # img = Image.open(src_dir+infile)
                Graphics(infile=src_dir+infile,
                         outfile=src_dir + infile).cut_by_ratio()
        else:
            pass
    else:
        flag = False
        print("source directory not exist!")
    return flag


def git_operation():
    '''
    git 命令行函数，将仓库提交

    ----------
    需要安装git命令行工具，并且添加到环境变量中
    '''
    os.system('git add --all')
    os.system('git commit -m "update photos"')
    os.system('git push origin master')


def main():
    """主程序入口"""
    res = cut_photo()        # 裁剪图片，裁剪成正方形，去中间部分
    if res:
        compress_photo()   # 压缩图片，并保存到 mini_photos 文件夹下
        #git_operation()    # 提交到 github/gitee 仓库
        handle_photo()     # 将文件处理成 json 格式，存到博客仓库中


if __name__ == "__main__":
    main()
