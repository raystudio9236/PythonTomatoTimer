#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import threading
import time
import sys


def time_format(seconds):
    """
    将x秒转换成 x分:x秒格式
    """
    return time.strftime('%M:%S', time.localtime(seconds))


# 进度条宽度
LOG_WIDTH = 35
# 清理字符
CLEAR_TO_END = '\033[K'


def progress_log(current, total):
    """
    打印当前进度
    """

    # 清理之前的进度输出
    sys.stdout.write(f'\r{CLEAR_TO_END}')

    # 计算当前进度
    progress = 1 - current / total

    # 计算当前要显示多少个#
    hashes = '#' * int(progress * LOG_WIDTH)

    # 计算除了显示#还要显示多少个空格
    spaces = ' ' * int(LOG_WIDTH - len(hashes))

    # 输出进度条
    sys.stdout.write(
        f'\r{time_format(current)}/{time_format(total)} [{hashes + spaces}] {progress * 100:.2f}%')


class TimeThread(threading.Thread):
    """
    番茄钟计时线程
    """

    def __init__(self, time):
        threading.Thread.__init__(self)
        # 保留剩余时间数据
        self.remain_time = time
        # 保留总时间数据
        self.total_time = time

    def run(self):
        """
        计时逻辑
        """

        print(f'倒计时开始，剩余时间 {time_format(self.remain_time)}')

        # 当当前剩余时间大于0时，继续计时
        while self.remain_time > 0:
            # 将剩余时间减1
            self.remain_time -= 1

            # 打印进度条
            progress_log(self.remain_time, self.total_time)

            # 将线程休眠1s
            time.sleep(1)

        print('\n倒计时结束，请选择下一项任务')


def print_category():
    """
    打印菜单，并获得用户输入
    """
    print('\n\n--- 命令行番茄钟 ---')
    print('1. Pomodoro (25分钟)')
    print('2. Short break (5分钟)')
    print('3. Long break (10分钟)')
    print('4. 退出')
    print('> ', end='')

    # 获得用户输入
    input_s = input()

    # 如果用户输入非法，则请用户重新输入
    while input_s not in ['1', '2', '3', '4']:
        print('输入有误，请重新输入')
        print('> ', end='')
        input_s = input()

    # 返回输入结果
    return input_s


def main():
    # 番茄中主循环
    while True:
        # 打印菜单，并获得用户输入
        input_s = print_category()

        # 根据选项启动不同的线程
        if input_s == '1':
            thread = TimeThread(1500)
            # 开始计时
            thread.start()
        elif input_s == '2':
            thread = TimeThread(300)
            # 开始计时
            thread.start()
        elif input_s == '3':
            thread = TimeThread(600)
            # 开始计时
            thread.start()
        else:
            return

        # 等待线程执行完毕
        thread.join()


if __name__ == '__main__':
    main()
