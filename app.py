from flask import Flask, request, url_for, redirect, render_template, flash

# Instantiate Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for flash messaging

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)

# Create operation
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        transaction = {
            'id': len(transactions) + 1,            # Generate a new ID
            'date': request.form['date'],           # Get the 'date' field from the form
            'amount': float(request.form['amount']) # Convert 'amount' to a float
        }
        transactions.append(transaction)
        flash("Transaction added successfully!", "success")
        return redirect(url_for("get_transactions"))

    return render_template("form.html")

# Update operation
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    transaction = next((t for t in transactions if t['id'] == transaction_id), None)
    if not transaction:
        flash("Transaction not found!", "error")
        return redirect(url_for("get_transactions"))

    if request.method == "POST":
        transaction['date'] = request.form['date']
        transaction['amount'] = float(request.form['amount'])
        flash("Transaction updated successfully!", "success")
        return redirect(url_for("get_transactions"))

    return render_template("edit.html", transaction=transaction)

# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    # Find the transaction with the matching ID and remove it from the list
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)  # Remove the transaction from the transactions list
            break                            # Exit the loop once the transaction is found and removed
    # Redirect to the transactions list page after deleting the transaction
    return redirect(url_for("get_transactions"))

#search operation
@app.route("/search", methods = ["GET", "POST"])
def search_transactions():
    if request.method == "POST":
        min_amount = float(request.form.get('min_amount'))
        max_amount = float(request.form.get('max_amount'))
        filtered_transactions = [
            t for t in transactions if min_amount <= t['amount'] <= max_amount
        ]
        return render_template("transactions.html", transactions = filtered_transactions)
    return render_template("search.html")

#calculate total balance
@app.route("/balance")
def total_balance():
    total_bal = sum(transaction['amount'] for transaction in transactions)
    return render_template("transactions.html", total_bal = total_bal)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
