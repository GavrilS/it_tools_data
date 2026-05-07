from flask import Flask, request, render_template_string, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# 1. Define the metrics
# We use 'labels' to group the metric by animal type
ANIMAL_VOTES = Counter('favorite_animals_total', 'Total number of animal submissions', ['animal_type'])\

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<body style="font-family: sans-serif; margin: 40px;">
    <h2>Кое е любимото ти животно?</h2>
    <form method="POST">
        <input type="text" name="animal" placeholder="напр. Котка" required>
        <button type="submit">Изпрати</button>
    </form>
    {% if animal %}
        <p>Твоето любимо животно е: <strong>{{ animal }}</strong>! 🐾</p>
    {% endif %}
    <br>
    <small><a href="/metrics">Виж метриките за Prometheus</a></small>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def favorite_animal():
    animal = None
    if request.method == 'POST':
        animal = request.form.get('animal').strip().lower()
        if animal:
            # 2. Increment the metric with the appropriate label
            ANIMAL_VOTES.labels(animal_type=animal).inc()
    
    return render_template_string(HTML_TEMPLATE, animal=animal)

# 3. Export the metrics endpoint
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(port=5000)
