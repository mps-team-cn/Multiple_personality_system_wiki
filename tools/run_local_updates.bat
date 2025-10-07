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
set SKIP_RETAG=0
set SKIP_LAST_UPDATED=0
set SKIP_PDF=0
set SKIP_FIX_MD=0
set SKIP_MARKDOWNLINT=0

REM 解析命令行参数
:parse_args
if "%~1"=="" goto end_parse
if /i "%~1"=="--skip-changelog" set SKIP_CHANGELOG=1
if /i "%~1"=="--skip-retag" set SKIP_RETAG=1
if /i "%~1"=="--skip-last-updated" set SKIP_LAST_UPDATED=1
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
echo   2. python tools/retag_and_related.py
echo   3. node scripts/gen-last-updated.mjs
echo   4. python tools/pdf_export/export_to_pdf.py --pdf-engine=tectonic --cjk-font="Microsoft YaHei"
echo   5. python tools/fix_md.py
echo   6. markdownlint "**/*.md" --ignore "node_modules" --ignore "tools/pdf_export/vendor"
echo.
echo 可选参数:
echo   --skip-changelog       跳过变更日志生成
echo   --skip-retag           跳过标签与关联词条重建
echo   --skip-last-updated    跳过最后更新时间索引生成
echo   --skip-pdf             跳过 PDF 导出
echo   --skip-fix-md          跳过 Markdown 自动修复
echo   --skip-markdownlint    跳过 markdownlint 校验
echo   -h, --help, /?         显示本帮助信息
echo.
echo 注意:
echo   - MkDocs Material 使用内置搜索,不再需要单独生成搜索索引
echo   - 标签索引由 MkDocs Material tags 插件自动生成,无需手动维护
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
    echo [1/6] 生成变更日志...
    python tools/gen_changelog_by_tags.py --latest-to-head
    if errorlevel 1 echo 警告: 变更日志生成失败
    echo.
) else (
    echo [1/6] 已跳过: 变更日志生成
    echo.
)

REM 2. 刷新 Frontmatter 标签与相关词条
if %SKIP_RETAG%==0 (
    echo [2/6] 刷新 Frontmatter 标签与相关词条...
    python tools/retag_and_related.py
    if errorlevel 1 echo 警告: 标签重建失败
    echo.
) else (
    echo [2/6] 已跳过: 标签与相关词条重建
    echo.
)

REM 3. 生成最后更新时间索引
if %SKIP_LAST_UPDATED%==0 (
    echo [3/6] 生成最后更新时间索引...
    node scripts/gen-last-updated.mjs
    if errorlevel 1 echo 警告: 最后更新时间索引生成失败
    echo.
) else (
    echo [3/6] 已跳过: 最后更新时间索引
    echo.
)

REM 4. 导出 PDF
if %SKIP_PDF%==0 (
    echo [4/6] 导出 PDF...
    python tools/pdf_export/export_to_pdf.py --pdf-engine=tectonic --cjk-font="Microsoft YaHei"
    if errorlevel 1 echo 警告: PDF 导出失败
    echo.
) else (
    echo [4/6] 已跳过: PDF 导出
    echo.
)

REM 注意: 以下工具已废弃,不再需要手动运行:
REM - generate_tags_index.py: MkDocs Material tags 插件自动生成
REM - build_search_index.py: MkDocs Material 内置搜索

REM 5. 自动修复 Markdown
if %SKIP_FIX_MD%==0 (
    echo [5/6] 自动修复 Markdown 格式...
    python tools/fix_md.py
    if errorlevel 1 echo 警告: Markdown 修复失败
    echo.
) else (
    echo [5/6] 已跳过: Markdown 自动修复
    echo.
)

REM 6. 运行 markdownlint
if %SKIP_MARKDOWNLINT%==0 (
    echo [6/6] 运行 markdownlint 校验...
    markdownlint "**/*.md" --ignore "node_modules" --ignore "tools/pdf_export/vendor"
    if errorlevel 1 echo 警告: markdownlint 校验发现问题
    echo.
) else (
    echo [6/6] 已跳过: markdownlint 校验
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
