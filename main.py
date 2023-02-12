import os
from dotenv import load_dotenv
from farcaster import MerkleApiClient
from farcaster.models import Parent



if __name__ == "__main__":
    load_dotenv()
    fcc = MerkleApiClient(access_token=os.getenv("FARC_SECRET"))
    print(fcc.get_healthcheck())

    def handle_command(notif):
        username = os.getenv("USERNAME")
        # Determine the command to be performed based on the event data
        if notif.content.cast.text.startswith(username + " command_1"):
            try:
                # Perform command 1
                result = perform_command_1(notif)
            except Exception as e:
                # Handle any exceptions that occur while performing command 1
                handle_error(e)
        if notif.content.cast.text.startswith(username + " command_2"):
            try:
                result = perform_command_2(notif)
            except Exception as e:
                handle_error(e)
        if notif.content.cast.text.startswith(username + " command_3"):
            try:
                result = perform_command_3(notif)
            except Exception as e:
                handle_error(e)
        # ... Add additional commands as needed
        else:
            pass

    def handle_error(error):
        # Log the error and take any necessary action to handle it
        print(f"An error occurred: {error}")

    def perform_command_1(notif):
        print("Running Command 1!")
        response = fcc.get_cast(
            hash="0xcd5082e1110a1ead6acb57bd8ed2e209cef6f892db64be02c3f8cc42247648b7"
        )
        print(response.cast.hash)
        print(response.cast.author.username)
        print(response.cast.text)

    def perform_command_2(notif):
        print("Running Command 2!")
        response = fcc.post_cast(
            "Hello World",
            parent=Parent(
                fid=notif.content.cast.author.fid, hash=notif.content.cast.hash
            ),
        )
        print(response.cast.hash)
        print(response.cast.text)

    def perform_command_3(notif):
        print("Running Command 3!")
        # This command will cause an error to be thrown
        fcc.get_cast(hash="1234567890")
        print("This line will not be printed")

    for notif in fcc.stream_notifications(max_counter=120):
        if notif and notif.content.cast.text.startswith(os.getenv("USERNAME")):
            handle_command(notif)
            pass
