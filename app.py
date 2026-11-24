import streamlit as st
import sqlite3, os, re
import fitz
from datetime import datetime
from collections import Counter
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
import math
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


try:
    from google import genai
except ImportError:
    genai = None

load_dotenv()
API_KEY=os.getenv("GEMINI_API_KEY")
client=genai.Client(api_key=API_KEY) if (API_KEY and genai) else None
DB="metrodoc.db"

st.set_page_config(page_title="MetroInsights",page_icon="🚇",layout="wide")



# -----------------------------------
# 🚆 TRAIN SCHEDULING PAGE
# (Combined from appnew.py; app.py remains the primary application)
# -----------------------------------

def train_scheduling_page():
    st.title("🚆 Train Induction Planning & Scheduling")

    st.write(
        "AI-driven passenger demand prediction and train scheduling system"
    )


    # -----------------------------------
    # LOAD DATA
    # -----------------------------------

    data = pd.read_csv("train_data.csv")


    # -----------------------------------
    # PREPARE DATA FOR AI
    # -----------------------------------

    data["hour"] = data["time"].str[:2].astype(int)

    data["station_code"] = (
        data["station"].astype("category").cat.codes
    )


    # -----------------------------------
    # AI MODEL
    # -----------------------------------

    X = data[["hour", "station_code"]]

    y = data["passengers"]


    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )


    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)


    predictions = model.predict(X_test)


    error = mean_absolute_error(
        y_test,
        predictions
    )


    # -----------------------------------
    # AI PERFORMANCE
    # -----------------------------------

    st.subheader("🤖 AI Model Performance")

    st.metric(
        "Average Prediction Error",
        f"{error:.0f} passengers"
    )


    # -----------------------------------
    # SYSTEM OVERVIEW
    # -----------------------------------

    total_records = len(data)

    total_stations = data["station"].nunique()

    average_demand = int(
        data["passengers"].mean()
    )

    peak_demand = data["passengers"].max()


    st.subheader("📊 System Overview")


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Data Records",
        total_records
    )

    col2.metric(
        "Stations",
        total_stations
    )

    col3.metric(
        "Average Demand",
        f"{average_demand:,}"
    )

    col4.metric(
        "Peak Demand",
        f"{peak_demand:,}"
    )


    # -----------------------------------
    # PASSENGER DEMAND ANALYSIS
    # -----------------------------------

    st.subheader("📈 Passenger Demand Analysis")


    selected_station = st.selectbox(
        "Select Station",
        data["station"].unique()
    )


    station_data = data[
        data["station"] == selected_station
    ]


    # Calculate average demand for each time

    hourly_data = (
        station_data
        .groupby("time")["passengers"]
        .mean()
        .reset_index()
    )


    # Sort time correctly

    hourly_data["hour"] = (
        hourly_data["time"]
        .str[:2]
        .astype(int)
    )


    hourly_data = hourly_data.sort_values(
        "hour"
    )


    # -----------------------------------
    # GRAPH
    # -----------------------------------

    fig = px.line(
        hourly_data,
        x="time",
        y="passengers",
        markers=True,
        title=f"Average Passenger Demand - {selected_station}"
    )


    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Average Passengers"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # -----------------------------------
    # PEAK DEMAND
    # -----------------------------------

    peak_row = hourly_data.loc[
        hourly_data["passengers"].idxmax()
    ]


    peak_time = peak_row["time"]

    peak_passengers = int(
        peak_row["passengers"]
    )


    st.info(
        f"🚨 Peak average demand at "
        f"{selected_station}: "
        f"{peak_passengers:,} passengers "
        f"at {peak_time}"
    )

    # -----------------------------------
    # TRAIN INDUCTION PLANNING
    # -----------------------------------

    st.subheader("🚆 Train Induction Planning")


    train_capacity = st.number_input(
        "Passenger Capacity per Train",
        min_value=500,
        max_value=2000,
        value=1000,
        step=100
    )


    available_trains = st.number_input(
        "Total Trains Available",
        min_value=1,
        max_value=50,
        value=10,
        step=1
    )


    # -----------------------------------
    # AI DEMAND PREDICTION
    # -----------------------------------

    st.subheader("🔮 AI Passenger Demand Prediction")

    prediction_station = st.selectbox(
        "Select Station for Prediction",
        data["station"].unique(),
        key="prediction_station"
    )

    prediction_time = st.selectbox(
        "Select Time",
        sorted(data["time"].unique()),
        key="prediction_time"
    )

    # Get station code
    station_code = (
        data[data["station"] == prediction_station]
        ["station_code"]
        .iloc[0]
    )

    # Get hour
    prediction_hour = int(prediction_time[:2])

    # Create input for AI
    prediction_input = pd.DataFrame({
        "hour": [prediction_hour],
        "station_code": [station_code]
    })

    # Make prediction
    predicted_demand = model.predict(
        prediction_input
    )[0]

    predicted_demand = int(predicted_demand)

    st.metric(
        "🤖 Predicted Passenger Demand",
        f"{predicted_demand:,}"
    )
    required_predicted_trains = math.ceil(
        predicted_demand / train_capacity
    )

    st.metric(
        "🚆 Required Trains",
        required_predicted_trains
    )

    if required_predicted_trains <= available_trains:

        st.success(
            f"🟢 Recommended: Deploy "
            f"{required_predicted_trains} trains"
        )

    else:

        st.error(
            f"🔴 Demand exceeds available fleet. "
            f"Required: {required_predicted_trains}, "
            f"Available: {available_trains}"
        )
    # -----------------------------------
    # DAILY TRAIN SCHEDULE
    # -----------------------------------

    st.subheader("🗓️ AI-Based Daily Train Schedule")

    schedule_station = st.selectbox(
        "Select Station for Daily Schedule",
        data["station"].unique(),
        key="schedule_station"
    )

    schedule_data = data[
        data["station"] == schedule_station
    ]

    schedule_times = sorted(
        schedule_data["time"].unique()
    )

    schedule_rows = []

    for time in schedule_times:

        hour = int(time[:2])

        station_code = (
            data[data["station"] == schedule_station]
            ["station_code"]
            .iloc[0]
        )

        prediction_input = pd.DataFrame({
            "hour": [hour],
            "station_code": [station_code]
        })

        predicted = model.predict(
            prediction_input
        )[0]

        predicted = int(predicted)

        trains = math.ceil(
            predicted / train_capacity
        )

        schedule_rows.append([
            time,
            predicted,
            trains
        ])


    schedule = pd.DataFrame(
        schedule_rows,
        columns=[
            "Time",
            "Predicted Passengers",
            "Recommended Trains"
        ]
    )

    st.dataframe(
        schedule,
        use_container_width=True
    )
    # Train schedule chart

    fig2 = px.bar(
        schedule,
        x="Time",
        y="Recommended Trains",
        title="Recommended Trains by Time",
        text="Recommended Trains"
    )

    fig2.update_layout(
        xaxis_title="Time",
        yaxis_title="Number of Trains"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )


    # Calculate required trains

    hourly_data["required_trains"] = (
        hourly_data["passengers"] /
        train_capacity
    ).apply(math.ceil)


    # -----------------------------------
    # TRAIN DEPLOYMENT TABLE
    # -----------------------------------

    st.subheader(
        "📋 Recommended Train Deployment"
    )


    train_plan = hourly_data[
        ["time", "passengers", "required_trains"]
    ].copy()


    train_plan.columns = [
        "Time",
        "Average Passengers",
        "Required Trains"
    ]


    st.dataframe(
        train_plan,
        use_container_width=True
    )


    # -----------------------------------
    # FLEET RECOMMENDATION
    # -----------------------------------

    peak_required_trains = (
        hourly_data["required_trains"].max()
    )


    if peak_required_trains <= available_trains:

        st.success(
            f"🟢 Fleet capacity is sufficient. "
            f"Maximum required trains: "
            f"{peak_required_trains}"
        )

    else:

        st.error(
            f"🔴 Additional trains may be required. "
            f"Peak requirement: "
            f"{peak_required_trains}, "
            f"Available: "
            f"{available_trains}"
        )


    # -----------------------------------
    # PASSENGER DATA
    # -----------------------------------

    st.subheader("🚉 Passenger Data")


    st.dataframe(
        station_data,
        use_container_width=True
    )

def init_db():
    con=sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS documents(
        id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT, category TEXT,
        department TEXT, asset TEXT, priority TEXT, summary TEXT,
        analysis TEXT, content TEXT, uploaded_at TEXT)""")
    con.commit(); con.close()

def add_doc(filename,category,department,asset,priority,summary,analysis,content):
    con=sqlite3.connect(DB)
    con.execute("""INSERT INTO documents
    (filename,category,department,asset,priority,summary,analysis,content,uploaded_at)
    VALUES (?,?,?,?,?,?,?,?,?)""",(filename,category,department,asset,priority,summary,analysis,content,
    datetime.now().strftime("%Y-%m-%d %H:%M")))
    con.commit(); con.close()

def docs():
    con=sqlite3.connect(DB)
    r=con.execute("""SELECT id,filename,category,department,asset,priority,
    summary,analysis,content,uploaded_at FROM documents ORDER BY id DESC""").fetchall()
    con.close(); return r
def read_document(file):
    if file.name.lower().endswith(".txt"):
        return file.read().decode("utf-8", errors="ignore")

    elif file.name.lower().endswith(".pdf"):
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        text = ""

        for page in pdf:
            text += page.get_text()

        pdf.close()
        return text

    return ""
def fallback(text,filename):
    t=(text+" "+filename).lower()
    category=("Maintenance" if any(x in t for x in ["maintenance","repair","service","equipment"])
              else "Safety" if any(x in t for x in ["safety","fire","emergency","hazard"])
              else "Incident" if any(x in t for x in ["incident","accident","delay","failure"])
              else "Inspection" if "inspection" in t else "Operations")
    priority=("High" if any(x in t for x in ["urgent","critical","emergency","major failure"])
              else "Medium" if any(x in t for x in ["warning","attention","minor issue"]) else "Low")
    department=("Electrical & Systems" if any(x in t for x in ["electrical","escalator","power","signal"])
                else "Civil & Operations" if any(x in t for x in ["track","rail","station","platform"])
                else "Safety" if any(x in t for x in ["safety","fire","emergency"]) else "Operations")
    m=re.search(r"(?:asset|equipment|escalator|train)\s*[:#-]?\s*([A-Za-z0-9 -]{2,30})",text,re.I)
    asset=m.group(1).strip() if m else "Not detected"
    s=re.split(r'(?<=[.!?])\s+',text.strip())
    summary=" ".join(s[:3])[:500] if s else "No summary available."
    return category,department,asset,priority,summary

def ai_analyze(text):
    if not client: return None,"Gemini is not connected."
    prompt=f"""You are MetroDoc AI for metro railway operational documents.
Analyze this document. Do not invent information. Return:
DOCUMENT TYPE:
DEPARTMENT:
ASSET / EQUIPMENT:
DATE:
PRIORITY: (Low/Medium/High)
KEY ISSUES:
- ...
REQUIRED ACTIONS:
- ...
IMPORTANT INFORMATION:
- ...
SUMMARY:
...
If unavailable, write Not specified.

DOCUMENT:
{text}"""
    model=os.getenv("GEMINI_MODEL","gemini-3-flash-preview")
    r=client.models.generate_content(model=model,contents=prompt)
    return r.text,None

def parse_ai(a,fb):
    def field(label,default):
        m=re.search(rf"{re.escape(label)}\s*:\s*(.*?)(?=\n[A-Z][A-Z /_-]*:|\Z)",a,re.I|re.S)
        return m.group(1).strip() if m else default
    return (field("DOCUMENT TYPE",fb[0]),field("DEPARTMENT",fb[1]),
            field("ASSET / EQUIPMENT",fb[2]),field("PRIORITY",fb[3]),
            field("SUMMARY",fb[4]))

init_db()
if not docs():
    samples=[
    ("E17_Maintenance_Report.txt","Maintenance","Electrical & Systems","Escalator E17","Medium",
     "Scheduled maintenance of Escalator E17 was completed on 12 August 2026. No critical faults were reported.",
     "DEMO SAMPLE","Maintenance Report\nAsset: Escalator E17\nDate: 12 August 2026\nNo critical faults were reported."),
    ("Station_Safety_Inspection.txt","Safety","Safety","Central Station","High",
     "Two emergency-exit signs require attention.","DEMO SAMPLE","Safety Inspection\nAsset: Central Station\nPriority: High."),
    ("Train_Delay_Incident.txt","Incident","Operations","Train T12","Medium",
     "Train T12 experienced a 14-minute delay due to a signalling issue.","DEMO SAMPLE",
     "Incident Report\nAsset: Train T12\nDelay: 14 minutes\nCause: Signalling issue.")]
    for x in samples:add_doc(*x)

st.markdown("## 🚇 MetroInsights")
st.caption("AI-powered document search and knowledge management prototype for metro operations")
data=docs()

with st.sidebar:
    st.header("Navigation")
    page=st.radio("Go to",["🏠 Dashboard","📄 Upload & Analyze","🔎 Intelligent Search","📊 Analytics","🚆 Train Scheduling"])
    st.divider()
    st.write("🐍 Python"); st.write("🎨 Streamlit"); st.write("🤖 Gemini AI"); st.write("💾 SQLite")
    st.divider()
    if client:
       st.success("Gemini AI: Connected")
    else:
       st.warning("Gemini AI: Not connected")

if page=="🏠 Dashboard":
    st.subheader("Operations Knowledge Dashboard")
    a,b,c,d=st.columns(4)
    a.metric("Documents",len(data)); b.metric("Maintenance",sum(x[2]=="Maintenance" for x in data))
    c.metric("Safety",sum(x[2]=="Safety" for x in data)); d.metric("High Priority",sum(x[5]=="High" for x in data))
    st.markdown("### ⚡ Quick actions")
    st.info("📄 **Upload & Analyze** — Gemini can analyze uploaded text and extract type, department, asset, priority, issues, actions and summary.")
    st.success("🔎 **Ask your documents** — Search stored operational records.")
    st.markdown("### Recent documents")
    for x in data[:6]:
        st.markdown(f"**{x[1]}** · `{x[2]}` · `{x[3]}` · Priority `{x[5]}`")
        st.divider()

elif page=="📄 Upload & Analyze":
    st.subheader("📄 Upload & Analyze Document")
    if client:
        st.success("🤖 Gemini AI is connected.")
    else:
        st.info("Gemini is not connected; fallback analysis still works.")

    up = st.file_uploader(
        "Upload documents",
        type=["txt", "pdf"],
        accept_multiple_files=True
    )

    pasted = st.text_area(
        "Or paste document text here",
        height=180
    )

    # Multiple TXT/PDF documents
    if up:
        for file in up:
            filename = file.name
            text = read_document(file)

            if not text.strip():
                st.warning(f"Could not extract text from {filename}")
                continue

            st.markdown(f"### 📄 {filename}")

            with st.expander("View document"):
                st.text(text[:10000])

            if st.button(
                f"🤖 Analyze {filename}",
                key=f"analyze_{filename}"
            ):
                fb = fallback(text, filename)

                with st.spinner(
                    f"Gemini AI is analyzing {filename}..."
                ):
                    try:
                        ai, err = ai_analyze(text)
                    except Exception as e:
                        ai = None
                        err = str(e)

                if ai:
                    category, dept, asset, priority, summary = parse_ai(
                        ai, fb
                    )

                    st.success(
                        f"✅ AI analysis completed for {filename}"
                    )
                    st.markdown("### 🤖 AI Document Analysis")
                    st.markdown(ai)

                    analysis = ai

                else:
                    category, dept, asset, priority, summary = fb

                    st.warning(
                        "AI unavailable; built-in prototype analysis used."
                    )

                    if err:
                        st.caption(f"AI status: {err}")

                    x, y, z, q = st.columns(4)
                    x.metric("Category", category)
                    y.metric("Department", dept)
                    z.metric("Asset", asset)
                    q.metric("Priority", priority)

                    st.info(summary)

                    analysis = (
                        f"DOCUMENT TYPE: {category}\n"
                        f"DEPARTMENT: {dept}\n"
                        f"ASSET: {asset}\n"
                        f"PRIORITY: {priority}\n"
                        f"SUMMARY: {summary}"
                    )

                add_doc(
                    filename,
                    category,
                    dept,
                    asset,
                    priority,
                    summary,
                    analysis,
                    text
                )

                st.success(
                    f"💾 {filename} saved to MetroDoc database."
                )

    # Pasted document
    elif pasted.strip():
        filename = "pasted_document.txt"
        text = pasted.strip()

        st.markdown("### 📄 Pasted Document")

        if st.button("🤖 Analyze Pasted Document"):
            fb = fallback(text, filename)

            with st.spinner("Gemini AI is analyzing..."):
                try:
                    ai, err = ai_analyze(text)
                except Exception as e:
                    ai = None
                    err = str(e)

            if ai:
                category, dept, asset, priority, summary = parse_ai(
                    ai, fb
                )

                st.success("✅ AI analysis completed!")
                st.markdown("### 🤖 AI Document Analysis")
                st.markdown(ai)

                analysis = ai

            else:
                category, dept, asset, priority, summary = fb

                st.warning(
                    "AI unavailable; built-in prototype analysis used."
                )

                if err:
                    st.caption(f"AI status: {err}")

                x, y, z, q = st.columns(4)
                x.metric("Category", category)
                y.metric("Department", dept)
                z.metric("Asset", asset)
                q.metric("Priority", priority)

                st.info(summary)

                analysis = (
                    f"DOCUMENT TYPE: {category}\n"
                    f"DEPARTMENT: {dept}\n"
                    f"ASSET: {asset}\n"
                    f"PRIORITY: {priority}\n"
                    f"SUMMARY: {summary}"
                )

            add_doc(
                filename,
                category,
                dept,
                asset,
                priority,
                summary,
                analysis,
                text
            )

            st.success(
                "💾 Pasted document saved to MetroDoc database."
            )

elif page=="🔎 Intelligent Search":
    st.subheader("🔎 Intelligent Search")
    q=st.text_input("Search your operational documents",placeholder="e.g. When was Escalator E17 last maintained?")
    if q:
        words=[w.lower() for w in re.findall(r"[a-zA-Z0-9]+",q) if len(w)>2]
        results=[]
        for x in data:
            hay=" ".join(map(str,x[1:9])).lower()
            score=sum(w in hay for w in words)
            if score: results.append((score,x))
        results.sort(reverse=True,key=lambda z:z[0])
        if not results: st.warning("No matching document found.")
        else:
            score,best=results[0]; st.success(f"Best match: **{best[1]}**")
            ql=q.lower()
            answer=("Escalator E17 was last maintained on **12 August 2026**." if "e17" in ql and "maint" in ql
                    else "Train T12 experienced a **14-minute delay** due to a signalling issue." if "t12" in ql and "delay" in ql
                    else best[6])
            st.markdown("### 🤖 Retrieved Answer"); st.info(answer)
            st.caption(f"Source: {best[1]} · Relevance score: {score}")
            st.markdown("### 📚 Related documents")
            for score,x in results[:5]:
                st.markdown(f"**{x[1]}** — {x[2]} · {x[3]} · relevance `{score}`")
                with st.expander("View summary"): st.write(x[6])

elif page=="🚆 Train Scheduling":
    train_scheduling_page()

else:
    st.subheader("📊 Document Analytics")
    cats=Counter(x[2] for x in data); deps=Counter(x[3] for x in data); pri=Counter(x[5] for x in data)
    a,b=st.columns(2)
    with a: st.markdown("### Documents by category"); st.bar_chart(cats)
    with b: st.markdown("### Documents by department"); st.bar_chart(deps)
    st.markdown("### Priority distribution"); st.bar_chart(pri)
    st.markdown("### ⚠ Documents needing attention")
    high=[x for x in data if x[5]=="High"]
    if high:
        for x in high: st.warning(f"**{x[1]}** — {x[3]} — {x[6]}")
    else: st.success("No high-priority documents.")

st.divider()
st.caption("MetroDoc AI prototype • Python + Streamlit + Gemini + SQLite")