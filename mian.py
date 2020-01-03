import pandas as pd
import requests
import bs4
import re
import sys
import os
import math
import urllib3
urllib3.disable_warnings()

URL = "https://job.rikunabi.com/2020/accounts/regist/ajax/"
SUBJECT = "school/gakubuGakka"
SCHOOL = "school/gakko/"
BunRi = "school/bunriKbn/"

def getSchoolName():
    """
    カタカナと区分から学校名のJSONを返却する
    ==================
    Param
    ==================
    dGakushuCode : 学校の区分ｎ
    KEYS_dic: 取得したデータ群
    """
    formData = {
        'dGakushuCode': '3',
        'dGakkoHead': 'ハ',
        'permAuthFlg':''
    }
    response = requests.post(url=URL+SCHOOL, data=formData, verify=False)


def getSubjectNames():
    formData = {
        'dGakkoCd': ''
    }
    response = requests.post(url=URL+SUBJECT, data=formData, verify=False)

def judgBnRi():
    formData = {
        'smGakkaId': ''
    }
    response = requests.post(url=URL+SUBJECT, data=formData, verify=False)



def main():
    """main function"""
    getSchoolName()
    getSubjectNames()


if __name__ == '__main__':
    main()



"""
学校区分 1~5
学校名 あ〜わ

学校名のJSONを取得
文字列をJSONに変換 => 配列からvalueなしとvalueがXXXXのデータを削除

valueを元に学校の学科を取得

"""
print('')
formData = {
    'dGakushuCode': '3',
    'dGakkoHead': 'ハ',
    'permAuthFlg':''
}
response = requests.post(url=URL+SCHOOL, data=formData, verify=False)
print(response.text)
