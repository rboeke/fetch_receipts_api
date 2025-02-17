import re
import datetime
import time

# helper function to verify items object
def verify_items(items):
    # required:
    # - shortDescription
    # - price
    required_keys = ["shortDescription", "price"]
    for item in items:
        for key in required_keys:
            # check if required key is in item
            if not key in list(item.keys()):
                raise Exception

            # check if shortDescription is str and matches pattern
            if key == "shortDescription":
                shortDescription = item[key]
                if not isinstance(shortDescription, str):
                    raise Exception
                if not re.match("^[\\w\\s\\-]+$", shortDescription):
                    raise Exception
                
            # check if price is str and matches pattern
            elif key == "price":
                price = item[key]
                if not isinstance(price, str):
                    raise Exception
                if not re.match("^\\d+\\.\\d{2}$", price):
                    raise Exception
    return

# helper function to verify receipt json
def verify_receipt(receipt):
    # required:
    # - retailer
    # - purchaseDate
    # - purchaseTime
    # - items
    # - total
    required_keys = ["retailer", "purchaseDate", "purchaseTime", "items", "total"]
    for key in required_keys:
        # check if required key is in receipt
        if not key in list(receipt.keys()):
            raise Exception
        
        # check if retailer matches pattern and is str
        if key == "retailer":
            retailer = receipt[key]
            if not isinstance(retailer, str):
                raise Exception
            if not re.match("^[\\w\\s\\-&]+$", retailer):
                raise Exception
        
        # check if purchaseDate is valid date and is str
        elif key == "purchaseDate":
            purchaseDate = receipt[key]
            if not isinstance(purchaseDate, str):
                raise Exception
            try:
                datetime.date.fromisoformat(purchaseDate)
            except:
                raise Exception
        
        # check if purchaseTime is valid time and is str
        elif key == "purchaseTime":
            purchaseTime = receipt[key]
            if not isinstance(purchaseTime, str):
                raise Exception
            try:
                time.strptime(purchaseTime, '%H:%M')
            except:
                raise Exception

        # check if items is array and contains at least 1 item
        elif key == "items":
            items = receipt[key]
            if not isinstance(items, list):
                raise Exception
            if not len(items) >= 1:
                raise Exception
            verify_items(items)

        # check if total is str and matches pattern
        elif key == "total":
            total = receipt[key]
            if not isinstance(total, str):
                raise Exception
            if not re.match("^\\d+\\.\\d{2}$", total):
                raise Exception
    return
