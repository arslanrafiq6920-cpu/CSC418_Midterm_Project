from flask import Flask, request, render_template_string
from urllib.parse import urlparse

app = Flask(__name__)
submissions = []

PAGE = """
<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Assignment Submission Portal</title>
<style>
body{font-family:Arial,sans-serif;background:#111827;color:#f9fafb;max-width:850px;margin:35px auto;padding:0 18px}
main{background:#1f2937;padding:24px;border-radius:14px} label{display:block;margin-top:14px}
input{box-sizing:border-box;width:100%;padding:11px;margin-top:6px;border:1px solid #4b5563;border-radius:7px;background:#111827;color:white}
button{margin-top:18px;padding:11px 17px;background:#2563eb;color:white;border:0;border-radius:7px;cursor:pointer}
.error{color:#fca5a5}.success{color:#86efac}li{margin:12px 0;overflow-wrap:anywhere}
</style></head>
<body><main><h1>Assignment Submission Portal</h1>
<p>Enter your details and a link to your assignment.</p>
{% if message %}<p class="{{ 'error' if error else 'success' }}">{{ message }}</p>{% endif %}
<form method="post">
<label>Student name<input name="name" value="{{ values.get('name','') }}"></label>
<label>Registration number<input name="registration_number" value="{{ values.get('registration_number','') }}"></label>
<label>Assignment title<input name="assignment_title" value="{{ values.get('assignment_title','') }}"></label>
<label>Submission URL<input name="submission_url" value="{{ values.get('submission_url','') }}" placeholder="https://example.com/my-assignment"></label>
<button type="submit">Submit assignment</button></form>
<h2>Saved submissions ({{ submissions|length }})</h2>
{% if submissions %}<ol>{% for s in submissions %}<li><strong>{{ s.name }}</strong> — {{ s.registration_number }} — {{ s.assignment_title }} — <a href="{{ s.submission_url }}" style="color:#93c5fd" target="_blank" rel="noopener">Open submission</a></li>{% endfor %}</ol>{% else %}<p>No submissions yet.</p>{% endif %}
</main></body></html>
"""

def valid_url(value):
    parsed = urlparse(value or "")
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)

@app.route("/", methods=["GET", "POST"])
def index():
    message, error, values = "", False, {}
    if request.method == "POST":
        values = {key: request.form.get(key, "").strip() for key in
                  ("name", "registration_number", "assignment_title", "submission_url")}
        missing = [key for key in ("name", "registration_number", "assignment_title", "submission_url") if not values[key]]
        if missing:
            message, error = "Please complete all required fields.", True
        elif not valid_url(values["submission_url"]):
            message, error = "Please enter a valid http:// or https:// submission URL.", True
        else:
            submissions.append(values.copy())
            message = "Assignment submitted successfully."
            values = {}
    return render_template_string(PAGE, submissions=submissions, message=message, error=error, values=values)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
