#!/usr/bin/env python3
"""
プロジェクト全体共有パッケージ生成スクリプト
AI株式投資支援システムの技術ドキュメント一括生成

使用方法:
    python3 generate_docs.py
    
生成物:
    - generated/README_STOCK_PROJECT.md
    - generated/architecture_diagram.md  
    - generated/n8n_workflow_template.json
    - generated/env_example.txt
"""

import os
import json
from datetime import datetime
from pathlib import Path

def create_directory_structure():
    """必要なディレクトリ構造を作成"""
    directories = [
        'generated',
        'output',
        'output/reports', 
        'tmp',
        'backup',
        'logs',
        'tests/test_data'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ ディレクトリ作成: {directory}/")

def create_readme():
    """README_STOCK_PROJECT.md を生成"""
    readme_content = """# AI駆動型株式投資支援システム

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

**作成日**: {date}  
**バージョン**: 1.0.0
""".format(date=datetime.now().strftime("%Y-%m-%d"))
    
    with open('generated/README_STOCK_PROJECT.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("✅ generated/README_STOCK_PROJECT.md")

def create_architecture_diagram():
    """architecture_diagram.md を生成"""
    diagram_content = """# システムアーキテクチャ図

## 全体システム構成

```mermaid
graph TB
    subgraph "データソース"
        YF[Yahoo Finance API]
        AV[Alpha Vantage API] 
        BD[ブローカーAPI]
        WH[Webhook受信]
    end

    subgraph "分析エンジン"
        HDS[HighDividendScreener]
        AS[AdvancedScreener]
        DTB[DayTradingBot]
        RA[RiskAnalyzer]
    end

    subgraph "AIエージェント連携"
        CLAUDE[Claude API]
        GPT[ChatGPT API]
        GEMINI[Gemini API]
    end

    subgraph "自動化・通知"
        N8N[n8n Workflow]
        SLACK[Slack通知]
        LINE[LINE Bot]
    end

    %% データフロー
    YF --> HDS
    AV --> AS
    BD --> DTB
    WH --> N8N
    
    HDS --> CLAUDE
    AS --> CLAUDE
    DTB --> N8N
    
    CLAUDE --> GPT
    GPT --> GEMINI
    GEMINI --> N8N
    
    N8N --> SLACK
    N8N --> LINE

    classDef aiNode fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    classDef dataNode fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef systemNode fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px

    class CLAUDE,GPT,GEMINI aiNode
    class YF,AV,BD,WH dataNode
    class N8N systemNode
```

**作成日**: {date}  
**図式形式**: Mermaid
""".format(date=datetime.now().strftime("%Y-%m-%d"))
    
    with open('generated/architecture_diagram.md', 'w', encoding='utf-8') as f:
        f.write(diagram_content)
    print("✅ generated/architecture_diagram.md")

def create_n8n_workflow():
    """n8n_workflow_template.json を生成"""
    workflow_template = {
        "name": "Stock AI Analysis Workflow",
        "nodes": [
            {
                "parameters": {
                    "rule": {
                        "interval": [{"field": "cronExpression", "cronExpression": "0 23 * * 1-5"}]
                    }
                },
                "id": "cron-trigger",
                "name": "Daily Market Analysis",
                "type": "n8n-nodes-base.cron",
                "typeVersion": 1,
                "position": [240, 300]
            },
            {
                "parameters": {
                    "command": "python3 ${PROJECT_ROOT}/affiliate_ai_quality/src/orchestrator.py --input ${SCREENER_OUTPUT} --verbose"
                },
                "id": "screener-exec", 
                "name": "Execute Stock Screener",
                "type": "n8n-nodes-base.executeCommand",
                "typeVersion": 1,
                "position": [440, 300]
            },
            {
                "parameters": {
                    "channel": "${SLACK_CHANNEL}",
                    "text": "📊 *株式分析完了* - {{ $json.timestamp }}\n\n*スコア*: {{ $json.total_score }}/120\n*推奨アクション*: {{ $json.recommendation }}"
                },
                "id": "slack-notification",
                "name": "Slack Notification", 
                "type": "n8n-nodes-base.slack",
                "typeVersion": 1,
                "position": [640, 300]
            }
        ],
        "connections": {
            "Daily Market Analysis": {
                "main": [[{"node": "Execute Stock Screener", "type": "main", "index": 0}]]
            },
            "Execute Stock Screener": {
                "main": [[{"node": "Slack Notification", "type": "main", "index": 0}]]
            }
        },
        "settings": {
            "timezone": "Asia/Tokyo",
            "saveExecutionProgress": True
        },
        "meta": {
            "templateCreatedBy": "AI Stock Analysis System",
            "templateId": "stock-ai-workflow-v1.0.0"
        }
    }
    
    with open('generated/n8n_workflow_template.json', 'w', encoding='utf-8') as f:
        json.dump(workflow_template, f, indent=2, ensure_ascii=False)
    print("✅ generated/n8n_workflow_template.json")

def create_env_example():
    """env_example.txt を生成"""
    env_content = """# AI株式投資支援システム - 環境変数設定ファイル
# 使用方法: cp env_example.txt .env → 各値を実際のものに変更

# プロジェクト基本設定
PROJECT_ROOT=/home/tkr/ai-shared-projects
PROJECT_NAME=ai_stock_analysis
VERSION=1.0.0

# データ出力設定
SCREENER_OUTPUT=output/high_dividend.json
ANALYSIS_RESULT=output/analysis_result.json
REPORT_OUTPUT=output/reports/

# AI API認証情報
CLAUDE_API_KEY=your_claude_api_key_here
OPENAI_API_KEY=your_openai_api_key_here  
GEMINI_API_KEY=your_gemini_api_key_here

# n8n設定
N8N_BASE_URL=http://localhost:5679
WEBHOOK_URL=https://your-n8n-server.com/webhook/trading-signal

# 通知設定
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_CHANNEL=#stock-analysis
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token

# ブローカーAPI設定
BROKER_API_KEY=your_broker_api_key
BROKER_API_ENDPOINT=https://api.yourbroker.com/v1/orders
TRADING_MODE=demo

# スクリーニング設定
MIN_DIVIDEND_YIELD=3.0
MAX_PER_RATIO=20.0
MIN_MARKET_CAP=10000000000

# リスク管理
MAX_DAILY_TRADES=10
MAX_TOTAL_EXPOSURE=1000000
RISK_TOLERANCE=medium
"""
    
    with open('generated/env_example.txt', 'w', encoding='utf-8') as f:
        f.write(env_content)
    print("✅ generated/env_example.txt")

def verify_files():
    """生成されたファイルの存在確認"""
    required_files = [
        'generated/README_STOCK_PROJECT.md',
        'generated/architecture_diagram.md',
        'generated/n8n_workflow_template.json', 
        'generated/env_example.txt'
    ]
    
    print("\n📋 ファイル生成確認:")
    all_exists = True
    
    for file_path in required_files:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            print(f"✅ {file_path} ({size:,} bytes)")
        else:
            print(f"❌ {file_path} - ファイルが見つかりません")
            all_exists = False
    
    return all_exists

def print_git_instructions():
    """Git操作手順を表示"""
    instructions = """
🚀 Git操作手順:

1. 生成されたファイルをステージング:
   git add generated/

2. コミット作成:
   git commit -m "docs: add comprehensive project documentation
   
   - README_STOCK_PROJECT.md: システム概要と導入手順
   - architecture_diagram.md: Mermaidアーキテクチャ図
   - n8n_workflow_template.json: 自動化ワークフロー
   - env_example.txt: 環境変数テンプレート"

3. リモートにプッシュ:
   git push origin main

4. チーム共有:
   - README_STOCK_PROJECT.md を読んでシステム全体を理解
   - n8n_workflow_template.json をn8nにインポートして動作確認
   - env_example.txt を基に .env ファイルを各環境で作成
"""
    print(instructions)

def main():
    """メイン処理"""
    print("🔧 AI株式投資支援システム - ドキュメント生成開始")
    print("=" * 60)
    
    try:
        # 1. ディレクトリ構造作成
        create_directory_structure()
        print()
        
        # 2. 各ドキュメント生成
        print("📝 ドキュメント生成:")
        create_readme()
        create_architecture_diagram()
        create_n8n_workflow()
        create_env_example()
        print()
        
        # 3. 生成確認
        success = verify_files()
        print()
        
        if success:
            print("✅ 全ドキュメント生成完了!")
            print_git_instructions()
        else:
            print("❌ 一部ファイルの生成に失敗しました")
            return 1
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return 1
    
    print("=" * 60)
    print("🎉 プロジェクト全体共有パッケージ生成完了!")
    return 0

if __name__ == "__main__":
    exit(main())