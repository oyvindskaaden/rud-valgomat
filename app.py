#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, make_response, redirect, url_for
import ast

def store_answer(answer):
    cookie = ast.literal_eval(request.cookies.get("ans"))
    cookie.append(answer)

    spm = get_question(cookie)

    resp = make_response(render_template("quiz.html", spm=spm))
    resp.set_cookie("ans", str(cookie))
    return resp

def get_question(answers):
    #returnerer streng med spørsmål
    return "streng"

def answers_done():
    #returnerer bool om lenden på cookien er like lang som antall spørsmål
    return False


@app.route('/', methods=['GET', 'POST'])
def index():
    if answers_done():
        # reroute til /resultat
        return redirect(url_for('resultat'))

    elif request.method == "POST":
        print(request.form["submit"])
        if request.form["submit"] == "Ja":
            answer = 1
            resp = store_answer(answer)
            return resp
        elif request.form["submit"] == "Nei":
            answer = 0
            rest = store_answer(answer)
            return resp
    elif request.method == "GET":
        cookie = []

        spm = get_question(cookie)

        resp = make_response(render_template("quiz.html", spm=spm))
        resp.set_cookie("ans", str(cookie))
        return resp

@app.route('/resultat')
def resultat():
    #må regne ut riktig linje og lagre linjen som variabelet linje

    return render_template("resultat.html", linje = linje)

if __name__ == "__main__":
    app.run(debug=True)
