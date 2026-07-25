# 💊 PharmaSense — Pharma Sales Analytics + AI Assistant

A mini analytics dashboard for pharma sales data (sales reps, doctors,
territories, products) with a natural-language "Ask AI" feature that
converts plain English questions into SQL queries and returns answers.

Built as a placement project — synthetic data only.

---

## 1. What this project does

- Generates a small SQLite database of **fake but realistic** pharma sales
  data: sales reps, doctors (HCPs), territories, products, and transactions.
- Displays it in an interactive **Streamlit** dashboard: revenue by
  territory, top products, top reps, sales trend over time, and a raw
  data explorer with CSV export.
- Adds a **Gen AI** feature: type a question like *"Which territory sold
  the most CardioEase?"*, and the app uses an LLM (Google Gemini, free
  tier) to write the SQL query for you, run it, and show the answer.

## 2. Tech stack (all free/beginner-friendly)

| Layer | Tool | Why |
|---|---|---|
| Data | SQLite | No server needed, built into Python |
| Backend logic | Python | `sqlite3`, `pandas` |
| Frontend/UI | Streamlit | Full working web app in pure Python — no HTML/CSS/JS needed |
| Charts | Plotly | Interactive charts with one line of code each |
| AI | Google Gemini API (free tier) | Turns English questions into SQL |
| Deployment | Streamlit Community Cloud | Free hosting, one click from GitHub |

## 3. How to run it locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create the database (only need to do this once)
python init_db.py

# 3. Launch the app
streamlit run app.py
```

It will open in your browser at `http://localhost:8501`.

For the "Ask AI" tab, get a **free** Gemini API key at
https://aistudio.google.com/apikey and paste it into the sidebar.

## 4. How to deploy it for free (so you have a live link)

1. Push this folder to a GitHub repo.
2. Go to https://share.streamlit.io, sign in with GitHub.
3. Click "New app", pick your repo, set the main file to `app.py`.
4. Deploy — you'll get a public URL like `yourname-pharmasense.streamlit.app`.

Having a **live link** (not just code) is a big plus in interviews —
open it on your phone to show it working.

---

## 5. How to explain this in your interview

**"Walk me through your project" — 60 second version:**

> "I built PharmaSense, a mini sales analytics tool modeled on how
> pharma companies like P360 manage sales operations data — reps,
> doctors, territories, and products. It's a SQLite database with
> normalized tables joined together, a Streamlit dashboard that
> visualizes revenue and performance with filters, and a natural
> language query feature where I use an LLM to convert an English
> question into SQL, run it against the database, and show the result.
> I deployed it on Streamlit Cloud so it's live."

**Be ready for these follow-ups (and honest, simple answers):**

- *"Why SQLite and not MySQL/Postgres?"*
  → "For a quick project, SQLite needs no server setup — it's a single
  file. In a production system I'd use something like PostgreSQL or
  MySQL, which is what I understand P360 works with alongside SFA
  tools like Veeva."

- *"Explain your database schema."*
  → Walk through the 5 tables (territories, reps, hcps, products,
  sales) and how they're joined via foreign keys. Practice drawing
  this on paper.

- *"How does the AI question-answering actually work?"*
  → "I send the database schema and the user's question as a prompt
  to Gemini, ask it to return only a SQL query, then I execute that
  query with `pandas.read_sql_query()` and display the result. I don't
  let it run arbitrary queries against a production database without
  validation — that's a real security consideration (SQL injection),
  which I'd handle with query allow-listing or a read-only DB user in
  a real system."
  (Mentioning this shows awareness beyond just "it works" — good signal.)

- *"What would you improve given more time?"*
  → Authentication/login, real-time data pipeline, better error
  handling on bad AI-generated SQL, role-based access (rep vs. manager
  view), unit tests.

- *"Why does this relate to what P360 does?"*
  → P360's own products (Activate, Automate) are about unified sales
  data intelligence and AI-powered insights/workflows — this project
  is a small-scale version of exactly that idea.

---

## 6. What to practice before the 27th (given your starting point)

Since you're new to coding, don't just memorize this code — be able to
**read and explain every part of it**, and be able to make small
changes live if asked (e.g., "add a filter for HCP specialty" or
"add average revenue per transaction"). That's what interviewers
actually probe for, more than the polish of the final product.

Suggested daily practice:
1. Type out (don't copy-paste) `init_db.py` yourself, line by line,
   understanding each part.
2. Do the same with `app.py`.
3. Try breaking it, then fixing it — that builds real understanding.
4. Practice the 60-second pitch above out loud.
5. Review basic SQL (`SELECT`, `JOIN`, `GROUP BY`, `WHERE`) since
   that's both in your project and on the aptitude test.
6. Skim a "Python basics in 1 hour" tutorial/video — variables,
   functions, lists, dictionaries, loops, `import`.
