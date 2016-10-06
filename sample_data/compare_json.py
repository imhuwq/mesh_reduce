# -*- coding: utf-8 -*-

import sys
import json


def json2dict(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)


def get_dict_diff(origin, target, diff):
    """ 比较两个 dict， 并且把二者的差异保存到传入的 diff (dict) 中再返回 """
    for key, value in origin.items():
        target_value = target.get(key, None)
        if value != target_value:

            if isinstance(value, dict):
                diff_dict = dict()
                get_dict_diff(value, target_value, diff_dict)

                if diff_dict:
                    diff[key] = diff_dict

            elif isinstance(value, list):
                diff_list = list()
                get_list_diff(value, target_value, diff_list)

                if diff_list:
                    diff[key] = diff_list

            else:
                diff[key] = value

    return diff


def get_list_diff(origin, target, diff):
    """ 比较两个 list， 并且把二者的差异保存到传入的 diff (list) 中再返回 """
    if origin != target:
        for index in range(len(origin)):
            if isinstance(origin[index], list):
                diff_list = list()
                get_list_diff(origin[index], target[index], diff_list)
                if diff_list:
                    diff.append(diff_list)

            elif isinstance(origin[index], dict):
                diff_dict = dict()
                origin_dict = origin[index]
                try:
                    target_dict = target[index]
                except IndexError:
                    target_dict = dict()
                get_dict_diff(origin_dict, target_dict, diff_dict)
                if diff_dict:
                    diff.append(diff_dict)

            else:
                if target is None or origin[index] not in target:
                    diff.append(origin[index])

    return diff


first_json_file = sys.argv[1]
secnd_json_file = sys.argv[2]

first_name = first_json_file.rsplit('.', 1)[0]
secnd_name = secnd_json_file.rsplit('.', 1)[0]

print('开始比较 <%s> and <%s>...' % (first_json_file, secnd_json_file))

go_on = raw_input('请确保两个 json 文件的数据结构是一致的，否则没有可比性: <y/n>')
if go_on.lower() in ['y', 'yes']:
    print('正在读取 json 文件...')
    first_dict = json2dict(first_json_file)
    secnd_dict = json2dict(secnd_json_file)

    print('正在计算...')
    diff_f2s = get_dict_diff(first_dict, secnd_dict, dict())
    diff_s2f = get_dict_diff(secnd_dict, first_dict, dict())

    if not diff_f2s and not diff_s2f:
        print('两个 json 文件内容完全一致!')

    else:
        if diff_f2s:
            print('正在写入输出文件 diff_%s>>>%s_.json' % (first_name, secnd_name))
            output_name = 'diff_%s>>>%s.json' % (first_name, secnd_name)

            with open(output_name, 'w') as f:
                json.dump(diff_f2s, f)

        if diff_s2f:
            print('正在写入输出文件 diff_%s>>>%s_.json' % (secnd_name, first_name))
            output_name = 'diff_%s>>>%s.json' % (secnd_name, first_name)

            with open(output_name, 'w') as f:
                json.dump(diff_s2f, f)

        print('已完成')
