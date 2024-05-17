# Integrate Python program into a Flutter web application.
Source: https://stackoverflow.com/questions/64853113/how-to-integrate-flutter-app-with-python-code <br>
## Setting Up: Installing modules
The following python modules are needed:
1. ngrok
2. tensorflow--2.15.0
3. keras--2.15.0
4. flask
5. opencv-python

Run `pip install {module_name}`, where module_name is the ones listed above. It is recommended to copy and paste the exact names so that there are no discrepancies. <br><br>
If VSC doesn't detect the module, try:
1. Open a new command prompt and run `where python3`. It should show a list of Python Interpreter file paths. <br>
E.g. {%USERPROFILE}/AppData/.../python3.exe
2. Copy the path and open the Command Palette (Ctrl+Shift+P) in VSC.
3. Type "Python: Select Interpreter" and select "Enter Interpreter Path".
4. Paste the copied interpreter path and press 'Enter'.
5. Open a new terminal in VSC, then run the command `{interpreter_path} -m pip install {module_name}`, where {interpreter_path} is the path you just pasted.
### Getting IDE Errors in dart?
This might be due to some missing dependencies. Simply run `dart pub get` for the IDE to auto link the dependencies together.
### Running the app
Run the Python program. A link to the localhost server should pop up in the terminal. It looks something like `Running on http://{ip_address}:{port_number}.` An example would be `http://127.0.0.1:5000`. <br><br>
Open a new terminal in VSC. Host the local server on the web with `ngrok http {port_number}`. You should see several items printed on-screen, such as Session Status, Account, Update, etc. <br><br>
Copy the https link in the 'Forwarding' section (up until the arrow), it should look something like `https://{hex_string}.ngrok-free.app`. Append "predict" to the end of the link, so that it becomes `https://{hex_string}.ngrok-free.app/predict`.<br><br>
Open a new terminal in VSC. Run the Flutter application with `flutter run --web-browser-flag "--disable-web-security"`. The web browser flag is to bypass ngrok's browser warning page and direct the user to the actual python API.




