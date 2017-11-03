#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, make_response, redirect, url_for
import ast
import json

def get_question(cookie, spm):
    #returnerer streng med spørsmål og om alle spørsmålene er ferdig
    print(len(cookie), len(spm))
    if len(cookie) >= len(spm):
        print("overflow")
        return ("Alle spørsmål er ferdig", True)
    else:
        sprsm = spm[str(len(cookie))]["spm"]
        return (sprsm, False)

def get_linje(result):
    print("res ", result)
    maxPos = 0
    rng = 5
    for i in range(len(result)):
        if result[maxPos] < result[i]:
            maxPos = i;

    for i in range(len(result)):
        if i != maxPos:
            if abs(result[i]-result[maxPos]) <= rng:
                maxPos = 1
                return maxPos

    return maxPos

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
        resp = make_response(redirect(url_for('resultat')))
        resp.set_cookie("ans", str(cookie))
        return resp
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
    #ans = [1,1,1,1,0,0,1,1,0,0,0]
    print(ans)

    with open("svar.json", "r") as f:
        svarFile = json.load(f)
    svar = svarFile["svar"]

    result = [0,0,0,0,0,0]

    with open("spm.json", "r") as f:
        spmFile = json.load(f)

    for i in range(len(ans)):
        vekt = spmFile[str(i)]["vekt"]
        print(i)
        print(ans)
        for j in range(len(vekt[0])):
            print(" ",j, " ", vekt[ans[i]][j])
            result[j] += vekt[ans[i]][j]



    linje = svar[get_linje(result)]

    return render_template("resultat.html", linje = linje)

if __name__ == "__main__":
    app.run(debug=True)
