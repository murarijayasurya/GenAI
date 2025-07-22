def format_response(result: dict) -> str:
    if "error" in result:
        return f"❌ Error: {result['error']}"

    rows = result["data"]
    cols = result["columns"]

    if not rows:
        return "No data found."
    if len(rows) == 1 and len(cols) == 1:
        field = cols[0].replace("SUM(", "").replace(")", "").replace("_", " ").title()
        value = rows[0][0]
        return f"{field}: {float(value):,.2f}"

    response = ""
    for row in rows:
        line = ", ".join([f"{col}: {val}" for col, val in zip(cols, row)])
        response += line + "\\n"
    return response.strip()
