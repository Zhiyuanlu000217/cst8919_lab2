Youtube video link: https://youtu.be/vXsNd9zYtfU

# Reflection

In this lab, I have learned how to:
- Deploy app on Azure Web App:

    In this lab, since we are using a simple Flask App, I have 
    enabled CI/CD feature to automatically deploy the code, 
    azure will detect the flask app, and automatically install 
    the dependencies and run `app.py` as the entry

- Set up Monitoring > Diagnostic settings:

    This will pipeline the app console log, such as 
    ```
    127.0.0.1 - - [13/Jun/2025 19:46:33] "POST /login HTTP/1.1" 200 
    ```
    to the Log Analytic workspace and able to retrieved later

- Query with KQL

    The query I am using is below:
    ```KQL
    AppServiceConsoleLogs
    | where TimeGenerated > ago(24h) 
    | where ResultDescription contains "POST /login"
    | where ResultDescription contains " 401 " or ResultDescription contains " 400 " 
    | project TimeGenerated, ResultDescription, Host, ClientIp = extract(@'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', 1, ResultDescription) // Extract IP if present
    | sort by TimeGenerated desc
    ```

    Which it will do the following:
    - Search within `AppServiceConsoleLogs` Table
    - The log is within 24 hours(as shown in code)
    - The log includes keyword `POST /login` and respond code `401`
    - Make the result display the `TimeGenerated`, `ResultDescription`, and `Host` columns, and also create a new column called `ClientIp` by finding and extracting any IPv4 address from the ResultDescription.

    A sample console log looks like below:
    ![Sample Console Log](/Image/sample_console_log.png)

    A sample result looks like below:
    ![Sample KQL result](/Image/sample_kql_result.png)

# Improvements

In real world, the situation can be much more complicated, and the log can be various as well. There are several way I think can help improve the detection logic:

- Create more structural log from the Application
- Detect more combinations, such as:
    - frequent change ip for single user
    - suspecious ip for logins
    - suspecious login device or request sender

