import 'package:flutter/material.dart';
import 'package:my_app/widget/dropzone_widget.dart';
import 'package:my_app/model/dropped_file.dart';
import 'package:my_app/widget/droppedImage_widget.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class RegistrationPage extends StatefulWidget {
  final String selectedName;
  const RegistrationPage({super.key, required this.selectedName});

  @override
  _RegistrationPageState createState() => _RegistrationPageState();
}

class _RegistrationPageState extends State<RegistrationPage> {
  DroppedFile? file;
  String? prediction;
  String? name;
  
  
  Future<Map<String, dynamic>> fetchData(DroppedFile file) async {
    final base64Image = base64Encode(file.bytes);
    const String url = 'https://b141-2001-f40-950-3d6-91e7-219-9c82-8489.ngrok-free.app';

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

    if (response.statusCode == 200) {
      final responseData = jsonDecode(response.body);
      return {'prediction': responseData['prediction']};
    } else {
      throw Exception('Failed to load data: unexpected response status code');
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
            DroppedFileWidget(file: file),
            
            SizedBox(
              height: 300,
              child: DropzoneWidget(
                onDroppedFile: (file) async {
                  setState(() => this.file = file);
                  try {
                    final response = await fetchData(file);
                    setState(() {
                      prediction = response['prediction'];
                    });
                    // Do something with the response
                  } catch (e) {
                    print(e);
                  }
                },
              ),
            ),
            if (prediction!= null && prediction==widget.selectedName)
              Text('Welcome $prediction', style: const TextStyle(fontSize: 24),),
            if (prediction!= null && prediction!=widget.selectedName)
              Text('Sorry, you are not ${widget.selectedName}', style: const TextStyle(fontSize: 24),),
          ],
        ),
      ),
    );
  }
}