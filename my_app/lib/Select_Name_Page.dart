import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:my_app/login_page.dart';

class SelectNamePage extends StatefulWidget {
  const SelectNamePage({super.key});

  @override
  _SelectNamePageState createState() => _SelectNamePageState();
}

class _SelectNamePageState extends State<SelectNamePage> {
  String? enteredName;
  List<String> names = [];
  String? message;

  @override
  void initState() {
    super.initState();
    _fetchNames();
  }

  Future<void> _fetchNames() async {
    const String url = 'https://2d4e-118-139-138-171.ngrok-free.app';
    // Get response and disable the web security
    final response = await http.get(Uri.parse('$url/names'), headers: {"ngrok-skip-browser-warning": "69420"});

    if (response.statusCode == 200) {
      final jsonData = jsonDecode(response.body);
      // Set the names to the list
      setState(() {
        names = jsonData['names'].cast<String>();
      });
    } else {
      throw Exception('Failed to load names: unexpected response status code');
    }
  }

  void _checkUsername() {
    if (names.contains(enteredName)) {
      setState(() {
        message = 'Username exists within the system.';
      });
    } else {
      setState(() {
        message = 'Username does not exist.';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Registration Page'),
      ),
      body: Container(
        alignment: Alignment.center,
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('Enter Username'),
            const SizedBox(height: 16),
            TextField(
              onChanged: (value) {
                enteredName = value;
              },
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Username',
              ),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _checkUsername,
              style: ElevatedButton.styleFrom(
                minimumSize: const Size(100, 50),
                foregroundColor: Colors.black, // Set the color of the text and icon when the button is pressed
              ),
              child: const SizedBox(
                width: 150,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: [
                    Icon(Icons.check, size: 24, color: Colors.black), // Add the icon for the check button
                    SizedBox(width: 10),
                    Expanded(
                      flex: 1,
                      child: Center(
                        child: Text('Check Username'),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 20),
            if (message != null)
              Text(
                message!,
                style: TextStyle(
                  color: message == 'Username exists within the system.' ? Colors.green : Colors.red,
                ),
              ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                if (names.contains(enteredName)) {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => LoginPage(selectedName: enteredName!)),
                  );
                }
              },
              style: ElevatedButton.styleFrom(
                minimumSize: const Size(100, 50),
                foregroundColor: Colors.black, // Set the color of the text and icon when the button is pressed
              ),
              child: const SizedBox(
                width: 150,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: [
                    Icon(Icons.login, size: 24, color: Colors.black), // Add the icon for the register button
                    SizedBox(width: 10),
                    Expanded(
                      flex: 1,
                      child: Center(
                        child: Text('Go to Login'),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
