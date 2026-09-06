import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:robolab_x/main.dart';

void main() {
  testWidgets('RoboLab-X launches to authentication', (tester) async {
    SharedPreferences.setMockInitialValues({});
    await tester.pumpWidget(const RoboLabXApp());
    await tester.pumpAndSettle();

    expect(find.text('RoboLab-X'), findsOneWidget);
    expect(find.text('Continue with Google'), findsOneWidget);
    expect(find.text('Continue as Guest'), findsOneWidget);
  });
}
