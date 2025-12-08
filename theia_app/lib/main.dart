import 'package:flutter/material.dart';
import 'screens/StartScreen.dart';

void main() {
  runApp(const MyApp());
}

// Root of the app – this wraps everything in MaterialApp
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: StartScreen(),   // <- your screen below
    );
  }
}













