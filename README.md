# problem-template-python
## これは何？

[進化計算コンペティション](https://ec-comp.jpnsec.org/)出題問題のPythonプログラムのテンプレートです．

## 出題者が行うタスク
### タスク一覧

出題者が問題プログラムを実装するにあたって行うことが想定されるタスク一覧です．
学習コストや作業コスト，タスク自体の必要性を鑑み，各タスクに参考として次のような優先度が設けてあります．

* 高 (しなければならない)
    * コンペティションシステム上で動作するために必要なタスクです．
* 中 (するべき)
    * 基本的に行うべきですが，動作には必要ではないタスクです．
* 低 (するとよい)
    * 行うことで開発や動作検証をしやすくできますが，動作には必要ではないタスクです．学習/作業コストが大きいと判断される場合は，タスクをオミットしても構いません．

| タスク                                  | 優先度 | 関連するツール/サービスの例 |
| :-------------------------------------- | :----: | :-------------------------- |
| 解評価の実装                            |   高   |                             |
| Docker Image化                          |   高   | Docker, Docker Hub          |
| READMEの作成                            |   中   |                             |
| 入力の検証                              |   中   | JSON Schema                 |
| テストコードの作成                      |   中   | unittest, pytest            |
| リンターやフォーマッタ                  |   低   | flak8, mypy, black, isort   |
| 型ヒント                                |   低   |                             |
| ロギング                                |   低   |                             |
| ビルド/テストツール                     |   低   | make, tox                   |
| CI/CD                                   |   低   | Github Actions, Travis CI   |
| 高度なパッケージ/プロジェクト管理ツール |   低   | Pipenv, Poetry, Rye         |


### 各タスク詳細

