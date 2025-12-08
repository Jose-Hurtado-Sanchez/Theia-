import 'package:flutter/material.dart';
import 'CreateFloorPlanScreen.dart';
import 'SelectFloorPlanScreen.dart';


class SelectScreen extends StatelessWidget {
  const SelectScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromARGB(255, 3, 241, 254),
      body: Column(
        children: [
        //top button
        Expanded(
          child: GestureDetector(
            onTap: () {
              print("Create Floor Plan tapped");

              // Navigate to Create Floor Plan screen!
              Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => const CreateFloorPlanScreen()), 
          );
            },
            child: Container(
              alignment: Alignment.center,
              child: const Text(
                "Create Floor Plan",
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: Colors.black,
                ),
              ),
            )
          )
        ),
        Container(
          height: 20,
          color: const Color(0xFF255F89),
        ),


        //bottom button
        Expanded(
          child: GestureDetector(
            onTap: () {
              print("View Saved Plans tapped");
              // Navigate to View Saved Plans screen
              Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => const SelectFloorPlanScreen()),
            );
            },
            child: Container(
              alignment: Alignment.center,
              child: const Text(
                "Selected Floor Plans",
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: Colors.black,
                ),
              ),
            )
          )
        ),
      ],)
    );
  }
}