#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, make_response, redirect, url_for
import ast
import json


def get_question(cookie, spm):
    #returnerer streng med spørsmål
    print(len(cookie), len(spm))
    if len(cookie) >= len(spm):
        print("overflow")
        return (redirect(url_for('resultat')), True)
    else:
        sprsm = spm[str(len(cookie))]["spm"]
        return (sprsm, False)

def answers_done(spm, cookie):
    #returnerer bool om lenden på cookien er like lang som antall spørsmål
    if len(cookie) >= len(spm):
        return True
    else:
        return False

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    with open("spm.json", "r") as f:
        spmFile = json.load(f)

    if request.method == "POST":
        cookie = ast.literal_eval(request.cookies.get("ans"))
        print(cookie)
        print(request.form["submit"])
        if request.form["submit"] == "Ja":
            answer = 1
        elif request.form["submit"] == "Nei":
            answer = 0
        cookie.append(answer)
    elif request.method == "GET":
        cookie = []


    spm, done = get_question(cookie, spmFile)

    if done:
        return redirect(url_for('resultat'))
    else:
        resp = make_response(render_template("quiz.html", spm=spm))
        resp.set_cookie("ans", str(cookie))
        return resp


@app.route('/resultat')
def resultat():
    #må regne ut riktig linje og lagre linjen som variabelet linje
    cookie = ast.literal_eval(request.cookies.get("ans"))
    print(cookie)

    ans = cookie
    #ans = [1,1,1,1,0,0,1,1,1,1]

    svar = ["svar 1", "svar 2","svar 3","svar 4","svar 5","svar 6"]

    result = [0,0,0,0,0,0]

    with open("spm.json", "r") as f:
        spmFile = json.load(f)

    for i in ans:
        vekt = spmFile[str(i)]["vekt"]
        for j in range(len(vekt[0])):
            print(j)
            result[j] += vekt[ans[j]][j]

    maxPos = 0
    for i in range(len(result)):
        print(maxPos,i)
        if result[maxPos] < result[i]:
            maxPos = i;

    linje = svar[maxPos]

    return render_template("resultat.html", linje = linje)

if __name__ == "__main__":
    app.run(debug=True)
