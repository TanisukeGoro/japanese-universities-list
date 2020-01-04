import pandas as pd
import requests
import json
import itertools
import time
import csv
from module.progress import progress_bar

" SSL エラー回避 "
import urllib3
urllib3.disable_warnings()

URL = 'https://job.rikunabi.com/2020/accounts/regist/ajax/'
SUBJECT = 'school/gakubuGakka'
SCHOOL = 'school/gakko/'
BunRi = 'school/bunriKbn/'
HIRAGANAs = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワ'
CATEGORIES = ['大学院(博士)', '大学院(修士)', '大学', '短大', '専門学校', '高専']


def remove_dumpdata(response):
    try:
        response.remove({'label': '選択してください', 'value': ''})
        response.remove({'label': '該当なし', 'value': 'XXXX'})
    except: print('remove error')
    return response


def getSchoolName(classification, hiragana):
    """
    カタカナと区分から学校名のJSONを返却する
    ==================
    Param
    ==================
    dGakushuCode : 学校の区分ｎ
    KEYS_dic: 取得したデータ群
    """

    formData = {
        'dGakushuCode': classification,
        'dGakkoHead': hiragana,
        'permAuthFlg':''
    }
    response = requests.post(url=URL+SCHOOL, data=formData, verify=False)
    response_json = json.loads(response.text)
    time.sleep(1)
    return remove_dumpdata(response_json)


def getSubjectNames(school_data):
    formData = {
        'dGakkoCd': school_data['value']
    }
    response = requests.post(url=URL+SUBJECT, data=formData, verify=False)
    response_json = json.loads(response.text)
    time.sleep(1)
    return remove_dumpdata(response_json)

def judgBnRi(subject):
    formData = {
        'smGakkaId': subject
    }
    response = requests.post(url=URL+BunRi, data=formData, verify=False)
    return response.text

def toCSV(school_data, subjects):
    """school + classification　の学校CSVを出力"""
    for subject in subjects:
        spamwriter.writerow([school_data['label'], school_data['value'], subject['label'], subject['value'], judgBnRi(subject['value'])])


def main():
    """main function"""

    for classification, hiragana in itertools.product(range(0,6), HIRAGANAs):
        school_datas = getSchoolName(classification, hiragana)
        school_info_data = pd.DataFrame( columns=['kana', 'name','name_id','subject','subject_id','bunri'])
        file_name = 'school_' + CATEGORIES[classification] + '.csv'

        if len(school_datas) >= 1:
            for index, school_data in enumerate(school_datas):
                progress_bar(curr_progress=index, end=len(school_datas), msg='学校区分: {0}, 学校名: {1}'.format(CATEGORIES[classification], school_data['label']))
                subjects = getSubjectNames(school_data)
                if len(school_datas) >= 1:
                    for subject in subjects:
                        tmp_se = pd.Series([hiragana, school_data['label'], school_data['value'], subject['label'], subject['value'], judgBnRi(subject['value'])], index=school_info_data.columns )
                        school_info_data = school_info_data.append( tmp_se, ignore_index=True )
        school_info_data.to_csv(file_name, mode='a' , header=False)




if __name__ == '__main__':
    main()



"""
学校区分 1~5
学校名 あ〜わ
f
学校名のJSONを取得
文字列をJSONに変換 => 配列からvalueなしとvalueがXXXXのデータを削除

valueを元に学校の学科を取得

"""
