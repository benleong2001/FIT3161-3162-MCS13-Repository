// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart'; 
import 'package:flutter_dropzone/flutter_dropzone.dart';
import 'package:my_app/model/dropped_file.dart';
class DropzoneWidget extends StatefulWidget {
  final ValueChanged<DroppedFile> onDroppedFile;
  
  const DropzoneWidget({Key? key, required this.onDroppedFile}) : super(key: key);

  @override
  // ignore: library_private_types_in_public_api
  _DropzoneWidgetState createState() => _DropzoneWidgetState();
}

class _DropzoneWidgetState extends State<DropzoneWidget> {
  late DropzoneViewController controller;
  @override
  Widget build(BuildContext context) {
    final colorButton = Colors.green.shade300;
    return Container(
      color: Colors.green,
      child: Stack(
        children: [
          DropzoneView(
            onCreated: (controller)=> this.controller = controller ,
            onDrop: acceptFile,), 
          Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.cloud_upload,size:80,color: Colors.white),
                Text('Drop your image here',style: TextStyle(color: Colors.white,fontSize: 24)),
                const SizedBox(height: 16,),
                ElevatedButton.icon(
                  style:ElevatedButton.styleFrom(
                    backgroundColor: colorButton,
                    padding: EdgeInsets.symmetric(horizontal: 32,vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                  ),
                  icon: Icon(Icons.search,color: Colors.white,size:32,),
                  label: Text('Upload Image',
                    style: TextStyle(color:Colors.white,fontSize: 16),
                  ),
                  onPressed: () async{
                    final file = await FilePicker.platform.pickFiles(
                      type: FileType.any,
                    );
                    if(file == null) return;
                    final name = file.files.single.name;
                    final bytes = file.files.single.bytes;
                    final droppedFile = DroppedFile(
                      name: name,
                      bytes: bytes!,
                    );
                    widget.onDroppedFile(droppedFile);
                    
                    
                    

                    
                    
                  },
                  ),
                ],
              ),
            ),
          ],
        ),
      );
    }
  

  Future acceptFile(dynamic event) async {
    final name = await controller.getFilename(event);
    final bytes = await controller.getFileData(event);
    final droppedFile = DroppedFile(
      name: name,
      bytes: bytes,
    );
    widget.onDroppedFile(droppedFile);
  }
}