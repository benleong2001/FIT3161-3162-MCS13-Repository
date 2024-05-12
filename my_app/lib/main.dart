import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:my_app/Select_Name_Page.dart';
import 'package:my_app/registration_page.dart';
import 'request.dart';
import 'package:http/http.dart' as http;

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
  const WebPage({Key? key}) : super(key: key);

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
                  MaterialPageRoute(builder: (context) => const Select_Name_Page()),
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
                        child: Text('Face Recognition Model'),
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

// Future<String> fetchData(String imagePath) async {
//   final request = http.MultipartRequest('POST', Uri.parse('https://b928-202-186-176-157.ngrok-free.app/predict'));
//   request.files.add(await http.MultipartFile.fromPath('image', imagePath));

//   final response = await request.send();
//   if (response.statusCode == 200) {
//     final responseBody = await response.stream.transform(utf8.decoder).join();
//     return responseBody;
//   } else {
//     throw Exception('Failed to fetch data');
//   }
// }