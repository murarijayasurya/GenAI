import requests

# Replace this with your actual Gemini API key (make sure not to commit it publicly!)
GEMINI_API_KEY = "Your Gemini API"

# def fallback_sql(question: str):
#     q = question.lower()
#
#     if "total sales" in q:
#         return "SELECT SUM(total_sales) FROM total_sales_metrics;"
#
#     if "roas" in q or "return on ad spend" in q:
#         return "SELECT SUM(ad_sales) / SUM(ad_spend) AS RoAS FROM ad_sales_metrics;"
#
#     if "highest cpc" in q or "cost per click" in q:
#         return """
#         SELECT item_id, ad_spend * 1.0 / clicks AS CPC
#         FROM ad_sales_metrics
#         WHERE clicks > 0
#         ORDER BY CPC DESC
#         LIMIT 1;
#         """
#
#     return None
def fallback_sql(question: str):
    q = question.lower()

    if "total sales" in q:
        return "SELECT SUM(total_sales) FROM total_sales_metrics;"

    if "roas" in q or "return on ad spend" in q:
        return "SELECT SUM(ad_sales) / SUM(ad_spend) AS RoAS FROM ad_sales_metrics;"

    if "highest cpc" in q or "cost per click" in q:
        return (
            "SELECT item_id, ad_spend * 1.0 / clicks AS CPC "
            "FROM ad_sales_metrics "
            "WHERE clicks > 0 "
            "ORDER BY CPC DESC "
            "LIMIT 1;"
        )

    if "eligible products" in q:
        return (
            "SELECT item_id, eligibility "
            "FROM product_eligibility "
            "WHERE eligibility = 'Eligible';"
        )

    if "ineligible products" in q:
        return (
            "SELECT item_id, eligibility, message "
            "FROM product_eligibility "
            "WHERE eligibility = 'Ineligible';"
        )

    return None

def question_to_sql(question: str) -> str:
    try:
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            "gemini-pro:generateContent?key=" + GEMINI_API_KEY
        )

        # Properly formatted triple-quoted string
        prompt = f"""
        Schema:
        1. ad_sales_metrics(date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold)
        2. total_sales_metrics(date, item_id, total_sales, total_units_ordered)
        3. product_eligibility(eligibility_datetime_utc, item_id, eligibility, message)

Question: {question}

SQL:
"""

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)

        result = response.json()
        text = result["candidates"][0]["content"]["parts"][0]["text"]

        # Clean result if it includes markdown code blocks
        return text.replace("```sql", "").replace("```", "").strip()

    except Exception as e:
        print("⚠️ Error during Gemini call:", e)
        return fallback_sql(question) or "SELECT 'Could not process the question.';"
