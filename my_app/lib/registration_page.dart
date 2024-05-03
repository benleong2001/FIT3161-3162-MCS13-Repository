import 'package:flutter/material.dart';
import 'package:my_app/widget/dropzone_widget.dart';
import 'package:my_app/model/dropped_file.dart';
import 'package:my_app/widget/droppedImage_widget.dart';
class RegistrationPage extends StatefulWidget {
  @override
  _RegistrationPageState createState() => _RegistrationPageState();
}

class _RegistrationPageState extends State<RegistrationPage> {
  DroppedFile? file;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Registration Page'),
      ),
      body: Container(
        alignment: Alignment.center,
        padding: const EdgeInsets.all(16),
       
          child:Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              DroppedFileWidget(file: file),
              const SizedBox(height: 16),
              Container(
              height: 300,
              child: 
              DropzoneWidget(
              onDroppedFile: (file){
                setState(() => this.file = file); 
                  
                  }
                  ),
                ),]
              
              )
          ),
        );
    }
  }
