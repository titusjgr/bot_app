# -*- coding: utf-8 -*-
# from players import player_ids
import re
import random as rand
import time
import numpy as np
from TeleApi import *


class AbcGame():
    def __init__(self):
        output_text = '歡迎來到A是什麼B是什麼'
        self.output(output_text)
        self.input(message, player_table)
        self.points = {player_id: 0 for player_id in self.player_table.keys()}
        self.game_intro()
        self.playing_loop()

    def input(self, message, player_table):  # id是str
        self.player_id = message.player.id
        self.player_first_name = message.player.first_name
        self.player_input = message.text
        self.time = message.time
        self.room_id = message.room_id
        self.player_table = player_table  # 以id作為key的dict

    def output(self, output_text):
        return PutTele(self.room_id, output_text)

    def game_intro(self):
        self.output('每次這遊戲會生出一個句子，然後接受4個回答\n如果沒有正確回答，就換下一個問題\n回答正確會加分，獲得3分就獲勝了')

    vocabs = ('水果', '咖哩', '玉米', '垃圾', '晚餐', '報社', '碑', '鼻子', '手錶', '表格', '布告', '蒼蠅', '車廂', '車站', '城市', '翅膀', '蟲', '窗戶', '詞語', '島', '燈', '凳子', '電影', '釘子', '耳朵', '耳環', '飯店', '房間', '墳', '缸', '胳膊', '歌', '工廠', '工人', '鼓', '工作', '故事', '瓜', '棺材', '鍋', '計劃', '肩膀', '教室', '角', '井', '鏡子', '橘子', '炕', '客人', '口袋', '口號', '筐', '礦山', '喇叭', '籃子', '狼', '老虎', '老鼠', '雷', '禮堂', '理由', '簾子', '路線', '旅館', '輪子', '鑼', '駱駝', '麻袋', '碼頭', '饅頭', '貓', '矛盾', '帽子', '門', '命令', '磨', '碾子', '鳥', '螃蟹', '琵琶', '棋子兒', '企業', '橋', '親戚', '琴', '青蛙', '蜻蜓', '人', '人家', '任務', '嗓子', '森林', '商店', '商品', '燒餅', '勺子', '舌頭', '屍體', '收音機', '書店', '刷子', '水庫', '水桶', '塑像', '算盤', '隧道', '嗩吶', '台階', '梯子', '題', '蹄子', '圖章', '兔子', '碗', '蚊子', '西瓜', '戲', '蝦', '香蕉', '箱子', '消息', '心', '信箱', '鴨子', '眼睛', '醫院', '椅子', '意見', '字', '影子', '魚網', '原則', '月餅', '針', '枕頭', '刀', '火', '剪子', '勁兒', '鋸', '筷子', '傘', '掃帚', '扇子', '勺子', '刷子', '梳子', '鎖', '香蕉', '兇器', '眼淚', '鑰匙', '椅子', '地圖', '日記', '書', '小說', '雜誌', '賬', '交易', '錢', '收入', '債務', '文字', '電影', '書', '小說', '影片', '比賽', '冰雹', '病', '電影', '風', '革命', '霜', '戲', '雪', '雨', '災荒', '戰鬥', '戰爭', '耳環', '筐', '牌', '棋', '嗓子', '手套', '笑容', '學校', '眼鏡', '被單', '被面', '被子', '灰', '樓', '皮', '土', '革命', '災荒', '戰鬥', '戰爭', '花兒', '汗', '汗珠', '露水', '水', '血', '眼淚', '雨', '鈔票', '文件', '紙', '信', '報紙', '飯', '工資', '禮物', '文件', '雜誌', '被面', '標語', '布', '地圖', '畫', '相片', '駱駝', '飯', '布景', '車床', '秤', '縫紉機', '機器', '馬達', '收音機', '水泵', '水車', '拖拉機', '戲', '儀器', '鑽石', '雕像', '驢', '騾子', '牛', '牲口', '象', '羊', '豬', '泥', '水', '血', '布景', '家具', '課', '唱片', '畫', '家具', '書', '衣服', '郵票', '火車', '課程')

    def generate_problem(self):
        selected_vocabs = rand.sample(self.vocabs, 2)
        self.output('A是%s，B是%s，那C是什麼？' % tuple(selected_vocabs))

    def player_answer(self, player_id, text):
        if re.fullmatch(r'.*我知道喔.+是.+', text) is not None:
            self.output('正確，%s加一分' % self.player_table[player_id])
            self.points[player_id] += 1
            return True, player_id
        else:
            self.output('可惜，錯了')
            return False, player_id

    def correct_answer(self):
        self.output('我知道喔，是%s' % tuple(rand.sample(self.vocabs, 1)))

    def playing_loop(self):
        ongoing = True
        correct_ans_counter = 0
        while ongoing is True:
            self.generate_problem()
            for _ in range(4):
                self.input(message, player_table)  # input contains ans and player_id
                correct_ans_counter += 1
                try:
                    a_try = self.player_answer(self.player_id, self.player_input)
                    if a_try[0] is True:
                        gain_player_id = a_try[1]
                        if self.points[gain_player_id] == 3:
                            ongoing = False
                            self.winner = gain_player_id
                        break
                except:
                    pass
            if correct_ans_counter >= 23:
                self.correct_answer()
                correct_ans_counter = 0
        self.output('%s贏了' % self.winner)

    def __del__(self):
        del self.vocabs


class Mosquito():
    def __init__(self):
        self.output('這個遊戲是死了幾隻蚊子')
        self.input()
        self.points = {player_id: 0 for player_id in self.player_table.keys()}
        self.game_intro()
        self.playing_loop()

    def input(self, message, player_table):  # id是str
        self.player_id = message.player.id
        self.player_first_name = message.player.first_name
        self.player_input = message.text
        self.time = message.time
        self.room_id = message.room_id
        self.player_table = player_table  # 以id作為key的dict

    def output(self, output_text):
        return PutTele(self.room_id, output_text)

    def game_intro(self):
        self.output('每次你們要從提示中猜出死了幾隻蚊子，請只要輸入數字\n如果4次都沒有正確回答，就換下一個問題\n回答正確會加分，獲得3分就獲勝了')

    def generate_problem(self):
        self.output('啪' * rand.randint(5, 13))
        s = '請問'[0:rand.randint(0, 1) * 2] + '蚊子'[0:rand.randint(0, 1) * 2] + '死' + '了'[0:rand.randint(0, 1)] + '幾隻'
        self.output(s)
        self.correct_answer = len(s)

    def player_answer(self, player_id, text):
        if self.correct_answer == int(text):
            self.output('正確，%s加一分' % self.player_table[player_id])
            self.points[player_id] += 1
            return True, player_id
        else:
            print('可惜，錯了')
            return False, player_id

    def correct_answer(self):
        self.output('答案是', self.correct_answer, '喔！')

    def playing_loop(self):
        ongoing = True
        correct_ans_counter = 0
        while ongoing is True:
            self.generate_problem()
            for _ in range(4):
                self.input()
                try:
                    a_try = self.player_answer(self.player_id, self.player_input)
                    if a_try[0] is True:
                        gain_player_id = a_try[1]
                        if self.points[gain_player_id] == 3:
                            ongoing = False
                            self.winner = gain_player_id
                        break
                except:
                    pass
            if correct_ans_counter >= 23:
                self.correct_answer()
                correct_ans_counter = 0
        self.output('%s贏了' % self.player_tabel[self.winner])


# 時間延遲以ms為單位，int
class BambooShoot():
    def __init__(self):
        self.output('這個遊戲是竹筍蹦蹦出')
        self.game_intro()
        self.playing_loop()

    def input(self, message, player_table):  # id是str
        self.player_id = message.player.id
        self.player_first_name = message.player.first_name
        self.player_input = message.text
        self.time = message.time
        self.room_id = message.room_id
        self.player_table = player_table  # 以id作為key的dict

    def output(self, output_text):
        return PutTele(self.room_id, output_text)

    def game_intro(self):
        self.output('每個人要輪流喊出1蹦出、2蹦出\n如果跳號、輸出錯誤或同時就輸了')

    def player_answer(self, player_id, text, ctime, last_time, last_player_id, counter):
        if text != str(counter) + '蹦出':
            self.output(player_id + '喊錯了')
            return 1, player_id, False  # 回傳數目，名稱，勝敗
            '''
        elif ctime == last_time:
            print(last_player_id + ' ' + player_id + '同時')
            return 2, (last_player_id, player_id), False
            '''
        else:
            self.output(player_id + '通過')
            return 1, player_id, True

    def playing_loop(self):
        self.output('開始')
        # init variables
        counter = 1
        alive = set(player_ids)
        loser = set()
        last_time = None
        last_player_id = None
        # actual loop
        while len(alive) > 1:
            try:
                player_id, text, ctime = input().split('  ')
                return_values = self.player_answer(player_id, text, ctime, last_time, last_player_id, counter)
                if return_values[2] is False:
                    if int(return_values[0]) == 2:
                        loser.add(player_id)
                        loser.add(last_player_id)
                    else:
                        loser.add(player_id)
                else:
                    counter += 1
                    # print(counter)
                alive.remove(player_id)
                last_time = ctime
                last_player_id = player_id
            except:
                pass
            # print(alive)
            # print(loser)

        for player_id in loser:
            print(player_id, end=' ')
        for player_id in alive:
            print(player_id, end='')
        print('輸了')


class Connect4():
    def __init__(self):
        print('這個遊戲是四連棋')
        self.game_intro()
        self.player_dict = {num + 1: player_id for num, player_id in enumerate(player_ids)}
        self.playing_loop()

    def game_intro(self):
        print('目標是讓四個子相連')
        print('你可以選擇一個直行(從0開始編碼)，棋會落到該行未有子的最上處')
        print('')  # 帶補充

    game_state = np.zeros((7, 7))

    def show_state(self):
        for i in range(7):
            for j in range(7):
                print(int(self.game_state[i][j]), end='  ')
            print()  # 空一行
            print()
        print('-' * (7 * 2 - 1))

    def choose_pos(self, player):
        inputing = True
        print('該' + str(player) + '了')
        while inputing is True:
            try:
                pos, player_id, __ = input().split('  ')
                if player_id != player:
                    raise ValueError
                pos = int(pos)
                for i in range(7 - 1, 0 - 1, -1):
                    if self.game_state[i][pos] == 0:
                        self.game_state[i][pos] = player
                        break
                else:
                    raise ValueError
                inputing = False
            except:
                print('已經滿了，請重選')

    def check_win(self):  # False表示沒有人連線
        winner = set()
        someone_won = False
        for i in range(7 - 3):  # starting up->down
            for j in range(7):  # lr
                for k in range(i, i + 3):  # 3格
                    if self.game_state[k][j] == 0 or self.game_state[k][j] != self.game_state[k + 1][j]:
                        break
                else:
                    winner.add(self.game_state[i][j])
                    someone_won = True
        for i in range(7 - 3):  # starting left->right
            for j in range(7):  # ud
                for k in range(i, i + 3):  # 3格
                    if self.game_state[j][k] == 0 or self.game_state[j][k] != self.game_state[j][k + 1]:
                        break
                else:
                    winner.add(self.game_state[j][i])
                    someone_won = True
        for i in range(0, 4):
            for j in range(0, 4):
                for k in range(0, 3):  # 3格
                    if self.game_state[i][j] == 0 or self.game_state[i + k][j + k] != self.game_state[i + k + 1][j + k + 1]:
                        break
                else:
                    winner.add(self.game_state[i][j])
                    someone_won = True
        for i in range(3, 3 + 4):
            for j in range(0, 4):
                for k in range(0, 3):  # 3格
                    if self.game_state[i][j] == 0 or self.game_state[i - k][j + k] != self.game_state[i - k - 1][j + k + 1]:
                        break
                else:
                    winner.add(self.game_state[i][j])
                    someone_won = True
        return someone_won, winner

    def rotate(self):
        print('順時鐘轉90度')
        self.game_state = np.fliplr(self.game_state.T)
        for j in range(7):
            n = 7 - 1  # count current non-zero location
            z = 0  # num of zeros
            for i in range(7 - 1, -1, -1):
                if self.game_state[i, j] != 0:
                    self.game_state[n, j] = self.game_state[i, j]
                    n -= 1
                else:
                    z += 1
            self.game_state[0:z, j] = 0

    def playing_loop(self):
        ongoing = True
        counter = 0
        game_steps = 0
        while ongoing is True:
            print(self.player_dict.keys())
            for player in tuple(self.player_dict.keys()):
                self.show_state()
                try:
                    self.choose_pos(player)
                    someone_won, winner = self.check_win()
                    game_steps += 1
                    if someone_won is True:
                        ongoing = False
                        break
                    if game_steps >= 49:
                        print('和局')
                except:
                    pass
            if counter >= 20:
                self.rotate()
                someone_won, winner = self.check_win()
                if someone_won is True:
                    ongoing = False
                counter = 0
            counter += rand.randint(1, 3)

        self.show_state()
        for player_id in winner:
            print(int(player_id), end=' ')
        print('贏了')

    def __del__(self):
        del self.player_dict


if __name__ == '__main__':
    inst = AbcGame()
    inst = Mosquito()
    inst = BambooShoot()
    inst = Connect4()
