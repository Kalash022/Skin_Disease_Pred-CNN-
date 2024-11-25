from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
from keras.preprocessing import image
import tensorflow as tf
from io import BytesIO
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Load the model
model = tf.keras.models.load_model('model/model_87.keras')

# Define lesion names and resource links
lesion_names = [
    'Melanocytic nevi', 'Melanoma', 'Benign keratosis-like lesions',
    'Basal cell carcinoma', 'Actinic keratoses', 'Vascular lesions',
    'Dermatofibroma'
]

lesion_resources = {
    "Melanocytic nevi": "https://www.skincancer.org/skin-cancer-information/moles/",
    "Melanoma": "https://www.cancer.org/cancer/melanoma-skin-cancer.html",
    "Benign keratosis-like lesions": "https://www.aad.org/public/diseases/a-z/keratosis-pilaris-overview",
    "Basal cell carcinoma": "https://www.cancer.org/cancer/basal-cell-carcinoma.html",
    "Actinic keratoses": "https://www.skincancer.org/skin-cancer-information/actinic-keratosis/",
    "Vascular lesions": "https://www.ncbi.nlm.nih.gov/books/NBK558940/",
    "Dermatofibroma": "https://dermnetnz.org/topics/dermatofibroma/"
}

# Verify the number of classes
num_classes = model.output_shape[-1]
if len(lesion_names) != num_classes:
    raise ValueError(f"Expected {num_classes} lesion names, but got {len(lesion_names)}")

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('upload_file'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('upload_file'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        file = request.files['file']
        if file:
            # Validate file type
            if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                flash('Invalid file type. Please upload a PNG, JPG, or JPEG image.')
                return redirect(url_for('upload_file'))

            # Process the image
            img_bytes = BytesIO(file.read())
            img = image.load_img(img_bytes, target_size=(100, 100))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)

            # Predict the image
            predictions = model.predict(img_array)
            score = tf.nn.softmax(predictions[0])

            # Get prediction results
            predicted_index = np.argmax(score)
            predicted_lesion = lesion_names[predicted_index]
            confidence = 100 * np.max(score)
            resource_link = lesion_resources[predicted_lesion]

            result = {
                "lesion": predicted_lesion,
                "confidence": confidence,
                "resource_link": resource_link
            }

            # Encode image for display
            img_bytes.seek(0)
            img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')

            return render_template(
                'result.html',
                lesion=result['lesion'],
                confidence=round(float(result['confidence']), 2),
                resource_link=result['resource_link'],
                img_data=img_base64
            )

    return render_template('upload.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)