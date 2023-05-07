import shogi.Ayane as ayane
import time

# 通常探索用の思考エンジンの接続テスト
# 同期的に思考させる。
def test_ayane1():

    print("test_ayane6 : ")

    server = ayane.MultiAyaneruServer()

    # 並列4対局

    # server.debug_print = True
    server.init_server(1)
    options1 = {
        "USI_Hash": "512",
        "Threads": "2",
        "NetworkDelay": "0",
        "NetworkDelay2": "0",
        "MaxMovesToDraw": "512",
        "MinimumThinkingTime": "0", 
        "NodeLimits": "100000"
    }
    options2 = {
        "USI_Hash": "512",
        "Threads": "2",
        "NetworkDelay": "0",
        "NetworkDelay2": "0",
        "MaxMovesToDraw": "512",
        "MinimumThinkingTime": "0",
        "NodeLimits": "140000"
    }

    # 1P,2P側のエンジンそれぞれを設定して初期化する。
    server.init_engine(0, "exe/YaneuraOu_NNUE-tournament-clang++-avx2.exe", options1)
    server.init_engine(1, "exe/YaneuraOu_NNUE-tournament-clang++-avx2.exe", options2)

    # 持ち時間設定。
    # server.set_time_setting("byoyomi 100")                 # 1手0.1秒
    # server.set_time_setting("byoyomi1p 100 byoyomi2p 200") # 1P側、1手0.1秒　2P側1手0.2秒
    server.set_time_setting("time 6000000")
    # これで対局が開始する
    server.game_start()

    # 10試合終了するのを待つ
    last_total_games = 0

    # ゲーム数が増えていたら、途中結果を出力する。
    def output_info():
        nonlocal last_total_games, server
        if last_total_games != server.total_games:
            last_total_games = server.total_games
            print(server.game_info())

    # 10局やってみる。
    while server.total_games < 2:
        # 評価値と棋譜を出力してみる。
        print(
            "game_ply = ", server.servers[0].game_ply, 
        )
        output_info()
        time.sleep(1)
    output_info()

    server.game_stop()

    # 対局棋譜の出力
    # 例えば100局やるなら
    # "17 - 1 - 82(17.17% R-273.35[-348.9,-197.79]) winrate black , white = 48.48% , 51.52%"のように表示される。(はず)
    for kifu in server.game_kifus:
        print(
            f"game sfen = {kifu.sfen} , "
            f"flip_turn = {kifu.flip_turn} , "
            f"game_result = {str(kifu.game_result)} , "
            f"is_player1_win = {kifu.is_player1_win}"
        )

    server.terminate()

if __name__ == "__main__":
    test_ayane1()