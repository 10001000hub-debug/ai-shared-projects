# AI駆動型株式投資支援システム

## 目的・背景

AI複数エージェント連携により、高配当株スクリーニング、デイトレード支援、アフィリエイトコンテンツ評価を統合したエンタープライズ投資プラットフォーム。

- **自動化**: n8nワークフローによる24時間監視・判定・通知
- **AI連携**: Claude、ChatGPT、Geminiによる多角的分析
- **リアルタイム**: WebhookとAPIによる即座の市場対応
- **品質管理**: 120点評価システムによる投資判断精度向上

---

## サブシステム概要

### 🔍 高配当株スクリーニングシステム
- **HighDividendScreener**: 配当利回り・PER・財務指標による初期フィルタリング
- **AdvancedScreener**: セクター分析・業績トレンド・リスク評価による詳細分析
- **DataCollector**: Yahoo Finance、Alpha Vantage、企業決算データ取得
- **RiskAnalyzer**: ボラティリティ、ベータ値、相関分析
- **ReportGenerator**: HTML/JSON/PDF形式での詳細レポート出力

### 📊 デイトレード支援システム
- **DayTradingBot**: テクニカル指標（RSI、MACD、ボリンジャーバンド）監視
- **SignalGenerator**: エントリー・エグジットシグナル生成
- **RiskManager**: 損切り・利確・ポジションサイジング自動制御
- **MarketDataStreamer**: リアルタイム価格・出来高データ受信
- **TradeExecutor**: ブローカーAPI経由での自動発注（デモ対応）

### 🤖 AIオーケストレーション基盤
- **Orchestrator CLI**: JSONスキーマ準拠の品質評価パイプライン
- **Multi-AI Coordinator**: Claude→ChatGPT→Gemini連携フロー
- **Content Evaluator**: 8軸120点品質スコアリング
- **Auto Publisher**: 114点以上で自動公開判定
- **Error Handler**: API制限・障害時のフェイルオーバー

---

## 関連リンク

- [アーキテクチャ図](generated/architecture_diagram.md) - システム構成とデータフロー
- [n8nワークフロー](generated/n8n_workflow_template.json) - 自動化テンプレート
- [環境変数サンプル](generated/env_example.txt) - 設定ファイル例

---

**作成日**: 2025-08-08  
**バージョン**: 1.0.0
