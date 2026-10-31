<!--
封面模板：复制成 tools/pdf_export/cover.md 后即生效，会完整替换内置封面。
- 内容原样插到 PDF 最前面，Markdown 和 LaTeX 都能写（raw_tex 已开）。
- 生效后 --cover-title / --cover-subtitle / --cover-date / --cover-footer / --cover-image 全部忽略。
- 不需要自己写 \newpage：后面会自动换页接目录。
- 图片用绝对路径或仓库相对路径，例如 \includegraphics{docs/assets/images/og-banner.png}
-->

\begin{titlepage}
\centering

\vspace*{2.5cm}

{\Huge 多意识体系统知识库\par}

\vspace{1.5cm}
{\Large Multiple Personality System Wiki\par}

\vspace{1.2cm}
{{VOLUME_CHAPTERS}}



\vfill
{\large \today\par}


\vspace{1cm}
\end{titlepage}
