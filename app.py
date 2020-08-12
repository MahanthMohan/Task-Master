from flask import Flask, render_template, redirect, request
from datetime import datetime
import json

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        taskContent = request.form["taskContent"]
        if len(taskContent) == 0:
            return redirect('/')
        else:
            file = open("tasks.json", "r")
            sample_object = json.load(file)
            file.close()

            y = {
                "taskName": taskContent,
                "dateCreated": datetime.now().strftime("%D %H:%M:%S")
            }
            sample_object["tasks"].append(y)

            file = open("tasks.json", "w+")
            json.dump(sample_object, file)
            file.close()
            return redirect('/')
    else:
        f = open("tasks.json", "r")
        taskList = json.load(f)["tasks"]
        f.close()
        return render_template('index.html', taskList=taskList)

@app.route("/delete/<task>")
def delete(task):
    f = open("tasks.json")
    obj = json.load(f)
    f.close()
    for element in obj['tasks']:
        if element["taskName"] == task:
            obj["tasks"].remove(element)
    f = open("tasks.json", "w")
    json.dump(obj, f)
    f.close()
    return redirect("/")

@app.route("/update/<task>", methods=['POST', 'GET'])
def update(task):
    if request.method == "POST":
        taskContent = request.form['taskContent']
        f = open("tasks.json")
        obj = json.load(f)
        f.close()
        for element in obj['tasks']:
            if element["taskName"] == task:
                element["taskName"] = taskContent
                element["dateCreated"] = datetime.now().strftime("%D %H:%M:%S")
        f = open("tasks.json", "w")
        json.dump(obj, f)
        f.close()
        return redirect("/")
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)