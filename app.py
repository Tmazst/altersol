
from flask import Flask,render_template,url_for,redirect,request,flash,jsonify,send_from_directory
from flask_login import login_user, LoginManager,current_user,logout_user, login_required
from Forms import Register, Login,Contact_Form, Project_Form, Web_Design_Brief,Logo_Options,Poster_Options,Brochure_Options,Flyer_Options
from models import *
from flask_bcrypt import Bcrypt
import secrets
import os
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
# from bs4 import BeautifulSoup as bs
from flask_colorpicker import colorpicker
import glob



#Did latest commit with the requirement file

#Change App
app = Flask(__name__)
app.config['SECRET_KEY'] = "sdsdjfe832j2rj_32j"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///altersol_db.db"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle':280}
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOADED"] = 'static/uploads'

db.init_app(app)

application = app

login_manager = LoginManager(app)

# Log in
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


ALLOWED_EXTENSIONS = {"txt", "xlxs",'docx', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Function to check if the file has an allowed extension
def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def process_file(file):

        filename = secure_filename(file)

        _img_name, _ext = os.path.splitext(file.filename)
        gen_random = secrets.token_hex(8)
        new_file_name = gen_random + _ext

        if file.filename == '':
            return 'No selected file'

        if file.filename and allowed_files(file):
            file_saved = file.save(os.path.join(app.config["UPLOADED"],new_file_name))
            flash(f"File Upload Successful!!", "success")
            return new_file_name

        else:
            return f"Allowed are [.txt, .xls,.docx, .pdf, .png, .jpg, .jpeg, .gif] only"

def createall(db_):
    db_.create_all()

encry_pw = Bcrypt()

@app.context_processor
def inject_ser():
    # ser = Serializer(app.config['SECRET_KEY'])  # Define or retrieve the value for 'ser'
    # count_jobs = count_ads()

    return dict()



# Function to retrieve all image files from a directory
def get_all_images_from_directory( extensions=("*.jpg", "*.png", "*.jpeg")):
    """
    Retrieve all image files from the specified directory.

    Args:
        directory_path (str): Path to the directory containing images.
        extensions (tuple): List of file extensions to look for (default: jpg, png, jpeg).

    Returns:
        list: List of file paths for images in the directory.
    """

    directory_path = os.path.join(app.root_path, 'static/partners')

    image_files = []
    
    for ext in extensions:
        image_files.extend(glob.glob(os.path.join('static/partners', ext)))
    
    return image_files


@app.route("/", methods=['POST','GET'])
def home():

    contact_form = Contact_Form()

    partners_imgs = get_all_images_from_directory()

    # if request.method == "POST":
    #     if contact_form.validate_on_submit():
    #         mail_enqueries(contact_form)
    #     else:
    #         return flash("Ooops!! Please be sure to fill both email & message fields, correctly","error")

    return render_template("index.html",contact_form=contact_form,partners_imgs=partners_imgs)

@app.route("/contact_us", methods=['POST','GET'])
def contact_us():
    
        contact_form = Contact_Form()
    
        if request.method == "POST":
            if contact_form.validate_on_submit():
                mail_enqueries(contact_form)
            else:
                return flash("Ooops!! Please be sure to fill both email & message fields, correctly","error")
    
        return jsonify({"status": "success", "message": "Form submitted successfully!"})


def mail_enqueries(contact_form):

    def send_link():
        app.config["MAIL_SERVER"] = "techxolutions.com"
        app.config["MAIL_PORT"] = 465
        app.config["MAIL_USE_TLS"] = True
        em = app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_INFO")
        app.config["MAIL_PASSWORD"] = os.environ.get("TX_PWD")

        mail = Mail(app)

        msg = Message(contact_form.subject.data, sender=contact_form.email.data, recipients=[em])
        msg.body = f"""{contact_form.message.data}\n
{contact_form.email.data}\n
<p style="font-size:25px;color:red">This is a Test</p>
                    """
        # try:
        mail.send(msg)
        flash("Your Message has been Successfully Sent!!", "success")
        return f"Email Sent Successfully"
        # except Exception as e:
        #     flash(f'Ooops Something went wrong!! Please Retry', 'error')
        #     return f"The mail was not sent"

        # Send the pwd reset request to the above email
    send_link()

@app.route("/recruitment")
def recruitment():

    return render_template("job_advert.html")

@app.route('/download/job-advert')
def download_job_advert():
    print("Downolading Advert: ",request.remote_addr)
    return send_from_directory(
        directory='static/recruitment',
        path='Q-Messanger_Job_advert_Marketing_Intern.pdf',
        as_attachment=True,
        mimetype='application/pdf'
    )


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
