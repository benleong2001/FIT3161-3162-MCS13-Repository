import 'package:flutter/material.dart';
import 'package:my_app/widget/dropzone_widget.dart';
import 'package:my_app/model/dropped_file.dart';
import 'package:my_app/widget/droppedImage_widget.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';


class RegistrationPage extends StatefulWidget {
  const RegistrationPage({super.key});

  @override
  _RegistrationPageState createState() => _RegistrationPageState();
}

class _RegistrationPageState extends State<RegistrationPage> {
  DroppedFile? file;
  String? prediction;
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
            const SizedBox(height: 16),
            SizedBox(
              height: 300,
              child: DropzoneWidget(
                onDroppedFile: (file) async {
                  setState(() => this.file = file);
                  try {
                    final response = await fetchData(file);
                    setState(() => prediction = response['prediction']);
                    // Do something with the response
                  } catch (e) {
                    print(e);
                  }
                },
              ),
            ),
            if(prediction != null)
              Text('Prediction: $prediction',style: const TextStyle(fontSize: 24),),
          ],
        ),
      ),
    );
  }
}

Future<Map<String, dynamic>> fetchData(DroppedFile file) async {
  final base64Image = base64Encode(file.bytes);

  final response = await http.post(
    Uri.parse('https://ffa6-202-186-176-157.ngrok-free.app/predict'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'name': file.name,
      'base64_bytes': base64Image,
    }),
  ).catchError((error) {
    throw Exception('Failed to load data: $error');
  });

  if (response.statusCode == 200) {
    return jsonDecode(response.body);
  } else {
    throw Exception('Failed to load data: unexpected response status code');
  }
}