import 'package:flutter/material.dart';
import 'dart:math' as math;
import 'SelectScreen.dart';

class StartScreen extends StatelessWidget {
  const StartScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF255F89), // Blue background
      body:GestureDetector(
        behavior: HitTestBehavior.opaque,
        onTap: () {
          // Navigate to next screen or perform any action
          Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => const SelectScreen()), 
          );
        },
      
      
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Click Anywhere text
            const Text(
              "Click Anywhere",
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),

            const SizedBox(height: 80),
            buildLogo()
            
          ],
        ),
      ),
    ),
    );
  }


  
}
// Function to build the logo with circles and lines
Widget buildLogo() {
  return SizedBox(
    height: 250,
    width: 250,
    child: LayoutBuilder(
      builder: (context, constraints) {
        final center = constraints.maxWidth / 2;
        final radius = 70;

        return Stack(
          alignment: Alignment.center,
          children: [
            for (double angle in [0, 45, 90, 135, 180, 225, 270, 315])
              Positioned(
                left: center + radius * math.cos(angle * math.pi / 180) - 25,
                top: center + radius * math.sin(angle * math.pi / 180) - 25,
                // white circles
                child: Container(
                  height: 55,
                  width: 55,
                  decoration: const BoxDecoration(
                    shape: BoxShape.circle,
                    color: Colors.white,
                  ),
                ),
               
              ),
              // smaller blue circles on the outside
          for (double angle in [0, 45, 90, 135, 180, 225, 270, 315])
              Positioned(
                left: center + (radius + 35) * math.cos(angle * math.pi / 180) - 15,
                top: center + (radius + 35) * math.sin(angle * math.pi / 180) - 15,
                // smaller blue circles
                child: Container(
                  height: 30,
                  width: 30,
                  decoration: const BoxDecoration(
                    shape: BoxShape.circle,
                    color: Color(0xFF255F89),
                  ),
                ),
              ),
            for (double angle in [0, 45, 90, 135, 180, 225, 270, 315]) 
              Positioned(
                left: center + (radius + 50) * math.cos(angle * math.pi / 180) - 2,
                top: center + (radius + 50) * math.sin(angle * math.pi / 180) - 20,
                child: Transform.rotate(
                  angle: (angle + 90) * math.pi / 180,
                // lines coming out of the eye
                child: Container(
                  height: 40,
                  width: 4,
                  color: Color.fromARGB(255, 255, 255, 255),
                  
                ),
                ),
            ),


            const Text(
              "THEIA",
              style: TextStyle(
                color: Colors.white,
                fontSize: 28,
                fontWeight: FontWeight.bold,
              ),
            )
          ],
        );
      },
    ),
  );
}