const vscode = require("vscode");
const path = require("path");
const fs = require("fs");
const os = require("os");
const { execFile } = require("child_process");

const SUPPORTED_HAUSA_SUFFIXES = new Set([".hausa", ".hrust"]);
const TRANSLATABLE_SUFFIXES = new Set([".hausa", ".hrust", ".py", ".rs"]);

function activate(context) {
  const output = vscode.window.createOutputChannel("Hausa Ecosystem");
  const diagnostics = vscode.languages.createDiagnosticCollection("hausa");
  const vocabulary = loadVocabulary(context.extensionPath, output);
  const pendingChecks = new Map();

  context.subscriptions.push(output, diagnostics);
  context.subscriptions.push(
    vscode.commands.registerCommand("hausa.runFile", () => runCurrentFile(output)),
    vscode.commands.registerCommand("hausa.checkFile", () => checkCurrentFile(output, diagnostics, true)),
    vscode.commands.registerCommand("hausa.translateToEnglish", () => translateCurrentFile("to-en", output)),
    vscode.commands.registerCommand("hausa.translateToHausa", () => translateCurrentFile("to-ha", output)),
    vscode.commands.registerCommand("hausa.selectProfile", selectVocabularyProfile),
    vscode.languages.registerCompletionItemProvider(
      [{ language: "hausa" }, { language: "hrust" }],
      new HausaCompletionProvider(vocabulary)
    ),
    vscode.languages.registerHoverProvider(
      [{ language: "hausa" }, { language: "hrust" }],
      new HausaHoverProvider(vocabulary)
    ),
    vscode.workspace.onDidSaveTextDocument((document) => {
      if (isHausaDocument(document) && configuration().get("diagnosticsOnSave", true)) {
        checkDocument(document, output, diagnostics, false);
      }
    }),
    vscode.workspace.onDidOpenTextDocument((document) => {
      if (isHausaDocument(document) && configuration().get("diagnosticsOnSave", true)) {
        checkDocument(document, output, diagnostics, false);
      }
    }),
    vscode.workspace.onDidChangeTextDocument((event) => {
      const document = event.document;
      if (!isHausaDocument(document) || !configuration().get("diagnosticsOnType", false)) return;
      const key = document.uri.toString();
      clearTimeout(pendingChecks.get(key));
      const configuredDelay = configuration().get("diagnosticsDelayMs", 750);
      const delay = Math.min(5000, Math.max(250, Number(configuredDelay) || 750));
      pendingChecks.set(key, setTimeout(async () => {
        pendingChecks.delete(key);
        await checkDocument(document, output, diagnostics, false, true);
      }, delay));
    }),
    vscode.workspace.onDidCloseTextDocument((document) => {
      const key = document.uri.toString();
      clearTimeout(pendingChecks.get(key));
      pendingChecks.delete(key);
      diagnostics.delete(document.uri);
    }),
    { dispose: () => {
      for (const timer of pendingChecks.values()) clearTimeout(timer);
      pendingChecks.clear();
    } }
  );

  if (vscode.window.activeTextEditor && isHausaDocument(vscode.window.activeTextEditor.document)) {
    checkDocument(vscode.window.activeTextEditor.document, output, diagnostics, false);
  }
}

function deactivate() {}

function configuration() {
  return vscode.workspace.getConfiguration("hausa");
}

function executablePath() {
  return configuration().get("executablePath", "hausa").trim() || "hausa";
}

function vocabularyProfile() {
  return configuration().get("vocabularyProfile", "all");
}

function activeDocument(allowedSuffixes) {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    vscode.window.showWarningMessage("Open a source file first.");
    return undefined;
  }
  const suffix = path.extname(editor.document.fileName).toLowerCase();
  if (!allowedSuffixes.has(suffix)) {
    vscode.window.showWarningMessage(`Unsupported file type: ${suffix || "no extension"}`);
    return undefined;
  }
  if (editor.document.isUntitled) {
    vscode.window.showWarningMessage("Save the file before using a Hausa command.");
    return undefined;
  }
  return editor.document;
}

function isHausaDocument(document) {
  return SUPPORTED_HAUSA_SUFFIXES.has(path.extname(document.fileName).toLowerCase());
}

async function saveDocument(document) {
  if (document.isDirty && !(await document.save())) {
    vscode.window.showWarningMessage("The file must be saved before this command can run.");
    return false;
  }
  return true;
}

async function runCurrentFile(output) {
  const document = activeDocument(SUPPORTED_HAUSA_SUFFIXES);
  if (!document || !(await saveDocument(document))) return;

  const args = ["run", document.fileName];
  if (path.extname(document.fileName).toLowerCase() === ".hausa") {
    args.push("--profile", vocabularyProfile());
  }
  const execution = new vscode.ProcessExecution(executablePath(), args, {
    cwd: path.dirname(document.fileName),
  });
  const task = new vscode.Task(
    { type: "hausa", file: document.fileName },
    vscode.TaskScope.Workspace,
    `Run ${path.basename(document.fileName)}`,
    "Hausa Ecosystem",
    execution
  );
  task.presentationOptions = { reveal: vscode.TaskRevealKind.Always, clear: true };
  try {
    await vscode.tasks.executeTask(task);
  } catch (error) {
    reportCliError(error, output);
  }
}

async function checkCurrentFile(output, diagnostics, reveal) {
  const document = activeDocument(SUPPORTED_HAUSA_SUFFIXES);
  if (!document || !(await saveDocument(document))) return;
  await checkDocument(document, output, diagnostics, reveal);
}

async function checkDocument(document, output, diagnostics, reveal, useUnsavedText = false) {
  let temporaryDirectory;
  let checkedFile = document.fileName;
  try {
    if (useUnsavedText && document.isDirty) {
      temporaryDirectory = await fs.promises.mkdtemp(path.join(os.tmpdir(), "hausa-check-"));
      checkedFile = path.join(temporaryDirectory, `document${path.extname(document.fileName)}`);
      await fs.promises.writeFile(checkedFile, document.getText(), "utf8");
    }
    const result = await executeCli(["check", checkedFile], path.dirname(document.fileName));
    diagnostics.delete(document.uri);
    writeOutput(output, result.stdout || `PASS: ${document.fileName}`, reveal);
  } catch (error) {
    const message = combinedProcessOutput(error);
    if (error.code === "ENOENT") {
      diagnostics.delete(document.uri);
      writeOutput(output, message, reveal);
      if (reveal) {
        vscode.window.showErrorMessage("Hausa CLI was not found. Install it or configure hausa.executablePath.");
      }
      return;
    }
    const position = diagnosticPosition(message, document);
    const lineLength = document.lineAt(position.line).text.length;
    const endColumn = lineLength > position.column ? lineLength : position.column;
    const diagnostic = new vscode.Diagnostic(
      new vscode.Range(position.line, position.column, position.line, endColumn),
      cleanDiagnosticMessage(message),
      vscode.DiagnosticSeverity.Error
    );
    diagnostic.source = "Hausa Ecosystem";
    diagnostics.set(document.uri, [diagnostic]);
    writeOutput(output, message, reveal);
    if (reveal) vscode.window.showErrorMessage("Hausa check failed. See Problems and Hausa Ecosystem output.");
  } finally {
    if (temporaryDirectory) {
      await fs.promises.rm(temporaryDirectory, { recursive: true, force: true }).catch(() => undefined);
    }
  }
}

async function translateCurrentFile(direction, output) {
  const document = activeDocument(TRANSLATABLE_SUFFIXES);
  if (!document || !(await saveDocument(document))) return;
  const suffix = path.extname(document.fileName).toLowerCase();
  if (direction === "to-en" && !SUPPORTED_HAUSA_SUFFIXES.has(suffix)) {
    vscode.window.showWarningMessage("Translate to English requires a .hausa or .hrust file.");
    return;
  }
  if (direction === "to-ha" && !new Set([".py", ".rs"]).has(suffix)) {
    vscode.window.showWarningMessage("Translate to Hausa requires a .py or .rs file.");
    return;
  }

  const targetSuffix = direction === "to-en"
    ? (suffix === ".hausa" ? ".py" : ".rs")
    : (suffix === ".py" ? ".hausa" : ".hrust");
  const defaultUri = vscode.Uri.file(document.fileName.slice(0, -suffix.length) + targetSuffix);
  const outputUri = await vscode.window.showSaveDialog({
    defaultUri,
    filters: { "Translated source": [targetSuffix.slice(1)] },
  });
  if (!outputUri) return;

  const args = [direction, document.fileName, "-o", outputUri.fsPath];
  if (suffix === ".hausa" || suffix === ".py") args.push("--profile", vocabularyProfile());
  try {
    const result = await executeCli(args, path.dirname(document.fileName));
    if (!fs.existsSync(outputUri.fsPath)) {
      throw new Error(`The translator did not create ${outputUri.fsPath}.`);
    }
    writeOutput(output, result.stdout, false);
    const translated = await vscode.workspace.openTextDocument(outputUri);
    await vscode.window.showTextDocument(translated);
    vscode.window.showInformationMessage(`Translated file created: ${path.basename(outputUri.fsPath)}`);
  } catch (error) {
    reportCliError(error, output);
  }
}

async function selectVocabularyProfile() {
  const profiles = ["core", "builtins", "database", "flask", "fastapi", "web", "all"];
  const selected = await vscode.window.showQuickPick(profiles, {
    placeHolder: `Current profile: ${vocabularyProfile()}`,
    title: "Select Hausa Python vocabulary profile",
  });
  if (!selected) return;
  await configuration().update("vocabularyProfile", selected, vscode.ConfigurationTarget.Workspace);
  vscode.window.showInformationMessage(`Hausa vocabulary profile: ${selected}`);
}

class HausaCompletionProvider {
  constructor(vocabulary) { this.vocabulary = vocabulary; }

  provideCompletionItems(document) {
    const entries = document.languageId === "hrust" ? this.vocabulary.rust : this.vocabulary.python;
    const profile = document.languageId === "hausa" ? vocabularyProfile() : "all";
    return Object.entries(entries).filter(([, details]) => {
      return profile === "all" || !details.profiles || details.profiles.includes(profile);
    }).map(([word, details]) => {
      const item = new vscode.CompletionItem(word, completionKind(details.category));
      item.detail = `${word} → ${details.english}`;
      item.documentation = new vscode.MarkdownString(`**${details.category}**\n\nTranslates to \`${details.english}\`.`);
      item.sortText = `1-${word}`;
      return item;
    });
  }
}

class HausaHoverProvider {
  constructor(vocabulary) { this.vocabulary = vocabulary; }

  provideHover(document, position) {
    const range = document.getWordRangeAtPosition(position, /[\p{L}\p{N}_']+/u);
    if (!range) return undefined;
    const word = document.getText(range);
    const entries = document.languageId === "hrust" ? this.vocabulary.rust : this.vocabulary.python;
    const details = entries[word];
    if (!details) return undefined;
    const markdown = new vscode.MarkdownString();
    markdown.appendMarkdown(`**${word}** → \`${details.english}\`\n\n`);
    markdown.appendMarkdown(`Category: ${details.category}`);
    if (details.profiles && details.profiles.length) {
      markdown.appendMarkdown(`\n\nProfiles: ${details.profiles.map((profile) => `\`${profile}\``).join(", ")}`);
    }
    return new vscode.Hover(markdown, range);
  }
}

function completionKind(category) {
  if (category === "type") return vscode.CompletionItemKind.Class;
  if (category === "constant") return vscode.CompletionItemKind.Constant;
  if (category === "builtin" || category === "framework") return vscode.CompletionItemKind.Function;
  return vscode.CompletionItemKind.Keyword;
}

function loadVocabulary(extensionPath, output) {
  try {
    return JSON.parse(fs.readFileSync(path.join(extensionPath, "vocabularies.json"), "utf8"));
  } catch (error) {
    writeOutput(output, `Could not load vocabularies.json: ${error.message}`, false);
    return { python: {}, rust: {} };
  }
}

function executeCli(args, cwd) {
  return new Promise((resolve, reject) => {
    execFile(executablePath(), args, { cwd, encoding: "utf8", timeout: 30000, maxBuffer: 1024 * 1024 }, (error, stdout, stderr) => {
      if (error) {
        error.stdout = stdout;
        error.stderr = stderr;
        reject(error);
      } else {
        resolve({ stdout, stderr });
      }
    });
  });
}

function diagnosticPosition(message, document) {
  let match = /layi\s+(\d+)/i.exec(message);
  let line = match ? Number(match[1]) - 1 : 0;
  let column = 0;
  const compilerMatch = /:(\d+):(\d+)/.exec(message);
  if (compilerMatch) {
    line = Number(compilerMatch[1]) - 1;
    column = Number(compilerMatch[2]) - 1;
  }
  line = Math.min(Math.max(line, 0), Math.max(document.lineCount - 1, 0));
  column = Math.min(Math.max(column, 0), document.lineAt(line).text.length);
  return { line, column };
}

function cleanDiagnosticMessage(message) {
  const lines = message.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  return lines.slice(0, 4).join(" — ") || "Hausa source check failed.";
}

function combinedProcessOutput(error) {
  return [error.stdout, error.stderr, error.message].filter(Boolean).join("\n").trim();
}

function writeOutput(output, text, reveal) {
  if (text) {
    output.appendLine(`[${new Date().toLocaleTimeString()}] ${text.trim()}`);
  }
  if (reveal) output.show(true);
}

function reportCliError(error, output) {
  const message = combinedProcessOutput(error);
  writeOutput(output, message, true);
  if (error.code === "ENOENT") {
    vscode.window.showErrorMessage("Hausa CLI was not found. Install it or configure hausa.executablePath.");
  } else {
    vscode.window.showErrorMessage("Hausa command failed. See the Hausa Ecosystem output channel.");
  }
}

module.exports = { activate, deactivate };
