import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

def execute_query(sql: str):
    try:
        conn = sqlite3.connect("database/ecommerce.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        conn.close()
        return {"columns": col_names, "data": rows}
    except Exception as e:
        return {"error": str(e)}

def visualize_query(sql: str):
    try:
        conn = sqlite3.connect("database/ecommerce.db")
        df = pd.read_sql(sql, conn)
        conn.close()

        if df.empty or len(df.columns) < 2:
            return None

        plt.figure(figsize=(8, 4))
        df.plot(kind="bar", x=df.columns[0], y=df.columns[1], legend=False)
        plt.xticks(rotation=45)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        encoded = base64.b64encode(buf.read()).decode('utf-8')
        return f"data:image/png;base64,{encoded}"
    except Exception as e:
        print("Visualization error:", e)
        return None
