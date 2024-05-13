// ignore: file_names
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:my_app/model/dropped_file.dart';

class DroppedFileWidget extends StatelessWidget{
  
  final DroppedFile? file;
  
  const DroppedFileWidget({
    super.key,
    required this.file,
  });
  
  


  @override
  Widget build(BuildContext context) => buildImage();

  Widget buildImage(){
    if (file == null) return buildEmptyFile('No File');
    return Image.memory(
      Uint8List.fromList(file!.bytes),
      width: 120,
      height: 120,
      fit: BoxFit.cover,
    );
  }

  Widget buildEmptyFile(String text)=>Container(
    width: 120,
    height: 120,
    color: Colors.blue.shade300,
    child: Center(
      child: Text(
        text,
        style: const TextStyle(
          color: Colors.white,
          fontSize: 16,
        ),
      ),
    )
  );

  }
    
