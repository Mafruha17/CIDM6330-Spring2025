# Activity Diagram Explanation

## **1. Device Lifecycle**
The device lifecycle represents the various states a device goes through during operation.
- **Unpaired:** Initial state before pairing.
- **Pairing:** Attempt to connect with the user.
- **Paired:** Successful connection established.
- **Connected:** Device is actively exchanging data.
- **Transmitting:** Data exchange is in progress.
- **Disconnected:** Device connection is lost due to logout or timeout.
- **Reconnect:** Device attempts to reconnect.
- **Device Reset:** The device is reset and returns to the unpaired state.

## **2. User Authentication**
This section handles user login and authentication to ensure secure access.
- **NotAuthenticated:** Initial state before login.
- **Authenticating:** The user is attempting to log in.
- **Authenticated:** Login successful, user granted access.
- **LoggedIn:** User session is active.
- **Logout:** User logs out and returns to the NotAuthenticated state.

## **3. Activity Flow**
Defines the sequence of actions for device pairing, data transmission, and event logging.
- **Start:** User initiates device pairing.
- **DeviceAuthentication:** Validates user credentials.
- **Success:** If credentials are valid, proceed to pairing.
- **Failure:** If invalid, retry login.
- **DevicePaired:** Device successfully connected.
- **TransmitData:** Device starts real-time monitoring.
- **NotifyProvider:** Alerts the provider when necessary.
- **LogEvent:** Stores alert records.
- **ProcessData:** Analyzes and stores monitoring results.
- **End:** Monitoring process completes.

## **4. Health Data Processing**
Manages health-related data and alerts in case of abnormal conditions.
- **ReceivingData:** The system receives health data.
- **Processing:** The data is validated and analyzed.
- **AlertGenerated:** If abnormalities are detected, an alert is created.
- **Stored:** The data is stored in the database.
- **Notified:** Alert is sent to the provider.

## **Summary**
The activity diagram outlines how devices interact with users, process authentication, transmit health data, and handle abnormal conditions. This ensures smooth operations for healthcare monitoring and secure data handling.
