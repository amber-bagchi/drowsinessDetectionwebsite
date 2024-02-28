from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['GET'])
def execute_command():
    try:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        bat_file_path = os.path.join(current_dir, 'static', 'execute.bat')
        os.system(bat_file_path)
        return jsonify({'success': True, 'message': 'Command executed successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
