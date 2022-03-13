import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import 'dart:convert' as convert;
import 'dart:async';
import 'dart:ui' as ui;

int i = 0;
int j = 0;
int m = 0;
int newloction = 0;
int location = 0;
double vertical = -10;
double horizontal = -10;
String location_name = '';
List last_locations = [0];
int count_replay = 0;
List accepted_locs = [
  [0],
  [15],
  [15],
  [0, 5, 6, 7, 8],
  [15],
  [15],
  [0, 3, 7, 8],
  [0, 3, 6, 8],
  [0, 3, 6, 7, 9, 11],
  [0, 8, 10, 11, 12],
  [0, 9, 12],
  [0, 8, 9],
  [0, 9, 10]
];
void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  _MyAppState createState() => _MyAppState();

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark(),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);
  @override
  HomeState createState() => HomeState();
}

class HomeState extends State<HomePage> {
  ui.Image? image;
  @override
  void initState() {
    super.initState();
    loadImage('assets/building.jpeg');
    Timer.periodic(const Duration(seconds: 1), update);
  }

  Future loadImage(String path) async {
    final data = await rootBundle.load(path);
    final bytes = data.buffer.asUint8List();
    final image = await decodeImageFromList(bytes);
    setState(() => this.image = image);
  }

  void update(Timer time) {
    getData();
    location = last_locations.last;
    setState(() {
      OpenPainter(image!).move(location);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        actions: [
          IconButton(
              icon: const Icon(Icons.replay),
              onPressed: () {
                i = 1;
                if (count_replay == 0) {
                  j = last_locations.length - 1;
                  m = j;
                } else {
                  m = j;
                }
                count_replay++;
                setState(() {});
              }),
          IconButton(
              icon: const Icon(Icons.play_arrow_outlined),
              onPressed: () {
                i = 2;
                vertical = -10;
                horizontal = -10;
                count_replay = 0;
                setState(() {});
              }),
        ],
        title: Text('location: ' + location_name),
      ),
      body: Center(
        child: image == null
            ? const CircularProgressIndicator()
            : Container(
                height: double.infinity,
                width: double.infinity,
                child: InteractiveViewer(
                  child: FittedBox(
                    child: SizedBox(
                      width: (image!.width.toDouble()),
                      height: image!.height.toDouble(),
                      child: CustomPaint(
                        painter: OpenPainter(image!),
                      ),
                    ),
                  ),
                ),
              ),
      ),
    );
  }
}

class OpenPainter extends CustomPainter {
  final ui.Image image;
  OpenPainter(this.image);

  void printLoc() {
    if (location == 1) {
      vertical = 79;
      horizontal = 70;
      location_name = 'Hallway';
    } else if (location == 2) {
      vertical = 79;
      horizontal = 230;
      location_name = 'Hallway';
    } else if (location == 3) {
      vertical = 180;
      horizontal = 160;
      location_name = 'Hallway';
    }
    /* 
    else if (location == 4) {
      vertical = 220;
      horizontal = 160;
      location_name = 'Hallway';
    }
    */
    else if (location == 5) {
      vertical = 175;
      horizontal = 220;
      location_name = 'Lectures Hall';
    } else if (location == 6) {
      vertical = 280;
      horizontal = 70;
      location_name = 'Hallway';
    } else if (location == 7) {
      vertical = 280;
      horizontal = 220;
      location_name = 'Hallway';
    } else if (location == 8) {
      vertical = 350;
      horizontal = 160;
      location_name = 'Hallway';
    } else if (location == 9) {
      vertical = 490;
      horizontal = 160;
      location_name = 'Hallway';
    } else if (location == 10) {
      vertical = 650;
      horizontal = 160;
      location_name = 'Hallway';
    } else if (location == 11) {
      vertical = 450;
      horizontal = 80;
      location_name = 'Electronics Lab';
    } else if (location == 12) {
      vertical = 565;
      horizontal = 100;
      location_name = 'Doctors Room';
    }
  }

  @override
  void paint(Canvas canvas, Size size) {
    var paint1 = Paint()..color = Colors.deepOrange;
    var paint2 = Paint()..color = Colors.blue;
    if (i == 0) {
      canvas.drawImage(image, Offset.zero, paint1);
    } else if (i == 1) {
      canvas.drawImage(image, Offset.zero, paint2);
      canvas.drawCircle(Offset(horizontal, vertical), 8, paint2);
    } else if (i == 2) {
      canvas.drawImage(image, Offset.zero, paint1);
      canvas.drawCircle(Offset(horizontal, vertical), 8, paint1);
    }
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => true;
  void move(int newlocation) {
    if (i == 1) {
      if (m > 0) {
        location = last_locations[m];
        m--;
        printLoc();
      }
    } else if (i == 2) {
      location = newlocation;
      printLoc();
    }
  }
}

Future getData() async {
  var url = "http://192.168.43.145:5000/api/get_estimation";
  http.Response response = await http.get(Uri.parse(url));
  var responsebody = response.body;
  print(responsebody);
  newloction = int.parse(responsebody);
  if (last_locations.last != newloction) {
    if (accepted_locs[newloction].contains(last_locations.last)) {
      last_locations.add(newloction);
    }
  }
  print(last_locations);
  return responsebody;
}

