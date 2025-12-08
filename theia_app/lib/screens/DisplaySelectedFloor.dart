import 'package:flutter/material.dart';

class SelectFloorPlanScreen extends StatelessWidget {
  const SelectFloorPlanScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF255F89), // blue background
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

              // Floor Plan Box
              Expanded(
                child: Container(
                  width: double.infinity,
                  decoration: BoxDecoration(
                    color: const Color(0xFFA7E8EB),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  padding: const EdgeInsets.all(16),

                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      // Centered Title
                      const Text(
                        "Floor Plans",
                        style: TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                          color: Colors.black,
                        ),
                      ),

                      const SizedBox(height: 20),

                      // Fake Floor Plans
                      Expanded(
                        child: ListView(
                          children: [
                            _fakeFloorPlanItem("Office Floor Plan"),
                            _fakeFloorPlanItem("Home Floor Plan"),
                            _fakeFloorPlanItem("Mall Layout"),
                            _fakeFloorPlanItem("WSU Engineering Building"),
                            _fakeFloorPlanItem("Airport Terminal A"),
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

  
  // Fake Floor Plan (will replace with real data later)
  
  Widget _fakeFloorPlanItem(String name) {
    return Container(
      margin: const EdgeInsets.symmetric(vertical: 8),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Text(
        name,
        style: const TextStyle(
          fontSize: 18,
          fontWeight: FontWeight.w500,
        ),
      ),
    );
  }
}
