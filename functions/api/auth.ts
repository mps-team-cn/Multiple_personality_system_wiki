/**
 * Cloudflare Pages Function: GitHub OAuth 代理 for Decap CMS
 * 
 * 流程：
 *  1️⃣ CMS 访问 /api/auth → 重定向到 GitHub 登录页
 *  2️⃣ 登录后 GitHub 回调 /api/auth?code=xxxx
 *  3️⃣ 函数用 code 换取 access_token
 *  4️⃣ 验证用户名是否在白名单内
 *  5️⃣ 返回 JSON { token: <access_token> } 给 CMS
 */

export async function onRequestGet(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const code = url.searchParams.get("code");

  const clientId = env.GITHUB_CLIENT_ID;
  const clientSecret = env.GITHUB_CLIENT_SECRET;

  // ✅ 修改为你允许登录后台的 GitHub 用户名
  const ALLOWED_USERS = ["kuliantnt", "fengqingyu430-collab", "shishuiliunian5"];

  // Step 1: 如果没有 code，说明是初次访问，跳转 GitHub 登录页
  if (!code) {
    const redirectUri = `${url.origin}/api/auth`;
    const authorizeUrl = `https://github.com/login/oauth/authorize?client_id=${clientId}&scope=repo,user&redirect_uri=${redirectUri}`;
    return Response.redirect(authorizeUrl, 302);
  }

  // Step 2: 用 code 向 GitHub 请求 access_token
  const tokenResponse = await fetch("https://github.com/login/oauth/access_token", {
    method: "POST",
    headers: { Accept: "application/json" },
    body: JSON.stringify({
      client_id: clientId,
      client_secret: clientSecret,
      code,
    }),
  });

  const tokenData = await tokenResponse.json();
  const accessToken = tokenData.access_token;

  if (!accessToken) {
    return new Response(JSON.stringify({ error: "Failed to get access token" }), {
      status: 400,
      headers: { "Content-Type": "application/json" },
    });
  }

  // Step 3: 拿 token 获取当前用户信息
  const userResponse = await fetch("https://api.github.com/user", {
    headers: {
      Authorization: `token ${accessToken}`,
      "User-Agent": "Plurality-Wiki-DecapCMS",
    },
  });

  const userData = await userResponse.json();

  // Step 4: 检查是否在白名单中
  if (!ALLOWED_USERS.includes(userData.login)) {
    return new Response(JSON.stringify({ error: "Unauthorized user" }), {
      status: 403,
      headers: { "Content-Type": "application/json" },
    });
  }

  // Step 5: 返回 token 给 Decap CMS
  return new Response(JSON.stringify({ token: accessToken }), {
    headers: { "Content-Type": "application/json" },
  });
}
