import pandas as pd

df = pd.read_csv("hotels.csv", dtype={"id": str})
df_card = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cards_security = pd.read_csv("card_security.csv", dtype=str)


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
        """Book a hotel by changing its availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False


class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f""" 
        Thank you for your reservation!
        Here are your booking data: 
        Name: {self.customer_name}
        Hotel name: {self.hotel.name}"""

        return content


class CreditCard:
    def __init__(self, card_number):
        self.card_number = card_number

    def validate(self, expiration_date, cvc, name_on_the_card):
        card_data = {"card_number": self.card_number, "expiration_date": expiration_date, "cvc": cvc,
                     "name_on_the_card": name_on_the_card}
        # print("User-entered card data:", card_data)
        if card_data in df_card:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_cards_security.loc[df_cards_security["number"] == self.card_number, "password"].squeeze()
        if password is None or password == "":
            print("No password found for this card.")
            return False

        if password == given_password:
            return True
        else:
            return False


class SpaReservation:
    def __init__(self, customer_name, hotel_name):
        self.customer_name = customer_name
        self.hotel_name = hotel_name

    def generate(self):
        content = f""" 
        Thank you for your spa reservation!
        Here are your booking data: 
        Name: {self.customer_name}
        Hotel name: {self.hotel_name}"""
        return content


print(df)

while True:
    hotel_ID = input("Enter the id of the hotel (or type 'exit' to quit): ")
    name = input("Enter your name: ")

    # Allow the user to exit the loop
    if hotel_ID.lower() == "exit":
        print("Goodbye! Exiting the program.")
        break

    # Check if the entered ID exists in the DataFrame
    if hotel_ID not in df["id"].values:
        print(f"No hotel found with ID {hotel_ID}. Please try again.")
        continue  # Ask for input again
    else:
        # Proceed if the ID is valid
        hotel = Hotel(hotel_ID)

        # Check availability and proceed with booking
        if hotel.available():

            card_number = input("Enter the card number")
            expiration_date = input("Enter the card expiration_date")
            cvc = input("Enter the card cvc")
            name_on_the_card = input("Enter the name on the card")

            credit_card = SecureCreditCard(card_number)

            if credit_card.validate(expiration_date, cvc, name_on_the_card):
                given_password = input("Enter your password")
                if credit_card.authenticate(given_password):

                    hotel.book()

                    reservation_ticket = ReservationTicket(customer_name=name, hotel_object=hotel)
                    print(reservation_ticket.generate())
                else:
                    print("credit card authentication failed.")

                spa = input("Do you want to book a spa package? yes/no: ").strip().lower()
                if spa == "yes":
                    spa_reservation = SpaReservation(customer_name=name, hotel_name=hotel.name)
                    print(spa_reservation.generate())






            else:
                print("There was a problem with your payment")
        else:
            print("Hotel is not free.")
        break  # Exit the loop after a successful booking or when the hotel is unavailable
