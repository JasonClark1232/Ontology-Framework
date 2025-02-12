from flask import Flask, request
import time
from rdflib import Graph, Namespace, URIRef

# Define Flask app
app = Flask(__name__)

# Define ontology path
ontology_path = "location_privacy.owl"
PRIV = Namespace("http://example.org/privacy.owl#")

@app.route("/")
def index():
    return """
    <h2>User Privacy Settings</h2>
    <form action="/update_privacy" method="post">
        <label>User:</label>
        <input type="text" name="user" required>
        <label>Privacy Status:</label>
        <select name="status">
            <option value="opt-in">Opt-In</option>
            <option value="opt-out">Opt-Out</option>
        </select>
        <button type="submit">Update Privacy</button>
    </form>
    """

@app.route("/update_privacy", methods=["POST"])
def update_privacy():
    try:
        user = request.form["user"]
        status = request.form["status"]

        print(f"🔍 Received update request for User: {user}, Status: {status}")  # Debugging log

        # Load ontology
        g = Graph()
        g.parse(ontology_path)

        user_uri = URIRef(f"http://example.org/privacy.owl#{user}")
        opt_in_uri = URIRef(f"http://example.org/privacy.owl#OptIn")
        opt_out_uri = URIRef(f"http://example.org/privacy.owl#OptOut")

        # Update ontology based on user selection
        g.remove((user_uri, PRIV.HasPrivacySetting, None))  # Remove old setting
        if status == "opt-in":
            g.add((user_uri, PRIV.HasPrivacySetting, opt_in_uri))
        else:
            g.add((user_uri, PRIV.HasPrivacySetting, opt_out_uri))

        # Save updated ontology
        g.serialize(ontology_path)

        print("✅ Privacy setting updated successfully!")  # Debugging log
        return f"✅ User {user} updated privacy to {status}"

    except Exception as e:
        print(f"❌ ERROR: {e}")  # Print the actual error message
        return f"❌ Internal Server Error: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
