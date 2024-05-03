import 'package:flutter/material.dart';
import 'package:my_app/registration_page.dart';
void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Face Authenticator',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const WebPage(),
    );
  }
}

class WebPage extends StatelessWidget {
  const WebPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Face Authenticator'),
        backgroundColor: Colors.blue,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Image.asset(
              'assets/images/FR.jpg',
              width: 100,
              height: 100,
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => RegistrationPage()),
                );
              },
              style: ElevatedButton.styleFrom(
                minimumSize: const Size(200, 50),
                foregroundColor: Colors.black, // Set the color of the text and icon when the button is pressed
              ),
              child: const SizedBox(
                width: 200,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: [
                    Icon(Icons.person_add, size: 24, color: Colors.black), // Add the icon for the register button
                    SizedBox(width: 10),
                    Expanded(
                      flex: 1,
                      child: Center(
                        child: Text('Register'),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: () {
                // Navigate to the sign-in page
              },
              style: ElevatedButton.styleFrom(
                minimumSize: const Size(200, 50),
                foregroundColor: Colors.black, // Set the color of the text and icon when the button is pressed
              ),
              child: const SizedBox(
                width: 200,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: [
                    Icon(Icons.login, size: 24, color: Colors.black), // Add the icon for the sign-in button
                    SizedBox(width: 10),
                    Expanded(
                      flex: 1,
                      child: Center(
                        child: Text('Sign In'),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: () {
                // Navigate to the delete account page
              },
              style: ElevatedButton.styleFrom(
                minimumSize: const Size(200, 50),
                foregroundColor: Colors.black, // Set the color of the text and icon when the button is pressed
              ),
              child: const SizedBox(
                width: 200,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: [
                    Icon(Icons.delete, size: 24, color: Colors.black), // Add the icon for the delete account button
                    SizedBox(width: 10),
                    Expanded(
                      flex: 1,
                      child: Center(
                        child: Text('Delete Account'),
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