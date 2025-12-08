import 'package:flutter/material.dart';

class CreateFloorPlanScreen extends StatefulWidget {
  const CreateFloorPlanScreen({super.key});

  @override
  State<CreateFloorPlanScreen> createState() => _CreateFloorPlanScreenState();
}

class _CreateFloorPlanScreenState extends State<CreateFloorPlanScreen> {
  String? selectedFloors;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF255F89), // blue background
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            children: [
              const SizedBox(height: 20),

              // Floor plan name
              TextField(
                decoration: InputDecoration(
                  hintText: "Name of Floor Plan",
                  filled: true,
                  fillColor: Colors.white,
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: BorderSide.none,
                  ),
                ),
              ),

              const SizedBox(height: 16),

              // Dropdown: How many floors
              DropdownButtonFormField<String>(
                value: selectedFloors,
                decoration: InputDecoration(
                  hintText: "How Many Floors?",
                  filled: true,
                  fillColor: Colors.white,
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: BorderSide.none,
                  ),
                ),
                items: ["1", "2", "3", "4", "5+"]
                    .map((floor) => DropdownMenuItem(
                          value: floor,
                          child: Text(floor),
                        ))
                    .toList(),
                onChanged: (value) {
                  setState(() {
                    selectedFloors = value;
                  });
                },
              ),

              const Spacer(),

              // Next button
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () {
                    // tb done
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFFA7E8EB), // light aqua
                    foregroundColor: Colors.black,
                    padding: const EdgeInsets.symmetric(vertical: 14),
                  ),
                  child: const Text(
                    "Next",
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                ),
              ),

              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }
}
