import 'package:flutter_test/flutter_test.dart';
import 'package:robolab_x/main.dart';

void main() {
  testWidgets('RoboLab X launches', (tester) async {
    await tester.pumpWidget(const RoboLabApp());
    expect(find.text('RoboLab X'), findsOneWidget);
    expect(find.text('Engineering, from idea to build.'), findsOneWidget);
  });
}
