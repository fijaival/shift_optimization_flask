# シフト自動生成 API

## 導入

このプロジェクトは、従業員のスキルセット、利用可能性、およびその他の制約を考慮して、効率的にシフトを自動生成する API を提供します。Flask をバックエンドフレームワークとして、SQLite をデータベースとして使用しています。

## 目次

- [導入](#導入)
- [機能](#機能)
- [始め方](#始め方)
  - [前提条件](#前提条件)
  - [インストール](#インストール)
  - [開発サーバ起動](#開発サーバ起動)
- [API エンドポイント](#apiエンドポイント)
- [依存関係](#依存関係)
- [参考サイト](#参考サイト)
- [API リクエストボディ](#リクエストボディ)

## 機能

- 従業員の利用可能性に基づいたシフト自動生成
- スキルセットと役割に基づくシフト割り当て
- シフトの調整と更新機能
- 従業員と管理者のためのインターフェース

## 始め方

### 前提条件

- Python 3.12.0 で動作確認済み
- pip

### インストール

リポジトリをクローンします。

```bash
git clone https://github.com/fijaival/shift_optimization_flask.git
cd shift_optimization_flask
```

python 仮想環境を構築し、環境を切り替えます。[参考](https://www.python.jp/install/windows/venv.html)

```
python -m venv .venv
.venv\Scripts\activate.bat
```

パッケージをインストールします。

```
pip install -r requirements.txt
```

### 開発サーバ起動

アプリケーションを起動します。

```
flask run
```

## API エンドポイント

- /api/v1
- `/users`
  - GET: 全ユーザ情報取得
- `/signin`
  - POST: ユーザ登録
- `/login`
  - POST: ログイン
- `/refresh`
  - POST: リフレッシュトークンによるアクセストークンの再発行
- `/logout`

  - DELETE: ログアウト

- `/dependencies`

  - GET: 全依存関係の取得
  - POST: 依存関係の追加
  - `/<int:dep_id>`
    - PUT: 特定の依存関係の更新
    - DELETE: 特定の依存関係の削除

- `/drivers`

  - GET: 全ドライバーの取得
  - POST: ドライバーの追加
  - `/<int:driver_id>`
    - PUT: 特定のドライバーの更新
    - DELETE: 特定のドライバーの削除

- `/drivers_requests`

  - POST: 希望シフト追加
  - `/<int:request_id>`
    - DELETE: 特定の希望シフトの削除
  - `/<int:year>/<int:month>`
    - GET: 特定の月のシフト希望取得

- `/employees_qualifications`

  - GET: 全資格情報の取得
  - POST: 資格情報の追加
  - `/<int:eq_id>`
    - DELETE: 特定の資格情報の削除

- `/employees_restrictions`

  - GET: 全制約条件の取得
  - POST: 制約条件の追加
  - `/<int:er_id>`
    - DELETE: 特定の制約条件の削除
    - PUT: 特定の制約条件の更新

- `/employees`

  - GET: 全授業院のすべての情報を取得
  - POST: 授業院の追加
  - '/<int:employee_id>'
    - GET: 特定の従業員の情報を取得
    - DELETE: 従業員の削除
    - PUT: 特定の従業員情報の更新

- `/qualifications`

  - GET: 全資格名の取得
  - POST: 資格の追加
  - '/<int:qual_id>'
    - DELETE: 資格の削除

- `/restrictions`

  - GET: 全制約条件名の取得
  - POST: 制約条件の追加
  - '/<int:res_id>'
    - DELETE: 制約条件の削除

- `/shift_generation/<int:year>/<int:month>`

  - GET: 特定の月のシフトを自動生成し、結果を返す

- `/shifts`

  - POST: 作成したシフトの登録
  - PUT: 勤務情報の更新
  - '/<int:year>/<int:month>'
    - GET: 特定の年月のシフトを一か月分取得
    - DELETE: 特定の年月の勤務情報をまとめて削除

- `/shifts_requests`
  - POST: シフト希望の登録
  - '/<int:year>/<int:month>'
    - GET: 特定の年月のシフト希望を一か月分取得
  - '/<int:request_id>'
    - DELETE: 特定の年月の勤務情報をまとめて削除

## 依存関係

プロジェクトの依存関係は requirements.txt にリストされています。

## 参考サイト

https://devlog.grapecity.co.jp/python-flask-web-api/<br>
https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/tutorial/layout.html<br>
https://menta.work/post/detail/3638/7PiI6kAHGQJbQTAbWjlJ<br>

## リクエストボディ

<br>

POST /qualifications

```
{
"name":"日勤相談員"
}
```

POST /restrictions

```
{
"name":"連続勤務"
}
```

POST /employees

```
{
    "last_name": "龍馬",
    "first_name": "坂本",
    "qualifications":[5],
    "restrictions":[{"id":1,"value":3}
    ],
    "dependencies":[6]
}
```

POST /employees_restrictions

```
{
    "employee_id":1,
    "restriction_id":"1",
    "value":4,
    "name":"夜勤の連続回数"
}
```

POST /employees_qualifications

```
{
    "employee_id":1,
    "qualification_id":1,
    "name":"全部休み"
}
```

POST /dependencies

```
{
"dependent_employee_id":1,
"first_name": "信長",
"last_name": "織田",
"required_employee_id": 3
}
```

POST /drivers

```
{
    "last_name": "光秀",
    "first_name": "明智"
}
```

POST /shifts_requests

```
[{"employee_id": 1, "date": "2023-11-03", "type_of_vacation": "公"},
 {"employee_id": 1, "date": "2023-11-04", "type_of_vacation": "公"},
 {"employee_id": 1, "date": "2023-11-10", "type_of_vacation": "公"}]
```

POST /drives_requests

```
[{"driver_id": 1, "date": "2023-11-03", "type_of_vacation": "公"},
 {"driver_id": 1, "date": "2023-11-04", "type_of_vacation": "公"},
 {"driver_id": 1, "date": "2023-11-10", "type_of_vacation": "公"}]
```
