import os
import json
import re
import mysql.connector
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import requests
from config import Config  # Import Config class

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder="templates")
CORS(app)  # Enable CORS for frontend communication

# MySQL Database Configuration
DB_CONFIG = {
    "host": Config.MYSQL_HOST,
    "user": Config.MYSQL_USER,
    "password": Config.MYSQL_PASSWORD,
    "database": Config.MYSQL_DB
}

# List of LLM models to try in fallback order
LLM_MODELS = ["mixtral-8x7b-32768", "llama3-8b", "gemma-7b"]

# Function to connect to MySQL
def connect_db():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

# Function to get existing table names
def get_existing_tables():
    conn = connect_db()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tables
    except mysql.connector.Error as err:
        print("❌ Error fetching tables:", err)
        conn.close()
        return []

# Function to get column names of a table
def get_table_columns(table_name):
    conn = connect_db()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute(f"SHOW COLUMNS FROM `{table_name}`;")
        columns = [row[0] for row in cursor.fetchall()]
        conn.close()
        return columns
    except mysql.connector.Error as err:
        print(f"❌ Error fetching columns for {table_name}:", err)
        conn.close()
        return []

# Function to convert natural language to SQL
def generate_sql(natural_query):
    """
    Converts a natural language query into an SQL query by detecting the table
    and requested columns.
    """

    existing_tables = get_existing_tables()
    detected_table = None

    # Find the table name in the query
    for table in existing_tables:
        if table in natural_query.lower():
            detected_table = table
            break

    if not detected_table:
        return use_llm_for_sql(natural_query)  # Fallback to LLM if no table is found

    # Extract potential column names
    query_words = natural_query.replace(detected_table, "").strip().split()
    table_columns = get_table_columns(detected_table)

    print(f"📌 Columns in `{detected_table}`: {table_columns}")

    # Filter valid columns
    valid_columns = [word.strip() for word in query_words if word in table_columns]

    # If valid columns are found, construct the SQL query
    if valid_columns:
        sql_query = f"SELECT {', '.join([f'`{col}`' for col in valid_columns])} FROM `{detected_table}`;"
    else:
        sql_query = f"SELECT * FROM `{detected_table}`;"  # Default to all columns if none are specified

    print(f"✅ Generated SQL Query: {sql_query}")
    return sql_query

# Function to convert natural language to SQL using Groq LLM (fallback)
def use_llm_for_sql(natural_query):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }

    prompt_message = (
        "You are an expert MySQL query generator. "
        "For the given English query, return ONLY a valid SQL query in a single line, ending with a semicolon. "
        "Do not include any explanation, comments, or additional text."
    )

    for model in LLM_MODELS:
        print(f"🔄 Trying model: {model}")

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": prompt_message},
                {"role": "user", "content": natural_query}
            ],
            "temperature": 0  # Low temperature for deterministic results
        }

        response = requests.post(url, headers=headers, json=payload)
        print(f"🔍 {model} API Response:", response.text)  # Debugging API response

        if response.status_code == 200:
            response_json = response.json()
            try:
                sql_query = response_json["choices"][0]["message"]["content"].strip()

                # Validate SQL query
                if re.match(r"^\s*(SELECT|SHOW|INSERT|UPDATE|DELETE|CREATE|DROP|ALTER)\s+.*;$", sql_query, re.IGNORECASE):
                    print(f"✅ Generated SQL Query: {sql_query}")
                    return sql_query
                else:
                    print("❌ No valid SQL query detected.")
            except (KeyError, IndexError) as e:
                print(f"Error extracting SQL from {model}: {e}")

    return None  # Return None if no valid SQL query was generated

# Route to serve the frontend (index.html)
@app.route("/")
def home():
    return send_from_directory("templates", "index.html")

# Route to handle user queries
@app.route("/query", methods=["POST"])
def process_query():
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "No query provided"}), 400

    user_query = data["query"]
    print("🔍 Received query:", user_query)

    # Convert natural query to SQL
    sql_query = generate_sql(user_query)
    if not sql_query:
        return jsonify({"error": "Could not generate a valid SQL query."}), 400

    conn = connect_db()
    if conn is None:
        return jsonify({"error": "Database connection failed."}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        
        # Set the correct database before executing the query
        cursor.execute(f"USE {Config.MYSQL_DB};")
        
        cursor.execute(sql_query)
        results = cursor.fetchall()
        conn.close()
        print("✅ SQL executed successfully.")
        return jsonify({"sql_query": sql_query, "results": results})
    except mysql.connector.Error as err:
        print("❌ SQL Execution Error:", err)
        return jsonify({"error": f"SQL Execution Error: {err}"})

if __name__ == "__main__":
    app.run(debug=True)
