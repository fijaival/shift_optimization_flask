https://devlog.grapecity.co.jp/python-flask-web-api/

[依存関係](https://poyo.hatenablog.jp/entry/2017/01/08/212227)

[進まん](https://qiita.com/keichiro24/items/c72c57b54332431c67ec)

[日本語 flask 公式](https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/tutorial/layout.html)

[MENTA 記事](https://menta.work/post/detail/3638/7PiI6kAHGQJbQTAbWjlJ)
仮想環境の構築
powershell ではまず

```
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

その後

```
.venv\Scripts\activate
```

API リクエストボディ<br>

POST /restrictions

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
    "last_name": "中田",
    "first_name": "正弘",
    "qualifications":[5],
    "restrictions":[
    ],
    "dependencies":[]
}
```

POST /employees_restrictions

```
{
    "employee_id":1,
    "restriction_id":"1",
    "value":4
}
```

POST /dependencies

```
{
    "dependent_employee_id":6,
    "required_employee_id":12
}
```
