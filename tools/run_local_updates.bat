@echo off
REM 用于在本地一次性执行常用维护脚本,统一入口便于日常更新。
REM Windows 批处理版本
REM 项目已迁移到 MkDocs Material,不再需要 Docsify 搜索索引

chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

REM 切换到仓库根目录
cd /d "%~dp0\.."

REM 默认执行全部步骤,可通过参数跳过特定命令
set SKIP_CHANGELOG=0
set SKIP_PDF=0
set SKIP_FIX_MD=0
set SKIP_MARKDOWNLINT=0

REM 解析命令行参数
:parse_args
if "%~1"=="" goto end_parse
if /i "%~1"=="--skip-changelog" set SKIP_CHANGELOG=1
if /i "%~1"=="--skip-pdf" set SKIP_PDF=1
if /i "%~1"=="--skip-fix-md" set SKIP_FIX_MD=1
if /i "%~1"=="--skip-markdownlint" set SKIP_MARKDOWNLINT=1
if /i "%~1"=="--help" goto show_help
if /i "%~1"=="-h" goto show_help
if /i "%~1"=="/?" goto show_help
shift
goto parse_args

:show_help
echo.
echo 用法: tools\run_local_updates.bat [选项]
echo.
echo 默认执行以下步骤:
echo   1. python tools/gen_changelog_by_tags.py --latest-to-head
echo   2. python tools/pdf_export/export_to_pdf.py --pdf-engine=tectonic --cjk-font="Microsoft YaHei"
echo   3. python tools/fix_md.py
echo   4. markdownlint "**/*.md" --ignore "node_modules" --ignore "tools/pdf_export/vendor"
echo.
echo 可选参数:
echo   --skip-changelog       跳过变更日志生成
echo   --skip-pdf             跳过 PDF 导出
echo   --skip-fix-md          跳过 Markdown 自动修复
echo   --skip-markdownlint    跳过 markdownlint 校验
echo   -h, --help, /?         显示本帮助信息
echo.
echo 注意:
echo   - MkDocs Material 使用内置搜索,不再需要单独生成搜索索引
echo   - 标签索引由 MkDocs Material tags 插件自动生成,无需手动维护
echo   - 页面修改时间由 git-revision-date-localized 插件自动获取,无需手动维护
echo.
goto end

:end_parse

echo.
echo ======================================
echo 开始执行维护任务
echo ======================================
echo.

REM 1. 生成变更日志
if %SKIP_CHANGELOG%==0 (
    echo [1/4] 生成变更日志...
    python tools/gen_changelog_by_tags.py --latest-to-head
    if errorlevel 1 echo 警告: 变更日志生成失败
    echo.
) else (
    echo [1/4] 已跳过: 变更日志生成
    echo.
)

REM 2. 导出 PDF
if %SKIP_PDF%==0 (
    echo [2/4] 导出 PDF...
    python tools/pdf_export/export_to_pdf.py --pdf-engine=tectonic --cjk-font="Microsoft YaHei"
    if errorlevel 1 echo 警告: PDF 导出失败
    echo.
) else (
    echo [2/4] 已跳过: PDF 导出
    echo.
)

REM 注意: 以下工具已废弃 (移至 tools/deprecated/),不再需要手动运行:
REM - retag_and_related.py: 标签由 Frontmatter 直接管理
REM - generate_tags_index.py: MkDocs Material tags 插件自动生成
REM - build_search_index.py: MkDocs Material 内置搜索
REM - gen-last-updated.mjs: MkDocs Material git-revision-date-localized 插件自动获取

REM 3. 自动修复 Markdown
if %SKIP_FIX_MD%==0 (
    echo [3/4] 自动修复 Markdown 格式...
    python tools/fix_md.py
    if errorlevel 1 echo 警告: Markdown 修复失败
    echo.
) else (
    echo [3/4] 已跳过: Markdown 自动修复
    echo.
)

REM 4. 运行 markdownlint
if %SKIP_MARKDOWNLINT%==0 (
    echo [4/4] 运行 markdownlint 校验...
    markdownlint "**/*.md" --ignore "node_modules" --ignore "tools/pdf_export/vendor"
    if errorlevel 1 echo 警告: markdownlint 校验发现问题
    echo.
) else (
    echo [4/4] 已跳过: markdownlint 校验
    echo.
)

echo.
echo ======================================
echo 全部任务执行完毕
echo ======================================
echo.
echo 提示: 使用 'mkdocs serve' 进行本地预览
echo       使用 'mkdocs build --strict' 进行构建测试
echo.

:end
endlocal
