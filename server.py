from api.PDFchatbot import PDFChatbot
from flask import Flask,render_template,redirect,request,flash
from flask_cors import CORS
from dotenv import load_dotenv
import os
import uuid
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = "dffergergeg45t54tgfhfghhtyhhhtyhhyhyh"
CORS(app)

bot = PDFChatbot()

@app.route("/",methods = ["GET",'POST'])
def index():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        pdf_file = request.files.get("pdf_file")
        os.makedirs("./pdfs", exist_ok=True)
        filename = f"pdfs/{str(uuid.uuid4())}.pdf"
        pdf_file.save(filename)
        pdf_file.close()
        bot.loadPDF(filename)
        if os.path.exists(filename):
            os.remove(filename)
        return redirect("/chatbot")


@app.route("/chatbot")
def chatbot():
    if bot.qa:
        return render_template("chatscreen.html")
    else:
        flash("Please upload PDF first")
        return redirect("/")


@app.route("/ask",methods = ["POST"])
def asktoBot():
    query = request.form.get("query")
    print(query)
    answer = bot.ask(query)
    return answer.get("result","Unable to answer")

if __name__ == "__main__":
    app.run(debug=True)


