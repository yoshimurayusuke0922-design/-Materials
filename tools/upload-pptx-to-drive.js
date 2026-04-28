#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const DRIVE_UPLOAD_URL = 'https://www.googleapis.com/upload/drive/v3/files';
const TOKEN_URL = 'https://oauth2.googleapis.com/token';

async function accessToken() {
  const rcPath = path.join(process.env.USERPROFILE || process.env.HOME, '.clasprc.json');
  const rc = JSON.parse(fs.readFileSync(rcPath, 'utf8'));
  const token = rc.tokens && rc.tokens.default;
  if (!token) {
    throw new Error('No default clasp token found. Run `clasp login` first.');
  }

  if (token.access_token && token.expiry_date && token.expiry_date > Date.now() + 60000) {
    return token.access_token;
  }

  const body = new URLSearchParams({
    client_id: token.client_id,
    client_secret: token.client_secret,
    refresh_token: token.refresh_token,
    grant_type: 'refresh_token',
  });

  const res = await fetch(TOKEN_URL, {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body,
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(`Token refresh failed: ${res.status} ${JSON.stringify(data)}`);
  }
  return data.access_token;
}

async function uploadPresentation({ pptxPath, folderId, name }) {
  const token = await accessToken();
  const boundary = `codex_${Date.now().toString(16)}`;
  const metadata = {
    name,
    mimeType: 'application/vnd.google-apps.presentation',
    parents: [folderId],
  };
  const file = fs.readFileSync(pptxPath);
  const head = Buffer.from(
    `--${boundary}\r\n` +
      'Content-Type: application/json; charset=UTF-8\r\n\r\n' +
      `${JSON.stringify(metadata)}\r\n` +
      `--${boundary}\r\n` +
      'Content-Type: application/vnd.openxmlformats-officedocument.presentationml.presentation\r\n\r\n',
    'utf8',
  );
  const tail = Buffer.from(`\r\n--${boundary}--\r\n`, 'utf8');
  const body = Buffer.concat([head, file, tail]);

  const params = new URLSearchParams({
    uploadType: 'multipart',
    supportsAllDrives: 'true',
    fields: 'id,name,mimeType,webViewLink',
  });
  const res = await fetch(`${DRIVE_UPLOAD_URL}?${params}`, {
    method: 'POST',
    headers: {
      authorization: `Bearer ${token}`,
      'content-type': `multipart/related; boundary=${boundary}`,
      'content-length': String(body.length),
    },
    body,
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(`Drive upload failed: ${res.status} ${JSON.stringify(data)}`);
  }
  return data;
}

async function main() {
  const [pptxPath, folderId, name] = process.argv.slice(2);
  if (!pptxPath || !folderId || !name) {
    console.error('Usage: node tools/upload-pptx-to-drive.js <pptxPath> <folderId> <googleSlidesName>');
    process.exit(2);
  }
  const result = await uploadPresentation({
    pptxPath: path.resolve(pptxPath),
    folderId,
    name,
  });
  console.log(JSON.stringify(result, null, 2));
}

main().catch(err => {
  console.error(err.message);
  process.exit(1);
});
