from importlib import import_module
from pprint import pprint
from codeparty_simulator.square_drop import Game

class GameController():
    def __init__(self,players):
        self.players = players
        self.log = []

    def start(self):
        game = Game([player.name for player in self.players])
        while True:
            game.next_turn()# タイル更新が入る。前回の行動によってタイルが消える
            helper = game.get_helper() #ヘルパーインスタンスを受け取る
            actions = list()
            for i,player in enumerate(self.players):# playerが行動を決定する
                actions.append(player.action(helper))
            
            new_log = game.get_log()
            for i,action in enumerate(actions):
                new_log["players"][i]["action"] = action


            self.log.append(new_log)# logにgameの情報とactionを書き込む

            pprint(new_log)
            for i,action in enumerate(actions):
                game.do_action(i,action)#ユーザが移動する。前回踏まれているところは消えているので落ちる
            

            if game.is_end():
                #self.log.append(game.get_result_log())
                return self.log
        
    






