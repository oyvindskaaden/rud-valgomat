#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, make_response, redirect, url_for
import ast
import json

def store_answer(answer, spmFile):
    cookie = ast.literal_eval(request.cookies.get("ans"))
    cookie.append(answer)
    print(cookie)

    spm = get_question(cookie, spmFile)

    resp = make_response(render_template("quiz.html", spm=spm))
    resp.set_cookie("ans", str(cookie))
    return resp

def get_question(answers, spm):
    #returnerer streng med spørsmål
    sprsm = spm[str(len(answers))]["spm"]
    return sprsm

def answers_done(spm):
    #returnerer bool om lenden på cookien er like lang som antall spørsmål
    return False

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    with open("spm.json", "r") as f:
        spmFile = json.load(f)
    if answers_done(spmFile):
        # reroute til /resultat
        return redirect(url_for('resultat'))

    elif request.method == "POST":
        print(request.form["submit"])
        if request.form["submit"] == "Ja":
            answer = 1
            resp = store_answer(answer, spmFile)
            return resp
        elif request.form["submit"] == "Nei":
            answer = 0
            resp = store_answer(answer, spmFile)
            return resp
    elif request.method == "GET":
        cookie = []

        spm = get_question(cookie,spmFile)

        resp = make_response(render_template("quiz.html", spm=spm))
        resp.set_cookie("ans", str(cookie))
        return resp

@app.route('/resultat')
def resultat():
    #må regne ut riktig linje og lagre linjen som variabelet linje

    return render_template("resultat.html", linje = linje)

if __name__ == "__main__":
    app.run(debug=True)
