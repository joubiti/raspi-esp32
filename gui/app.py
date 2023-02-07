from flask import Flask, request, render_template, send_file,send_from_directory, make_response
import os
import shutil

app = Flask(__name__)

file_path = r"C:\Users\pc\Desktop\trac bal\internshipJB\TracBal\src\main.cpp"
bin_path = r"C:\Users\pc\Desktop\trac bal\internshipJB\TracBal\.pio\build\az-delivery-devkit-v4\firmware.bin"
target_bin_path = r"C:\Users\pc\Desktop\gui\firmware\firmware.bin"
path_to_auth = r"auth/64E7F0D15B9C950715520B90C5131090.txt"

version = 0

@app.route('/', methods=['GET', 'POST'])
def index():
    global version
    if request.method == 'POST':
        frequency = request.form['frequency']
        with open(file_path, 'r') as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            if "#define LED_FREQUENCY" in line:
                lines[i] = "#define LED_FREQUENCY " + frequency + "\n"
                break
        with open(file_path, 'w') as file:
            file.writelines(lines)
        os.chdir("C:\\Users\\pc\\Desktop\\trac bal\\internshipJB\\TracBal")
        os.system("pio run -t clean")
        os.system("pio run")
        shutil.copyfile(bin_path, target_bin_path)
        version+=1
        return send_file(target_bin_path, as_attachment= True)
    return '''
        <form method="post">
            LED Frequency: <input type="text" name="frequency"><br>
            <input type="submit" value="Update LED Frequency">
        </form>
    '''
@app.route('/flash', methods=['GET', 'POST'])
def flash():
    if request.method == 'POST':
        file_path = request.form['file_path']
        port = request.form['port']
        command = "esptool.py --chip esp32 --port " + port + " --baud 921600 write_flash -z 0x1000 " + file_path
        return command
    return '''
        <form method="post">
            File Path: <input type="text" name="file_path"><br>
            Port: <input type="text" name="port"><br>
            <input type="submit" value="Flash">
        </form>
    '''

@app.route('/serial', methods=['GET', 'POST'])
def serial():
    if request.method== 'POST':
        file_path = request.form['file_path']
        port = request.form['port']
        return render_template('flash.html', file_path=file_path, port=port)
    return render_template('flash.html')

@app.route('/firmware/<path:filename>', methods=['GET'])
def get_firmware(filename):
    global version
    response = make_response(send_from_directory('firmware', filename, as_attachment= True))
    response.headers['X-Version'] = version
    return response

@app.route('/.well-known/pki-validation/<path:filename>', methods=['GET'])
def get_auth(filename):
    return send_from_directory('auth', filename, as_attachment= True)

if __name__ == '__main__':
    app.run(debug= True, host='0.0.0.0')
