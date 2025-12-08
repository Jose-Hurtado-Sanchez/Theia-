import 'package:flutter/material.dart';

class SelectFloorPlanScreen extends StatelessWidget {
  const SelectFloorPlanScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF255F89),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Title
              Text(
                "Select Floor Plan",
                style: const TextStyle(
                  fontSize: 26,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFFA7E8EB),
                ),
              ),

              const SizedBox(height: 20),

              // BOX for floor plans
              Expanded(
                child: Container(
                  width: double.infinity,
                  decoration: BoxDecoration(
                    color: const Color(0xFFA7E8EB),
                    borderRadius: BorderRadius.circular(14),
                  ),
                  padding: const EdgeInsets.all(16),

                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      // Centered title text
                      const Text(
                        "Floor Plans",
                        style: TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                          color: Colors.black,
                        ),
                      ),

                      const SizedBox(height: 20),

                      // Fake floor plans
                      Expanded(
                        child: ListView(
                          children: [
                            floorPlanItem("Office Floor 1"),
                            floorPlanItem("Office Floor 2"),
                            floorPlanItem("Home Floor 1"),
                            floorPlanItem("Home Floor 2"),
                            floorPlanItem("Library Floor"),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  // simple fake floor plan 
  Widget floorPlanItem(String name) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(10),
      ),
      child: Text(
        name,
        style: const TextStyle(fontSize: 18, color: Colors.black),
      ),
    );
  }
}
