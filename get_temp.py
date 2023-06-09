import subprocess, datetime, json
import time, os

# 保存ファイル名を決定
basedir = os.path.dirname(os.path.abspath(__file__))
now = datetime.datetime.now()
fname = basedir + now.strftime(r'/%Y-%m-%d.json')
dt = now.strftime('%Y-%m-%d %H:%M:%S')

# ラズパイコマンドで実行して標準出力を得る
def exec_cmd(param):
    proc = subprocess.run(['vcgencmd', param], stdout=subprocess.PIPE)
    value  = proc.stdout.decode('utf8')
    return value

# CPU温度と電圧を得る
def get_temp():
    # ファイルから既存の値を得る
    data = []
    if os.path.exists(fname):
        with open(fname, encoding='UTF-8') as fp:
            data = json.load(fp)
    # 値を取得
    s = exec_cmd('measure_temp') # 温度
    temp = s.split('=')[1]
    temp = float(temp.replace("C", '').strip())
    s = exec_cmd('measure_volts') # 電圧
    volt = s.split('=')[1]
    volt = float(volt.replace('V', '').strip())
    print(temp, volt)
    # JSONファイルに保存
    data.append({'time':dt, 'temp':temp, 'volt':volt})
    with open(fname, 'w', encoding='UTF-8') as fp:
        json.dump(data, fp)

if __name__ == '__main__':
    get_temp()