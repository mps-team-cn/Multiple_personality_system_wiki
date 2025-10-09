// GitHub OAuth 代理 for Sveltia CMS (Multiple Personality System Wiki)
// 兼容 Cloudflare Pages Functions 环境

function json(data: any, status = 200, extra: Record<string, string> = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json", ...extra },
  });
}

function rand() {
  return Math.random().toString(36).slice(2) + Date.now().toString(36);
}

export async function onRequestGet(context: any) {
  const { request, env } = context;
  const url = new URL(request.url);
  const code = url.searchParams.get("code");
  const state = url.searchParams.get("state");

  const clientId = env.GITHUB_CLIENT_ID;
  const clientSecret = env.GITHUB_CLIENT_SECRET;
  const redirectUri = `${url.origin}/api/auth`;

  if (!clientId || !clientSecret)
    return json(
      { error: "Missing env", message: "请在 Cloudflare Pages 设置 GITHUB_CLIENT_ID / SECRET" },
      500
    );

  // 读取 state cookie
  const cookie = request.headers.get("Cookie") || "";
  const cookies = Object.fromEntries(
    cookie.split(";").filter(Boolean).map((c) => {
      const [k, ...v] = c.trim().split("=");
      return [k, v.join("=")];
    })
  );
  const storedState = cookies["oauth_state"];

  // Step 1：初次访问 -> 跳 GitHub 登录
  if (!code) {
    const newState = rand();
    const authorizeUrl = new URL("https://github.com/login/oauth/authorize");
    authorizeUrl.searchParams.set("client_id", clientId);
    authorizeUrl.searchParams.set("scope", "repo,user");
    authorizeUrl.searchParams.set("redirect_uri", redirectUri);
    authorizeUrl.searchParams.set("state", newState);

    return new Response(null, {
      status: 302,
      headers: {
        Location: authorizeUrl.toString(),
        "Set-Cookie": `oauth_state=${newState}; Path=/; Max-Age=300; HttpOnly; Secure; SameSite=Lax`,
      },
    });
  }

  // Step 2：校验 state
  if (!state || !storedState || state !== storedState)
    return json(
      { error: "Invalid state", hint: "域名不一致或重复请求，请重新登录" },
      400,
      { "Set-Cookie": "oauth_state=; Path=/; Max-Age=0" }
    );

  const clearState = "oauth_state=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Lax";

  // Step 3：用 code 换 token
  let tokenData: any;
  try {
    const r = await fetch("https://github.com/login/oauth/access_token", {
      method: "POST",
      headers: { Accept: "application/json" },
      body: JSON.stringify({
        client_id: clientId,
        client_secret: clientSecret,
        code,
        redirect_uri: redirectUri,
      }),
    });
    tokenData = await r.json();
  } catch (e) {
    tokenData = {};
  }

  // 失败则回退表单模式
  if (!tokenData?.access_token) {
    const form = new URLSearchParams({
      client_id: clientId,
      client_secret: clientSecret,
      code: code!,
      redirect_uri: redirectUri,
    });
    const r2 = await fetch("https://github.com/login/oauth/access_token", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: form.toString(),
    });
    tokenData = await r2.json();
  }

  const accessToken = tokenData?.access_token;
  if (!accessToken)
    return json(
      { error: "Failed to get access token", details: tokenData },
      400,
      { "Set-Cookie": clearState }
    );

  // Step 4：获取用户信息并检查白名单
  const userRes = await fetch("https://api.github.com/user", {
    headers: {
      Authorization: `token ${accessToken}`,
      "User-Agent": "Plurality-Wiki-SveltiaCMS",
    },
  });
  const user = await userRes.json();

  const ALLOWED_USERS = ["kuliantnt"]; // 允许登录后台的 GitHub 用户
  if (!ALLOWED_USERS.includes(user.login))
    return json(
      { error: "Unauthorized user", login: user.login },
      403,
      { "Set-Cookie": clearState }
    );

  // Step 5：返回 token（Sveltia CMS 使用 popup 模式，需要 postMessage）
  const html = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>认证成功</title>
</head>
<body>
  <script>
    (function() {
      function recieveMessage(e) {
        console.log("recieveMessage %o", e)
        // send message to main window with the app
        window.opener.postMessage(
          'authorization:github:success:${JSON.stringify({ token: accessToken, provider: "github" })}',
          e.origin
        )
      }
      window.addEventListener("message", recieveMessage, false)
      // Start handshake with parent
      console.log("Sending message: %o", "github")
      window.opener.postMessage("authorizing:github", "*")
    })()
  </script>
  <p style="text-align: center; font-family: sans-serif; margin-top: 50px;">
    认证成功！正在跳转...
  </p>
</body>
</html>`;
  return new Response(html, {
    status: 200,
    headers: {
      "Content-Type": "text/html; charset=utf-8",
      "Set-Cookie": clearState,
    },
  });
}
