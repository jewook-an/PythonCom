from flask import Flask, render_template, request, redirect, send_file
from extractors.wwr import extract_wwr_jobs
from file import save_to_file

app = Flask("JobScrapper")
db = {} # 데이터베이스

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/search")
def search():
  keyword = request.args.get("keyword")
  if keyword == None: # 키워드 미입력 시
    return redirect("/")
  if keyword in db: # 키워드가 데이터베이스에 있으면
    jobs = db[keyword]
  else: # 키워드가 데이터베이스에 없으면
    print(keyword)
    wwr = extract_wwr_jobs(keyword)
    print(wwr)
    jobs = wwr
    db[keyword] = jobs # 스크랩 해온 데이터 -> 데이터베이스
  return render_template("search.html", keyword = keyword, jobs=jobs)

@app.route("/export") # 데이터 다운로드
def export():
  keyword = request.args.get("keyword")
  if keyword == None:
    return redirect("/")
  if keyword not in db:
    return redirect(f"/search?keyword={keyword}")
  save_to_file(keyword, db[keyword])
  return send_file(f"{keyword}.csv", as_attachment=True)

# app.run("0.0.0.0")

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)