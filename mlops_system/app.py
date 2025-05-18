import os
from flask import Flask, request, jsonify, send_file, render_template

from .auth import requires_auth
from .dataset import upload_dataset, list_datasets, merge_datasets, DATASET_DIR
from .training import train_yolo

app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)


@app.route('/')
def index():
    """Render simple UI."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
@requires_auth
def upload():
    file = request.files.get('file')
    name = request.form.get('name')
    if not file or not name:
        return jsonify({'error': 'file and name required'}), 400
    path = os.path.join('/tmp', file.filename)
    file.save(path)
    upload_dataset(path, name)
    return jsonify({'status': 'uploaded', 'dataset': name})

@app.route('/datasets', methods=['GET'])
@requires_auth
def datasets():
    return jsonify({'datasets': list_datasets()})

@app.route('/datasets/merge', methods=['POST'])
@requires_auth
def merge():
    data = request.json
    names = data.get('names', [])
    fmt = data.get('format', 'zip')
    output = os.path.join('/tmp', f'merged.{fmt}')
    merge_datasets(names, output, fmt)
    return send_file(output, as_attachment=True)

@app.route('/datasets/<name>/train', methods=['POST'])
@requires_auth
def train(name):
    val = float(request.json.get('val_split', 0.2))
    result_dir = train_yolo(name, val_split=val)
    return jsonify({'result_dir': result_dir})

def main():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
