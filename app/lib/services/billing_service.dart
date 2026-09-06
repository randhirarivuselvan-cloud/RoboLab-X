import 'dart:async';
import 'package:in_app_purchase/in_app_purchase.dart';
import 'api_service.dart';
import 'session_service.dart';

class BillingService {
  static const monthlyId = 'robolab_pro_monthly';
  static const annualId = 'robolab_pro_annual';

  final InAppPurchase _iap = InAppPurchase.instance;
  StreamSubscription<List<PurchaseDetails>>? _subscription;
  List<ProductDetails> products = const [];
  String? lastError;

  Future<bool> initialize(void Function(PurchaseDetails) onVerifiedPurchase) async {
    final available = await _iap.isAvailable();
    if (!available) return false;

    final response = await _iap.queryProductDetails({monthlyId, annualId});
    products = response.productDetails;
    lastError = response.error?.message;

    _subscription ??= _iap.purchaseStream.listen((purchases) async {
      for (final purchase in purchases) {
        if (purchase.status == PurchaseStatus.purchased || purchase.status == PurchaseStatus.restored) {
          final verified = await _verifyWithBackend(purchase);
          if (verified) {
            onVerifiedPurchase(purchase);
            if (purchase.pendingCompletePurchase) {
              await _iap.completePurchase(purchase);
            }
          }
        } else if (purchase.status == PurchaseStatus.error) {
          lastError = purchase.error?.message ?? 'Google Play purchase failed.';
        }
      }
    });
    return true;
  }

  Future<bool> _verifyWithBackend(PurchaseDetails purchase) async {
    try {
      final session = await SessionService.restore();
      if (session == null) {
        lastError = 'Sign in before activating RoboLab Pro.';
        return false;
      }
      final token = purchase.verificationData.serverVerificationData;
      if (token.isEmpty) {
        lastError = 'Google Play did not provide verification data.';
        return false;
      }
      final data = await ApiService.postJson(
        '/api/v1/billing/google/verify',
        {'product_id': purchase.productID, 'purchase_token': token},
        token: session.token,
      );
      await SessionService.applyServerSession(data, session);
      lastError = null;
      return data['verified'] == true;
    } catch (e) {
      lastError = e.toString();
      return false;
    }
  }

  Future<void> buy(ProductDetails product) async {
    await _iap.buyNonConsumable(purchaseParam: PurchaseParam(productDetails: product));
  }

  Future<void> restore() => _iap.restorePurchases();

  Future<void> dispose() async {
    await _subscription?.cancel();
  }
}
