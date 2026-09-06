import 'dart:async';
import 'package:in_app_purchase/in_app_purchase.dart';

class BillingService {
  static const monthlyId = 'robolab_pro_monthly';
  static const annualId = 'robolab_pro_annual';

  final InAppPurchase _iap = InAppPurchase.instance;
  StreamSubscription<List<PurchaseDetails>>? _subscription;
  List<ProductDetails> products = const [];

  Future<bool> initialize(void Function(PurchaseDetails) onPurchase) async {
    final available = await _iap.isAvailable();
    if (!available) return false;
    final response = await _iap.queryProductDetails({monthlyId, annualId});
    products = response.productDetails;
    _subscription ??= _iap.purchaseStream.listen((purchases) async {
      for (final purchase in purchases) {
        if (purchase.status == PurchaseStatus.purchased || purchase.status == PurchaseStatus.restored) {
          onPurchase(purchase);
        }
        if (purchase.pendingCompletePurchase) {
          await _iap.completePurchase(purchase);
        }
      }
    });
    return true;
  }

  Future<void> buy(ProductDetails product) async {
    await _iap.buyNonConsumable(purchaseParam: PurchaseParam(productDetails: product));
  }

  Future<void> restore() => _iap.restorePurchases();

  Future<void> dispose() async {
    await _subscription?.cancel();
  }
}
