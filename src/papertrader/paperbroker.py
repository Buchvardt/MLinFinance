class PaperBroker():

    def __init__(self, symbol_amounts: dict):
        """
        symbol amount is a dict
        i.e {"ETH": 1.0, "USDT": 1800}
        """

        self.symbol_amounts= symbol_amounts 

    def get_balance(self):

        return self.symbol_amounts

    def update_balance(self, symbol_amounts: dict):

        for k, v in symbol_amounts.items():

            self.symbol_amounts[k] = v

    def buy(self, symbol_buy, symbol_sell, price, quantity, fee):

        total_cost = price * quantity


        if symbol_buy in list(self.symbol_amounts.keys()):

            new_balance_buy = self.symbol_amounts[symbol_buy] + quantity * (1 - fee)

        else:

            print(f"{symbol_buy} is not in balance {self.symbol_amounts}")

        if symbol_sell in list(self.symbol_amounts.keys()):

            new_balance_sell = self.symbol_amounts[symbol_sell] - total_cost

        else:

             print(f"{symbol_sell} is not in balance {self.symbol_amounts}")


        if new_balance_sell > 0:

            self.update_balance({symbol_sell: new_balance_sell, symbol_buy: new_balance_buy})

        else:

            print(f"Cannot but {quantity} of {symbol_buy}. Not enough {symbol_sell}!")



if __name__ == "__main__":

    balance = {"ETH": 1.0, "USDT": 1800.0}

    broker_instance = PaperBroker(balance)

    broker_instance.buy("ETH", "USDT", 389.51, 2, 0.01)

    print(broker_instance.get_balance())