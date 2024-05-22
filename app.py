from app_initialization import create_app
import ssl


app = create_app()

if __name__ == '__main__':
    # httpsでの実行はpython app.pyで実行
    # app.run(ssl_context="adhoc")
    app.run()
