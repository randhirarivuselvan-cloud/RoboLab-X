import 'package:google_sign_in/google_sign_in.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'api_service.dart';

class UserSession {
  final String mode;
  final String token;
  final String displayName;
  final String? email;
  final bool isPro;

  const UserSession({
    required this.mode,
    required this.token,
    required this.displayName,
    this.email,
    this.isPro = false,
  });
}

class SessionService {
  static const _tokenKey = 'session_token';
  static const _modeKey = 'session_mode';
  static const _nameKey = 'session_name';
  static const _emailKey = 'session_email';
  static const _proKey = 'session_pro';

  static Future<UserSession?> restore() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString(_tokenKey);
    if (token == null || token.isEmpty) return null;
    return UserSession(
      mode: prefs.getString(_modeKey) ?? 'guest',
      token: token,
      displayName: prefs.getString(_nameKey) ?? 'Guest Engineer',
      email: prefs.getString(_emailKey),
      isPro: prefs.getBool(_proKey) ?? false,
    );
  }

  static Future<UserSession> continueAsGuest() async {
    final data = await ApiService.postJson('/api/v1/auth/guest', {});
    final session = UserSession(
      mode: 'guest',
      token: data['token'].toString(),
      displayName: data['user']?['name']?.toString() ?? 'Guest Engineer',
      isPro: data['user']?['pro'] == true,
    );
    await _persist(session);
    return session;
  }

  static Future<UserSession> signInWithGoogle() async {
    final signIn = GoogleSignIn.instance;
    await signIn.initialize(
      serverClientId: const String.fromEnvironment('GOOGLE_SERVER_CLIENT_ID'),
    );
    final account = await signIn.authenticate();
    final authorization = await account.authorizationClient.authorizationForScopes(const ['email', 'profile']);
    final authentication = account.authentication;
    final idToken = authentication.idToken;
    if (idToken == null || idToken.isEmpty) {
      throw StateError('Google did not return an ID token. Check GOOGLE_SERVER_CLIENT_ID.');
    }
    final data = await ApiService.postJson('/api/v1/auth/google', {'id_token': idToken});
    final session = UserSession(
      mode: 'google',
      token: data['token'].toString(),
      displayName: data['user']?['name']?.toString() ?? account.displayName ?? 'Engineer',
      email: data['user']?['email']?.toString() ?? account.email,
      isPro: data['user']?['pro'] == true,
    );
    // Keep authorization referenced so Android can request scopes if needed later.
    authorization;
    await _persist(session);
    return session;
  }

  static Future<void> setPro(bool value) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_proKey, value);
  }

  static Future<void> signOut() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_tokenKey);
    await prefs.remove(_modeKey);
    await prefs.remove(_nameKey);
    await prefs.remove(_emailKey);
    await prefs.remove(_proKey);
    try {
      await GoogleSignIn.instance.signOut();
    } catch (_) {}
  }

  static Future<void> _persist(UserSession session) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_tokenKey, session.token);
    await prefs.setString(_modeKey, session.mode);
    await prefs.setString(_nameKey, session.displayName);
    if (session.email != null) await prefs.setString(_emailKey, session.email!);
    await prefs.setBool(_proKey, session.isPro);
  }
}
