# Indoor-Localization
Tracking a object within a building

# System Main Components
1. ESP ESP NodeMCU
2. AI Model (Random Forest model)
3. Web Server (Flask)
4. Mobile APP (Flutter)

# System Description
1. **ESP NodeMCU** that scans the available Access Points and send signal strength to server
2. **Server** that decide (according to data receive from ESP) where we are through a Trained AI model
3. **Mobile application** that display the location on the map

# How to get started
1. Create Virtual Env (optional)
    ``` python -m venv <environment-name> ```
2. Activate the Venv
    * Bash 
    ``` source virtualenv_name/Scripts/activate ```
    * Powershell 
    ``` ./virtualenv_name/Scripts/activate ```
2. Install Requirements.txt packages
    ``` pip install -r requirements.txt ```
3. Collect data about surrounding routers signal strength ``` See file in ready-to-model dir ```
4. Use this data to train the AI model and save it
