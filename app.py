from flask import Flask, jsonify, request
from datetime import datetime, timezone

app = Flask(__name__)

invoices = []

@app.route('/api/invoices', methods=['GET'])
def list_invoices():
    return jsonify({"invoices": invoices, "count": len(invoices)})

@app.route('/api/invoices', methods=['POST'])
def create_invoice():
    data = request.json
    invoice = {
        "id": len(invoices) + 1,
        "customer": data.get("customer"),
        "amount": data.get("amount"),
        "currency": data.get("currency", "USD"),
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    invoices.append(invoice)
    return jsonify(invoice), 201

@app.route('/api/invoices/<int:invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    for inv in invoices:
        if inv["id"] == invoice_id:
            return jsonify(inv)
    return jsonify({"error": "not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
