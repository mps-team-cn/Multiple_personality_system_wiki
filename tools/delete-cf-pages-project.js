#!/usr/bin/env node

/**
 * Cloudflare Pages 项目批量删除脚本
 * 用于删除有大量 deployments 的 Pages 项目
 */

const https = require('https');

// 配置项
const CONFIG = {
  API_TOKEN: process.env.CF_API_TOKEN,
  ACCOUNT_ID: process.env.CF_ACCOUNT_ID,
  PROJECT_NAME: process.env.CF_PAGES_PROJECT,
  KEEP_PRODUCTION: process.env.KEEP_PRODUCTION !== 'false', // 默认保留最新 production
  PER_PAGE: 25, // Cloudflare Pages API 最大值为 25
  MAX_PAGES: 200,
  CONCURRENT_DELETES: 5, // 并发删除数量
};

// API 请求封装
function apiRequest(method, path, data = null) {
  return new Promise((resolve, reject) => {
    const fullPath = `/client/v4${path}`;
    const options = {
      hostname: 'api.cloudflare.com',
      port: 443,
      path: fullPath,
      method: method,
      headers: {
        'Authorization': `Bearer ${CONFIG.API_TOKEN}`,
        'Content-Type': 'application/json',
      },
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(body);
          if (parsed.success) {
            resolve(parsed);
          } else {
            reject(new Error(`API Error: ${JSON.stringify(parsed.errors)}`));
          }
        } catch (e) {
          reject(new Error(`Failed to parse response: ${body}`));
        }
      });
    });

    req.on('error', reject);
    if (data) req.write(JSON.stringify(data));
    req.end();
  });
}

// 获取所有 deployments（分页）
async function getAllDeployments() {
  console.log('📋 正在获取所有部署列表...');
  const allDeployments = [];

  for (let page = 1; page <= CONFIG.MAX_PAGES; page++) {
    try {
      const path = `/accounts/${encodeURIComponent(CONFIG.ACCOUNT_ID)}/pages/projects/${encodeURIComponent(CONFIG.PROJECT_NAME)}/deployments?per_page=${CONFIG.PER_PAGE}&page=${page}`;
      const response = await apiRequest('GET', path);

      if (!response.result || response.result.length === 0) {
        break; // 没有更多数据
      }

      allDeployments.push(...response.result);
      console.log(`   第 ${page} 页: ${response.result.length} 个部署`);

      // 如果返回的数量少于每页数量，说明已经是最后一页
      if (response.result.length < CONFIG.PER_PAGE) {
        break;
      }
    } catch (error) {
      console.error(`❌ 获取第 ${page} 页失败:`, error.message);
      break;
    }
  }

  console.log(`✅ 共找到 ${allDeployments.length} 个部署\n`);
  return allDeployments;
}

// 过滤需要删除的 deployments
function filterDeploymentsToDelete(deployments) {
  if (!CONFIG.KEEP_PRODUCTION) {
    return deployments;
  }

  // 找到最新的 production 部署
  const productionDeployments = deployments
    .filter(d => d.environment === 'production')
    .sort((a, b) => new Date(b.created_on) - new Date(a.created_on));

  const latestProduction = productionDeployments[0];

  if (latestProduction) {
    console.log(`🔒 保留最新 production 部署: ${latestProduction.id} (${latestProduction.created_on})`);
    return deployments.filter(d => d.id !== latestProduction.id);
  }

  return deployments;
}

// 批量删除 deployments
async function deleteDeployments(deployments) {
  const total = deployments.length;
  console.log(`\n🗑️  开始删除 ${total} 个部署...\n`);

  let deleted = 0;
  let failed = 0;

  // 分批并发删除
  for (let i = 0; i < deployments.length; i += CONFIG.CONCURRENT_DELETES) {
    const batch = deployments.slice(i, i + CONFIG.CONCURRENT_DELETES);
    const promises = batch.map(async (deployment) => {
      try {
        const path = `/accounts/${encodeURIComponent(CONFIG.ACCOUNT_ID)}/pages/projects/${encodeURIComponent(CONFIG.PROJECT_NAME)}/deployments/${encodeURIComponent(deployment.id)}?force=true`;
        await apiRequest('DELETE', path);
        deleted++;
        return { success: true, id: deployment.id };
      } catch (error) {
        failed++;
        return { success: false, id: deployment.id, error: error.message };
      }
    });

    const results = await Promise.all(promises);

    // 显示进度
    const progress = ((deleted + failed) / total * 100).toFixed(1);
    process.stdout.write(`\r   进度: ${deleted + failed}/${total} (${progress}%) | 成功: ${deleted} | 失败: ${failed}`);

    // 显示失败详情
    const failures = results.filter(r => !r.success);
    if (failures.length > 0) {
      console.log();
      failures.forEach(f => {
        console.log(`   ⚠️  删除失败: ${f.id} - ${f.error}`);
      });
    }
  }

  console.log('\n');
  return { deleted, failed };
}

// 删除项目
async function deleteProject() {
  console.log(`\n🗑️  正在删除项目 "${CONFIG.PROJECT_NAME}"...`);
  try {
    const path = `/accounts/${encodeURIComponent(CONFIG.ACCOUNT_ID)}/pages/projects/${encodeURIComponent(CONFIG.PROJECT_NAME)}`;
    await apiRequest('DELETE', path);
    console.log(`✅ 项目删除成功！\n`);
    return true;
  } catch (error) {
    console.error(`❌ 项目删除失败: ${error.message}\n`);
    return false;
  }
}

// 验证环境变量
function validateConfig() {
  const missing = [];
  if (!CONFIG.API_TOKEN) missing.push('CF_API_TOKEN');
  if (!CONFIG.ACCOUNT_ID) missing.push('CF_ACCOUNT_ID');
  if (!CONFIG.PROJECT_NAME) missing.push('CF_PAGES_PROJECT');

  if (missing.length > 0) {
    console.error('❌ 缺少必需的环境变量:', missing.join(', '));
    console.error('\n使用方法:');
    console.error('  export CF_API_TOKEN="your-api-token"');
    console.error('  export CF_ACCOUNT_ID="your-account-id"');
    console.error('  export CF_PAGES_PROJECT="your-project-name"');
    console.error('  export KEEP_PRODUCTION="true"  # 可选，默认 true\n');
    process.exit(1);
  }
}

// 主函数
async function main() {
  console.log('🚀 Cloudflare Pages 项目删除工具\n');
  console.log('='.repeat(50));

  validateConfig();

  console.log(`📌 配置信息:`);
  console.log(`   账户 ID: ${CONFIG.ACCOUNT_ID}`);
  console.log(`   项目名称: ${CONFIG.PROJECT_NAME}`);
  console.log(`   保留最新 production: ${CONFIG.KEEP_PRODUCTION ? '是' : '否'}`);
  console.log('='.repeat(50) + '\n');

  try {
    // 1. 获取所有部署
    const allDeployments = await getAllDeployments();

    if (allDeployments.length === 0) {
      console.log('⚠️  未找到任何部署，直接删除项目...\n');
    } else {
      // 2. 过滤需要删除的部署
      const deploymentsToDelete = filterDeploymentsToDelete(allDeployments);

      if (deploymentsToDelete.length === 0) {
        console.log('⚠️  没有需要删除的部署\n');
      } else {
        // 3. 批量删除部署
        const { deleted, failed } = await deleteDeployments(deploymentsToDelete);

        console.log(`📊 删除统计:`);
        console.log(`   成功: ${deleted}`);
        console.log(`   失败: ${failed}`);
        console.log(`   总计: ${deploymentsToDelete.length}\n`);

        if (failed > 0) {
          console.log('⚠️  部分部署删除失败，但将继续尝试删除项目...\n');
        }
      }
    }

    // 4. 删除项目
    const projectDeleted = await deleteProject();

    if (projectDeleted) {
      console.log('🎉 所有操作完成！项目已彻底删除。');
    } else {
      console.log('⚠️  项目删除失败，可能仍有未删除的部署。');
      console.log('   建议重新运行脚本或手动检查。');
      process.exit(1);
    }

  } catch (error) {
    console.error('\n❌ 发生错误:', error.message);
    process.exit(1);
  }
}

// 运行
main();
