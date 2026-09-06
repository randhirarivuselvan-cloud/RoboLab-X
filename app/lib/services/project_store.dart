import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

class SavedProject {
  final String id;
  final String title;
  final String idea;
  final DateTime updatedAt;
  final Map<String, dynamic> payload;

  SavedProject({required this.id, required this.title, required this.idea, required this.updatedAt, required this.payload});

  Map<String, dynamic> toJson() => {
    'id': id,
    'title': title,
    'idea': idea,
    'updated_at': updatedAt.toIso8601String(),
    'payload': payload,
  };

  factory SavedProject.fromJson(Map<String, dynamic> json) => SavedProject(
    id: json['id'].toString(),
    title: json['title']?.toString() ?? 'Untitled project',
    idea: json['idea']?.toString() ?? '',
    updatedAt: DateTime.tryParse(json['updated_at']?.toString() ?? '') ?? DateTime.now(),
    payload: (json['payload'] is Map<String, dynamic>) ? json['payload'] as Map<String, dynamic> : <String, dynamic>{},
  );
}

class ProjectStore {
  static const _key = 'robolab_projects_v2';

  static Future<List<SavedProject>> load() async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getStringList(_key) ?? const [];
    final items = <SavedProject>[];
    for (final item in raw) {
      try {
        items.add(SavedProject.fromJson(jsonDecode(item) as Map<String, dynamic>));
      } catch (_) {}
    }
    items.sort((a, b) => b.updatedAt.compareTo(a.updatedAt));
    return items;
  }

  static Future<void> save(SavedProject project) async {
    final prefs = await SharedPreferences.getInstance();
    final projects = await load();
    projects.removeWhere((p) => p.id == project.id);
    projects.insert(0, project);
    final trimmed = projects.take(50).map((p) => jsonEncode(p.toJson())).toList();
    await prefs.setStringList(_key, trimmed);
  }

  static Future<void> delete(String id) async {
    final prefs = await SharedPreferences.getInstance();
    final projects = await load();
    projects.removeWhere((p) => p.id == id);
    await prefs.setStringList(_key, projects.map((p) => jsonEncode(p.toJson())).toList());
  }
}
