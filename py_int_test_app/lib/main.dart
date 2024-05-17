import 'dart:convert';

import 'package:flutter/material.dart';

import 'request.dart';

void main() {
  test();
  runApp(const MainApp());
}

class MainApp extends StatelessWidget {
  const MainApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: Scaffold(
        body: Center(
          child: Text('Hello World!'),
        ),
      ),
    );
  }

}

void test() async {
  // Code goes here
    var data = await getData('http://10.0.2.2:5000/');
    var decodedData = jsonDecode(data);
    print(decodedData['query']);
}


