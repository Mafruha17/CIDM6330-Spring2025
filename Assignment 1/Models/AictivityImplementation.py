class Device:
    def __init__(self):
        self.state = "Unpaired"
    
    def initiate_pairing(self):
        print("Initiating Pairing...")
        self.state = "Pairing"
    
    def pairing_successful(self):
        print("Pairing Successful!")
        self.state = "Paired"
    
    def pairing_failed(self):
        print("Pairing Failed!")
        self.state = "Unpaired"
    
    def authenticate_user(self):
        print("User Authentication in Progress...")
        self.state = "Connected"
    
    def logout(self):
        print("User Logged Out.")
        self.state = "Disconnected"
    
    def reconnect(self):
        print("Reconnecting...")
        self.state = "Connected"


class UserAuthentication:
    def __init__(self):
        self.state = "NotAuthenticated"
    
    def login(self, success=True):
        print("User Login Attempt...")
        if success:
            self.state = "Authenticated"
            print("Authentication Successful!")
        else:
            self.state = "NotAuthenticated"
            print("Authentication Failed!")
    
    def logout(self):
        print("User Logged Out.")
        self.state = "NotAuthenticated"


class ActivityFlow:
    def __init__(self, device, user_auth):
        self.device = device
        self.user_auth = user_auth

    def start_pairing(self):
        self.device.initiate_pairing()
        if self.user_auth.state == "Authenticated":
            self.device.pairing_successful()
        else:
            self.device.pairing_failed()

    def transmit_data(self):
        if self.device.state == "Connected":
            print("Transmitting Data...")
        else:
            print("Device not connected. Cannot transmit data.")


class HealthDataProcessing:
    def __init__(self):
        self.state = "ReceivingData"

    def process_data(self):
        print("Processing Health Data...")
        abnormal_condition = False  # Change this based on real condition
        if abnormal_condition:
            self.generate_alert()
        else:
            print("Data processed successfully.")

    def generate_alert(self):
        print("Abnormal Condition Detected! Generating Alert...")
        self.state = "AlertGenerated"
        self.store_data()

    def store_data(self):
        print("Storing Data in Database...")
        self.state = "Stored"


# Example Execution
if __name__ == "__main__":
    device = Device()
    user_auth = UserAuthentication()
    activity = ActivityFlow(device, user_auth)
    health_processing = HealthDataProcessing()

    user_auth.login(success=True)
    activity.start_pairing()
    device.authenticate_user()
    activity.transmit_data()
    health_processing.process_data()
