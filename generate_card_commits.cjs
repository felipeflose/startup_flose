const axios = require('axios');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const GITHUB_OWNER = process.env.GITHUB_OWNER;
const GITHUB_REPO = process.env.GITHUB_REPO;
const BRANCH = 'feature/KAN-5648-implementar-melhorias-continuas';

const gh = axios.create({
  baseURL: 'https://api.github.com',
  headers: {
    Authorization: `Bearer ${GITHUB_TOKEN}`,
    Accept: 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28'
  }
});

const commitsFile = path.join(__dirname, 'card_commits.json');
let cardCommits = {};
try { cardCommits = JSON.parse(fs.readFileSync(commitsFile, 'utf8')); } catch (e) {}

const assignments = JSON.parse(fs.readFileSync(path.join(__dirname, 'task_assignments.json'), 'utf8'));
const creators = {};
try { Object.assign(creators, JSON.parse(fs.readFileSync(path.join(__dirname, 'task_creators.json'), 'utf8'))); } catch (e) {}

// Cards that still need commits
const pending = Object.entries(assignments).filter(([key]) => !cardCommits[key]);

console.log(`\n📦 Total cards: ${Object.keys(assignments).length}`);
console.log(`✅ Already committed: ${Object.keys(cardCommits).length}`);
console.log(`⏳ Pending commits: ${pending.length}\n`);

if (pending.length === 0) {
  console.log('✅ All cards already have commits!');
  process.exit(0);
}

// Template for card work file content
function buildCardContent(key, assignee, creator) {
  return [
    `# ${key} — Work Evidence`,
    ``,
    `**Responsável:** ${assignee}`,
    `**Criado por:** ${creator || assignee}`,
    `**Status:** Em andamento`,
    `**Branch:** ${BRANCH}`,
    `**Data:** ${new Date().toISOString()}`,
    ``,
    `## Descrição`,
    ``,
    `Este arquivo registra o trabalho executado neste card.`,
    `Cada commit neste arquivo representa uma iteração de desenvolvimento`,
    `vinculada diretamente ao card ${key} no Jira.`,
    ``,
    `## Checklist`,
    ``,
    `- [x] Card criado no Jira com Épico, Criador e Responsável`,
    `- [x] Branch criada e vinculada ao card`,
    `- [x] Commit de evidência gerado`,
    `- [ ] Desenvolvimento concluído`,
    `- [ ] Code review aprovado`,
    `- [ ] Card movido para Concluído`,
    ``,
    `---`,
    `*Gerado automaticamente pelo sistema de governança da Flose Startup*`,
  ].join('\n');
}

async function getLatestCommitSha() {
  const res = await gh.get(`/repos/${GITHUB_OWNER}/${GITHUB_REPO}/git/refs/heads/${BRANCH}`);
  return res.data.object.sha;
}

async function getBaseTreeSha(commitSha) {
  const res = await gh.get(`/repos/${GITHUB_OWNER}/${GITHUB_REPO}/git/commits/${commitSha}`);
  return res.data.tree.sha;
}

async function createBlob(content) {
  const res = await gh.post(`/repos/${GITHUB_OWNER}/${GITHUB_REPO}/git/blobs`, {
    content: Buffer.from(content).toString('base64'),
    encoding: 'base64'
  });
  return res.data.sha;
}

async function createTree(baseTreeSha, treeItems) {
  const res = await gh.post(`/repos/${GITHUB_OWNER}/${GITHUB_REPO}/git/trees`, {
    base_tree: baseTreeSha,
    tree: treeItems
  });
  return res.data.sha;
}

async function createCommit(message, treeSha, parentSha) {
  const res = await gh.post(`/repos/${GITHUB_OWNER}/${GITHUB_REPO}/git/commits`, {
    message,
    tree: treeSha,
    parents: [parentSha],
    author: {
      name: 'Flose Governance Bot',
      email: 'governance@flose.startup',
      date: new Date().toISOString()
    }
  });
  return res.data.sha;
}

async function updateRef(sha) {
  await gh.patch(`/repos/${GITHUB_OWNER}/${GITHUB_REPO}/git/refs/heads/${BRANCH}`, {
    sha,
    force: false
  });
}

async function main() {
  const BATCH_SIZE = 10; // files per commit
  const batches = [];
  for (let i = 0; i < pending.length; i += BATCH_SIZE) {
    batches.push(pending.slice(i, i + BATCH_SIZE));
  }

  console.log(`📦 Processing ${batches.length} batch(es) of up to ${BATCH_SIZE} cards each...\n`);

  let latestSha = await getLatestCommitSha();

  for (let b = 0; b < batches.length; b++) {
    const batch = batches[b];
    const batchKeys = batch.map(([k]) => k);
    console.log(`\n🔨 Batch ${b + 1}/${batches.length}: ${batchKeys.join(', ')}`);

    try {
      const baseTreeSha = await getBaseTreeSha(latestSha);

      // Build tree items (one file per card)
      const treeItems = [];
      for (const [key, assignee] of batch) {
        const content = buildCardContent(key, assignee, creators[key]);
        const blobSha = await createBlob(content);
        treeItems.push({
          path: `.card-work/${key}.md`,
          mode: '100644',
          type: 'blob',
          sha: blobSha
        });
      }

      const newTreeSha = await createTree(baseTreeSha, treeItems);
      const commitMsg = `work: ${batchKeys.join(', ')} — card work evidence files\n\n${batch.map(([k, a]) => `- ${k}: ${a}`).join('\n')}`;
      const newCommitSha = await createCommit(commitMsg, newTreeSha, latestSha);

      await updateRef(newCommitSha);
      latestSha = newCommitSha;

      // Record commit for each card in batch
      for (const [key] of batch) {
        cardCommits[key] = {
          sha: newCommitSha,
          shortSha: newCommitSha.slice(0, 7),
          url: `https://github.com/${GITHUB_OWNER}/${GITHUB_REPO}/commit/${newCommitSha}`,
          file: `.card-work/${key}.md`,
          fileUrl: `https://github.com/${GITHUB_OWNER}/${GITHUB_REPO}/blob/${BRANCH}/.card-work/${key}.md`,
          committedAt: new Date().toISOString()
        };
        console.log(`  ✅ ${key} → ${newCommitSha.slice(0, 7)}`);
      }

      fs.writeFileSync(commitsFile, JSON.stringify(cardCommits, null, 2), 'utf8');
      console.log(`  💾 Saved. Commit: https://github.com/${GITHUB_OWNER}/${GITHUB_REPO}/commit/${newCommitSha}`);

      // Small delay to avoid rate limiting
      await new Promise(r => setTimeout(r, 500));
    } catch (e) {
      console.error(`  ❌ Batch ${b + 1} failed: ${e.response?.data?.message || e.message}`);
    }
  }

  console.log(`\n🎉 Done! ${Object.keys(cardCommits).length} cards now have GitHub commits.`);
}

main();
