import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:my_app/registration_page.dart';

class SelectNamePage extends StatefulWidget {
  const SelectNamePage({super.key});

  @override
  _SelectNamePageState createState() => _SelectNamePageState();
}

class _SelectNamePageState extends State<SelectNamePage> {
  String? selectedName;
  List<String> names = [];
  
  @override
  void initState() { 
    super.initState();
    _fetchNames();
  }

 Future<void> _fetchNames() async {
  const String url = 'https://de32-2001-f40-950-3d6-38c0-84cf-8145-a251.ngrok-free.app';
  //get response and disable the web security
  final response = await http.get(Uri.parse('$url/names'),headers:{"ngrok-skip-browser-warning":"69420"});
  
  if (response.statusCode == 200) {
    final jsonData = jsonDecode(response.body);
    //set the names to the list
    setState(() {
      names = jsonData['names'].cast<String>();
      selectedName = names.first;
    });
  } else {
    throw Exception('Failed to load names: unexpected response status code');
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
            Text('Select Username'),
            const SizedBox(height: 16),
            DropdownButton<String>(
              value: selectedName,
              onChanged: (value) {
                setState(() {
                  selectedName = value;
                });
              },
              items: names.map((name) {
                return DropdownMenuItem<String>(
                  value: name,
                  child: Text(name),
                );
              }).toList(),
            ),
            const SizedBox(height: 20), 
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => RegistrationPage(selectedName: selectedName!)),
                );
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
  }}