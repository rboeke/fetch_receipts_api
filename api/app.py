import flask
from flask import request
import re
import math
import verify_json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# increment unique id starting at 1
id_count = 1

# receipts dictionary:
#   stores receipt objects with unique id as key
receipts = {}

@app.route('/', methods=["GET"])
def home():
    return "<h1>Receipts API Running</h1>", 200

@app.route('/receipts/process', methods=['POST'])
def process():
    global id_count
    try:
        new_receipt = request.json

        verify_json.verify_receipt(new_receipt)

        # assign unique id and update id_count
        unique_id = id_count
        id_count += 1

        # add new_receipt to receipts
        receipts[unique_id] = new_receipt

        return {"id": str(unique_id)}, 200
    except:
        # Exception raised, return receipt invalid and status 400
        return "The receipt is invalid.", 400

@app.route('/receipts/<id>/points', methods=['GET'])
def points(id):
    try:
        # load receipt with specified id
        receipt = receipts[int(id)]
        points = 0

        # One point for every alphanumeric character in the retailer name.
        points += len(re.findall("[a-zA-Z0-9]", receipt["retailer"]))
        
        # 50 points if the total is a round dollar amount with no cents.
        if int(float(receipt["total"])) == float(receipt["total"]):
            points += 50

        # 25 points if the total is a multiple of 0.25.
        if float(receipt["total"]) % 0.25 == 0:
            points += 25

        # 5 points for every two items on the receipt.
        # I will assume that we get zero points for a single item
        points += 5 * int(len(receipt["items"]) / 2)

        # If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
        for item in receipt["items"]:
            if len(item["shortDescription"].strip()) % 3 == 0:
                points += math.ceil(float(item["price"]) * 0.2)

        # 6 points if the day in the purchase date is odd.
        if not int(receipt["purchaseDate"][-2:]) % 2 == 0:
            points += 6

        # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
        # I will assume the range is exclusive on both ends
        time = int(receipt["purchaseTime"].replace(":", ""))
        if time < 1600 and time > 1400:
            points += 10

        return {"points": points}, 200
    except:
        # Exception raised, return no receipt found and status 404
        return "No receipt found for that ID.", 404

app.run()