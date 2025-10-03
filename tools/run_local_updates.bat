@echo off
REM Windows 环境下一键执行常用维护脚本的批处理入口。
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION

REM 切换到仓库根目录，确保相对路径一致。
pushd "%~dp0.."

set "SKIP_CHANGELOG=0"
set "SKIP_RETAG=0"
set "SKIP_LAST_UPDATED=0"
set "SKIP_PDF=0"
set "SKIP_TAG_INDEX=0"
set "SKIP_FIX_MD=0"
set "SKIP_MARKDOWNLINT=0"

:parse_args
if "%~1"=="" goto after_parse
if "%~1"=="--skip-changelog" (
  set "SKIP_CHANGELOG=1"
  shift
  goto parse_args
)
if "%~1"=="--skip-retag" (
  set "SKIP_RETAG=1"
  shift
  goto parse_args
)
if "%~1"=="--skip-last-updated" (
  set "SKIP_LAST_UPDATED=1"
  shift
  goto parse_args
)
if "%~1"=="--skip-pdf" (
  set "SKIP_PDF=1"
  shift
  goto parse_args
)
if "%~1"=="--skip-tag-index" (
  set "SKIP_TAG_INDEX=1"
  shift
  goto parse_args
)
if "%~1"=="--skip-fix-md" (
  set "SKIP_FIX_MD=1"
  shift
  goto parse_args
)
if "%~1"=="--skip-markdownlint" (
  set "SKIP_MARKDOWNLINT=1"
  shift
  goto parse_args
)
if "%~1"=="--help" goto show_help
if "%~1"=="-h" goto show_help

echo 未识别的参数: %~1 1>&2
popd
exit /b 1

:show_help
echo 用法：tools\run_local_updates.bat [选项]
echo.
echo 默认执行以下步骤：
echo   1. python tools\gen_changelog_by_tags.py --latest-to-head
echo   2. python tools\retag_and_related.py
echo   3. node scripts\gen-last-updated.mjs
echo   4. python tools\pdf_export\export_to_pdf.py --pdf-engine=tectonic --cjk-font="Microsoft YaHei"
echo   5. python tools\generate_tags_index.py
echo   6. python tools\fix_md.py
echo   7. markdownlint "**\*.md" --ignore "node_modules" --ignore "tools\pdf_export\vendor"
echo.
echo 可选参数：
echo   --skip-changelog      跳过变更日志生成
echo   --skip-retag          跳过标签与相关词条重建
echo   --skip-last-updated   跳过最后更新时间索引生成
echo   --skip-pdf            跳过 PDF 导出
echo   --skip-tag-index      跳过标签索引生成
echo   --skip-fix-md         跳过 Markdown 自动修复
echo   --skip-markdownlint   跳过 markdownlint 校验
echo   -h, --help            显示本帮助信息
popd
exit /b 0

:after_parse

call :maybe_run !SKIP_CHANGELOG! "生成变更日志" python tools\gen_changelog_by_tags.py --latest-to-head
if errorlevel 1 goto script_fail
call :maybe_run !SKIP_RETAG! "刷新 Frontmatter 标签与相关词条" python tools\retag_and_related.py
if errorlevel 1 goto script_fail
call :maybe_run !SKIP_LAST_UPDATED! "生成最后更新时间索引" node scripts\gen-last-updated.mjs
if errorlevel 1 goto script_fail
call :maybe_run !SKIP_PDF! "导出 PDF" python tools\pdf_export\export_to_pdf.py --pdf-engine=tectonic --cjk-font="Microsoft YaHei"
if errorlevel 1 goto script_fail
call :maybe_run !SKIP_TAG_INDEX! "生成标签索引" python tools\generate_tags_index.py
if errorlevel 1 goto script_fail
call :maybe_run !SKIP_FIX_MD! "自动修复 Markdown" python tools\fix_md.py
if errorlevel 1 goto script_fail
call :maybe_run !SKIP_MARKDOWNLINT! "运行 markdownlint" markdownlint "**\*.md" --ignore "node_modules" --ignore "tools\pdf_export\vendor"
if errorlevel 1 goto script_fail

echo.
echo 全部任务执行完毕。

popd
exit /b 0

:maybe_run
set "SKIP_FLAG=%~1"
set "STEP_DESC=%~2"
shift
shift
if "%SKIP_FLAG%"=="1" (
  echo 已跳过：%STEP_DESC%
  exit /b 0
)

echo.
echo ^>^>^> %STEP_DESC%
%*
exit /b %errorlevel%

:script_fail
popd
exit /b %errorlevel%
