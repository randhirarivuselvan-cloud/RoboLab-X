import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:in_app_purchase/in_app_purchase.dart';
import 'services/api_service.dart';
import 'services/session_service.dart';
import 'services/project_store.dart';
import 'services/billing_service.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const RoboLabXApp());
}

class RoboLabXApp extends StatelessWidget {
  const RoboLabXApp({super.key});

  @override
  Widget build(BuildContext context) {
    final scheme = ColorScheme.fromSeed(
      seedColor: const Color(0xFF7C4DFF),
      brightness: Brightness.dark,
      surface: const Color(0xFF111218),
    );
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'RoboLab-X',
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: scheme,
        scaffoldBackgroundColor: const Color(0xFF0B0C10),
        cardTheme: const CardThemeData(
          elevation: 0,
          margin: EdgeInsets.zero,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.all(Radius.circular(22))),
        ),
        inputDecorationTheme: const InputDecorationTheme(
          filled: true,
          border: OutlineInputBorder(borderRadius: BorderRadius.all(Radius.circular(18)), borderSide: BorderSide.none),
        ),
        navigationBarTheme: const NavigationBarThemeData(height: 72),
      ),
      home: const BootstrapPage(),
    );
  }
}

class BootstrapPage extends StatefulWidget {
  const BootstrapPage({super.key});
  @override
  State<BootstrapPage> createState() => _BootstrapPageState();
}

class _BootstrapPageState extends State<BootstrapPage> {
  UserSession? session;
  bool loading = true;

  @override
  void initState() {
    super.initState();
    _restore();
  }

  Future<void> _restore() async {
    session = await SessionService.restore();
    if (mounted) setState(() => loading = false);
  }

  @override
  Widget build(BuildContext context) {
    if (loading) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }
    if (session == null) {
      return AuthPage(onAuthenticated: (s) => setState(() => session = s));
    }
    return AppShell(
      session: session!,
      onSessionChanged: (s) => setState(() => session = s),
      onSignedOut: () => setState(() => session = null),
    );
  }
}

class AuthPage extends StatefulWidget {
  final ValueChanged<UserSession> onAuthenticated;
  const AuthPage({super.key, required this.onAuthenticated});
  @override
  State<AuthPage> createState() => _AuthPageState();
}

class _AuthPageState extends State<AuthPage> {
  bool busy = false;
  String? error;

  Future<void> _run(Future<UserSession> Function() action) async {
    setState(() { busy = true; error = null; });
    try {
      widget.onAuthenticated(await action());
    } catch (e) {
      if (mounted) setState(() => error = e.toString().replaceFirst('Exception: ', ''));
    } finally {
      if (mounted) setState(() => busy = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(28),
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 560),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const _BrandMark(size: 88),
                  const SizedBox(height: 28),
                  Text('RoboLab-X', textAlign: TextAlign.center, style: theme.textTheme.displaySmall?.copyWith(fontWeight: FontWeight.w900, letterSpacing: -1.5)),
                  const SizedBox(height: 10),
                  Text('AI robotics engineering workspace', textAlign: TextAlign.center, style: theme.textTheme.titleMedium?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
                  const SizedBox(height: 36),
                  FilledButton.icon(
                    onPressed: busy ? null : () => _run(SessionService.signInWithGoogle),
                    icon: const Icon(Icons.account_circle_outlined),
                    label: const Padding(padding: EdgeInsets.symmetric(vertical: 16), child: Text('Continue with Google')),
                  ),
                  const SizedBox(height: 12),
                  OutlinedButton.icon(
                    onPressed: busy ? null : () => _run(SessionService.continueAsGuest),
                    icon: const Icon(Icons.person_outline),
                    label: const Padding(padding: EdgeInsets.symmetric(vertical: 16), child: Text('Continue as Guest')),
                  ),
                  if (busy) ...[
                    const SizedBox(height: 24),
                    const LinearProgressIndicator(),
                  ],
                  if (error != null) ...[
                    const SizedBox(height: 18),
                    _MessageCard(icon: Icons.error_outline, text: error!, error: true),
                  ],
                  const SizedBox(height: 28),
                  Text('Guest projects are stored locally on this device. Sign in with Google for an account identity and future cloud sync.', textAlign: TextAlign.center, style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class AppShell extends StatefulWidget {
  final UserSession session;
  final ValueChanged<UserSession> onSessionChanged;
  final VoidCallback onSignedOut;
  const AppShell({super.key, required this.session, required this.onSessionChanged, required this.onSignedOut});
  @override
  State<AppShell> createState() => _AppShellState();
}

class _AppShellState extends State<AppShell> {
  int index = 0;

  @override
  Widget build(BuildContext context) {
    final pages = [
      HomePage(session: widget.session, onBuild: () => setState(() => index = 1), onPro: () => setState(() => index = 3)),
      BuilderPage(session: widget.session),
      const ProjectsPage(),
      ProPage(session: widget.session, onSessionChanged: widget.onSessionChanged),
      SettingsPage(session: widget.session, onSignedOut: widget.onSignedOut),
    ];
    return Scaffold(
      body: IndexedStack(index: index, children: pages),
      bottomNavigationBar: NavigationBar(
        selectedIndex: index,
        onDestinationSelected: (value) => setState(() => index = value),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.auto_awesome_outlined), selectedIcon: Icon(Icons.auto_awesome), label: 'Build'),
          NavigationDestination(icon: Icon(Icons.folder_outlined), selectedIcon: Icon(Icons.folder), label: 'Projects'),
          NavigationDestination(icon: Icon(Icons.workspace_premium_outlined), selectedIcon: Icon(Icons.workspace_premium), label: 'Pro'),
          NavigationDestination(icon: Icon(Icons.settings_outlined), selectedIcon: Icon(Icons.settings), label: 'Settings'),
        ],
      ),
    );
  }
}

class HomePage extends StatelessWidget {
  final UserSession session;
  final VoidCallback onBuild;
  final VoidCallback onPro;
  const HomePage({super.key, required this.session, required this.onBuild, required this.onPro});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return _PageFrame(
      title: 'RoboLab-X',
      subtitle: 'Welcome, ${session.displayName}',
      child: ListView(
        padding: const EdgeInsets.fromLTRB(20, 8, 20, 28),
        children: [
          Container(
            padding: const EdgeInsets.all(24),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(28),
              gradient: LinearGradient(colors: [theme.colorScheme.primaryContainer, theme.colorScheme.secondaryContainer]),
            ),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              const _BrandMark(size: 48),
              const SizedBox(height: 22),
              Text('From idea to engineered project.', style: theme.textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w900)),
              const SizedBox(height: 10),
              const Text('Describe a robot or embedded system. RoboLab-X routes the work through specialist engineering roles, verification, quality checks and consensus.'),
              const SizedBox(height: 22),
              FilledButton.icon(onPressed: onBuild, icon: const Icon(Icons.auto_awesome), label: const Text('Start engineering')),
            ]),
          ),
          const SizedBox(height: 22),
          Text('Engineering suite', style: theme.textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w800)),
          const SizedBox(height: 12),
          const Wrap(spacing: 10, runSpacing: 10, children: [
            _FeatureChip(Icons.account_tree_outlined, 'Architecture'),
            _FeatureChip(Icons.electrical_services_outlined, 'Circuits'),
            _FeatureChip(Icons.memory_outlined, 'Firmware'),
            _FeatureChip(Icons.precision_manufacturing_outlined, 'Robotics'),
            _FeatureChip(Icons.view_in_ar_outlined, 'CAD specs'),
            _FeatureChip(Icons.science_outlined, 'Simulation'),
            _FeatureChip(Icons.fact_check_outlined, 'Verification'),
            _FeatureChip(Icons.inventory_2_outlined, 'BOM'),
          ]),
          const SizedBox(height: 22),
          Card(
            child: ListTile(
              contentPadding: const EdgeInsets.all(18),
              leading: CircleAvatar(child: Icon(session.isPro ? Icons.workspace_premium : Icons.engineering_outlined)),
              title: Text(session.isPro ? 'RoboLab Pro active' : '48 specialist engineering fleet'),
              subtitle: Text(session.isPro ? 'Advanced capabilities are enabled for this account.' : 'Upgrade to Pro for full specialist routing, deeper verification, CAD/simulation specs and priority generation.'),
              trailing: const Icon(Icons.chevron_right),
              onTap: onPro,
            ),
          ),
        ],
      ),
    );
  }
}

class BuilderPage extends StatefulWidget {
  final UserSession session;
  const BuilderPage({super.key, required this.session});
  @override
  State<BuilderPage> createState() => _BuilderPageState();
}

class _BuilderPageState extends State<BuilderPage> {
  final controller = TextEditingController();
  bool busy = false;
  bool requestPro = true;
  Map<String, dynamic>? result;
  String? error;

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  Future<void> generate() async {
    final idea = controller.text.trim();
    if (idea.length < 3 || busy) return;
    setState(() { busy = true; error = null; });
    try {
      final data = await ApiService.postJson(
        '/api/v1/projects/generate',
        {'idea': idea, 'pro': requestPro, 'use_ai': true},
        token: widget.session.token,
        timeout: const Duration(seconds: 150),
      );
      final project = (data['project'] as Map?)?.cast<String, dynamic>() ?? <String, dynamic>{};
      setState(() => result = data);
      final title = _projectTitle(idea);
      await ProjectStore.save(SavedProject(
        id: data['request_id']?.toString() ?? DateTime.now().microsecondsSinceEpoch.toString(),
        title: title,
        idea: idea,
        updatedAt: DateTime.now(),
        payload: project,
      ));
    } catch (e) {
      final offline = <String, dynamic>{
        'offline': true,
        'idea': idea,
        'message': 'Saved as an offline draft. Re-run when the RoboLab-X backend is reachable.',
      };
      await ProjectStore.save(SavedProject(
        id: 'offline-${DateTime.now().microsecondsSinceEpoch}',
        title: _projectTitle(idea),
        idea: idea,
        updatedAt: DateTime.now(),
        payload: offline,
      ));
      if (mounted) setState(() => error = 'Backend unavailable. Your idea was saved locally as an offline draft.');
    } finally {
      if (mounted) setState(() => busy = false);
    }
  }

  String _projectTitle(String idea) {
    final compact = idea.replaceAll(RegExp(r'\s+'), ' ').trim();
    return compact.length <= 42 ? compact : '${compact.substring(0, 42)}…';
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return _PageFrame(
      title: 'Engineering Builder',
      subtitle: 'Describe the outcome, constraints and environment',
      child: ListView(
        padding: const EdgeInsets.fromLTRB(20, 8, 20, 28),
        children: [
          TextField(
            controller: controller,
            minLines: 7,
            maxLines: 14,
            textCapitalization: TextCapitalization.sentences,
            decoration: const InputDecoration(
              hintText: 'Example: Design a compact indoor delivery robot using an ESP32, wheel encoders and ultrasonic sensors. It should carry 2 kg, stop safely if an obstacle appears, and run for at least 90 minutes.',
            ),
          ),
          const SizedBox(height: 14),
          Card(
            child: SwitchListTile(
              value: requestPro,
              onChanged: (v) => setState(() => requestPro = v),
              title: const Text('Request Pro-depth engineering'),
              subtitle: const Text('Uses the full specialist fleet when your account or beta entitlement allows it.'),
              secondary: const Icon(Icons.workspace_premium_outlined),
            ),
          ),
          const SizedBox(height: 14),
          FilledButton.icon(
            onPressed: busy ? null : generate,
            icon: busy ? const SizedBox.square(dimension: 20, child: CircularProgressIndicator(strokeWidth: 2)) : const Icon(Icons.bolt),
            label: Padding(padding: const EdgeInsets.symmetric(vertical: 14), child: Text(busy ? 'Engineering project…' : 'Generate engineering project')),
          ),
          if (error != null) ...[
            const SizedBox(height: 14),
            _MessageCard(icon: Icons.cloud_off_outlined, text: error!, error: true),
          ],
          if (result != null) ...[
            const SizedBox(height: 22),
            _ResultOverview(data: result!),
            const SizedBox(height: 14),
            ExpansionTile(
              title: const Text('Full structured project JSON'),
              leading: const Icon(Icons.data_object),
              children: [
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(color: theme.colorScheme.surfaceContainer, borderRadius: BorderRadius.circular(18)),
                  child: SelectableText(const JsonEncoder.withIndent('  ').convert(result)),
                ),
              ],
            ),
          ],
        ],
      ),
    );
  }
}

class ProjectsPage extends StatefulWidget {
  const ProjectsPage({super.key});
  @override
  State<ProjectsPage> createState() => _ProjectsPageState();
}

class _ProjectsPageState extends State<ProjectsPage> {
  Future<List<SavedProject>> projects = ProjectStore.load();
  void refresh() => setState(() => projects = ProjectStore.load());

  @override
  Widget build(BuildContext context) {
    return _PageFrame(
      title: 'My Projects',
      subtitle: 'Local project workspace',
      action: IconButton(onPressed: refresh, icon: const Icon(Icons.refresh)),
      child: FutureBuilder<List<SavedProject>>(
        future: projects,
        builder: (context, snapshot) {
          final items = snapshot.data ?? const <SavedProject>[];
          if (snapshot.connectionState != ConnectionState.done) return const Center(child: CircularProgressIndicator());
          if (items.isEmpty) return const _EmptyState(icon: Icons.folder_open_outlined, title: 'No projects yet', text: 'Generate a project in the Builder and it will appear here automatically.');
          return ListView.separated(
            padding: const EdgeInsets.fromLTRB(20, 8, 20, 28),
            itemCount: items.length,
            separatorBuilder: (_, __) => const SizedBox(height: 10),
            itemBuilder: (context, i) {
              final p = items[i];
              return Card(
                child: ListTile(
                  contentPadding: const EdgeInsets.all(16),
                  leading: const CircleAvatar(child: Icon(Icons.precision_manufacturing_outlined)),
                  title: Text(p.title, maxLines: 2, overflow: TextOverflow.ellipsis),
                  subtitle: Text('${p.updatedAt.toLocal()}${p.payload['offline'] == true ? ' • Offline draft' : ''}', maxLines: 1, overflow: TextOverflow.ellipsis),
                  trailing: PopupMenuButton<String>(
                    onSelected: (value) async {
                      if (value == 'delete') { await ProjectStore.delete(p.id); refresh(); }
                    },
                    itemBuilder: (_) => const [PopupMenuItem(value: 'delete', child: Text('Delete'))],
                  ),
                  onTap: () => showModalBottomSheet<void>(
                    context: context,
                    isScrollControlled: true,
                    showDragHandle: true,
                    builder: (_) => DraggableScrollableSheet(
                      expand: false,
                      initialChildSize: .78,
                      maxChildSize: .95,
                      builder: (_, scroll) => ListView(controller: scroll, padding: const EdgeInsets.all(20), children: [
                        Text(p.title, style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold)),
                        const SizedBox(height: 12),
                        SelectableText(const JsonEncoder.withIndent('  ').convert(p.payload)),
                      ]),
                    ),
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}

class ProPage extends StatefulWidget {
  final UserSession session;
  final ValueChanged<UserSession> onSessionChanged;
  const ProPage({super.key, required this.session, required this.onSessionChanged});
  @override
  State<ProPage> createState() => _ProPageState();
}

class _ProPageState extends State<ProPage> {
  final billing = BillingService();
  bool loading = true;
  bool storeAvailable = false;
  String? message;

  @override
  void initState() {
    super.initState();
    _init();
  }

  Future<void> _init() async {
    final available = await billing.initialize(_purchaseReceived);
    if (mounted) setState(() { storeAvailable = available; loading = false; });
  }

  void _purchaseReceived(PurchaseDetails purchase) {
    if (!mounted) return;
    setState(() => message = 'Purchase received from Google Play. Server-side entitlement verification must confirm it before Pro is permanently enabled.');
  }

  @override
  void dispose() {
    billing.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return _PageFrame(
      title: 'RoboLab Pro',
      subtitle: widget.session.isPro ? 'Pro active' : 'Push every project further',
      child: ListView(
        padding: const EdgeInsets.fromLTRB(20, 8, 20, 28),
        children: [
          Container(
            padding: const EdgeInsets.all(24),
            decoration: BoxDecoration(borderRadius: BorderRadius.circular(28), gradient: LinearGradient(colors: [theme.colorScheme.primary, theme.colorScheme.tertiary])),
            child: const Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Icon(Icons.workspace_premium, size: 44),
              SizedBox(height: 18),
              Text('48 specialist engineers. One coherent project.', style: TextStyle(fontSize: 24, fontWeight: FontWeight.w900)),
              SizedBox(height: 8),
              Text('Advanced generation, adversarial verification, power analysis, firmware review, CAD-ready specifications, simulation planning, export and priority processing.'),
            ]),
          ),
          const SizedBox(height: 18),
          const _PlanCard(title: 'Monthly', price: '₹99', period: '/ month', detail: 'Flexible access to RoboLab Pro.'),
          const SizedBox(height: 10),
          const _PlanCard(title: 'Annual', price: '₹799', period: '/ year', detail: 'Best value for ongoing robotics projects.', recommended: true),
          const SizedBox(height: 18),
          if (loading) const LinearProgressIndicator(),
          if (!loading && billing.products.isNotEmpty)
            ...billing.products.map((product) => Padding(
              padding: const EdgeInsets.only(bottom: 10),
              child: FilledButton(
                onPressed: () => billing.buy(product),
                child: Padding(padding: const EdgeInsets.symmetric(vertical: 14), child: Text('Subscribe • ${product.price}')),
              ),
            )),
          if (!loading && !storeAvailable)
            const _MessageCard(icon: Icons.storefront_outlined, text: 'Google Play Billing is not available in this build/device. Install a Play-distributed test build to test subscriptions.'),
          OutlinedButton.icon(onPressed: storeAvailable ? billing.restore : null, icon: const Icon(Icons.restore), label: const Text('Restore purchases')),
          if (message != null) ...[
            const SizedBox(height: 12),
            _MessageCard(icon: Icons.verified_outlined, text: message!),
          ],
          const SizedBox(height: 18),
          const Text('Pro capabilities', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800)),
          const SizedBox(height: 10),
          const Wrap(spacing: 8, runSpacing: 8, children: [
            _FeatureChip(Icons.groups_2_outlined, '48 specialists'),
            _FeatureChip(Icons.fact_check_outlined, 'Consensus'),
            _FeatureChip(Icons.bolt_outlined, 'Power analysis'),
            _FeatureChip(Icons.code_outlined, 'Firmware review'),
            _FeatureChip(Icons.view_in_ar_outlined, 'CAD specs'),
            _FeatureChip(Icons.science_outlined, 'Simulation plan'),
            _FeatureChip(Icons.download_outlined, 'Project export'),
            _FeatureChip(Icons.speed_outlined, 'Priority generation'),
          ]),
        ],
      ),
    );
  }
}

class SettingsPage extends StatelessWidget {
  final UserSession session;
  final VoidCallback onSignedOut;
  const SettingsPage({super.key, required this.session, required this.onSignedOut});

  @override
  Widget build(BuildContext context) {
    return _PageFrame(
      title: 'Settings',
      subtitle: 'Account and app configuration',
      child: ListView(
        padding: const EdgeInsets.fromLTRB(20, 8, 20, 28),
        children: [
          Card(child: ListTile(
            contentPadding: const EdgeInsets.all(18),
            leading: CircleAvatar(child: Icon(session.mode == 'google' ? Icons.account_circle : Icons.person_outline)),
            title: Text(session.displayName),
            subtitle: Text(session.email ?? 'Guest session'),
            trailing: session.isPro ? const Chip(label: Text('PRO')) : const Chip(label: Text('FREE')),
          )),
          const SizedBox(height: 12),
          Card(child: Column(children: [
            ListTile(leading: const Icon(Icons.cloud_outlined), title: const Text('Backend'), subtitle: Text(ApiService.baseUrl)),
            const Divider(height: 1),
            const ListTile(leading: Icon(Icons.security_outlined), title: Text('Secrets'), subtitle: Text('AI keys and Google secrets stay on the backend, never inside the APK.')),
            const Divider(height: 1),
            const ListTile(leading: Icon(Icons.info_outline), title: Text('RoboLab-X Android'), subtitle: Text('Version 2.0.0 (20) • Engineering API v3')),
          ])),
          const SizedBox(height: 18),
          OutlinedButton.icon(
            onPressed: () async { await SessionService.signOut(); onSignedOut(); },
            icon: const Icon(Icons.logout),
            label: const Padding(padding: EdgeInsets.symmetric(vertical: 12), child: Text('Sign out')),
          ),
        ],
      ),
    );
  }
}

class _ResultOverview extends StatelessWidget {
  final Map<String, dynamic> data;
  const _ResultOverview({required this.data});

  @override
  Widget build(BuildContext context) {
    final project = (data['project'] as Map?)?.cast<String, dynamic>() ?? const <String, dynamic>{};
    final analysis = (project['analysis'] as Map?)?.cast<String, dynamic>() ?? const <String, dynamic>{};
    final quality = (project['quality_evaluation'] as Map?)?.cast<String, dynamic>() ?? const <String, dynamic>{};
    final consensus = (project['consensus'] as Map?)?.cast<String, dynamic>() ?? const <String, dynamic>{};
    return Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
      const _MessageCard(icon: Icons.check_circle_outline, text: 'Engineering project generated and saved locally.'),
      const SizedBox(height: 12),
      Wrap(spacing: 10, runSpacing: 10, children: [
        _Metric(label: 'Specialists', value: '${analysis['specialist_count'] ?? '—'}'),
        _Metric(label: 'Requirements', value: '${analysis['requirement_count'] ?? '—'}'),
        _Metric(label: 'Quality', value: '${quality['score'] ?? quality['quality_score'] ?? '—'}'),
        _Metric(label: 'Consensus', value: '${consensus['confidence'] ?? '—'}'),
      ]),
      const SizedBox(height: 12),
      Card(child: Padding(padding: const EdgeInsets.all(18), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Text('Matched engineering domains', style: TextStyle(fontWeight: FontWeight.w800)),
        const SizedBox(height: 10),
        Text(((analysis['matched_domains'] as List?) ?? const []).join(' • ').isEmpty ? 'General robotics engineering' : ((analysis['matched_domains'] as List?) ?? const []).join(' • ')),
      ]))),
    ]);
  }
}

class _PageFrame extends StatelessWidget {
  final String title;
  final String subtitle;
  final Widget child;
  final Widget? action;
  const _PageFrame({required this.title, required this.subtitle, required this.child, this.action});

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Column(children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(20, 18, 14, 10),
          child: Row(children: [
            const _BrandMark(size: 42),
            const SizedBox(width: 12),
            Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(title, style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w900)),
              Text(subtitle, maxLines: 1, overflow: TextOverflow.ellipsis, style: Theme.of(context).textTheme.bodySmall?.copyWith(color: Theme.of(context).colorScheme.onSurfaceVariant)),
            ])),
            if (action != null) action!,
          ]),
        ),
        Expanded(child: child),
      ]),
    );
  }
}

class _BrandMark extends StatelessWidget {
  final double size;
  const _BrandMark({required this.size});
  @override
  Widget build(BuildContext context) => Container(
    width: size, height: size,
    decoration: BoxDecoration(
      borderRadius: BorderRadius.circular(size * .28),
      gradient: LinearGradient(begin: Alignment.topLeft, end: Alignment.bottomRight, colors: [Theme.of(context).colorScheme.primary, Theme.of(context).colorScheme.tertiary]),
      boxShadow: [BoxShadow(color: Theme.of(context).colorScheme.primary.withValues(alpha: .22), blurRadius: 24, spreadRadius: 2)],
    ),
    child: Icon(Icons.hub, size: size * .55, color: Colors.white),
  );
}

class _FeatureChip extends StatelessWidget {
  final IconData icon; final String label;
  const _FeatureChip(this.icon, this.label);
  @override
  Widget build(BuildContext context) => Chip(avatar: Icon(icon, size: 18), label: Text(label));
}

class _MessageCard extends StatelessWidget {
  final IconData icon; final String text; final bool error;
  const _MessageCard({required this.icon, required this.text, this.error = false});
  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.all(16),
    decoration: BoxDecoration(
      color: error ? Theme.of(context).colorScheme.errorContainer : Theme.of(context).colorScheme.secondaryContainer,
      borderRadius: BorderRadius.circular(18),
    ),
    child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [Icon(icon), const SizedBox(width: 12), Expanded(child: Text(text))]),
  );
}

class _Metric extends StatelessWidget {
  final String label; final String value;
  const _Metric({required this.label, required this.value});
  @override
  Widget build(BuildContext context) => Container(
    width: 150,
    padding: const EdgeInsets.all(16),
    decoration: BoxDecoration(color: Theme.of(context).colorScheme.surfaceContainer, borderRadius: BorderRadius.circular(18)),
    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [Text(value, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w900)), const SizedBox(height: 3), Text(label)]),
  );
}

class _PlanCard extends StatelessWidget {
  final String title; final String price; final String period; final String detail; final bool recommended;
  const _PlanCard({required this.title, required this.price, required this.period, required this.detail, this.recommended = false});
  @override
  Widget build(BuildContext context) => Card(
    child: Padding(
      padding: const EdgeInsets.all(18),
      child: Row(children: [
        Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Row(children: [Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800)), if (recommended) ...[const SizedBox(width: 8), const Chip(label: Text('BEST VALUE'))]]),
          const SizedBox(height: 6),
          Text(detail),
        ])),
        const SizedBox(width: 12),
        Column(crossAxisAlignment: CrossAxisAlignment.end, children: [Text(price, style: const TextStyle(fontSize: 24, fontWeight: FontWeight.w900)), Text(period)]),
      ]),
    ),
  );
}

class _EmptyState extends StatelessWidget {
  final IconData icon; final String title; final String text;
  const _EmptyState({required this.icon, required this.title, required this.text});
  @override
  Widget build(BuildContext context) => Center(child: Padding(padding: const EdgeInsets.all(32), child: Column(mainAxisSize: MainAxisSize.min, children: [Icon(icon, size: 60), const SizedBox(height: 16), Text(title, style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold)), const SizedBox(height: 8), Text(text, textAlign: TextAlign.center)])));
}
