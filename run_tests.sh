#!/bin/bash
#
# 標準化測試執行腳本
# 用於確保測試結果一致性
#
# 使用方法:
#   chmod +x run_tests.sh
#   ./run_tests.sh
#   ./run_tests.sh --verbose  # 詳細輸出
#   ./run_tests.sh --html     # 生成 HTML 報告

set -e  # 遇到錯誤立即退出

# 顏色定義
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 項目根目錄
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}DLsite Classification Manager${NC}"
echo -e "${BLUE}測試套件執行腳本${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 檢查虛擬環境
if [ ! -d ".venv" ]; then
    echo -e "${RED}❌ 虛擬環境不存在${NC}"
    echo -e "${YELLOW}請先執行: uv venv && uv pip install -r requirements.txt${NC}"
    exit 1
fi

# 解析參數
VERBOSE=false
HTML_REPORT=false
QUICK=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--html)
            HTML_REPORT=true
            shift
            ;;
        -q|--quick)
            QUICK=true
            shift
            ;;
        *)
            echo -e "${RED}未知參數: $1${NC}"
            exit 1
            ;;
    esac
done

echo -e "${GREEN}📋 測試配置${NC}"
echo "  - 測試目錄: tests/"
echo "  - 覆蓋模組: tools.url, tools.check, tools.save_read,"
echo "             common.security, common.regex"
echo "  - 詳細模式: $VERBOSE"
echo "  - HTML報告: $HTML_REPORT"
echo ""

# 構建基本測試命令
TEST_CMD="uv run pytest tests/"

# 添加覆蓋率參數 - 涵蓋所有已測試模組
COV_OPTS="--cov=dlsite_classification.tools.url"
COV_OPTS="$COV_OPTS --cov=dlsite_classification.tools.check"
COV_OPTS="$COV_OPTS --cov=dlsite_classification.tools.save_read"
COV_OPTS="$COV_OPTS --cov=dlsite_classification.tools.copy"
COV_OPTS="$COV_OPTS --cov=dlsite_classification.tools.move"
COV_OPTS="$COV_OPTS --cov=dlsite_classification.tools.saerch"
COV_OPTS="$COV_OPTS --cov=dlsite_classification.tools.scan"
COV_OPTS="$COV_OPTS --cov=dlsite_classification.tools.rep"
COV_OPTS="$COV_OPTS --cov=dlsite_classification.crawler.work"
COV_OPTS="$COV_OPTS --cov=dlsite_classification.crawler.common"
COV_OPTS="$COV_OPTS --cov=dlsite_classification.extract.extract"
COV_OPTS="$COV_OPTS --cov=dlsite_classification.extract.structure"
COV_OPTS="$COV_OPTS --cov=dlsite_classification.common.security"
COV_OPTS="$COV_OPTS --cov=dlsite_classification.common.regex"
COV_OPTS="$COV_OPTS --cov-branch"

# 只顯示測試的模組（不顯示整個項目）
COV_OPTS="$COV_OPTS --cov-report=term-missing:skip-covered"

# 根據參數調整
if [ "$VERBOSE" = true ]; then
    TEST_CMD="$TEST_CMD -vv"
else
    TEST_CMD="$TEST_CMD -v"
fi

if [ "$HTML_REPORT" = true ]; then
    COV_OPTS="$COV_OPTS --cov-report=html"
    echo -e "${YELLOW}📊 將生成 HTML 報告到 htmlcov/ 目錄${NC}"
    echo ""
fi

if [ "$QUICK" = true ]; then
    # 快速模式：只運行測試，不生成覆蓋率報告
    echo -e "${YELLOW}⚡ 快速模式：跳過覆蓋率分析${NC}"
    echo ""
    FINAL_CMD="$TEST_CMD"
else
    FINAL_CMD="$TEST_CMD $COV_OPTS"
fi

# 顯示執行命令
echo -e "${BLUE}🚀 執行命令:${NC}"
echo "  $FINAL_CMD"
echo ""

# 執行測試
echo -e "${GREEN}▶️  開始測試...${NC}"
echo ""

# 執行並捕獲結果
if eval "$FINAL_CMD"; then
    EXIT_CODE=0
else
    EXIT_CODE=$?
fi

echo ""
echo -e "${BLUE}========================================${NC}"

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ 所有測試通過！${NC}"

    if [ "$HTML_REPORT" = true ]; then
        echo ""
        echo -e "${YELLOW}📊 HTML 報告已生成${NC}"
        echo -e "   打開: ${BLUE}file://$PROJECT_ROOT/htmlcov/index.html${NC}"
    fi
else
    echo -e "${RED}❌ 測試失敗${NC}"
    echo -e "${YELLOW}   退出碼: $EXIT_CODE${NC}"
fi

echo -e "${BLUE}========================================${NC}"

exit $EXIT_CODE
