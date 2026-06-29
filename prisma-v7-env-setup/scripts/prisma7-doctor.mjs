#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

function readJsonIfExists(filePath) {
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch {
    return null;
  }
}

function fileExists(filePath) {
  try {
    fs.accessSync(filePath, fs.constants.F_OK);
    return true;
  } catch {
    return false;
  }
}

function parseEnvFile(contents) {
  const env = {};
  for (const line of contents.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const equalsIndex = trimmed.indexOf("=");
    if (equalsIndex <= 0) continue;

    const key = trimmed.slice(0, equalsIndex).trim();
    let value = trimmed.slice(equalsIndex + 1).trim();
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    env[key] = value;
  }
  return env;
}

function parseSemver(version) {
  const cleaned = version.replace(/^v/, "").split("-")[0] ?? "";
  const [major, minor, patch] = cleaned.split(".").map((s) => Number(s));
  if (![major, minor, patch].every((n) => Number.isFinite(n))) return null;
  return { major, minor, patch };
}

function semverGte(a, b) {
  if (a.major !== b.major) return a.major > b.major;
  if (a.minor !== b.minor) return a.minor > b.minor;
  return a.patch >= b.patch;
}

function formatStatus(ok) {
  return ok ? "OK" : "WARN";
}

function main() {
  const cwd = process.cwd();
  console.log("Prisma v7 doctor");
  console.log(`cwd: ${cwd}`);

  const nodeVersion = parseSemver(process.versions.node);
  const minA = { major: 20, minor: 19, patch: 0 };
  const minB = { major: 22, minor: 12, patch: 0 };
  const minC = { major: 24, minor: 0, patch: 0 };
  const nodeOk =
    nodeVersion &&
    (semverGte(nodeVersion, minA) ||
      semverGte(nodeVersion, minB) ||
      semverGte(nodeVersion, minC));
  console.log(
    `node: v${process.versions.node} (${formatStatus(Boolean(nodeOk))}; expected >=20.19 or >=22.12 or >=24.0)`
  );

  const packageJsonPath = path.join(cwd, "package.json");
  const packageJson = readJsonIfExists(packageJsonPath);
  const hasPackageJson = Boolean(packageJson);
  console.log(`package.json: ${hasPackageJson ? "found" : "missing"}`);

  const deps = {
    ...(packageJson?.dependencies ?? {}),
    ...(packageJson?.devDependencies ?? {}),
  };

  const prismaDep = deps["prisma"];
  const prismaClientDep = deps["@prisma/client"];
  if (hasPackageJson) {
    console.log(`deps.prisma: ${prismaDep ?? "(none)"}`);
    console.log(`deps.@prisma/client: ${prismaClientDep ?? "(none)"}`);
  }

  const configCandidates = [
    "prisma.config.ts",
    "prisma.config.mts",
    "prisma.config.js",
    "prisma.config.mjs",
  ];
  const foundConfig = configCandidates.find((p) => fileExists(path.join(cwd, p)));
  console.log(
    `prisma.config: ${foundConfig ? `${foundConfig} (${formatStatus(true)})` : `(missing; ${formatStatus(false)})`}`
  );

  const schemaCandidates = [
    path.join("prisma", "schema.prisma"),
    "schema.prisma",
  ];
  const foundSchema = schemaCandidates.find((p) => fileExists(path.join(cwd, p)));
  console.log(`schema.prisma: ${foundSchema ? `${foundSchema} (${formatStatus(true)})` : `(missing; ${formatStatus(false)})`}`);

  if (foundSchema) {
    const schemaText = fs.readFileSync(path.join(cwd, foundSchema), "utf8");

    const hasDatasourceUrl = /datasource\s+\w+\s*\{[\s\S]*?\b(url|directUrl)\s*=/.test(
      schemaText
    );
    console.log(
      `schema datasource url/directUrl: ${hasDatasourceUrl ? `present (${formatStatus(false)})` : `absent (${formatStatus(true)})`}`
    );

    const generatorProviderMatch = schemaText.match(
      /generator\s+\w+\s*\{[\s\S]*?\bprovider\s*=\s*"([^"]+)"/
    );
    const generatorProvider = generatorProviderMatch?.[1];
    console.log(`generator provider: ${generatorProvider ?? "(unknown)"}`);
    if (generatorProvider === "prisma-client") {
      console.log(
        `note: provider "prisma-client" usually requires driver adapter or Accelerate; see references/adapters.md`
      );
    } else if (generatorProvider === "prisma-client-js") {
      console.log(
        `note: provider "prisma-client-js" is the legacy generator and is often the easiest path for minimal code changes`
      );
    }
  }

  const envPath = path.join(cwd, ".env");
  if (fileExists(envPath)) {
    const env = parseEnvFile(fs.readFileSync(envPath, "utf8"));
    const hasDbUrl = typeof env.DATABASE_URL === "string" && env.DATABASE_URL.length > 0;
    console.log(
      `.env: found (${formatStatus(true)}); DATABASE_URL: ${hasDbUrl ? `set (${formatStatus(true)})` : `missing (${formatStatus(false)})`}`
    );
  } else {
    console.log(`.env: missing`);
  }

  console.log("\nNext actions (typical):");
  if (!prismaDep || !prismaClientDep) {
    console.log(`- Install deps: npm i @prisma/client && npm i -D prisma`);
  }
  if (!foundConfig) {
    console.log(`- Create prisma.config.ts (see references/templates.md)`);
  }
  if (!foundSchema) {
    console.log(`- Create prisma/schema.prisma (see references/templates.md)`);
  }
  if (foundConfig && foundSchema) {
    console.log(`- Validate: npx prisma validate`);
    console.log(`- Generate: npx prisma generate`);
    console.log(`- Migrate (dev): npx prisma migrate dev`);
  }
}

main();

