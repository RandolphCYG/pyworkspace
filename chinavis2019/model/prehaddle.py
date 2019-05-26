# -*- coding: utf-8 -*-
# @Time    : 2019/3/27 19:38
# @Author  : Randolph
# @Email   : cyg0504@outlook.com
# @File    : prehaddle.py
# @Software: PyCharm

import pandas as pd
import numpy as np
import os.path
import json
from collections import Counter

path0 = '../res/传感器布置表.csv'
path1 = '../res/传感器日志数据/day1.csv'
path2 = '../res/传感器日志数据/day2.csv'
path3 = '../res/传感器日志数据/day3.csv'
# 入口位置
entrance_port = [11300, 11502, 11504, 11507]
# 出口位置
exit_port = [10019, 11505, 11515, 11517]
# 签到处
check_in_desk = [11202, 11203, 11204, 11205, 11302, 11303, 11304, 11305]
# 展厅
exhibition_hall = [10215, 10216, 10217, 10218, 10315, 10316, 10317, 10318,
                   10415, 10416, 10417, 10418, 10515, 10516, 10517, 10518,
                   10615, 10616, 10617, 10618, 10715, 10716, 10717, 10718,
                   10815, 10816, 10817, 10818, 10915, 10916, 10917, 10918,
                   11015, 11016, 11017, 11018, 11115, 11116, 11117, 11118]
# 主会场，11228为主会场出入口
main_venue = [10219, 10220, 10221, 10222, 10223, 10224,
              10319, 10320, 10321, 10322, 10323, 10324, 10325, 10326, 10327,
              10419, 10420, 10421, 10422, 10423, 10424, 10425, 10426, 10427,
              10519, 10520, 10521, 10522, 10523, 10524, 10525, 10526, 10527,
              10619, 10620, 10621, 10622, 10623, 10624, 10625, 10626, 10627,
              10719, 10720, 10721, 10722, 10723, 10724, 10725, 10726, 10727,
              10819, 10820, 10821, 10822, 10823, 10824, 10825, 10826, 10827,
              10919, 10920, 10921, 10922, 10923, 10924, 10925, 10926, 10927,
              11019, 11020, 11021, 11022, 10423, 11024, 11025, 11026, 11027,
              11119, 11120, 11121, 11122, 10423, 11124, 11125, 11126, 11127]
# 服务台
service_desk = [11419, 11420, 11519, 11520]
# 房间
room1 = [10610, 10611, 10710, 10711, 10810, 10811, 10910, 10911]
room2 = [11010, 11011, 11110, 11111]
room3 = [11421, 11422, 11423, 11424, 11521, 11522, 11523, 11524]
room4 = [11425, 11426, 11525, 11526]
room5 = [21001, 21002, 21003, 21004, 21101, 21102, 21103, 21104]
room6 = [20610, 20611, 20710, 20711]
# 厕所
toilet1 = [10410, 10411, 10510, 10511]
toilet2 = [11427, 11428, 11527, 11528]
toilet3 = [20410, 20411, 20510, 20511]
# 海报区
poster_area = [10307, 10308, 10407, 10408, 10507, 10508, 10607,
               10608, 10707, 10708, 10807, 10808, 10907, 10908]
# 分会场
breakout_venue_a = [10201, 10202, 10203, 10204, 10301, 10302, 10303, 10304]
breakout_venue_b = [10401, 10402, 10403, 10404, 10501, 10502, 10503, 10504]
breakout_venue_c = [10601, 10602, 10603, 10604, 10701, 10702, 10703, 10704]
breakout_venue_d = [10801, 10802, 10803, 10804, 10901, 10902, 10903, 10904]
# 扶梯
escalator_first_north = [10110, 10111]
escalator_first_south = [11410, 11411]
escalator_second_north = [20110, 20111]
escalator_second_south = [21410, 21411]
# 餐厅
restaurant = [20202, 20203, 20204, 20205, 20302, 20303, 20304, 20305,
              20402, 20403, 20404, 20405, 20502, 20503, 20504, 20505,
              20602, 20603, 20604, 20605, 20702, 20703, 20704, 20705,
              20802, 20803, 20804, 20805, 20902, 20903, 20904, 20905]
# 休息区
lounge_area = [21300, 21301, 21302, 21303, 21304, 21305,
               21400, 21401, 21402, 21403, 21404, 21405,
               21500, 21501, 21502, 21503, 21504, 21505]
# 所有区域的name对应的sid
place_all = {
    'entrance_port': entrance_port,
    'exit_port': exit_port,
    'check_in_desk': check_in_desk,
    'exhibition_hall': exhibition_hall,
    'main_venue': main_venue,
    'service_desk': service_desk,
    'room1': room1,
    'room2': room2,
    'room3': room3,
    'room4': room4,
    'room5': room5,
    'room6': room6,
    'toilet1': toilet1,
    'toilet2': toilet2,
    'toilet3': toilet3,
    'poster_area': poster_area,
    'breakout_venue_a': breakout_venue_a,
    'breakout_venue_b': breakout_venue_b,
    'breakout_venue_c': breakout_venue_c,
    'breakout_venue_d': breakout_venue_d,
    'escalator_first_north': escalator_first_north,
    'escalator_first_south': escalator_first_south,
    'escalator_second_north': escalator_second_north,
    'escalator_second_south': escalator_second_south,
    'restaurant': restaurant,
    'lounge_area': lounge_area
}


def s2t(second_time):
    """
    秒数转时间函数
    :param second_time: 25240
    :return: 07:00:40
    """
    m, s = divmod(second_time, 60)
    h, m = divmod(m, 60)
    return '%02d:%02d:%02d' % (h, m, s)


def split_time(n):
    """
    设置从07:00:00 18:10:00
    即使是卫生间以秒为划分看到的效果也是很差的，
    结论就是没有必要以秒区划分，这样我们尽量将划分时间划为1~10分钟的整数分钟即可
    :param n:几分钟统计一次,给整数
    :return:
    """
    time_slice = n * 60
    time_index = (65400 - 25200) // time_slice
    time_range = []
    for i in range(time_index + 1):
        moment = 25200 + i * time_slice
        time_range.append(moment)
    return time_range


def write(save_path, save_content):
    with open(save_path, 'a', newline='') as f:
        df = pd.DataFrame(save_content)
        df.to_csv(f, index=False, sep=',', header=['id', 'sid', 'time'])


def core(path):
    """
    打开三天文件，转成np列表
    :param path:三天的日志
    :return:
    """
    df_y = pd.read_csv(path, encoding='utf-8', error_bad_lines=False,
                       usecols=[0, 1, 2])  # pd.dataframe
    log_data = np.array(df_y)  # np.ndarray()
    log_list = log_data.tolist()  # list
    # print(train_x_list[0][1])
    # print(type(train_x_list))
    return log_list


def analysis_place(path, place, place_name):
    """
    分析各区域内部人员id，位置sid，时间time
    :param place:
    :param place_name:
    :return:
    """
    save_path = '../res/place/' + place_name + '.csv'
    sensor_list = []
    for i, sid in enumerate(core(path)):
        if sid[:][1] in place:
            sensor_list.append(sid[:][:])
    write(save_path, sensor_list)


def analysis_person(path, person_id):
    """
    分析某个人员行动轨迹
    :param person_id:
    :return:
    """
    save_path = '../res/test/' + str(person_id) + '.csv'
    go_list = []
    for i, sid in enumerate(core(path)):
        if sid[:][0] == person_id:
            print(sid[:][0], sid[:][1], s2t(sid[:][2]))
    #         go_list.append(sid[:][:])
    # write(save_path, go_list)


def analysis_place_person_count(path, place, place_name):
    """
    分析区域内部，当日人员停留总人数，再将区域内部每隔十分钟的人数存进json文件
    如何计算区域内部实时人数？？————如何判断出入 根据出入情况计算当前区域的人员id总数目
    我们的传感器只会记录发生变化时候的人员ID的记录，也就是必须算一下积分
    人员id在该区域第一次检测到的时候，人员id存一个列表以记录该区域实时人数，不断地拿该列表去遍历
    当该列表中的人员ID在门口的位置出现第二次的时候，开始减去即可
    （奇数检测到+，偶数时-即可，然后统计列表长度即实时人数）
    :param path: 三天日志数据路径待发到core()处理
    :param place: 待分析的区域
    :param place_name: 待分析的区域名字
    :return:
    """
    time_range = split_time(5)  # 给定划分时间的分钟数目，10则代表十分钟计算一次
    person_list = []
    time_list = []

    which_day = path.split('/')[3].split('.')[0]

    for i, sid in enumerate(core(path)):
        if sid[:][1] in place:      #  and sid[:][0] not in person_list:
            if sid[:][0] not in person_list:
                person_list.append(sid[:][0])
                time_list.append(sid[:][2])
            # else:
            #     print('第二次及以上在门口出现的人员：', sid[:][0])
    print(str(place_name) + '人数：' + str(len(person_list)))
    # 这里想到一个比较好的处理方法，将数据类型改成集合，可以用集合的相关操作计算
    # print(str(place_name) + '时间点：' + str(len(time_list)))

    exist_time_range_list = []
    num_list = []
    for m in range(len(time_range)):
        if m + 1 < len(time_range):     # 防止迭代溢出
            len_list = []
            count_time_list = []

            for n in range(len(time_list)):
                if time_range[m] <= time_list[n] < time_range[m + 1]:
                    count_time_list.append(time_list[n])
                    len_list.append(len(count_time_list))
                    exist_time_range = str(s2t(time_range[m])) + '~' + str(s2t(time_range[m + 1]))

            if len_list:    # 当时间段内有记录
                exist_time_range_list.append(exist_time_range)
                # print(list(reversed(len_list))[0])
                num_list.append(list(reversed(len_list))[0])

    t_p_list = [exist_time_range_list, num_list]

    place_stat = {which_day: t_p_list}
    data_dict = place_stat
    return data_dict


def analysis_person_stay():
    """
    判断每个人停留时间长度较长的点
    :return:
    """
    take_part_in_person_list = []
    read_path = '../res/person/'
    for i, f in enumerate(os.listdir(read_path)):
        handle_path = '../res/person/' + f
        print(i, handle_path)

        with open(handle_path, 'r') as file:
            data = pd.read_csv(file)
            for i in range(len(data)):
                if i + 1 < len(data):   # 错误处理，防止i+1超过迭代数目
                    if data['time'].iloc[i + 1] - \
                            data['time'].iloc[i] > 60:    # 两时间类型数据可以相减
                        for k, v in zip(place_all.keys(), place_all.values()):
                            if data['sid'].iloc[i] in v:    # 判断停留所在的地点, 停留时间
                                print(k, data['sid'].iloc[i], s2t(
                                    data['time'].iloc[i + 1] - data['time'].iloc[i]))

                                # 主会场分析
                                if k == 'main_venue':
                                    print(
                                        data['id'].iloc[i], '与会人员', data['sid'].iloc[i])
                                    if data['id'].iloc[i] not in take_part_in_person_list:
                                        take_part_in_person_list.append(
                                            data['id'].iloc[i])
    print(len(take_part_in_person_list))


def analysis_some_person_stay(person_id):
    """
    判断mou个人停留时间长度较长的点
    :return:
    """
    handle_path = '../res/person/' + str(person_id) + '.csv'
    print(handle_path)
    with open(handle_path, 'r') as file:
        data = pd.read_csv(file)
        # print(type(data['time'].iloc[5]))
        for i in range(len(data)):
            if i + 1 < len(data):   # 错误处理，防止i+1超过迭代数目
                if data['time'].iloc[i + 1] - data['time'].iloc[i] > 60:
                    for k, v in zip(place_all.keys(), place_all.values()):
                        if data['sid'].iloc[i] in v:    # 判断停留所在的地点, 停留时间
                            print(k, data['sid'].iloc[i], s2t(
                                data['time'].iloc[i + 1] - data['time'].iloc[i]))


if __name__ == "__main__":
    m_dict = analysis_place_person_count(path1, toilet1, 'toilet1')
    print(m_dict)

    # split_time(time_slice3)

    # all_results = {}
    # for k, v in zip(place_all.keys(), place_all.values()):
    #     print(k, v)  # 遍历区域，计算每十分钟该区域扫描到的信号（信号筛选掉就是人数）数目，存成json文件
    #     result_list_day1 = analysis_place_person_count(path1, v, k)  # {'day1': [['07:00:00~07:10:00', ...], [8, ...]]}
    #     result_list_day2 = analysis_place_person_count(path2, v, k)
    #     result_list_day3 = analysis_place_person_count(path3, v, k)
    #     result_list = {}
    #     result_list.update(result_list_day1)
    #     result_list.update(result_list_day2)
    #     result_list.update(result_list_day3)    # {'day1': [[][]], 'day2': [[][]], 'day3': [[][]]}
    #     single_results = {k: result_list}   # {'entrance_port': {'day1': [[][]], 'day2': [[][]], 'day3': [[][]]}}
    #     all_results.update(single_results)  # {'entrance_port': V1, 'place2': V2, ...}
    #     break
    # 写入json
    # with open("../res/results/place_split_time_person_num.json", 'a') as outfile:
    #     json.dump(all_results, outfile, ensure_ascii=False)
    #     outfile.write('\n')

    # analysis_person(path1, 11778)
    # analysis_some_person_stay(10019)

    # 各区域内部的人员
    # for k, v in zip(place_all.keys(), place_all.values()):
    #     print(k, v)
    #     analysis_place(path1, v, k)

    # 人员分析
    # analysis_person(path1, 10638)
    # analysis_some_person_stay(person_id=10638)

    # print('第一天各区域人数:')

    # data2json
    # day1_num = analysis_place_person_count(path1, main_venue, 'main_venue')
    # day2_num = analysis_place_person_count(path2, main_venue, 'main_venue')
    # day3_num = analysis_place_person_count(path3, main_venue, 'main_venue')

    # day1_checkin_num = analysis_place_person_count(path1, check_in_desk, 'check_in_desk')
    # day1_main_venue_num = analysis_place_person_count(path1, main_venue, 'main_venue')
    # day1_no_need_check_in_list = set(day1_num).difference(set(day1_checkin_num))  # 进了门没有签到的人
    # print(day1_no_need_check_in_list)
    # print(len(day1_no_need_check_in_list))
    #
    # print('第二天各区域人数:')
    # day2_num = analysis_place_person_count(path2, entrance_port, 'entrance_port')
    # day2_checkin_num = analysis_place_person_count(path2, check_in_desk, 'check_in_desk')
    # day2_main_venue_num = analysis_place_person_count(path2, main_venue, 'main_venue')
    # day2_no_need_check_in_list = set(day2_num).difference(set(day2_checkin_num))  # 进了门没有签到的人
    # print(day2_no_need_check_in_list)
    # print(len(day2_no_need_check_in_list))
    #
    # two_day_no_need_check_in_num_joint_list = list(set(day1_no_need_check_in_list).intersection(set(day2_no_need_check_in_list)))
    # print(two_day_no_need_check_in_num_joint_list)
    # print('前两天未签到人员的交集', len(two_day_no_need_check_in_num_joint_list))
    #
    # print('分析有可能是内部服务人员的所有人员：')
    # print('分析人员待的时间：')
    # for i, p_id in enumerate(two_day_no_need_check_in_num_joint_list):
    #     print('处理id中：', p_id)
    #     analysis_person(path1, p_id)

    #     # analysis_person_stay(path1, p_id)
