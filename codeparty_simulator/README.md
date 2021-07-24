

## Helperクラス
- helper.get_enemy_players(name):
    - 他のplayersクラスのリストを返す
- helper.get_tiles():
    - タイルを3次元配列で取得する。
- helper.get_players():
    - playerクラスのリストを返す
- helper.get_enemy_players(name):
    - name以外のplayerクラスのリストを返す
- helper.get_my_player(name):
    - 自分のplayerクラスを返す。
- helper.get_my_point(name):
    - 自分の座表を返す。
- helper.get_distance_points_from_me(name):
    - 自分から見て他プレイヤーとの距離のリストを返す。
- helper.get_distance_points_from_point(point):
    - 特定の座標から各プレイヤーとの距離のリストを返す。
- helper.get_XX_tile(name):
    - 自分の位置からXXに位置するタイルクラスを返す
- helper.get_turn_num():
    - ターン数を取得する
- helper.get_toward_distination(from_point, dist_point):
    - from_pointからdist_pointに向かうときに向かうべき方向を返す。tileの有無は考慮しない
- helper.get_before_action(name):
    - 特定のプレイヤーの前回の行動を取る
- get_around_tiles(name):
    - 特定のプレイヤーのタイル一覧を配列で取得する。上下左右の順

## Tileクラス
- tile.get_is_alive():
    - タイルが利用可能かどうか true or false

## Playerクラス
- player.name
    - 名前を取得する
- player.point
    - 座標を取得する
- player.is_alive
    - 生きているかどうかを取得する　true or False
- player.before_action
    - 前回の行動を取得する