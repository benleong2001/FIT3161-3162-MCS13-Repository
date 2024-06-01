import 'dart:developer';

import 'package:flutter/material.dart';
import 'package:my_app/widget/dropzone_widget.dart';
import 'package:my_app/model/dropped_file.dart';
import 'package:my_app/widget/dropped_image_widget.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class LoginPage extends StatefulWidget {
  final String selectedName;
  const LoginPage({super.key, required this.selectedName});

  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  DroppedFile? file;
  String? prediction;
  String? error;
  String? name;
  bool _loading = false;
  
  
  Future<Map<String, dynamic>> fetchData(DroppedFile droppedFile) async {
    String fileName = droppedFile.name;
    String extension = fileName.split('.').last.toLowerCase();
    final String base64Image;
    if (extension != 'jpg' && extension != 'jpeg' && extension != 'png') {
      base64Image = "";
      file = null;
    }
    else {
      base64Image = base64Encode(droppedFile.bytes);
    }
    
    const String url = 'https://6e75-118-139-137-175.ngrok-free.app';

    final response = await http.post(
      Uri.parse('$url/predict'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'name': name,
        'base64_bytes': base64Image,
      }),
    ).catchError((error) {
      throw Exception('Failed to load data: $error');
    });

    switch (response.statusCode) {
      case 200:
        final responseData = jsonDecode(response.body);
        log("Received response");
        return {'prediction': responseData['prediction']};
      case 452:
        final responseData = jsonDecode(response.body);
        String error = responseData['error'];
        throw Exception("452: $error");
      case 453:
        final responseData = jsonDecode(response.body);
        String error = responseData['error'];
        throw Exception("453: $error");
      default:
        throw Exception('Unexpected response status code (500), please check with the system administrator.');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Verification Page'),
      ),
      body: Container(
        alignment: Alignment.center,
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('Uploaded Image:'),
            // Image File Display
            DroppedFileWidget(file: file),
            const SizedBox(height: 20),
            
            // Dropzone
            SizedBox(
              height: 300,
              child: DropzoneWidget(
                onDroppedFile: (file) async {
                  setState(() {
                    this.file = file;
                    _loading = true;
                  });
                  try {
                    final response = await fetchData(file);
                    setState(() {
                      prediction = response['prediction'];
                      error = null;
                      _loading = false;
                    });
                    // Do something with the response
                  } catch (e) {
                    setState(() {
                      error = e.toString();
                      _loading = false;
                    });
                  }
                },
              ),
            ),
            const SizedBox(height: 20),

            // Display the predictions
            if (_loading) 
              const CircularProgressIndicator()
            else
              if (error != null) 
                Text('$error', style: const TextStyle(fontSize: 24),)
              else if (prediction!= null) 
                if (prediction==widget.selectedName)
                  Text('Welcome, ${widget.selectedName}!', style: const TextStyle(fontSize: 24),)
                else
                  Text('Sorry, you are not ${widget.selectedName}.', style: const TextStyle(fontSize: 24),),

          ],
        ),
      ),
    );
  }
}