import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

const apiUrl = String.fromEnvironment('ROBOLAB_API_URL', defaultValue: 'http://10.0.2.2:8000');

void main() => runApp(const RoboLabApp());

class RoboLabApp extends StatelessWidget {
  const RoboLabApp({super.key});
  @override
  Widget build(BuildContext context) => MaterialApp(
    title: 'RoboLab X', debugShowCheckedModeBanner: false,
    theme: ThemeData(useMaterial3: true, colorSchemeSeed: Colors.indigo, brightness: Brightness.dark),
    home: const HomePage(),
  );
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});
  @override State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final prompt = TextEditingController();
  String output = 'Describe what you want to build. RoboLab X will turn the idea into an engineering plan.';
  bool loading = false;
  bool pro = false;

  Future<void> generate() async {
    if (prompt.text.trim().isEmpty || loading) return;
    setState(() => loading = true);
    try {
      final response = await http.post(Uri.parse('$apiUrl/api/generate'), headers: {'content-type':'application/json'}, body: jsonEncode({'prompt': prompt.text.trim()}));
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      setState(() => output = data['result']?.toString() ?? data['detail']?.toString() ?? 'No result');
    } catch (_) {
      setState(() => output = 'RoboLab X is offline. Your project remains available locally; reconnect to generate with the cloud engineering pipeline.');
    } finally { setState(() => loading = false); }
  }

  Future<void> togglePro() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('pro_preview', !pro);
    setState(() => pro = !pro);
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('RoboLab X'), actions: [IconButton(onPressed: togglePro, icon: Icon(pro ? Icons.workspace_premium : Icons.lock_open))]),
    body: SafeArea(child: ListView(padding: const EdgeInsets.all(20), children: [
      const Text('Engineering, from idea to build.', style: TextStyle(fontSize: 30, fontWeight: FontWeight.bold)),
      const SizedBox(height: 8),
      Text(pro ? 'PRO PREVIEW • 48 specialist engineering roles' : 'CORE • Start building for free'),
      const SizedBox(height: 24),
      TextField(controller: prompt, maxLines: 5, decoration: const InputDecoration(labelText:'What are you building?', hintText:'Example: A line-following robot with obstacle detection', border: OutlineInputBorder())),
      const SizedBox(height: 12),
      FilledButton.icon(onPressed: loading ? null : generate, icon: loading ? const SizedBox(width:18,height:18,child:CircularProgressIndicator(strokeWidth:2)) : const Icon(Icons.auto_awesome), label: Text(loading ? 'Engineering…' : 'Build with RoboLab')),
      const SizedBox(height: 20),
      Card(child: Padding(padding: const EdgeInsets.all(18), child: SelectableText(output, style: const TextStyle(height:1.5)))),
      const SizedBox(height: 20),
      if (pro) const Card(child: ListTile(leading: Icon(Icons.verified), title: Text('RoboLab Pro'), subtitle: Text('Consensus review • advanced validation • firmware review • power analysis • CAD-ready specs • simulation planning')),
      const SizedBox(height: 24),
      const Text('Professional workflow', style: TextStyle(fontSize:20,fontWeight:FontWeight.bold)),
      const SizedBox(height:8),
      const Wrap(spacing:8, runSpacing:8, children: [Chip(label:Text('Requirements')), Chip(label:Text('Circuit')), Chip(label:Text('Firmware')), Chip(label:Text('CAD')), Chip(label:Text('Simulation')), Chip(label:Text('Verification'))]),
    ])),
  );
}
