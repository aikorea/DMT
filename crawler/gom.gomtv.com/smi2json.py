#*- coding: utf-8 -*-
import argparse
import os
import re
import json
import codecs
from bs4 import BeautifulSoup
import chardet.universaldetector

import time
start_time = time.time()

# Argument parsing
parser = argparse.ArgumentParser(description='SMI files to DMT json file')
parser.add_argument('--in_dir', help='Directory to SMI files')
parser.add_argument('--out_file', help='Output json filename')
parser.add_argument('--iou', help='EN/KR sync IOU criteria')
args = parser.parse_args()

IN_DIR = 'subtitle'
OUT_FILENAME = "gom.json"
MIN_IOU = 0.8
NUM_THREAD = 4
if args.in_dir:
    IN_DIR = args.in_dir
if args.out_file:
    OUT_FILENAME = args.out_file
if args.iou:
    MIN_IOU = float(args.iou)

# SMI files loading
pat_smi = re.compile(".*\.smi$")
smi_path_list = [os.path.join(IN_DIR, filename) for filename in os.walk(IN_DIR).next()[2]\
				if pat_smi.match(filename) is not None]
print str(len(smi_path_list)) + ' subtitles files founds'

pat_tag = re.compile('<sync start=\d+><p class=\w+>', flags=re.IGNORECASE)
pat_start = re.compile('start=\d+', flags=re.IGNORECASE)
pat_lang = re.compile('class=\w+', flags=re.IGNORECASE)
pat_hangul = re.compile(u'[ㄱ-ㅣ가-힣]+')

sub_ll = list()

# SMI parsing
for smi_path in smi_path_list:
    # Open SMI with detected encoding
    print 'parsing ' + smi_path + "..."

    try:
        detector = chardet.universaldetector.UniversalDetector()
        with open(smi_path, 'r') as fd:
            lines = fd.readlines()
        for line in lines:
            detector.feed(line)
            if detector.done: break
        detector.close()
        chdt = detector.result
        print '\tencoding : ' + str(chdt['encoding'])
        if chdt['encoding'] is None:
            continue

        if chdt['encoding'] != "utf-8" or chdt['encoding'] != "ascii":
            with codecs.open(smi_path, "r", encoding=chdt['encoding']) as fd:
                smi_data = fd.read()
        else:
            with open(smi_path, 'r') as fd:
                smi_data = fd.read()

        if smi_data[:10].find("SAMI") == -1:
            print "\tNot a smi file (header : " + smi_data[:10] + ")"
            continue
    except Exception, e:
        print e
        continue    

    # Parse subtitle tag and sort with language(en/kr)
    kr_sub_list = list()
    en_sub_list = list()
    mat_list = [mat for mat in pat_tag.finditer(smi_data)]
    for i in range(len(mat_list)):
        tag_str = mat_list[i].group(0)
        start = int(pat_start.search(tag_str).group(0)[6:])
        lang = pat_lang.search(tag_str).group(0)[6:]
        if i < len(mat_list) - 1:
            raw_text = smi_data[mat_list[i].end():mat_list[i+1].start()]
        else:
            raw_text = smi_data[mat_list[i].end():]
        text = BeautifulSoup(raw_text, 'lxml').get_text()
        text = text.replace('\r\n', ' ').replace('\n', ' ').strip()
        if len(text) > 0:
            if lang.upper().find("KR") != -1:
                kr_sub_list.append((start, text))
            elif lang.upper().find("EN") != -1:
                en_sub_list.append((start, text))

    if len(kr_sub_list) == 0 or len(en_sub_list) == 0:
        print "\tNot an en-kr subtitle"
        continue
    else:
        print "\tKR : " + str(len(kr_sub_list)) + " EN : " + str(len(en_sub_list))

    # matched sync count - IOU > 0.9
    kr_start_set = {sub[0] for sub in kr_sub_list}
    en_start_set = {sub[0] for sub in en_sub_list}
    start_iou = float(len(kr_start_set & en_start_set)) / len(kr_start_set | en_start_set)
    if start_iou < MIN_IOU:
        print "\tEN-KR subtitles do not match.(IOU : " + str(start_iou) + ")"
        continue

    # merge EN/KR subtitles
    sub_list = list()
    kr_cnt = 0
    en_cnt = 0
    while kr_cnt < len(kr_sub_list) and en_cnt < len(en_sub_list):
        kr_sub = kr_sub_list[kr_cnt]
        en_sub = en_sub_list[en_cnt]
        if kr_sub[0] == en_sub[0]:  # sync matched.
            if len(pat_hangul.findall(en_sub[1])) > 0:
                # EN subtitle should not have korean character
                # print "\tkr found in en sub - " + en_sub[1]
                pass
            elif len(pat_hangul.findall(kr_sub[1])) == 0 or kr_sub[1].find(en_sub[1]) != -1:
                # KR subtitle has no korean character of have same of EN subtitle
                # print "\ten found in kr sub - " + kr_sub[1]
                pass
            else:
                sub_list.append((kr_sub[0], kr_sub[1], en_sub[1]))
            kr_cnt += 1
            en_cnt += 1
        elif kr_sub[0] > en_sub[0]:
            en_cnt += 1 
        elif kr_sub[0] < en_sub[0]:
            kr_cnt += 1

    print "\t" + str(len(sub_list)) + " lines merged"

    if len(sub_list) > 0:
    	sub_ll.append(sub_list)

# merge parsed subs and make JSON output
print str(len(sub_ll)) + ' files parsed'
if len(sub_ll) > 0:
    print 'merge parcors'
    parcors = list()
    for sub_list in sub_ll:
        for sub in sub_list:
            parcors.append({'kr':sub[1], 'en':sub[2]})

    data = dict()
    data['source'] = 'gom'
    data['type'] = 'sentence'
    data['values'] = parcors

    print 'JSON file write...'
    with open(OUT_FILENAME, 'w') as fd:
        json.dump(data, fd, indent=2)

print 'Done!'
print 'Elapsed time:' + str(time.time() - start_time)