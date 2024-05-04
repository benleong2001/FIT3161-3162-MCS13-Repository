# Testing to integrate Python program into a Flutter web application.
Source: https://stackoverflow.com/questions/64853113/how-to-integrate-flutter-app-with-python-code <br>
## Setting Up: Install the flask module
run `pip install flask`. <br><br>
If VSC doesn't detect the module, try:
1. Open a new command prompt and run `where python3`. It should show a list of Python Interpreter file paths. <br>
E.g. {%USERPROFILE}/AppData/.../python3.exe
2. Copy the path and open the Command Palette (Ctrl+Shift+P) in VSC.
3. Type "Python: Select Interpreter" and select "Enter Interpreter Path".
4. Paste the copied interpreter path and press 'Enter'.
5. Open a new terminal in VSC, then run the command `{interpreter_path} -m pip install flask`, where {interpreter_path} is the path you just pasted.
### Running the app
Run the Python program. A link to the localhost server should pop up in the terminal. It looks something like `Running on http://127.0.0.1:5000`. <br><br>
Open a new terminal in VSC. Run the Flutter application with `flutter run`. It should send a HTTP request to obtain the information from the server.




