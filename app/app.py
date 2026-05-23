from flask import Flask, render_template, request, redirect, url_for
from models import ItemModel

app = Flask(__name__)
model = ItemModel()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task = request.form.get('task')
        if task:
            # Добавляем задачу в БД
            conn = model.get_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO items (name) VALUES (%s)', (task,))
            conn.commit()
            cursor.close()
            conn.close()
        return redirect(url_for('index'))
    
    items = model.get_all_items()
    return render_template('index.html', items=items)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
