import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

const apiUrl = String.fromEnvironment('ROBOLAB_API_URL', defaultValue: 'http://10.0.2.2:8000');

void main() => runApp(const RoboLabXApp());

class RoboLabXApp extends StatelessWidget {
  const RoboLabXApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'RoboLab-X',
      theme: ThemeData(useMaterial3: true, colorSchemeSeed: Colors.indigo, brightness: Brightness.dark),
      home: const WorkspacePage(),
    );
  }
}

class WorkspacePage extends StatefulWidget {
  const WorkspacePage({super.key});
  @override
  State<WorkspacePage> createState() => _WorkspacePageState();
}

class _WorkspacePageState extends State<WorkspacePage> {
  final controller = TextEditingController();
  bool pro = false;
  bool busy = false;
  Map<String, dynamic>? result;

  Future<void> generate() async {
    if (controller.text.trim().length < 3 || busy) return;
    setState(() => busy = true);
    try {
      final response = await http.post(
        Uri.parse('$apiUrl/api/v1/projects/generate'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'idea': controller.text.trim(), 'pro': pro}),
      );
      if (response.statusCode >= 200 && response.statusCode < 300) {
        setState(() => result = jsonDecode(response.body) as Map<String, dynamic>);
      } else {
        throw Exception('Backend returned ${response.statusCode}');
      }
    } catch (_) {
      setState(() => result = {'project': {'idea': controller.text.trim(), 'offline': true, 'message': 'Offline draft created. Connect to RoboLab-X API for full engineering synthesis.'}});
    } finally {
      if (mounted) setState(() => busy = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('RoboLab-X'), actions: [
        Row(children: [const Text('PRO'), Switch(value: pro, onChanged: (v) => setState(() => pro = v)), const SizedBox(width: 8)])
      ]),
      body: ListView(padding: const EdgeInsets.all(20), children: [
        Text('Engineering workspace', style: Theme.of(context).textTheme.headlineMedium?.copyWith(fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        const Text('Describe what you want to build. RoboLab-X turns the idea into a structured engineering project.'),
        const SizedBox(height: 20),
        TextField(controller: controller, minLines: 5, maxLines: 10, decoration: const InputDecoration(border: OutlineInputBorder(), hintText: 'Example: Build a line-following robot with obstacle detection'),),
        const SizedBox(height: 12),
        FilledButton.icon(onPressed: busy ? null : generate, icon: busy ? const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2)) : const Icon(Icons.auto_awesome), label: Text(busy ? 'Engineering…' : 'Generate Project')),
        if (result != null) ...[
          const SizedBox(height: 24),
          Card(child: Padding(padding: const EdgeInsets.all(16), child: SelectableText(const JsonEncoder.withIndent('  ').convert(result)))),
        ],
      ]),
    );
  }
}
